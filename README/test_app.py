import unittest
import json
from app import app

class FakeJobDetectorTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JobShield", response.data)

    def test_analytics_page(self):
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Machine Learning Model Benchmarks", response.data)

    def test_history_page(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Audit & Scan History", response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"System Architecture", response.data)

    def test_scan_real_job(self):
        response = self.app.post('/scan', data={
            'scan_mode': 'form',
            'title': 'Senior Python Backend Developer',
            'company_name': 'TechCorp Global',
            'company_profile': 'TechCorp is an established software engineering company.',
            'description': 'We are looking for a Senior Python Developer with Django experience.',
            'requirements': '5+ years experience, BS in Computer Science.',
            'benefits': 'Health insurance, 401k, PTO.',
            'contact_email': 'jobs@techcorp.com',
            'telecommuting': '0',
            'has_company_logo': '1',
            'has_questions': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Legitimate Job Posting", response.data)

    def test_scan_fake_job(self):
        response = self.app.post('/scan', data={
            'scan_mode': 'quick',
            'quick_title': 'Urgent Data Entry',
            'quick_company': 'Quick Cash LLC',
            'raw_text': 'Earn $50/hour working from home! No experience required! We send an upfront cashier check for $3000 to purchase equipment from our vendor. Contact us on Telegram @hr_manager.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fraudulent", response.data)
        self.assertIn(b"Red Flags", response.data)

    def test_api_predict(self):
        payload = {
            "title": "Data Entry Assistant",
            "company_name": "Fast Earn LLC",
            "company_profile": "",
            "description": "Send resume on Telegram @quick_hire. Upfront check of $2,000 sent for software licenses.",
            "requirements": "No experience needed.",
            "benefits": "$500 daily guaranteed.",
            "telecommuting": 1,
            "has_company_logo": 0,
            "has_questions": 0
        }
        response = self.app.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["result"]["is_fake"])
        self.assertGreaterEqual(data["result"]["risk_percentage"], 70.0)

    def test_api_metrics(self):
        response = self.app.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("champion_model", data)
        self.assertIn("models", data)

if __name__ == '__main__':
    unittest.main()
