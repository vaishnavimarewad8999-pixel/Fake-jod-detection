import os
import json
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

SUSPICIOUS_PHRASES = [
    r"telegram", r"whatsapp", r"cashier'?s?\s*check", r"western\s*union", r"moneygram",
    r"gift\s*card", r"wire\s*transfer", r"no\s*experience\s*(needed|required)",
    r"upfront\s*check", r"passive\s*income", r"daily\s*payout", r"guaranteed\s*income",
    r"reship", r"package\s*inspector", r"secret\s*shopper", r"mystery\s*shopper",
    r"urgent\s*requirement", r"immediate\s*hire", r"start\s*today", r"macbook\s*provided",
    r"@gmail\.com", r"@yahoo\.com", r"@hotmail\.com", r"@outlook\.com"
]

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_metadata_features(df):
    """Derive rich numerical/categorical features from raw columns."""
    features = pd.DataFrame(index=df.index)
    
    # 1. Direct flags
    features['has_company_logo'] = df['has_company_logo'].fillna(0).astype(int)
    features['telecommuting'] = df['telecommuting'].fillna(0).astype(int)
    features['has_questions'] = df['has_questions'].fillna(0).astype(int)
    
    # 2. Company profile absence flag
    features['profile_missing'] = df['company_profile'].fillna('').apply(lambda x: 1 if len(str(x).strip()) == 0 else 0)
    
    # 3. Combined raw text for keyword analysis
    combined_raw = (
        df['title'].fillna('') + ' ' +
        df['company_profile'].fillna('') + ' ' +
        df['description'].fillna('') + ' ' +
        df['requirements'].fillna('') + ' ' +
        df['benefits'].fillna('')
    )
    
    # 4. Count of suspicious trigger terms
    def count_triggers(text):
        text_lower = str(text).lower()
        count = sum(1 for phrase in SUSPICIOUS_PHRASES if re.search(phrase, text_lower))
        return count
    
    features['suspicious_term_count'] = combined_raw.apply(count_triggers)
    
    # 5. Text length & Capitalization ratio
    features['char_length'] = combined_raw.apply(lambda x: len(str(x)))
    features['caps_ratio'] = combined_raw.apply(
        lambda x: sum(1 for c in str(x) if c.isupper()) / max(len(str(x)), 1)
    )
    
    return features

def prepare_data(data_path="dataset/fake_job_postings.csv"):
    df = pd.read_csv(data_path)
    
    # Combined textual feature for NLP
    df['full_text'] = (
        df['title'].fillna('') + ' ' +
        df['company_profile'].fillna('') + ' ' +
        df['description'].fillna('') + ' ' +
        df['requirements'].fillna('') + ' ' +
        df['benefits'].fillna('')
    ).apply(clean_text)
    
    meta_df = extract_metadata_features(df)
    
    X = pd.concat([df[['full_text']], meta_df], axis=1)
    y = df['fraudulent'].values
    
    return X, y, df

def train_and_evaluate():
    os.makedirs("model", exist_ok=True)
    print("Preparing dataset and engineering features...")
    X, y, raw_df = prepare_data()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples")
    print(f"Fraudulent ratio in train: {np.mean(y_train):.2%}, test: {np.mean(y_test):.2%}")
    
    # Preprocessor: TF-IDF for full_text + StandardScaler for numeric features
    meta_cols = ['has_company_logo', 'telecommuting', 'has_questions', 'profile_missing', 'suspicious_term_count', 'char_length', 'caps_ratio']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(max_features=4000, ngram_range=(1, 2), stop_words='english', sublinear_tf=True), 'full_text'),
            ('meta', StandardScaler(), meta_cols)
        ]
    )
    
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=18, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=2.0, random_state=42),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.5) # Using non-negative features for text
    }
    
    # Separate preprocessor for MultinomialNB (text only, because NaiveBayes requires non-negative features)
    text_preprocessor = ColumnTransformer(
        transformers=[
            ('text', TfidfVectorizer(max_features=4000, ngram_range=(1, 2), stop_words='english'), 'full_text')
        ]
    )
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    best_pipeline = None
    
    for name, clf in models.items():
        print(f"\n--- Training {name} ---")
        if name == "Multinomial Naive Bayes":
            pipe = Pipeline([
                ('preprocessor', text_preprocessor),
                ('classifier', clf)
            ])
        else:
            pipe = Pipeline([
                ('preprocessor', preprocessor),
                ('classifier', clf)
            ])
            
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        
        # Probabilities
        if hasattr(pipe, "predict_proba"):
            y_proba = pipe.predict_proba(X_test)[:, 1]
            roc_auc = float(roc_auc_score(y_test, y_proba))
        else:
            roc_auc = float(roc_auc_score(y_test, y_pred))
            
        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "roc_auc": round(roc_auc * 100, 2),
            "confusion_matrix": {
                "true_negative": cm[0][0],
                "false_positive": cm[0][1],
                "false_negative": cm[1][0],
                "true_positive": cm[1][1]
            }
        }
        
        print(f"Accuracy:  {acc*100:.2f}%")
        print(f"Precision: {prec*100:.2f}%")
        print(f"Recall:    {rec*100:.2f}%")
        print(f"F1 Score:  {f1*100:.2f}%")
        print(f"ROC-AUC:   {roc_auc*100:.2f}%")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipe
            
    print(f"\n==========================================")
    print(f"Selected Champion Model: {best_model_name} with F1: {best_f1*100:.2f}%")
    print(f"==========================================")
    
    # Save best pipeline
    model_path = "model/fake_job_detector.joblib"
    joblib.dump(best_pipeline, model_path)
    print(f"Saved best model to '{model_path}'")
    
    # Extract top indicative features (from TF-IDF vocabulary + coefficients/importances)
    top_features = extract_top_features(best_pipeline, best_model_name)
    with open("model/top_features.json", "w") as f:
        json.dump(top_features, f, indent=4)
        
    # Save overall metrics
    metrics_summary = {
        "champion_model": best_model_name,
        "models": results,
        "dataset_stats": {
            "total_records": len(raw_df),
            "real_jobs": int(np.sum(y == 0)),
            "fake_jobs": int(np.sum(y == 1)),
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }
    }
    
    with open("model/metrics.json", "w") as f:
        json.dump(metrics_summary, f, indent=4)
    print("Saved evaluation metrics to 'model/metrics.json'")

def extract_top_features(pipeline, model_name):
    """Extract top indicative keywords for fake jobs."""
    try:
        preprocessor = pipeline.named_steps['preprocessor']
        text_vec = preprocessor.named_transformers_['text']
        feature_names = list(text_vec.get_feature_names_out())
        
        classifier = pipeline.named_steps['classifier']
        if hasattr(classifier, 'feature_importances_'):
            # Random Forest
            importances = classifier.feature_importances_[:len(feature_names)]
            top_indices = np.argsort(importances)[::-1][:30]
            top_keywords = [{"word": feature_names[i], "score": round(float(importances[i]) * 100, 3)} for i in top_indices]
        elif hasattr(classifier, 'coef_'):
            # Logistic Regression
            coefs = classifier.coef_[0][:len(feature_names)]
            top_indices = np.argsort(coefs)[::-1][:30]
            top_keywords = [{"word": feature_names[i], "score": round(float(coefs[i]), 3)} for i in top_indices]
        else:
            top_keywords = []
            
        return {"top_fraud_indicators": top_keywords}
    except Exception as e:
        print("Feature extraction note:", e)
        return {"top_fraud_indicators": []}

if __name__ == "__main__":
    train_and_evaluate()
