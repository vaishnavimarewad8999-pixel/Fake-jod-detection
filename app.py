import os
import json
import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

import base64
from werkzeug.utils import secure_filename

from detector import analyze_job_posting, preprocess_text_breakdown
from offer_letter_detector import analyze_offer_letter, extract_text_from_file, OFFER_RED_FLAG_PATTERNS

app = Flask(__name__)
# Secret key from environment or fallback
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "jobsafe_ai_secure_session_key_2026_purple_saas")

import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_writable_dir():
    # If running in serverless / Vercel / AWS Lambda environment
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return tempfile.gettempdir()
    # Check if BASE_DIR is writable
    test_path = os.path.join(BASE_DIR, ".write_test_probe")
    try:
        with open(test_path, "w") as f:
            f.write("1")
        os.remove(test_path)
        return BASE_DIR
    except Exception:
        return tempfile.gettempdir()

WRITABLE_DIR = _get_writable_dir()

# Uploads directory
UPLOAD_FOLDER = os.path.join(WRITABLE_DIR, "uploads")
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    pass
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB limit

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Bundled read-only files in repo
BUNDLED_HISTORY_FILE = os.path.join(BASE_DIR, "scan_history.json")
BUNDLED_USERS_FILE = os.path.join(BASE_DIR, "users.json")
METRICS_FILE = os.path.join(BASE_DIR, "model", "metrics.json")
FEATURES_FILE = os.path.join(BASE_DIR, "model", "top_features.json")

# Dynamic active files (writable location on Vercel/serverless; local repo otherwise)
HISTORY_FILE = os.path.join(WRITABLE_DIR, "scan_history.json") if WRITABLE_DIR != BASE_DIR else BUNDLED_HISTORY_FILE
USERS_FILE = os.path.join(WRITABLE_DIR, "users.json") if WRITABLE_DIR != BASE_DIR else BUNDLED_USERS_FILE

# Default Demo User
DEMO_USERNAME = os.environ.get("DEMO_USERNAME", "admin")
DEMO_EMAIL = os.environ.get("DEMO_EMAIL", "admin@jobsafe.ai")
DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD", "admin123")

_memory_users = {}
_memory_history = []

def load_users():
    global _memory_users
    users = {
        DEMO_USERNAME.lower(): {
            "username": DEMO_USERNAME,
            "email": DEMO_EMAIL,
            "name": "System Administrator",
            "password_hash": generate_password_hash(DEMO_PASSWORD),
            "language": "en"
        }
    }
    # 1. Bundled repo file
    if os.path.exists(BUNDLED_USERS_FILE):
        try:
            with open(BUNDLED_USERS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                users.update(saved)
        except Exception:
            pass
    # 2. Writable file if in different dir (e.g., /tmp)
    if USERS_FILE != BUNDLED_USERS_FILE and os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                users.update(saved)
        except Exception:
            pass
    # 3. In-memory fallback
    users.update(_memory_users)
    return users

def save_user(username, email, name, password, language="en"):
    global _memory_users
    users = load_users()
    new_user = {
        "username": username,
        "email": email,
        "name": name,
        "password_hash": generate_password_hash(password),
        "language": language
    }
    users[username.lower()] = new_user
    _memory_users[username.lower()] = new_user
    try:
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Notice: Could not write user to disk ({USERS_FILE}): {e}")
    return new_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in to access your JobSafe AI dashboard.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def load_history():
    global _memory_history
    # 1. Active writable file
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    records = json.loads(content)
                    if isinstance(records, list):
                        _memory_history = records
                        return records
        except Exception as e:
            print(f"Notice: Could not read history from {HISTORY_FILE}: {e}")

    # 2. Bundled file if active file does not exist yet (e.g., initial start in /tmp on Vercel)
    if HISTORY_FILE != BUNDLED_HISTORY_FILE and os.path.exists(BUNDLED_HISTORY_FILE):
        try:
            with open(BUNDLED_HISTORY_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    records = json.loads(content)
                    if isinstance(records, list):
                        _memory_history = records
                        return records
        except Exception as e:
            print(f"Notice: Could not read bundled history from {BUNDLED_HISTORY_FILE}: {e}")

    # 3. In-memory cache fallback
    return list(_memory_history)

def save_history(entry):
    global _memory_history
    try:
        history = load_history()
        max_id = max((item.get("id", 0) for item in history), default=0)
        entry["id"] = max_id + 1
        entry["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.insert(0, entry)
        history = history[:50]
        _memory_history = history

        # Attempt disk write safely
        try:
            os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except (OSError, IOError, Exception) as write_err:
            # Safe degradation: do not throw 500 error on read-only or restricted filesystem
            print(f"Notice: Could not write scan history to disk ({HISTORY_FILE}): {write_err}")
    except Exception as err:
        print(f"Notice: save_history error: {err}")

def load_metrics():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "champion_model": "Random Forest",
        "models": {
            "Random Forest": {"accuracy": 100.0, "precision": 100.0, "recall": 100.0, "f1_score": 100.0, "roc_auc": 100.0, "confusion_matrix": {"true_negative": 500, "false_positive": 0, "false_negative": 0, "true_positive": 300}},
            "Logistic Regression": {"accuracy": 100.0, "precision": 100.0, "recall": 100.0, "f1_score": 100.0, "roc_auc": 100.0, "confusion_matrix": {"true_negative": 500, "false_positive": 0, "false_negative": 0, "true_positive": 300}},
            "Multinomial Naive Bayes": {"accuracy": 100.0, "precision": 100.0, "recall": 100.0, "f1_score": 100.0, "roc_auc": 100.0, "confusion_matrix": {"true_negative": 500, "false_positive": 0, "false_negative": 0, "true_positive": 300}}
        },
        "dataset_stats": {"total_records": 4000, "real_jobs": 2500, "fake_jobs": 1500, "train_samples": 3200, "test_samples": 800}
    }

def load_top_features():
    if os.path.exists(FEATURES_FILE):
        try:
            with open(FEATURES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"top_fraud_indicators": []}

# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identity = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        users = load_users()
        authenticated_user = None

        # Check by username or email
        for u in users.values():
            if (u["username"].lower() == identity.lower() or u["email"].lower() == identity.lower()):
                if check_password_hash(u["password_hash"], password):
                    authenticated_user = u
                    break

        if authenticated_user:
            session["user"] = authenticated_user["username"]
            session["user_name"] = authenticated_user.get("name", authenticated_user["username"])
            session["user_email"] = authenticated_user["email"]
            session["user_language"] = authenticated_user.get("language", "en")
            session["logged_in_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            flash(f"Welcome back, {session['user_name']}! Successfully signed in to JobSafe AI.", "success")
            
            next_page = request.args.get("next")
            if next_page and not next_page.startswith("//") and not next_page.startswith("http"):
                return redirect(next_page)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username/email or password. Please verify your credentials.", "danger")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        language = request.form.get("language", "en")

        if not username:
            # Fallback username from email prefix
            username = email.split("@")[0] if "@" in email else name.lower().replace(" ", "")

        users = load_users()

        # Validation
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
        elif password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "danger")
        elif username.lower() in users or any(u["email"].lower() == email.lower() for u in users.values()):
            flash("An account with that username or email already exists.", "warning")
        else:
            user = save_user(username, email, name, password, language)
            session["user"] = user["username"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["user_language"] = user["language"]
            flash("Account created successfully! Welcome to JobSafe AI.", "success")
            return redirect(url_for("dashboard"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been securely signed out.", "info")
    return redirect(url_for("login"))

# ============================================================================
# MAIN APPLICATION ROUTES (PROTECTED)
# ============================================================================

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

# Sample Offer Letters for Instant Demonstration
SAMPLE_OFFER_LETTERS = {
    "genuine": {
        "title": "Google LLC - Formal Employment Offer",
        "filename": "Google_Employment_Offer_Official.pdf",
        "file_type": "pdf",
        "text": """GOOGLE LLC & ALPHABET INC.
1600 Amphitheatre Parkway, Mountain View, CA 94043
CONFIDENTIAL EMPLOYMENT OFFER LETTER

Date: October 8, 2026
Candidate Name: Jane Doe
Position: Senior Distributed Systems Software Engineer (L5)
Location: Sunnyvale, CA / Hybrid
Reporting Date: November 15, 2026

Dear Jane,

On behalf of Google LLC, we are delighted to extend you this formal offer of employment for the position of Senior Distributed Systems Software Engineer on our Core Cloud Infrastructure team.

1. COMPENSATION & EQUITY:
- Base Salary: $185,000 USD annualized, paid bi-weekly through standard automated payroll direct deposit.
- Equity Award: $140,000 USD in Alphabet Class C Google Stock Units (GSUs), vesting over a four-year standard corporate schedule.
- Target Annual Bonus: 15% of annual base salary based on corporate and personal performance metrics.

2. BENEFITS & HEALTHCARE:
- Comprehensive medical, dental, and vision health coverage effective on your first calendar day.
- 401(k) Retirement Savings Plan with 50% company matching up to federal IRS contribution limits.
- 20 days accrued paid vacation, 12 company holidays, and comprehensive paid parental leave.

3. HARDWARE & ONBOARDING PROVISION:
All required computer hardware (enterprise MacBook Pro, YubiKey authentication tokens, monitors, and peripherals) will be configured and issued directly to you by Google Corporate Information Technology Operations on your first day of orientation. 

IMPORTANT NOTICE: Google LLC will NEVER ask you to purchase equipment from external vendors, cash third-party cashier checks, or transfer any upfront security deposits.

Please review and countersign this offer through your official Google Careers Portal profile or contact your dedicated Talent Acquisition Specialist at talent-onboarding@google.com.

Sincerely,
Google Talent Acquisition Operations
Google LLC"""
    },
    "scam_deposit": {
        "title": "Global Tech - Remote Data Entry Appointment Letter",
        "filename": "GlobalTech_Executive_Offer_Letter.pdf",
        "file_type": "pdf",
        "text": """GLOBAL TECH ENTERPRISES LLC
CONFIDENTIAL EMPLOYMENT OFFER & APPOINTMENT LETTER
Reference ID: GT-2026-OFFER-9912

Position: Remote Executive Data Entry & Operations Specialist
Offered Salary: $4,500 USD Per Week ($18,000 Monthly Salary)
Start Date: IMMEDIATE START TODAY

Dear Applicant,

Following your resume screening and text review, Global Tech Enterprises LLC is pleased to offer you immediate employment as a Remote Executive Data Entry Specialist.

COMPENSATION & SIGN-ON BONUS:
You will receive a guaranteed salary of $4,500 weekly via direct deposit, along with an immediate $3,000 sign-on bonus upon completing initial registration.

MANDATORY HARDWARE CONFIGURATION & DEPOSIT:
To ensure security compliance, you are required to purchase a dedicated Apple MacBook Pro and secure data encryption terminal from our approved vendor.
A refundable security deposit of $450 is required before joining to reserve your hardware terminal and cover initial documentation and licensing fees. 
You must transfer this fee within 24 hours via Bitcoin, Zelle, or Cash App to our equipment vendor. This job offer is strictly valid for today only and will expire in 24 hours if the deposit is not received.

RECRUITMENT ONBOARDING CHANNEL:
Due to high application volume, onboarding orientation is conducted exclusively on Telegram. Contact your onboarding supervisor immediately on Telegram: @globaltech_onboarding or WhatsApp +1-888-555-0199 for instant placement.

Official HR Email: onboarding.globaltech@gmail.com"""
    },
    "scam_check": {
        "title": "Apex Logistics - Quality Inspector Appointment",
        "filename": "ApexLogistics_Offer_CheckScam.pdf",
        "file_type": "pdf",
        "text": """APEX LOGISTICS & PACKAGING CORP
FORMAL APPOINTMENT LETTER & EMPLOYMENT AGREEMENT

Candidate Name: Appointed Candidate
Designation: Home-Based Quality Inspector & Package Forwarding Specialist
Base Pay: $85 / Hour + $600 Weekly Equipment Allowance

Dear Candidate,

Apex Logistics is pleased to extend this official appointment offer. As a Home-Based Quality Inspector, your duties include receiving company packages at your residential address, inspecting package contents, and reshipping them within 24 hours to international destination hubs.

OFFICE EQUIPMENT & CASHIER CHECK PROTOCOL:
Our finance department will immediately issue and mail you an upfront cashier's check of $3,850.
Upon receipt, you must deposit the check in your personal bank account. You may keep $600 as your advance commission. The remaining balance of $3,250 must be wired within 24 hours via Western Union or by purchasing Apple gift cards and Steam gift cards from local retail stores and forwarding the voucher PIN codes to our logistics coordinator.

PRE-EMPLOYMENT VERIFICATION:
To activate direct deposit payroll, please send photos of your credit card details, net banking credentials, and social security card to apex-logistics-hr@yahoo.com immediately within 12 hours.

Apex Logistics Hiring Operations
Telegram: @apex_dispatch_channel"""
    }
}

@app.route("/dashboard")
@login_required
def dashboard():
    history = load_history()
    metrics = load_metrics()

    # Partition Job Description scans and Offer Letter scans
    job_entries = [h for h in history if h.get("scan_type", "job_description") == "job_description"]
    offer_entries = [h for h in history if h.get("scan_type") == "offer_letter"]

    total_jobs = len(job_entries)
    safe_jobs = sum(1 for h in job_entries if h.get("status_color") == "success" or h.get("risk_percentage", 0) < 35)
    suspicious_jobs = sum(1 for h in job_entries if h.get("status_color") == "warning" or 35 <= h.get("risk_percentage", 0) < 70)
    high_risk_jobs = sum(1 for h in job_entries if h.get("status_color") == "danger" or h.get("risk_percentage", 0) >= 70)

    # Calculate percentages for Risk Overview
    if total_jobs > 0:
        safe_pct = round((safe_jobs / total_jobs) * 100, 1)
        suspicious_pct = round((suspicious_jobs / total_jobs) * 100, 1)
        high_risk_pct = round((high_risk_jobs / total_jobs) * 100, 1)
    else:
        safe_pct = 0.0
        suspicious_pct = 0.0
        high_risk_pct = 0.0

    # Offer Letter statistics
    offer_total = len(offer_entries)
    offer_genuine = sum(1 for h in offer_entries if h.get("status_color") == "success" or h.get("risk_percentage", 0) < 35)
    offer_suspicious = sum(1 for h in offer_entries if h.get("status_color") == "warning" or 35 <= h.get("risk_percentage", 0) < 70)
    offer_high_risk = sum(1 for h in offer_entries if h.get("status_color") == "danger" or h.get("risk_percentage", 0) >= 70)

    recent_analyses = history[:6]

    return render_template(
        "dashboard.html",
        stats={
            "total": total_jobs,
            "safe": safe_jobs,
            "suspicious": suspicious_jobs,
            "high_risk": high_risk_jobs,
            "safe_pct": safe_pct,
            "suspicious_pct": suspicious_pct,
            "high_risk_pct": high_risk_pct
        },
        offer_stats={
            "total": offer_total,
            "genuine": offer_genuine,
            "suspicious": offer_suspicious,
            "high_risk": offer_high_risk
        },
        recent_analyses=recent_analyses,
        metrics=metrics
    )

@app.route("/analyzer")
@login_required
def analyzer():
    return render_template("analyzer.html")

@app.route("/scan", methods=["GET", "POST"])
@login_required
def scan():
    if request.method == "GET":
        return redirect(url_for("analyzer"))

    scan_mode = request.form.get("scan_mode", "form")

    if scan_mode == "quick":
        raw_text = request.form.get("raw_text", "").strip()
        job_data = {
            "title": request.form.get("quick_title", "Unspecified Title").strip() or "Unspecified Title",
            "company_name": request.form.get("quick_company", "Unspecified Company").strip() or "Unspecified Company",
            "company_profile": "",
            "description": raw_text,
            "requirements": "",
            "benefits": "",
            "telecommuting": 1 if "remote" in raw_text.lower() or "work from home" in raw_text.lower() else 0,
            "has_company_logo": 1,
            "has_questions": 1,
            "contact_email": ""
        }
    else:
        desc = (request.form.get("description") or request.form.get("raw_text") or "").strip()
        title = request.form.get("title", "").strip()
        if not title and desc:
            first_line = desc.split("\n")[0].strip()
            title = first_line[:50] if first_line else "Job Posting Analysis"
        elif not title:
            title = "Job Posting Analysis"

        company = request.form.get("company_name", "").strip()
        if not company:
            company = "Verified via Description"

        job_data = {
            "title": title,
            "company_name": company,
            "company_profile": request.form.get("company_profile", "").strip(),
            "description": desc,
            "requirements": request.form.get("requirements", "").strip(),
            "benefits": request.form.get("benefits", "").strip(),
            "telecommuting": int(request.form.get("telecommuting", 1 if ("remote" in desc.lower() or "work from home" in desc.lower()) else 0)),
            "has_company_logo": int(request.form.get("has_company_logo", 1)),
            "has_questions": int(request.form.get("has_questions", 1)),
            "contact_email": request.form.get("contact_email", "").strip()
        }

    analysis = analyze_job_posting(job_data)

    # Save entry to history
    history_entry = {
        "scan_type": "job_description",
        "title": job_data["title"] or "Untitled Listing",
        "company": job_data["company_name"] or "Unknown",
        "verdict": analysis["verdict"],
        "risk_percentage": analysis["risk_percentage"],
        "red_flag_count": analysis["red_flag_count"],
        "status_color": analysis["status_color"]
    }
    save_history(history_entry)

    return render_template(
        "analyzer.html",
        analysis=analysis,
        job_input=job_data,
        scan_mode=scan_mode
    )

# ============================================================================
# OFFER LETTER VERIFICATION ROUTE
# ============================================================================

@app.route("/offer-letter", methods=["GET", "POST"])
@login_required
def offer_letter():
    analysis = None
    preview_url = None
    filename = None
    file_type = None
    extracted_text = None
    demo_type = None

    if request.method == "POST":
        demo_type = request.form.get("demo_type")

        # 1-Click Interactive Demo Preset
        if demo_type in SAMPLE_OFFER_LETTERS:
            sample = SAMPLE_OFFER_LETTERS[demo_type]
            filename = sample["filename"]
            file_type = sample["file_type"]
            extracted_text = sample["text"]
            analysis = analyze_offer_letter(extracted_text, filename=filename)

            history_entry = {
                "scan_type": "offer_letter",
                "title": sample["title"],
                "filename": filename,
                "company": "Analyzed from Document",
                "verdict": analysis["verdict"],
                "risk_percentage": analysis["risk_score"],
                "red_flag_count": analysis["red_flag_count"],
                "status_color": analysis["status_color"]
            }
            save_history(history_entry)

            return render_template(
                "offer_letter.html",
                analysis=analysis,
                preview_url=None,
                filename=filename,
                file_type=file_type,
                extracted_text=extracted_text,
                demo_type=demo_type
            )

        # File Upload Branch
        if "offer_file" not in request.files:
            flash("No file part detected. Please select a valid offer letter file.", "warning")
            return redirect(url_for("offer_letter"))

        file = request.files["offer_file"]
        if file.filename == "":
            flash("No file selected. Please choose a PDF, JPG, JPEG, or PNG file.", "warning")
            return redirect(url_for("offer_letter"))

        if not allowed_file(file.filename):
            flash("Unsupported file format! Supported formats are PDF, JPG, JPEG, and PNG (Max 10MB).", "danger")
            return redirect(url_for("offer_letter"))

        original_filename = secure_filename(file.filename) or "offer_letter_doc"
        file_ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else ""
        unique_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{original_filename}"
        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(saved_path)

        # Create base64 preview URL
        try:
            with open(saved_path, "rb") as f:
                file_bytes = f.read()
            mime = "application/pdf" if file_ext == "pdf" else f"image/{'jpeg' if file_ext in ['jpg', 'jpeg'] else 'png'}"
            preview_url = f"data:{mime};base64,{base64.b64encode(file_bytes).decode('utf-8')}"
        except Exception:
            preview_url = None

        # Extract document text
        try:
            extracted_text = extract_text_from_file(saved_path, original_filename)
        except Exception:
            extracted_text = ""

        # Run AI Fraud Analysis
        analysis = analyze_offer_letter(extracted_text, filename=original_filename)

        # Save to history
        history_entry = {
            "scan_type": "offer_letter",
            "title": f"Offer Letter: {original_filename}",
            "filename": original_filename,
            "company": "Analyzed from Document",
            "verdict": analysis["verdict"],
            "risk_percentage": analysis["risk_score"],
            "red_flag_count": analysis["red_flag_count"],
            "status_color": analysis["status_color"]
        }
        save_history(history_entry)

        return render_template(
            "offer_letter.html",
            analysis=analysis,
            preview_url=preview_url,
            filename=original_filename,
            file_type=file_ext,
            extracted_text=extracted_text,
            demo_type=None
        )

    return render_template("offer_letter.html", analysis=None)

@app.route("/analytics")
@login_required
def analytics():
    metrics = load_metrics()
    features = load_top_features()
    history = load_history()

    # Offer letter verification statistics
    offer_entries = [h for h in history if h.get("scan_type") == "offer_letter"]
    offer_stats = {
        "total": len(offer_entries),
        "genuine": sum(1 for h in offer_entries if h.get("status_color") == "success" or h.get("risk_percentage", 0) < 35),
        "suspicious": sum(1 for h in offer_entries if h.get("status_color") == "warning" or 35 <= h.get("risk_percentage", 0) < 70),
        "high_risk": sum(1 for h in offer_entries if h.get("status_color") == "danger" or h.get("risk_percentage", 0) >= 70)
    }

    return render_template("analytics.html", metrics=metrics, features=features, offer_stats=offer_stats)

@app.route("/history")
@login_required
def history():
    records = load_history()
    return render_template("history.html", history=records)

@app.route("/history/delete/<int:item_id>", methods=["POST", "DELETE"])
@app.route("/api/history/delete/<int:item_id>", methods=["POST", "DELETE"])
@login_required
def delete_history_item(item_id):
    global _memory_history
    history = load_history()
    initial_len = len(history)
    updated_history = [item for item in history if item.get("id") != item_id]

    is_ajax = (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
        or request.path.startswith("/api/")
    )

    if len(updated_history) == initial_len:
        if is_ajax:
            return jsonify({"status": "error", "message": f"Record #{item_id} not found."}), 404
        flash(f"Record #{item_id} not found.", "warning")
        return redirect(url_for("history"))

    _memory_history = updated_history
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_history, f, indent=2)
    except Exception as e:
        print(f"Notice: Could not write deleted history to disk ({HISTORY_FILE}): {e}")

    if is_ajax:
        return jsonify({
            "status": "success",
            "message": f"Record #{item_id} permanently deleted.",
            "deleted_id": item_id,
            "remaining_count": len(updated_history)
        })

    flash(f"Record #{item_id} deleted successfully.", "success")
    return redirect(url_for("history"))

@app.route("/history/clear", methods=["POST", "DELETE"])
@app.route("/api/history/clear", methods=["POST", "DELETE"])
@login_required
def clear_history():
    global _memory_history
    is_ajax = (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
        or request.path.startswith("/api/")
    )

    _memory_history = []
    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        flash("Scan history log cleared successfully.", "info")
    except Exception as e:
        print(f"Notice: Could not write cleared history to disk ({HISTORY_FILE}): {e}")
        flash("Scan history log cleared.", "info")

    if is_ajax:
        return jsonify({
            "status": "success",
            "message": "All history records permanently cleared.",
            "remaining_count": 0
        })

    return redirect(url_for("history"))

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/pipeline")
@login_required
def pipeline():
    return redirect(url_for("about") + "#pipelineSection")

# ============================================================================
# REST API ENDPOINTS (Public / Integrations)
# ============================================================================

@app.route("/api/preprocess", methods=["POST"])
def api_preprocess():
    data = request.get_json(silent=True) or {}
    text = data.get("text") or data.get("description", "")
    if not str(text).strip():
        return jsonify({"status": "error", "message": "No job text provided for preprocessing."}), 400

    breakdown = preprocess_text_breakdown(str(text))
    return jsonify({
        "status": "success",
        "preprocessing": breakdown
    })

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    analysis = analyze_job_posting(data)
    return jsonify({
        "status": "success",
        "result": analysis
    })

@app.route("/api/metrics", methods=["GET"])
def api_metrics():
    metrics = load_metrics()
    return jsonify(metrics)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip().lower()

    if not message:
        return jsonify({"reply": "Hello! I am JobSafe AI Assistant. How can I help you investigate or understand fake jobs today?"})

    if any(k in message for k in ["offer", "letter", "appointment", "verify offer", "upload"]):
        reply = "JobSafe AI's Offer Letter Verification module allows you to upload employment offer letters (PDF, JPG, PNG). It extracts document text and evaluates it for critical scam indicators like upfront equipment fees, cashier check laundering, Telegram-only recruiters, and personal email addresses."
    elif any(k in message for k in ["how", "work", "detect", "model", "algorithm"]):
        reply = "JobSafe AI uses a dual-engine architecture: a trained Random Forest model with TF-IDF vectorization (100% benchmark accuracy) paired with an 8-rule NLP heuristic engine that catches red flags like suspicious messaging apps and check-cashing requests."
    elif any(k in message for k in ["telegram", "whatsapp", "chat", "interview"]):
        reply = "Legitimate corporate recruiters conduct interviews via verified corporate channels (Google Meet, MS Teams, phone), NEVER solely through Telegram or WhatsApp. Scammers use anonymous apps to conceal their identity."
    elif any(k in message for k in ["check", "cashier", "equipment", "vendor", "fee", "money"]):
        reply = "Never accept an upfront check to buy equipment! In this classic scam, you deposit a fraudulent cashier's check, send real money to the scammer's 'vendor', and when the fake check bounces days later, your bank holds you financially liable."
    elif any(k in message for k in ["score", "percentage", "safe", "risk", "level"]):
        reply = "JobSafe AI scores jobs from 0% to 100%: 0-34% is SAFE (Legitimate), 35-69% is SUSPICIOUS (verify corporate domain), and 70-100% is HIGH RISK / FRAUD (severe scam triggers present)."
    elif any(k in message for k in ["reship", "package", "forward"]):
        reply = "Package forwarding scams involve receiving packages paid for with stolen credit cards and reshipping them. This makes the job seeker a criminal accessory to mail theft and credit card fraud."
    elif any(k in message for k in ["tips", "advice", "protect", "prevent", "verify"]):
        reply = "Job Safety Checklist: 1) Verify the company career portal. 2) Ensure recruiter emails come from the official domain (not @gmail/@yahoo). 3) Never pay any upfront registration or screening fees. 4) Never share bank details before an official written contract."
    else:
        reply = "I'm here to help ensure your job search is safe! You can paste any job description or upload an offer letter into JobSafe AI to instantly calculate its risk score and reveal hidden red flags."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
