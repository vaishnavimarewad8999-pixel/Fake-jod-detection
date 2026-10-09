from detector import analyze_job_posting, preprocess_text_breakdown

# Test 1: Real Job (Full Structured Fields)
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

# Test 3: Job Description-Only Input (No Company Info, No Logo, No Email, No Benefits)
pure_desc_sample = {
    "description": "We are seeking a Backend Developer proficient in Python and Django. Responsibilities include designing scalable REST APIs, writing clean automated tests, and collaborating with our engineering team. Requirements: 3+ years software engineering experience and a degree in Computer Science."
}

print("--- Testing Real Sample (Structured) ---")
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

print("\n--- Testing Description-Only Normal Job ---")
res_desc = analyze_job_posting(pure_desc_sample)
print(f"Verdict: {res_desc['verdict']}")
print(f"Risk: {res_desc['risk_percentage']}%")
print(f"Red Flags: {len(res_desc['red_flags'])}")

assert res_real['risk_percentage'] < 30.0, "Real sample risk should be low"
assert res_fake['risk_percentage'] >= 70.0, "Fake sample risk should be high"
assert res_desc['risk_percentage'] < 25.0, "Description-only normal job risk should be low"
assert len(res_desc['red_flags']) == 0, "Description-only normal job must have 0 red flags"
assert not any(f['category'] == "Missing Company Information" for f in res_desc['red_flags']), "Must not contain Missing Company Information"

# Test 4: Preprocessing Breakdown
prep_test = preprocess_text_breakdown("APPLY TODAY: Contact hr@company.com or click https://bit.ly/quickjob! Earn $500/day.")
assert prep_test["stats"]["raw_chars"] > prep_test["stats"]["cleaned_chars"]
assert prep_test["stats"]["urls_count"] >= 1
assert prep_test["stats"]["emails_count"] >= 1
assert len(prep_test["stages"]) == 5
assert "preprocessing" in res_real
assert "model_info" in res_real
assert "matched_features" in res_fake
print("\nAll detector tests including preprocessing breakdown passed successfully!")
