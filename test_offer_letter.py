import unittest
import os
import json
import io
from app import app, load_history
from offer_letter_detector import analyze_offer_letter, OFFER_RED_FLAG_PATTERNS

class OfferLetterVerificationTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        # Sign in demo user session
        with self.client.session_transaction() as sess:
            sess["user"] = "admin"
            sess["user_name"] = "System Administrator"
            sess["user_email"] = "admin@jobsafe.ai"

    def test_detector_genuine_offer(self):
        text = """Google LLC Formal Employment Offer
Candidate: Alice Smith
Position: Staff Software Engineer
Base Salary: $210,000 per year
Benefits: 401(k) matching, health insurance, paid leave.
Hardware will be provided directly by Google Corporate IT Operations on your start date.
Contact: talent-onboarding@google.com"""
        result = analyze_offer_letter(text, filename="google_offer.pdf")
        self.assertEqual(result["verdict"], "Likely Genuine")
        self.assertEqual(result["risk_level"], "LOW RISK")
        self.assertLess(result["risk_score"], 35.0)
        self.assertEqual(result["red_flag_count"], 0)
        self.assertIn("This result is an AI-based risk assessment", result["disclaimer"])

    def test_detector_scam_upfront_fee_and_telegram(self):
        text = """OFFICIAL APPOINTMENT LETTER
Congratulations! You are hired as Remote Data Entry Specialist ($4,500/week).
You must pay a refundable security deposit of $400 before joining for laptop equipment.
Pay immediately via Bitcoin or Zelle within 24 hours.
Contact supervisor on Telegram @hr_onboarding_fast or email hr.team@gmail.com."""
        result = analyze_offer_letter(text, filename="scam_offer.pdf")
        self.assertEqual(result["verdict"], "High Risk")
        self.assertEqual(result["risk_level"], "HIGH RISK")
        self.assertGreaterEqual(result["risk_score"], 70.0)
        self.assertGreaterEqual(result["red_flag_count"], 3)
        flag_categories = [f["category"] for f in result["red_flags"]]
        self.assertTrue(any("Upfront" in c for c in flag_categories))
        self.assertTrue(any("Untraceable" in c for c in flag_categories))
        self.assertTrue(any("Messaging" in c for c in flag_categories))

    def test_detector_scam_cashier_check(self):
        text = """EMPLOYMENT AGREEMENT
We will send you an upfront cashier's check of $3,500.
Deposit the check and purchase office equipment from our approved vendor via wire transfer."""
        result = analyze_offer_letter(text, filename="check_scam.pdf")
        self.assertEqual(result["verdict"], "High Risk")
        self.assertGreaterEqual(result["risk_score"], 70.0)
        flag_categories = [f["category"] for f in result["red_flags"]]
        self.assertTrue(any("Check" in c for c in flag_categories))

    def test_detector_empty_text(self):
        result = analyze_offer_letter("", filename="empty.pdf")
        self.assertEqual(result["verdict"], "Suspicious")
        self.assertEqual(result["risk_level"], "MODERATE RISK")
        self.assertIn("No legible text", result["analysis_summary"])

    def test_route_offer_letter_get(self):
        resp = self.client.get("/offer-letter")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"AI Offer Letter Verification", resp.data)
        self.assertIn(b"Upload Offer Letter", resp.data)

    def test_route_offer_letter_demo_genuine(self):
        resp = self.client.post("/offer-letter", data={"demo_type": "genuine"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Likely Genuine", resp.data)
        self.assertIn(b"Google_Employment_Offer_Official.pdf", resp.data)

    def test_route_offer_letter_demo_scam(self):
        resp = self.client.post("/offer-letter", data={"demo_type": "scam_deposit"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"High Risk", resp.data)
        self.assertIn(b"GlobalTech_Executive_Offer_Letter.pdf", resp.data)

    def test_route_offer_letter_upload_invalid_extension(self):
        data = {
            "offer_file": (io.BytesIO(b"fake executable content"), "contract.exe")
        }
        resp = self.client.post("/offer-letter", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Unsupported file format", resp.data)

    def test_route_offer_letter_upload_valid_file(self):
        sample_doc = b"Google LLC Offer Letter. Position: Software Engineer. Salary: $160,000. Verified talent-onboarding@google.com."
        data = {
            "offer_file": (io.BytesIO(sample_doc), "my_offer.png")
        }
        resp = self.client.post("/offer-letter", data=data, content_type="multipart/form-data")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"my_offer.png", resp.data)

    def test_dashboard_and_analytics_offer_stats(self):
        dash_resp = self.client.get("/dashboard")
        self.assertEqual(dash_resp.status_code, 200)
        self.assertIn(b"Offer Letter Verification", dash_resp.data)

        analytics_resp = self.client.get("/analytics")
        self.assertEqual(analytics_resp.status_code, 200)
        self.assertIn(b"Offer Letter Verification Analytics", analytics_resp.data)

    def test_api_chat_offer_letter(self):
        resp = self.client.post("/api/chat", json={"message": "how do I verify an offer letter?"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("Offer Letter Verification", data["reply"])

if __name__ == "__main__":
    unittest.main()
