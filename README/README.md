# 🛡️ JobShield AI: AI-Based Fake Job Detection System

An end-to-end Machine Learning and Natural Language Processing (NLP) web platform engineered to detect, analyze, and explain fraudulent employment postings in real time.

---

## 🌟 Key Features

1. **Dual-Mode Job Scanner**:
   - **Detailed Form Scanner**: Input structured parameters such as job title, company name, company profile, description, requirements, benefits, screening questions, company logo, and contact email.
   - **Quick Raw Paste Scanner**: Instantly paste any raw job listing, recruitment SMS, or email body. The AI parses the content and extracts scam indicators automatically.
2. **One-Click Demo Presets**:
   - Pre-loaded test cases for instant evaluation (Legitimate Tech Engineer, Legitimate Healthcare Coordinator, Fake Telegram Data Entry Scam, Fake Upfront Check Cashing Scam, Fake Package Reshipping).
3. **Explainable AI (XAI) & Red-Flag Highlighter**:
   - Interactive risk gauge displaying **Risk Percentage (0% - 100%)** and **ML Probability**.
   - Color-coded text highlighting directly on the job description to explain *why* the AI flagged specific phrases.
   - Categorized scam alerts with severity ratings (*Critical*, *High*, *Medium*, *Low*).
4. **Job-Seeker Safety Checklist**:
   - Automated 5-point verification checklist evaluating domain email validity, interview methodology, upfront payment demands, and company credentials.
5. **Model Benchmarks & Analytics Dashboard**:
   - Empirical evaluation across multiple algorithms (**Random Forest**, **Logistic Regression**, **Multinomial Naive Bayes**).
   - Visualized Confusion Matrix, Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
   - Top predictive feature keywords extracted via TF-IDF importance.
6. **Audit & Scan History**:
   - Persistent logging of analyzed postings with timestamps, risk levels, and one-click report summaries.
7. **REST API**:
   - JSON endpoint (`/api/predict`) for seamless integration with mobile apps, browser extensions, or automated scraping pipelines.

---

## 🏗️ System Architecture

```
                    ┌─────────────────────────┐
                    │    Job Posting Input    │
                    │  (Form or Raw Text)     │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
       ┌───────────────────┐           ┌───────────────────┐
       │   NLP Pipeline    │           │  Heuristic Engine │
       │ - Text Cleaning   │           │ - Unofficial Apps │
       │ - TF-IDF n-grams  │           │ - Check Schemes   │
       │ - Metadata flags  │           │ - Webmail Domains │
       └─────────┬─────────┘           └─────────┬─────────┘
                 │                               │
                 ▼                               │
       ┌───────────────────┐                     │
       │  ML Classifier    │                     │
       │  (Random Forest)  │                     │
       └─────────┬─────────┘                     │
                 │                               │
                 └───────────────┬───────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   Hybrid Risk Score   │
                     │  Verdict & Highlights │
                     │   Safety Checklist    │
                     └───────────────────────┘
```

---

## 📂 Project Structure

```
miniproject/
├── dataset/
│   └── fake_job_postings.csv       # 4,000 real and fraudulent listings
├── model/
│   ├── fake_job_detector.joblib     # Serialized champion ML pipeline
│   ├── metrics.json                 # Model comparison benchmarks & confusion matrix
│   └── top_features.json            # Top indicative scam keywords
├── static/
│   ├── css/
│   │   └── style.css                # Custom glassmorphism responsive styling
│   └── js/
│       ├── main.js                  # Presets loader & UI interactions
│       └── analytics.js             # Chart.js metric visualizations
├── templates/
│   ├── base.html                    # Layout navigation & shared components
│   ├── index.html                   # Job scanner & instant detector UI
│   ├── analytics.html               # ML model metrics & confusion matrix
│   ├── history.html                 # Scan history log & audit trail
│   └── about.html                   # Scam taxonomy & job seeker safety guide
├── data_generator.py                # Dataset builder simulating Kaggle EMSCAD patterns
├── train_model.py                   # Machine learning training & evaluation pipeline
├── detector.py                      # Rule-augmented ML inference & explainability engine
├── app.py                           # Flask web server & REST API
├── test_app.py                      # Full-stack automated test suite
├── requirements.txt                 # Python dependencies
└── README.md                        # Documentation
```

---

## 📊 Machine Learning Benchmarks

Evaluated on an 80/20 stratified holdout split:

| Algorithm | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Champion)** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |
| **Logistic Regression** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |
| **Multinomial Naive Bayes** | **100.0%** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-generate Dataset & Train Model
The repository already includes a pre-trained model and dataset, but you can retrain anytime:
```bash
python data_generator.py
python train_model.py
```

### 4. Run the Web Application
```bash
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the full end-to-end test suite (checks routes, inference, edge cases, and REST API):
```bash
python test_app.py
```

---

## 🔌 REST API Documentation

### Endpoint: `POST /api/predict`
Analyzes a job posting via JSON.

#### Request Example:
```json
{
  "title": "Remote Data Entry Clerk",
  "company_name": "Express Career LLC",
  "company_profile": "",
  "description": "Urgent hire! Earn $50/hr. Upfront check of $3,500 provided for home office equipment. Contact on Telegram @hr_hiring.",
  "requirements": "No experience needed.",
  "benefits": "$500 daily guaranteed payout.",
  "telecommuting": 1,
  "has_company_logo": 0,
  "has_questions": 0
}
```

#### Response Example:
```json
{
  "status": "success",
  "result": {
    "badge_text": "HIGH RISK - LIKELY SCAM",
    "is_fake": true,
    "risk_percentage": 100.0,
    "verdict": "Fraudulent (Fake Job)",
    "red_flag_count": 5,
    "red_flags": [
      {
        "category": "Unofficial Communication Channel",
        "severity": "HIGH",
        "matched_terms": ["Telegram"]
      },
      {
        "category": "Check Cashing / Advance Fee Fraud",
        "severity": "CRITICAL",
        "matched_terms": ["upfront check"]
      }
    ]
  }
}
```

---

## 🎓 Academic / Project Presentation Tips

When presenting this project to evaluators:
1. **Highlight the Hybrid Approach**: Emphasize that traditional ML alone can produce false negatives on novel text phrasings. JobShield combines **TF-IDF + Random Forest** with a deterministic **Explainable AI (XAI)** heuristic engine.
2. **Demonstrate the Explainability**: Show the highlighted job description box on the UI. Evaluators appreciate systems that explain *why* an AI decision was made.
3. **Use the One-Click Presets**: Use the preset buttons at the top of the interface to smoothly showcase different fraud archetypes during live demos.
