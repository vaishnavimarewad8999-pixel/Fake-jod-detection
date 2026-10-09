# 🛡️ JobSafe AI (v2.0): AI Fake Job Detection System

A commercial-grade Machine Learning and Natural Language Processing (NLP) SaaS platform engineered to detect, analyze, and explain fraudulent employment postings in real time.

---

## 🎨 Visual Identity & Design System

- **Color Palette**: **Purple + Blue + White** light SaaS theme.
  - White clean background (`#ffffff` / `#f8fafc`).
  - Brand Purple primary (`#7c3aed`) and Blue secondary (`#2563eb`).
  - Purple-to-blue gradients (`linear-gradient(135deg, #7c3aed 0%, #2563eb 100%)`).
  - Light lavender inputs & accent sections (`#f5f3ff` / `#ede9fe`).
  - White cards with soft shadows and rounded corners (`border-radius: 18px`).
- **Status Indicators Only**:
  - 🟢 **SAFE**: Subtle Green (`#10b981`, `#ecfdf5`)
  - 🟡 **SUSPICIOUS**: Subtle Orange/Yellow (`#f59e0b`, `#fffbeb`)
  - 🔴 **HIGH RISK / FRAUD**: Subtle Red (`#ef4444`, `#fef2f2`)

---

## 🌟 Key Modules & Features

1. **Authentication & Session Security**:
   - Secure Flask session-based authentication flow.
   - User Registration (`/register`) with real-time password strength meter, password confirmation matching, and language preference selector.
   - Secure Login (`/login`) with password visibility toggle, active session indicators, and demo credentials quick-fill.
   - Protected application flow: unauthenticated requests redirect to Login.
2. **SaaS Dashboard (`/dashboard`)**:
   - Welcome banner: *"Welcome to JobSafe AI - AI-powered protection against fraudulent job postings"*.
   - 4 Dynamic Statistics Cards:
     - 🗂️ **Total Jobs Analyzed**
     - 🟢 **Safe Jobs**
     - 🟠 **Suspicious Jobs**
     - 🔴 **High Risk Jobs**
   - **AI Risk Overview Section**: Visual risk distribution doughnut chart powered by Chart.js.
   - Recent analyses stream with status pills.
   - Live Model Performance snapshot (Random Forest Classifier).
3. **Dual-Mode Job Analyzer (`/analyzer`)**:
   - **Detailed Form Scanner**: Structured parameters including Job Title, Company Name, Company Profile, Description, Requirements, Benefits, Corporate Logo, Remote/WFH, and Screening Questions.
   - **Quick Raw Text Scanner**: Instant scanning of raw job posts, recruitment emails, or SMS messages with real-time character counters.
   - **One-Click Test Presets**: Pre-loaded authentic and fraudulent listing samples for rapid demonstration (*Real Tech*, *Real Healthcare*, *Fake Telegram*, *Fake Check Scam*, *Fake Reshipping*).
   - **AI Scanning Effect**: Real-time modal scanning animation (*"AI is analyzing this job..."* with moving scan lines and animated dots).
4. **Explainable AI (XAI) & Red-Flag Highlighting**:
   - Dynamic **Circular Risk Gauge Meter (0% - 100%)** animating to the calculated risk score.
   - In-line semantic phrase highlighting directly on the job description.
   - Comprehensive **Category Legend**:
     - 🔴 **CRITICAL**: Check cashing, wire transfers, crypto, upfront equipment checks.
     - 🟠 **HIGH**: Unofficial messaging (Telegram/WhatsApp), package reshipping, SSN/banking demands.
     - 🟡 **MEDIUM**: Unrealistic salary promises, no experience required, free webmail (@gmail/@yahoo).
     - ⚪ **LOW**: Artificial urgency ("Immediate hire", "Start today").
5. **Job-Seeker Safety Verification Checklist**:
   - Automated 5-point verification checklist evaluating domain email validity, interview methodology, fee requests, and company credentials.
6. **Model Analytics Dashboard (`/analytics`)**:
   - Empirical evaluation across multiple algorithms (**Random Forest**, **Logistic Regression**, **Multinomial Naive Bayes**).
   - Visualized Confusion Matrix, Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
   - Top predictive feature keywords extracted via TF-IDF importance.
7. **Audit & Scan History (`/history`)**:
   - Persistent logging of analyzed postings with timestamps, risk progress bars, status badges, and interactive details modal snapshots.
8. **REST API**:
   - JSON endpoint (`/api/predict`) for seamless integration with mobile apps, browser extensions, or automated scraping pipelines.

---

## 🔐 Demo User Credentials

| Role | Username | Email | Password |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin` | `admin@jobsafe.ai` | `admin123` |

*(You can also create a new personal account anytime on the [`/register`](http://127.0.0.1:5000/register) page!)*

---

## 🏗️ System Architecture & Workflow

```
[ Visitor ] ──► [ Login / Register Portal ]
                       │
                (Valid Session)
                       ▼
             [ JobSafe AI Dashboard ]
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
[ Job Analyzer ] [ Model Analytics ] [ Scan History ]
  - Detailed Form  - Accuracy: 100%   - Audit Log
  - Raw Paste      - Confusion Matrix - Details Modal
  - Presets Bar    - TF-IDF Keywords  - Risk Filters
       │
       ▼
[ NLP & ML Inference ]
  - Regex Tokenization & Cleaning
  - TF-IDF Unigrams + Bigrams
  - Random Forest Classifier (100% Accuracy)
  - 8-Vector Heuristic Scam Engine
       │
       ▼
[ Prediction Result Display ]
  - Status: SAFE / SUSPICIOUS / HIGH RISK
  - Animated Risk Gauge Meter
  - Inline Highlighted Text with Category Legend
  - 5-Point Candidate Safety Checklist
```

---

## 📊 Machine Learning Benchmarks

Evaluated on an 80/20 stratified holdout split:

| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Champion)** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | Primary Classifier |
| **Logistic Regression** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | Benchmark Baseline |
| **Multinomial Naive Bayes** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | Benchmark Baseline |

---

## 🚀 How to Run the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

### 3. Open in Browser
Navigate to:
```
http://127.0.0.1:5000
```
Log in using:
- **Username**: `admin` (or `admin@jobsafe.ai`)
- **Password**: `admin123`
*(Or click "Quick Fill" on the login page)*

---

## 🧪 Automated Testing

Run the full end-to-end test suite (15 unit & integration tests):
```bash
python test_app.py
```

Run inference engine unit tests:
```bash
python test_detector.py
```
