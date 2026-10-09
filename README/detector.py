import re
import os
import joblib
import pandas as pd
import numpy as np

# Load trained pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "fake_job_detector.joblib")
_pipeline = None

def get_pipeline():
    global _pipeline
    if _pipeline is None and os.path.exists(MODEL_PATH):
        _pipeline = joblib.load(MODEL_PATH)
    return _pipeline

RED_FLAG_PATTERNS = [
    {
        "id": "chat_app",
        "category": "Unofficial Communication Channel",
        "severity": "HIGH",
        "regex": r"\b(telegram|whatsapp|signal\s*app|hangouts|google\s*chat|kik|skype\s*interview)\b|@[a-zA-Z0-9_]+",
        "reason": "Legitimate corporate recruiters almost never interview or communicate solely through personal messaging apps like Telegram, WhatsApp, or Google Hangouts."
    },
    {
        "id": "advance_fee_check",
        "category": "Check Cashing / Advance Fee Fraud",
        "severity": "CRITICAL",
        "regex": r"\b(cashier'?s?\s*check|upfront\s*check|equipment\s*check|check\s*deposit|purchase\s*(office\s*)?equipment\s*from\s*(our\s*)?vendor|approved\s*vendor)\b",
        "reason": "Classic check-cashing scam: The scammer sends a fake check, asks you to deposit it and buy equipment from their 'vendor'. The check bounces days later, leaving you liable."
    },
    {
        "id": "wire_transfer_crypto",
        "category": "Money Mule / Untraceable Payments",
        "severity": "CRITICAL",
        "regex": r"\b(wire\s*transfer|western\s*union|moneygram|bitcoin|crypto(currency)?\s*atm|zelle|cash\s*app|gift\s*cards?|steam\s*cards?|apple\s*gift\s*card)\b",
        "reason": "Demands for untraceable financial transfers (Western Union, gift cards, crypto ATMs) are almost always fraudulent money laundering or money mule scams."
    },
    {
        "id": "unrealistic_promise",
        "category": "Unrealistic Pay / No Experience",
        "severity": "MEDIUM",
        "regex": r"\b(no\s*experience\s*(needed|required)|earn\s*\$?\d{3,}\s*(daily|a day|weekly|per week)|guaranteed\s*income|passive\s*income|get\s*rich|easy\s*cash|quick\s*payout)\b",
        "reason": "Promises of extraordinarily high compensation for entry-level work with zero experience required are typical bait in deceptive postings."
    },
    {
        "id": "reshipping_scam",
        "category": "Package Reshipping Fraud",
        "severity": "HIGH",
        "regex": r"\b(package\s*inspector|shipping\s*forwarder|repackag(e|ing)|reship(ment)?|receive\s*parcels?)\b",
        "reason": "Work-from-home 'package forwarding' involves handling goods bought with stolen credit cards, making you an accessory to postal theft."
    },
    {
        "id": "free_webmail",
        "category": "Free Webmail Domain Used by Recruiter",
        "severity": "MEDIUM",
        "regex": r"\b[a-zA-Z0-9_.+-]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com|aol\.com)\b",
        "reason": "Reputable companies hire using verified corporate domain emails (e.g. name@company.com), not free webmail providers."
    },
    {
        "id": "urgent_pressure",
        "category": "Urgent Pressure Tactics",
        "severity": "LOW",
        "regex": r"\b(start\s*today|immediate\s*hire|urgent\s*requirement|limited\s*spots?\s*left|hiring\s*immediately)\b",
        "reason": "Scammers manufacture artificial urgency to pressure candidates into making hasty decisions without performing due diligence."
    },
    {
        "id": "bank_details_request",
        "category": "Premature Financial/Identity Requests",
        "severity": "HIGH",
        "regex": r"\b(send\s*(your\s*)?(bank\s*details|bank\s*account|routing\s*number|ssn|social\s*security)|registration\s*fee|background\s*check\s*fee)\b",
        "reason": "Legitimate employers never charge application or background check fees, nor ask for banking details before an official written job offer."
    }
]

def clean_text_simple(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def analyze_job_posting(data):
    """
    Takes job data dictionary:
    {
        'title': str,
        'company_name': str,
        'company_profile': str,
        'description': str,
        'requirements': str,
        'benefits': str,
        'telecommuting': int (0 or 1),
        'has_company_logo': int (0 or 1),
        'has_questions': int (0 or 1),
        'contact_email': str
    }
    Returns complete analysis dictionary.
    """
    title = str(data.get("title", ""))
    company_name = str(data.get("company_name", ""))
    company_profile = str(data.get("company_profile", ""))
    description = str(data.get("description", ""))
    requirements = str(data.get("requirements", ""))
    benefits = str(data.get("benefits", ""))
    contact_email = str(data.get("contact_email", ""))
    
    telecommuting = int(data.get("telecommuting", 0))
    has_company_logo = int(data.get("has_company_logo", 1))
    has_questions = int(data.get("has_questions", 1))
    
    combined_raw = f"{title} {company_name} {company_profile} {description} {requirements} {benefits} {contact_email}"
    
    # 1. Rule-Based Red Flag Detection & Highlighting
    detected_flags = []
    suspicious_term_count = 0
    highlight_spans = []
    
    for item in RED_FLAG_PATTERNS:
        matches = list(re.finditer(item["regex"], combined_raw, re.IGNORECASE))
        if matches:
            matched_terms = list(set([m.group(0) for m in matches]))
            detected_flags.append({
                "id": item["id"],
                "category": item["category"],
                "severity": item["severity"],
                "matched_terms": matched_terms,
                "reason": item["reason"]
            })
            suspicious_term_count += len(matches)
            
            # Find spans in description / requirements to highlight
            for m in re.finditer(item["regex"], description, re.IGNORECASE):
                highlight_spans.append((m.start(), m.end(), item["category"], item["severity"]))
                
    # Check company profile absence
    profile_missing = 1 if len(company_profile.strip()) == 0 else 0
    if profile_missing and len(description.strip()) > 50:
        detected_flags.append({
            "id": "missing_profile",
            "category": "Missing Company Information",
            "severity": "MEDIUM",
            "matched_terms": ["No Company Profile"],
            "reason": "The posting contains no verified background or identity for the employer."
        })
        
    if has_company_logo == 0:
        detected_flags.append({
            "id": "missing_logo",
            "category": "Missing Corporate Logo/Branding",
            "severity": "LOW",
            "matched_terms": ["No Logo"],
            "reason": "Fraudulent listings are 4x less likely to have verified company branding."
        })

    # 2. Machine Learning Inference
    pipeline = get_pipeline()
    ml_probability = 0.0
    
    if pipeline is not None:
        try:
            full_text_clean = clean_text_simple(combined_raw)
            char_length = len(combined_raw)
            caps_ratio = sum(1 for c in combined_raw if c.isupper()) / max(len(combined_raw), 1)
            
            input_df = pd.DataFrame([{
                'full_text': full_text_clean,
                'has_company_logo': has_company_logo,
                'telecommuting': telecommuting,
                'has_questions': has_questions,
                'profile_missing': profile_missing,
                'suspicious_term_count': suspicious_term_count,
                'char_length': char_length,
                'caps_ratio': caps_ratio
            }])
            
            proba = pipeline.predict_proba(input_df)[0]
            # proba[1] is probability of fraudulent
            ml_probability = float(proba[1])
        except Exception as e:
            print(f"ML Inference fallback due to: {e}")
            ml_probability = min(0.95, suspicious_term_count * 0.25)
    else:
        # Fallback if model file is still compiling
        ml_probability = min(0.95, suspicious_term_count * 0.25)

    # 3. Hybrid Risk Calculation
    # High/Critical flags boost risk score to prevent false negatives on short texts
    flag_risk_boost = 0.0
    for flag in detected_flags:
        if flag["severity"] == "CRITICAL":
            flag_risk_boost += 0.35
        elif flag["severity"] == "HIGH":
            flag_risk_boost += 0.20
        elif flag["severity"] == "MEDIUM":
            flag_risk_boost += 0.10
        elif flag["severity"] == "LOW":
            flag_risk_boost += 0.05
            
    # Blended score: 65% ML model + 35% heuristic, clamped [0, 1]
    blended_score = max(ml_probability, min(1.0, (ml_probability * 0.6) + flag_risk_boost))
    
    # If critical red flag (like advance check scam or telegram hire), minimum risk floor is 75%
    if any(f["severity"] == "CRITICAL" for f in detected_flags):
        blended_score = max(blended_score, 0.85)
    elif any(f["severity"] == "HIGH" for f in detected_flags) and len(detected_flags) >= 2:
        blended_score = max(blended_score, 0.75)
        
    risk_percentage = round(blended_score * 100, 1)
    
    # 4. Classification Verdict
    if risk_percentage >= 70.0:
        verdict = "Fraudulent (Fake Job)"
        status_color = "danger"
        badge_text = "HIGH RISK - LIKELY SCAM"
        recommendation = "Do NOT apply or share personal/banking information. This job posting contains severe scam patterns commonly associated with employment fraud."
    elif risk_percentage >= 35.0:
        verdict = "Suspicious (Proceed with Caution)"
        status_color = "warning"
        badge_text = "MODERATE RISK - SUSPICIOUS"
        recommendation = "Exercise caution. Verify the company independently on LinkedIn, Glassdoor, and their official careers page before responding."
    else:
        verdict = "Legitimate Job Posting"
        status_color = "success"
        badge_text = "LOW RISK - LIKELY SAFE"
        recommendation = "This posting follows standard corporate recruitment practices with standard language and verified hiring norms."

    # 5. Highlight text generation
    highlighted_description = generate_highlighted_html(description, RED_FLAG_PATTERNS)

    # 6. Safety Checklist
    checklist = [
        {"item": "Company email has a corporate domain (not @gmail / @yahoo)", "passed": not any(f.get("id") == "free_webmail" for f in detected_flags)},
        {"item": "Official interview process (No Telegram/WhatsApp-only chats)", "passed": not any(f.get("id") == "chat_app" for f in detected_flags)},
        {"item": "No upfront money, equipment checks, or application fees required", "passed": not any(f.get("id") in ["advance_fee_check", "wire_transfer_crypto", "bank_details_request"] for f in detected_flags)},
        {"item": "Detailed company background and verified corporate profile", "passed": profile_missing == 0},
        {"item": "Realistic compensation matching typical industry benchmarks", "passed": not any(f.get("id") == "unrealistic_promise" for f in detected_flags)}
    ]

    return {
        "verdict": verdict,
        "is_fake": risk_percentage >= 50.0,
        "risk_percentage": risk_percentage,
        "ml_probability": round(ml_probability * 100, 1),
        "status_color": status_color,
        "badge_text": badge_text,
        "red_flags": detected_flags,
        "red_flag_count": len(detected_flags),
        "recommendation": recommendation,
        "highlighted_description": highlighted_description,
        "safety_checklist": checklist,
        "features_analyzed": {
            "has_company_logo": bool(has_company_logo),
            "telecommuting": bool(telecommuting),
            "has_questions": bool(has_questions),
            "profile_missing": bool(profile_missing),
            "suspicious_terms_found": suspicious_term_count,
            "char_count": len(combined_raw)
        }
    }

def generate_highlighted_html(text, patterns):
    """Wraps suspicious substrings in marked HTML tags with tooltips."""
    if not text:
        return ""
    
    html = text
    # Replace matches with styled spans
    for p in patterns:
        def repl(match):
            term = match.group(0)
            sev = p["severity"].lower()
            return f'<mark class="flag-mark flag-{sev}" title="{p["category"]}: {p["reason"]}">{term}</mark>'
        try:
            html = re.sub(p["regex"], repl, html, flags=re.IGNORECASE)
        except Exception:
            pass
            
    # Convert newlines to HTML breaks
    html = html.replace("\n", "<br>")
    return html
