"""
JobSafe AI - Offer Letter Verification Module
Analyzes employment offer letters (PDF, JPG, JPEG, PNG) for fraud indicators.
"""

import os
import re
import subprocess
from pypdf import PdfReader

# Genuine Offer Letter Scam Red-Flag Heuristics
OFFER_RED_FLAG_PATTERNS = [
    {
        "id": "upfront_fee",
        "category": "Upfront Payment or Security Deposit Demand",
        "severity": "CRITICAL",
        "regex": r"\b(security\s*deposit|refundable\s*deposit|training\s*(fee|cost|charge)|registration\s*fee|laptop\s*deposit|equipment\s*(deposit|fee)|uniform\s*fee|visa\s*(processing\s*)?fee|documentation\s*charge|pay\s*before\s*joining|pay\s*\$?\d{2,}\s*to\s*(reserve|confirm|process))\b",
        "reason": "Legitimate employers NEVER ask a candidate to pay a security deposit, training fee, or laptop fee before joining."
    },
    {
        "id": "advance_check",
        "category": "Cashier Check / Equipment Purchase Scam",
        "severity": "CRITICAL",
        "regex": r"\b(cashier'?s?\s*check|upfront\s*check|check\s*deposit|purchase\s*(office\s*)?equipment\s*from\s*(our\s*)?vendor|approved\s*vendor|deposit\s*the\s*check\s*and\s*send)\b",
        "reason": "Fake offer letters often direct victims to deposit a counterfeit cashier check and wire money to a fake vendor for home office equipment."
    },
    {
        "id": "untraceable_payment",
        "category": "Demands for Untraceable Payment Methods",
        "severity": "CRITICAL",
        "regex": r"\b(wire\s*transfer|western\s*union|moneygram|bitcoin|crypto(currency)?|zelle|cash\s*app|gift\s*cards?|steam\s*cards?|apple\s*gift\s*card)\b",
        "reason": "Official corporations never ask candidates to send funds via cryptocurrency, Western Union, Zelle, or retail gift cards."
    },
    {
        "id": "sensitive_data_demand",
        "category": "Premature Financial or Identity Harvesting",
        "severity": "HIGH",
        "regex": r"\b(bank\s*login|net\s*banking|credit\s*card\s*(number|details|cvv)|atm\s*pin|send\s*your\s*(full\s*)?ssn|social\s*security\s*card|bank\s*account\s*passbook)\b",
        "reason": "Demands for credit card numbers, ATM PINs, online banking logins, or SSN card photos before formal onboarding are high identity theft risks."
    },
    {
        "id": "chat_recruitment",
        "category": "Unofficial Messaging Channel",
        "severity": "HIGH",
        "regex": r"\b(telegram|whatsapp|signal\s*app|google\s*chat|kik|skype\s*interview)\b|(?<![a-zA-Z0-9_.+-])@[a-zA-Z0-9_]{3,}(?!\.[a-zA-Z]{2,})",
        "reason": "Corporate offer letters do not conduct onboarding or communication exclusively via personal messaging platforms like Telegram or WhatsApp."
    },
    {
        "id": "free_webmail",
        "category": "Free Webmail Domain Used in Official Offer",
        "severity": "HIGH",
        "regex": r"\b[a-zA-Z0-9_.+-]+@(gmail\.com|yahoo\.com|hotmail\.com|outlook\.com|aol\.com)\b",
        "reason": "Legitimate enterprise offer letters originate from corporate domain emails (e.g. hr@company.com), never free public webmail accounts."
    },
    {
        "id": "urgent_deadline",
        "category": "Extreme Pressure or Unrealistic Deadline",
        "severity": "MEDIUM",
        "regex": r"\b(within\s*(24|12|6)\s*hours|valid\s*(only\s*)?for\s*today|immediate\s*acceptance\s*required|limited\s*spots?\s*left|expire(s)?\s*in\s*24\s*hours)\b",
        "reason": "Scammers enforce tight, high-pressure deadlines to prevent candidates from verifying the organization or consulting mentors."
    },
    {
        "id": "unrealistic_compensation",
        "category": "Unrealistic or Guaranteed Extravagant Compensation",
        "severity": "MEDIUM",
        "regex": r"\b(guaranteed\s*bonus\s*of\s*\$?\d{4,}|earn\s*\$?\d{3,}\s*(daily|a day)|get\s*rich|no\s*experience\s*required.*\$?\d{5,}|free\s*macbook\s*pro\s*shipped\s*today)\b",
        "reason": "Offers featuring extraordinarily inflated compensation packages for minimal or entry-level duties frequently indicate deception."
    },
    {
        "id": "suspicious_links",
        "category": "Suspicious External Links / URL Shorteners",
        "severity": "HIGH",
        "regex": r"\b(bit\.ly|tinyurl\.com|t\.me|wa\.me|goo\.gl|cutt\.ly|is\.gd|rb\.gy)/[a-zA-Z0-9_-]+",
        "reason": "Official offer documents avoid using URL shorteners or direct instant-messaging invite links."
    },
    {
        "id": "reshipping_tasks",
        "category": "Package Reshipping or Money Mule Clauses",
        "severity": "HIGH",
        "regex": r"\b(package\s*inspector|shipping\s*forwarder|repackag(e|ing)|receive\s*and\s*forward\s*parcels?|payment\s*processing\s*agent)\b",
        "reason": "Offers mentioning package forwarding or personal payment processing involve victims in stolen goods handling and money laundering."
    }
]

def extract_text_from_pdf(file_path):
    """Extracts raw text from a PDF file using pypdf."""
    text_parts = []
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
    return "\n\n".join(text_parts).strip()

def extract_text_from_image(file_path):
    """Extracts text from an image file using Windows native OCR or pytesseract."""
    # 1. Try pytesseract if available
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(file_path)
        ocr_text = pytesseract.image_to_string(img)
        if ocr_text and len(ocr_text.strip()) > 10:
            return ocr_text.strip()
    except Exception:
        pass

    # 2. Try Windows native Runtime OCR via PowerShell
    try:
        abs_path = os.path.abspath(file_path)
        ps_script = f"""
        Add-Type -AssemblyName System.Runtime.WindowsRuntime
        $asTaskGeneric = [System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }}[0]
        function Await($WinRtTask, $ResultType) {{
            $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
            $netTask = $asTask.Invoke($null, @($WinRtTask))
            $netTask.Wait(-1) | Out-Null
            $netTask.Result
        }}
        [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
        [Windows.Media.Ocr.OcrEngine,Windows.Foundation.UniversalApiContract,ContentType=WindowsRuntime] | Out-Null
        $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync('{abs_path}')) ([Windows.Storage.StorageFile])
        $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
        if ($engine -eq $null) {{ $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new('en-US')) }}
        $ocrResult = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $ocrResult.Text
        """
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True,
            timeout=15
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception as e:
        print(f"Windows OCR failed: {e}")

    # Fallback placeholder if image has no machine-readable text
    return ""

def extract_text_from_file(file_path, filename=""):
    """Determines file type and routes to appropriate extraction handler."""
    ext = os.path.splitext(filename or file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    return ""

def analyze_offer_letter(text, filename=""):
    """
    Evaluates extracted offer letter text against genuine employment scam patterns.
    Returns structured analysis dictionary.
    """
    cleaned_text = text.strip() if text else ""
    detected_flags = []
    suspicious_count = 0
    highlight_spans = []

    if cleaned_text:
        for item in OFFER_RED_FLAG_PATTERNS:
            matches = list(re.finditer(item["regex"], cleaned_text, re.IGNORECASE))
            if matches:
                matched_terms = list(set([m.group(0) for m in matches]))
                detected_flags.append({
                    "id": item["id"],
                    "category": item["category"],
                    "severity": item["severity"],
                    "matched_terms": matched_terms,
                    "reason": item["reason"]
                })
                suspicious_count += len(matches)

    # Calculate Risk Score based strictly on detected signals
    flag_risk_boost = 0.0
    for flag in detected_flags:
        if flag["severity"] == "CRITICAL":
            flag_risk_boost += 0.40
        elif flag["severity"] == "HIGH":
            flag_risk_boost += 0.25
        elif flag["severity"] == "MEDIUM":
            flag_risk_boost += 0.12

    if not cleaned_text:
        # Document had no extractable text
        risk_score = 45.0
        verdict = "Suspicious"
        status_color = "warning"
        risk_level = "MODERATE RISK"
        badge_text = "MODERATE RISK - NO TEXT FOUND"
        summary = "No legible text could be extracted from this document. Please ensure the document is clear, non-corrupted, and contains readable text."
        recommendation = "Upload a higher-resolution version or a text-based PDF to verify the authenticity of the offer."
    elif len(detected_flags) == 0:
        # No red flags detected
        risk_score = 8.0
        verdict = "Likely Genuine"
        status_color = "success"
        risk_level = "LOW RISK"
        badge_text = "LOW RISK - LIKELY GENUINE"
        summary = "No deceptive fee requests, untraceable payments, or suspicious recruitment vectors were detected in this offer letter."
        recommendation = "The offer letter follows standard corporate practices. As a standard precaution, independently verify the hiring organization's official website and domain."
    else:
        # Calculate blended score
        calculated_risk = min(1.0, 0.15 + flag_risk_boost)
        if any(f["severity"] == "CRITICAL" for f in detected_flags):
            calculated_risk = max(calculated_risk, 0.85)
        elif any(f["severity"] == "HIGH" for f in detected_flags) and len(detected_flags) >= 2:
            calculated_risk = max(calculated_risk, 0.78)
        elif any(f["severity"] == "HIGH" for f in detected_flags):
            calculated_risk = max(calculated_risk, 0.70)
        elif any(f["severity"] == "MEDIUM" for f in detected_flags):
            calculated_risk = max(calculated_risk, 0.45)

        risk_score = round(calculated_risk * 100, 1)

        if risk_score >= 70.0:
            verdict = "High Risk"
            status_color = "danger"
            risk_level = "HIGH RISK"
            badge_text = "HIGH RISK - POTENTIAL SCAM"
            summary = f"This offer letter contains {len(detected_flags)} serious red flag(s) commonly associated with fraudulent employment schemes."
            recommendation = "DO NOT transfer any money, purchase equipment, or share banking credentials. Contact the hiring company directly using their publicly listed corporate contact number."
        else:
            verdict = "Suspicious"
            status_color = "warning"
            risk_level = "MODERATE RISK"
            badge_text = "MODERATE RISK - SUSPICIOUS"
            summary = f"This document triggered {len(detected_flags)} suspicious indicator(s) that require verification before proceeding."
            recommendation = "Exercise caution. Confirm the recruiter's identity on LinkedIn and check whether the communication originated from a verified corporate domain."

    # Generate highlighted HTML text
    highlighted_html = generate_offer_highlighted_html(cleaned_text, OFFER_RED_FLAG_PATTERNS)

    return {
        "verdict": verdict,
        "status_color": status_color,
        "risk_level": risk_level,
        "badge_text": badge_text,
        "risk_score": risk_score,
        "red_flags": detected_flags,
        "red_flag_count": len(detected_flags),
        "analysis_summary": summary,
        "recommended_action": recommendation,
        "highlighted_text": highlighted_html,
        "extracted_text": cleaned_text[:2500] if cleaned_text else "No extractable text found.",
        "filename": filename,
        "disclaimer": "This result is an AI-based risk assessment and should not be treated as official verification."
    }

def generate_offer_highlighted_html(text, patterns):
    """Highlights flagged phrases in HTML with contextual badges."""
    if not text:
        return "<p class='text-muted italic'>No extractable text found in document.</p>"

    html = text
    for p in patterns:
        def repl(match):
            term = match.group(0)
            sev = p["severity"].lower()
            return f'<mark class="flag-mark flag-{sev}" title="{p["category"]}: {p["reason"]}">{term}</mark>'
        try:
            html = re.sub(p["regex"], repl, html, flags=re.IGNORECASE)
        except Exception:
            pass

    return html.replace("\n", "<br>")
