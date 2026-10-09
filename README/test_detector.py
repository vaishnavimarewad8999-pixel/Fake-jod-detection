import json
from detector import analyze_job_posting

# Test 1: Real Job
real_sample = {
    "title": "Senior Cloud Infrastructure Engineer",
    "company_name": "Apex Cloud Technologies",
    "company_profile": "Apex Cloud Technologies is an industry-leading cloud infrastructure provider serving Fortune 500 enterprises.",
    "description": "We are seeking an experienced Senior Cloud Engineer. In this role, you will design, architect, and deploy reliable AWS/Kubernetes systems.",
    "requirements": "BS/MS in Computer Science. 5+ years with Linux, Docker, Terraform, and Python. Solid understanding of CI/CD pipelines.",
    "benefits": "Competitive salary ($130,000 - $160,000), 401(k) matching, health and dental insurance, 20 days PTO.",
    "telecommuting": 0,
    "has_company_logo": 1,
    "has_questions": 1,
    "contact_email": "jobs@apexcloud.io"
}

# Test 2: Fake Job (Advance fee / Telegram scam)
fake_sample = {
    "title": "URGENT: Work From Home Data Entry Clerk ($45/hour)",
    "company_name": "Global Career Express",
    "company_profile": "",
    "description": "Earn $45-$65/hour from home! No experience required! You will receive an upfront cashier's check of $3,500 to purchase equipment from our approved vendor. Send your resume on Telegram: @hr_hiring_dept or WhatsApp.",
    "requirements": "No degree or experience needed. Must have an active bank account to receive check deposit.",
    "benefits": "$500 daily guaranteed payout, Apple MacBook provided.",
    "telecommuting": 1,
    "has_company_logo": 0,
    "has_questions": 0,
    "contact_email": "quickhire2024@gmail.com"
}

print("--- Testing Real Sample ---")
res_real = analyze_job_posting(real_sample)
print(f"Verdict: {res_real['verdict']}")
print(f"Risk: {res_real['risk_percentage']}%")
print(f"Red Flags: {len(res_real['red_flags'])}")

print("\n--- Testing Fake Sample ---")
res_fake = analyze_job_posting(fake_sample)
print(f"Verdict: {res_fake['verdict']}")
print(f"Risk: {res_fake['risk_percentage']}%")
print(f"Red Flags: {len(res_fake['red_flags'])}")
print(f"Sample Red Flag: {res_fake['red_flags'][0]['category']}")

assert res_real['risk_percentage'] < 30.0, "Real sample risk should be low"
assert res_fake['risk_percentage'] >= 70.0, "Fake sample risk should be high"
print("\nAll tests passed successfully!")
