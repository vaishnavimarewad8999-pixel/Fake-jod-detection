import os
import random
import pandas as pd
import numpy as np

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Templates for Real Jobs
REAL_JOB_TITLES = [
    "Senior Full Stack Software Engineer", "Data Scientist - Machine Learning", "DevOps Engineer (Kubernetes/AWS)",
    "Product Manager - SaaS", "Frontend React Developer", "Cybersecurity Analyst", "Cloud Architect - Azure",
    "Database Administrator (PostgreSQL)", "UI/UX Product Designer", "QA Automation Engineer",
    "Digital Marketing Specialist", "Financial Analyst - Corporate Finance", "HR Operations Coordinator",
    "Technical Support Engineer", "Content Strategy Lead", "Network Systems Administrator",
    "Mobile Developer (iOS/Android)", "AI Research Scientist", "Business Intelligence Developer",
    "Account Executive - Enterprise Sales", "Clinical Research Coordinator", "Supply Chain Analyst",
    "Registered Nurse - ICU", "Civil Engineer - Infrastructure", "Electrical Project Engineer"
]

REAL_COMPANIES = [
    {"name": "Apex Cloud Technologies", "profile": "Apex Cloud Technologies is an industry-leading cloud infrastructure provider serving Fortune 500 enterprises globally with 99.99% SLA availability."},
    {"name": "Nova Health Solutions", "profile": "Nova Health Solutions pioneers modern healthcare analytics and patient record systems, operating accredited research facilities across North America."},
    {"name": "Vanguard Financial Analytics", "profile": "Vanguard Financial is a registered fintech firm providing algorithmic risk management tools and portfolio optimization software."},
    {"name": "NextGen Robotics", "profile": "Founded in 2018, NextGen Robotics designs autonomous warehouse logistics hardware and embedded computer vision pipelines."},
    {"name": "Helix Biosystems", "profile": "Helix Biosystems operates state-of-the-art genomic sequencing laboratories backed by premier venture capital firms."},
    {"name": "Meridian Enterprise Software", "profile": "Meridian builds mission-critical ERP solutions for multinational manufacturing conglomerates with over 1,200 employees."},
    {"name": "Pinnacle Digital Media", "profile": "Pinnacle Digital is an award-winning creative digital agency handling branding, web platforms, and growth marketing for global clients."},
    {"name": "Global Logistics Hub", "profile": "Global Logistics Hub manages multi-modal freight transport systems, IoT supply chain tracking, and automated fulfillment centers."}
]

REAL_DESCRIPTIONS = [
    "We are seeking an experienced {title} to join our engineering division. In this role, you will collaborate with cross-functional teams to design, architect, and deploy reliable systems. You will participate in code reviews, sprint planning, and architectural discussions while adhering to industry best practices.",
    "Our team is expanding and looking for a dedicated {title}. You will be responsible for analyzing business requirements, building scalable solutions, and monitoring production metrics. Ideal candidates thrive in an agile environment and possess strong problem-solving acumen.",
    "Join our high-impact team as a {title}. You will lead key technical initiatives, optimize system performance, and mentor junior colleagues. We foster a culture of continuous learning, transparent communication, and engineering excellence.",
    "We have an exciting opportunity for a {title} to contribute directly to our core product lines. You will work alongside product managers, designers, and site reliability engineers to deliver high-quality, maintainable software and services."
]

REAL_REQUIREMENTS = [
    "Bachelor's degree in Computer Science, Engineering, or relevant technical field. 3+ years of professional industry experience. Strong familiarity with modern frameworks, RESTful APIs, version control (Git), and CI/CD pipelines.",
    "BS/MS in relevant discipline or equivalent practical experience. Demonstrable expertise with SQL, relational database modeling, and distributed architectures. Strong analytical and communication skills.",
    "5+ years of hands-on experience in production environments. Deep understanding of software design patterns, system scalability, and test-driven development (TDD). Ability to work effectively in a collaborative team setting.",
    "Proven track record delivering client-facing applications. Solid grasp of performance tuning, automated testing, containerization (Docker), and cloud security standards."
]

REAL_BENEFITS = [
    "Competitive salary ($110,000 - $145,000 based on experience), comprehensive medical/dental/vision coverage, 401(k) matching up to 5%, 20 days paid vacation plus public holidays, and annual professional development stipend.",
    "Health, dental, and life insurance. Generous PTO and sick leave policy. Flexible working hours, company-provided MacBook Pro or workstation, and mental health wellness days.",
    "Attractive compensation package, equity options, parental leave (16 weeks paid), remote office setup budget ($1,500), and annual wellness reimbursement.",
    "Standard corporate benefits including comprehensive health insurance, retirement contribution matching, commuter allowance, and ongoing technical certification sponsorships."
]

REAL_INDUSTRIES = ["Information Technology", "Financial Services", "Hospital & Health Care", "Computer Software", "Internet", "Telecommunications", "Marketing & Advertising"]
REAL_FUNCTIONS = ["Engineering", "Information Technology", "Finance", "Product Management", "Marketing", "Design", "Quality Assurance"]

# Templates for Fake / Scam Jobs
FAKE_JOB_TITLES = [
    "URGENT: Work From Home Data Entry Assistant ($45-$65/hr)",
    "Immediate Hire: Remote Customer Service Representative - No Experience Needed",
    "Virtual Personal Assistant - Flexible Hours ($3500/Month Guaranteed)",
    "Work at Home Data Entry Clerk - Weekly Direct Deposit",
    "Payment Processing Agent / Wire Transfer Coordinator",
    "Package Inspector & Shipping Forwarder (Work From Home)",
    "Mystery Shopper / Financial Evaluator (Quick Payout $600/Assignment)",
    "Part-Time Online Typist / Form Filler - Earn $300-$500 Daily",
    "Cryptocurrency Exchange Assistant - Instant Commissions",
    "Remote Administrative Assistant - Immediate Start (MacBook Provided)",
    "Home-Based Online Order Processor - No Background Check",
    "Quick Cash Data Entry Specialist - Urgent Vacancy Today"
]

FAKE_COMPANIES = [
    {"name": "Global Express Solutions Inc", "profile": "We are a newly established global business consulting firm helping individuals earn passive income while working from the comfort of their home."},
    {"name": "Apex Home Careers LLC", "profile": ""}, # Scams frequently lack company profile
    {"name": "Premier Wealth Management Group", "profile": "A private international conglomerate providing financial flexibility and guaranteed high-yield employment opportunities worldwide."},
    {"name": "FastTrack Dispatch Services", "profile": ""},
    {"name": "Secure Swift Transfer Services", "profile": "Leading decentralized transaction processing network looking for verified individuals to facilitate client remittances."},
    {"name": "National Consumer Review Board", "profile": ""}
]

FAKE_DESCRIPTIONS = [
    "URGENT REQUIREMENT! We are looking for immediate workers to start today. Earn $45 to $75 per hour working only 2 to 3 hours a day from your home computer or mobile phone. No previous experience required! Job duties include entering numeric records into simple spreadsheets, replying to pre-written emails, and confirming daily entries. You will receive an upfront check of $3,500 to purchase home office equipment from our approved vendor. Send your resume immediately to our HR recruiter on Telegram: @hr_hiring_manager24 or WhatsApp +1-800-FAKE-JOB.",
    "Exciting Home Career Opportunity! Earn guaranteed weekly income of $1,800. We need trustworthy individuals to receive company parcels at their residential address, inspect contents, repackage them, and print prepaid courier slips to reship internationally. No interview required! Candidates must have an active bank account to receive upfront stipend. Contact us right away via Google Hangouts or email your personal details (Full name, phone, home address, banking institution) to careers.globalrecruit@gmail.com.",
    "Immediate opening for Online Payment Agent. You will act as an intermediary for our overseas clients. You will receive client payments into your personal account and transfer funds via Western Union, MoneyGram, or Bitcoin ATM minus your 10% commission ($500-$1000 per transaction). High payout guaranteed! Must be ready to start immediately. Send WhatsApp message to +1-555-019-8833 with code #QUICK_HIRE.",
    "Secret Mystery Shopper needed across all cities! Receive $600 per assignment. We will send you an official cashier's check of $2,850. You will deposit the check in your bank, keep $600 as your commission, and test customer service by purchasing gift cards (Apple, Steam, eBay) and texting photos of the codes to our field supervisor. Act fast, limited spots available!",
    "Remote Data Entry / Virtual Assistant. Flexible working hours, make your own schedule! We provide a brand new Apple MacBook Pro and printer. To facilitate equipment setup, you will be issued an electronic check to order software licenses through our verified vendor portal. Please reach out to Mr. Davis on Telegram @hr_onboarding_official for an instant chat interview."
]

FAKE_REQUIREMENTS = [
    "No experience or degree required! Anyone aged 18+ can apply. Must have a smartphone or computer with internet access. Must possess an active personal bank account for immediate direct payroll deposit. Must be responsive on Telegram or WhatsApp.",
    "Zero qualifications required. Must be honest, reliable, and able to follow basic instructions. Must be willing to receive packages at residential address and forward them within 24 hours.",
    "No resume needed! Basic typing skills and willingness to start immediately. Must have an active checking or savings account. Must be available to communicate via unofficial messaging platforms (Telegram/Skype/Signal).",
    "Open to all students, stay-at-home parents, and retirees. No interview, instant hiring! Must be capable of purchasing retail gift cards or processing wire transfers promptly upon receiving check deposit."
]

FAKE_BENEFITS = [
    "Earn $500 - $800 daily! Guaranteed weekly payout, no taxes deducted, free Apple laptop and $3,000 sign-up equipment allowance check provided upon registration.",
    "Guaranteed weekly salary of $2,000 plus 15% instant cash commission on all processed payments. Work whenever you want with zero supervision.",
    "$45-$75 per hour! Instant payout every Friday via Western Union, Zelle, or Bitcoin. Work from anywhere in the world without fixed hours.",
    "Flexible part-time schedule, instant sign-on bonus of $500 after your first assignment, all equipment and training materials covered by upfront check."
]

FAKE_INDUSTRIES = ["Financial Services", "Logistics & Supply Chain", "Customer Service", "General Business", "Internet", "Retail"]
FAKE_FUNCTIONS = ["Data Entry", "Administrative", "Customer Service", "Financial Processing", "Shipping & Receiving"]

def generate_job_record(is_fake=False, job_id=1):
    if not is_fake:
        title = random.choice(REAL_JOB_TITLES)
        company = random.choice(REAL_COMPANIES)
        desc_tmpl = random.choice(REAL_DESCRIPTIONS)
        description = desc_tmpl.format(title=title)
        reqs = random.choice(REAL_REQUIREMENTS)
        benefits = random.choice(REAL_BENEFITS)
        telecommuting = random.choice([0, 0, 1])
        has_company_logo = random.choice([1, 1, 1, 0])
        has_questions = random.choice([1, 1, 0])
        emp_type = random.choice(["Full-time", "Full-time", "Contract", "Part-time"])
        experience = random.choice(["Mid-Senior level", "Associate", "Entry level", "Director"])
        education = random.choice(["Bachelor's Degree", "Master's Degree", "High School or equivalent", "Unspecified"])
        industry = random.choice(REAL_INDUSTRIES)
        function = random.choice(REAL_FUNCTIONS)
        fraudulent = 0
    else:
        title = random.choice(FAKE_JOB_TITLES)
        company = random.choice(FAKE_COMPANIES)
        description = random.choice(FAKE_DESCRIPTIONS)
        reqs = random.choice(FAKE_REQUIREMENTS)
        benefits = random.choice(FAKE_BENEFITS)
        telecommuting = random.choice([1, 1, 1, 0])
        has_company_logo = random.choice([0, 0, 0, 1]) # Scams rarely have verified logos
        has_questions = random.choice([0, 0, 1])
        emp_type = random.choice(["Part-time", "Full-time", "Contract", "Temporary"])
        experience = random.choice(["Entry level", "Not Applicable", "Associate"])
        education = random.choice(["Unspecified", "High School or equivalent"])
        industry = random.choice(FAKE_INDUSTRIES)
        function = random.choice(FAKE_FUNCTIONS)
        fraudulent = 1

    return {
        "job_id": job_id,
        "title": title,
        "company_profile": company["profile"],
        "description": description,
        "requirements": reqs,
        "benefits": benefits,
        "telecommuting": telecommuting,
        "has_company_logo": has_company_logo,
        "has_questions": has_questions,
        "employment_type": emp_type,
        "required_experience": experience,
        "required_education": education,
        "industry": industry,
        "function": function,
        "fraudulent": fraudulent
    }

def create_dataset(output_path="dataset/fake_job_postings.csv", n_real=2500, n_fake=1500):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    records = []
    
    # Generate real jobs
    for i in range(1, n_real + 1):
        records.append(generate_job_record(is_fake=False, job_id=i))
        
    # Generate fake jobs
    for j in range(1, n_fake + 1):
        records.append(generate_job_record(is_fake=True, job_id=n_real + j))
        
    random.shuffle(records)
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created at '{output_path}' with {len(df)} records ({n_real} real, {n_fake} fake).")
    return df

if __name__ == "__main__":
    create_dataset()
