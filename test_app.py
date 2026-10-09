import unittest
import json
from app import app

class JobSafeAITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def login(self, username="admin", password="admin123"):
        return self.app.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # 1. Authentication Tests
    def test_unauthenticated_access_redirects(self):
        """Unauthenticated user accessing protected route is redirected to /login"""
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers.get('Location', ''))

        response_analyzer = self.app.get('/analyzer')
        self.assertEqual(response_analyzer.status_code, 302)

        response_history = self.app.get('/history')
        self.assertEqual(response_history.status_code, 302)

    def test_login_valid_credentials(self):
        """Valid credentials log in successfully and redirect to dashboard"""
        response = self.login("admin", "admin123")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JobSafe AI", response.data)
        self.assertIn(b"Welcome to", response.data)

    def test_login_invalid_credentials(self):
        """Invalid credentials show error notification"""
        response = self.login("admin", "wrongpassword")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid username/email or password", response.data)

    def test_register_new_user(self):
        """New user can register and access dashboard"""
        import uuid
        uid = uuid.uuid4().hex[:6]
        response = self.app.post('/register', data={
            'name': 'Sarah Connor',
            'email': f'sarah_{uid}@skynet.com',
            'username': f'sarahc_{uid}',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
            'language': 'en'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JobSafe AI", response.data)
        self.assertIn(b"Welcome", response.data)

    def test_logout_clears_session(self):
        """Logout clears session and redirects back to login page"""
        self.login("admin", "admin123")
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JobSafe AI", response.data)
        self.assertIn(b"Sign In to Dashboard", response.data)

        # Verify subsequent protected page access is blocked
        protected_resp = self.app.get('/dashboard')
        self.assertEqual(protected_resp.status_code, 302)

    # 2. Main Protected Pages Tests (With Session)
    def test_home_page(self):
        """Logged in user on / is redirected to dashboard containing JobSafe AI"""
        self.login("admin", "admin123")
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JobSafe AI", response.data)

    def test_dashboard_page(self):
        """Dashboard renders with statistics and welcome banner"""
        self.login("admin", "admin123")
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to", response.data)
        self.assertIn(b"JobSafe AI", response.data)
        self.assertIn(b"Total Jobs Analyzed", response.data)
        self.assertIn(b"AI Risk Overview", response.data)

    def test_analyzer_page(self):
        """Job Analyzer page renders with input form and presets"""
        self.login("admin", "admin123")
        response = self.app.get('/analyzer')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Job Listing Analyzer", response.data)
        self.assertIn(b"Detailed Form", response.data)

    def test_analytics_page(self):
        """Model Analytics page renders benchmarks and charts"""
        self.login("admin", "admin123")
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Machine Learning Model Benchmarks", response.data)

    def test_history_page(self):
        """History page renders audit trail"""
        self.login("admin", "admin123")
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Audit &", response.data)

    def test_about_page(self):
        """About page renders 5-step pipeline architecture and Why JobSafe AI"""
        self.login("admin", "admin123")
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"System Architecture", response.data)
        self.assertIn(b"Why JobSafe AI?", response.data)

    # 3. Job Prediction Tests
    def test_scan_real_job(self):
        """Authentic job posting classifies as Legitimate"""
        self.login("admin", "admin123")
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
        """Scam listing triggers red flags and classifies as Fraudulent"""
        self.login("admin", "admin123")
        response = self.app.post('/scan', data={
            'scan_mode': 'quick',
            'quick_title': 'Urgent Data Entry',
            'quick_company': 'Quick Cash LLC',
            'raw_text': 'Earn $50/hour working from home! No experience required! We send an upfront cashier check for $3000 to purchase equipment from our vendor. Contact us on Telegram @hr_manager.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fraudulent", response.data)
        self.assertIn(b"Red Flags", response.data)

    # 4. REST API Tests (Public / Integrations)
    def test_api_predict(self):
        """REST API predicts job risk from JSON payload"""
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
        """REST API returns champion model metrics"""
        response = self.app.get('/api/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("champion_model", data)
        self.assertIn("models", data)

    # 5. Interactive Pipeline & Preprocessing Tests
    def test_pipeline_route_redirect(self):
        """Accessing /pipeline redirects to about#pipelineSection"""
        self.login("admin", "admin123")
        response = self.app.get('/pipeline')
        self.assertEqual(response.status_code, 302)
        self.assertIn("pipelineSection", response.headers.get("Location", ""))

    def test_api_preprocess_endpoint(self):
        """/api/preprocess sanitizes text and returns transformation stages and metrics"""
        payload = {
            "text": "HIRING NOW! Contact us at recruiter@jobsafe.ai or visit https://jobs.example.com/apply. $50/hr & bonus!"
        }
        response = self.app.post('/api/preprocess', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("preprocessing", data)
        self.assertIn("cleaned_text", data["preprocessing"])
        self.assertIn("stats", data["preprocessing"])
        self.assertIn("stages", data["preprocessing"])
        # Verify URLs and emails were stripped in cleaned_text
        self.assertNotIn("https://", data["preprocessing"]["cleaned_text"])
        self.assertNotIn("@jobsafe.ai", data["preprocessing"]["cleaned_text"])

    def test_api_predict_includes_preprocessing_and_model_info(self):
        """/api/predict returns full 5-stage pipeline data: preprocessing, model_info, red_flags, risk"""
        payload = {
            "title": "Data Entry Assistant",
            "company_name": "Quick Cash LLC",
            "description": "Earn $50/hr working from home! No experience needed! Contact recruiter on Telegram @instant_hire. We send upfront cashier check for $3000.",
            "requirements": "None",
            "benefits": "$500 daily",
            "contact_email": "quickhire@gmail.com"
        }
        response = self.app.post('/api/predict', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        res = data["result"]
        # Step 2: Preprocessing
        self.assertIn("preprocessing", res)
        # Step 3: AI/ML Analysis
        self.assertIn("model_info", res)
        self.assertIn("ml_probability", res)
        # Step 4: Red-Flag Detection
        self.assertIn("red_flags", res)
        self.assertGreater(len(res["red_flags"]), 0)
        # Step 5: Risk Prediction
        self.assertIn("verdict", res)
        self.assertIn("risk_percentage", res)
        self.assertGreaterEqual(res["risk_percentage"], 70.0)

    def test_about_page_pipeline_cards_present(self):
        """About page renders all 5 clickable pipeline cards and modal inclusion"""
        self.login("admin", "admin123")
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"How JobSafe AI Works", response.data)
        self.assertIn(b"openPipelineStep(1)", response.data)
        self.assertIn(b"openPipelineStep(2)", response.data)
        self.assertIn(b"openPipelineStep(3)", response.data)
        self.assertIn(b"openPipelineStep(4)", response.data)
        self.assertIn(b"openPipelineStep(5)", response.data)
        self.assertIn(b"pipelineStudioModal", response.data)
    # 6. Audit & History Management Tests
    def test_history_page_renders_delete_and_clear_buttons(self):
        """History page includes Delete action buttons and Clear All History controls"""
        self.login("admin", "admin123")
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Audit &amp; Scan History", response.data)
        self.assertIn(b"deleteHistoryItem", response.data)
        self.assertIn(b"clearAllHistory", response.data)
        self.assertIn(b"historySearchInput", response.data)

    def test_delete_history_item_success_and_persistence(self):
        """Deleting a history record removes it permanently from disk and returns success"""
        import os
        from app import HISTORY_FILE, load_history, save_history
        self.login("admin", "admin123")

        # Backup current history
        backup = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                backup = json.load(f)

        try:
            # Create a test record
            test_item = {
                "scan_type": "job_description",
                "title": "Temporary Test Listing For Deletion",
                "company": "Temp Corp",
                "verdict": "Suspicious",
                "risk_percentage": 50.0,
                "red_flag_count": 1,
                "status_color": "warning"
            }
            save_history(test_item)
            test_id = test_item["id"]

            # Verify it is on disk
            current_history = load_history()
            self.assertTrue(any(item["id"] == test_id for item in current_history))

            # Send AJAX delete request
            del_response = self.app.post(
                f'/history/delete/{test_id}',
                headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
            )
            self.assertEqual(del_response.status_code, 200)
            data = json.loads(del_response.data)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["deleted_id"], test_id)

            # Verify it is permanently removed from disk
            reloaded_history = load_history()
            self.assertFalse(any(item["id"] == test_id for item in reloaded_history))

        finally:
            # Restore backup
            with open(HISTORY_FILE, "w") as f:
                json.dump(backup, f, indent=2)

    def test_delete_nonexistent_history_item_returns_404(self):
        """Attempting to delete a nonexistent ID returns 404 error"""
        self.login("admin", "admin123")
        response = self.app.post(
            '/history/delete/9999999',
            headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
        )
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "error")
        self.assertIn("not found", data["message"].lower())

    def test_clear_all_history_endpoint(self):
        """Clearing history empties scan_history.json and returns remaining_count 0"""
        import os
        from app import HISTORY_FILE, load_history, save_history
        self.login("admin", "admin123")

        backup = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                backup = json.load(f)

        try:
            # Ensure at least 1 record exists
            save_history({
                "scan_type": "job_description",
                "title": "Clear Test Record",
                "company": "Clear Corp",
                "verdict": "Legitimate Job Posting",
                "risk_percentage": 5.0,
                "red_flag_count": 0,
                "status_color": "success"
            })

            # Send AJAX clear request
            clear_response = self.app.post(
                '/history/clear',
                headers={'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json'}
            )
            self.assertEqual(clear_response.status_code, 200)
            data = json.loads(clear_response.data)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["remaining_count"], 0)

            # Verify disk is empty
            self.assertEqual(len(load_history()), 0)

        finally:
            # Restore backup
            with open(HISTORY_FILE, "w") as f:
                json.dump(backup, f, indent=2)

    # 7. Vercel / Read-Only Filesystem Resilience Tests
    def test_scan_route_succeeds_even_when_filesystem_is_readonly(self):
        """POST /scan completes with HTTP 200 and legitimate detection even if disk throws Errno 30 Read-only filesystem"""
        from unittest.mock import patch
        self.login("admin", "admin123")

        # Mock open to raise OSError(30, "Read-only file system: '/var/task/scan_history.json'") on write
        real_open = open
        def mock_open_readonly(file, mode="r", *args, **kwargs):
            if "w" in mode and "scan_history" in str(file):
                raise OSError(30, "Read-only file system: '/var/task/scan_history.json'")
            return real_open(file, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=mock_open_readonly):
            response = self.app.post('/scan', data={
                'scan_mode': 'form',
                'title': 'Vercel Read-Only Test Engineer',
                'company_name': 'CloudCorp',
                'description': 'We are looking for a Software Engineer with Python and AWS experience.',
                'requirements': 'BS in Computer Science.',
                'benefits': 'Health insurance.',
                'contact_email': 'careers@cloudcorp.com'
            })
            # Must NOT be 500 Internal Server Error
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Vercel Read-Only Test Engineer", response.data)
            self.assertIn(b"Legitimate Job Posting", response.data)

    def test_dashboard_action_buttons_spacing(self):
        """Dashboard action buttons container uses flex, gap: 16px, and align-items: center"""
        self.login("admin", "admin123")
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"hero-actions-container", response.data)
        self.assertIn(b"display: flex", response.data)
        self.assertIn(b"gap: 16px", response.data)
        self.assertIn(b"align-items: center", response.data)
        self.assertIn(b"Analyze Job", response.data)
        self.assertIn(b"Verify Offer Letter", response.data)
        self.assertIn(b"Model Analytics", response.data)

if __name__ == '__main__':
    unittest.main()

