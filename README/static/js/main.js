// Sample Presets for Interactive Demo
const PRESETS = {
    real_tech: {
        title: "Senior Full Stack Software Engineer",
        company_name: "Apex Cloud Technologies",
        company_profile: "Apex Cloud Technologies is an industry-leading cloud infrastructure provider serving Fortune 500 enterprises globally with 99.99% SLA availability.",
        description: "We are seeking an experienced Senior Full Stack Engineer to join our core platform engineering team. In this role, you will architect, build, and deploy reliable cloud microservices using Node.js, Python, React, and Kubernetes on AWS. You will collaborate in an Agile squad, participate in code reviews, and drive architectural standards.",
        requirements: "BS/MS in Computer Science or equivalent. 4+ years of professional full-stack development. Proficiency in modern TypeScript/JavaScript, RESTful APIs, Docker, and PostgreSQL. Strong communication and problem-solving skills.",
        benefits: "Competitive base salary ($130,000 - $160,000), comprehensive health/dental/vision insurance, 401(k) matching up to 5%, 20 days paid vacation, and annual learning stipend.",
        contact_email: "recruiting@apexcloudtechnologies.com",
        telecommuting: 0,
        has_company_logo: 1,
        has_questions: 1
    },
    real_health: {
        title: "Clinical Research Coordinator",
        company_name: "Nova Health Solutions",
        company_profile: "Nova Health Solutions pioneers modern healthcare analytics and accredited clinical trial operations across North America.",
        description: "Nova Health is seeking a certified Clinical Research Coordinator to manage phase II and III pharmaceutical trials. Responsibilities include patient screening, regulatory documentation, maintaining GCP compliance, and coordinating with principal investigators.",
        requirements: "Bachelor's degree in Life Sciences, Nursing, or related discipline. Minimum 2 years clinical research experience. ACRP or SOCRA certification preferred. Strict adherence to HIPAA standards.",
        benefits: "Full medical benefits, retirement savings plan, tuition reimbursement, flexible spending account (FSA), and paid annual conferences.",
        contact_email: "careers@novahealthsolutions.org",
        telecommuting: 0,
        has_company_logo: 1,
        has_questions: 1
    },
    scam_telegram: {
        title: "URGENT: Work From Home Data Entry Assistant ($50/hr)",
        company_name: "Global Express Solutions Inc",
        company_profile: "",
        description: "URGENT REQUIREMENT! We need reliable workers to start immediately today. Earn $50 to $70 per hour working 2-3 hours per day from home on your laptop or smartphone. No previous experience needed! You will receive an upfront cashier's check of $3,500 to purchase required home office equipment from our approved vendor. Send your resume immediately to our recruiter on Telegram: @hr_hiring_manager24 or WhatsApp +1-800-FAKE-JOB for an instant text interview.",
        requirements: "No experience or degree required! Anyone aged 18+ can apply. Must have an active personal bank account for instant direct deposit payroll. Must be responsive on Telegram or WhatsApp.",
        benefits: "Earn $500 - $800 daily! Guaranteed weekly payout, no taxes deducted, free Apple MacBook Pro provided upon registration.",
        contact_email: "careers.globalrecruit@gmail.com",
        telecommuting: 1,
        has_company_logo: 0,
        has_questions: 0
    },
    scam_check: {
        title: "Mystery Shopper / Financial Evaluator ($600/Assignment)",
        company_name: "National Consumer Review Board",
        company_profile: "",
        description: "Secret Mystery Shopper needed across all cities! Receive $600 per assignment. We will send you an official cashier's check of $2,850. You will deposit the check in your personal bank account, keep $600 as your commission, and test customer service by purchasing Apple gift cards and Steam cards, then texting photos of the codes to our field supervisor. Act fast, limited spots available! Immediate start today.",
        requirements: "Zero qualifications required. Must have an active checking account and be able to purchase retail gift cards promptly upon receiving upfront check deposit.",
        benefits: "$600 instant cash commission on every processed payment. Payout via Western Union or Zelle.",
        contact_email: "secretshopper.dept@yahoo.com",
        telecommuting: 1,
        has_company_logo: 0,
        has_questions: 0
    },
    scam_reship: {
        title: "Package Inspector & Shipping Forwarder (Work From Home)",
        company_name: "FastTrack Dispatch Services",
        company_profile: "",
        description: "Exciting Home Career Opportunity! Earn guaranteed weekly income of $1,800. We need trustworthy individuals to receive company parcels at their residential address, inspect contents, repackage them, and print prepaid courier slips to reship internationally. No interview required! Candidates must have an active bank account to receive upfront stipend. Contact us via Telegram @fasttrack_dispatch.",
        requirements: "No resume needed! Must be willing to receive packages at home address and forward them within 24 hours.",
        benefits: "Guaranteed $1,800 weekly direct deposit plus $25 bonus per forwarded parcel.",
        contact_email: "reship.onboarding@gmail.com",
        telecommuting: 1,
        has_company_logo: 0,
        has_questions: 0
    }
};

function loadPreset(key) {
    const data = PRESETS[key];
    if (!data) return;

    // Populate Detailed Form
    const titleElem = document.getElementById("form_title");
    const compElem = document.getElementById("form_company_name");
    const profElem = document.getElementById("form_company_profile");
    const descElem = document.getElementById("form_description");
    const reqElem = document.getElementById("form_requirements");
    const benElem = document.getElementById("form_benefits");
    const emailElem = document.getElementById("form_contact_email");
    const logoElem = document.getElementById("form_has_company_logo");
    const teleElem = document.getElementById("form_telecommuting");
    const questElem = document.getElementById("form_has_questions");

    if (titleElem) titleElem.value = data.title;
    if (compElem) compElem.value = data.company_name;
    if (profElem) profElem.value = data.company_profile;
    if (descElem) descElem.value = data.description;
    if (reqElem) reqElem.value = data.requirements;
    if (benElem) benElem.value = data.benefits;
    if (emailElem) emailElem.value = data.contact_email;
    if (logoElem) logoElem.checked = (data.has_company_logo === 1);
    if (teleElem) teleElem.checked = (data.telecommuting === 1);
    if (questElem) questElem.checked = (data.has_questions === 1);

    // Also populate Quick Raw Text
    const quickTitle = document.getElementById("quick_title");
    const quickComp = document.getElementById("quick_company");
    const quickRaw = document.getElementById("quick_raw_text");

    if (quickTitle) quickTitle.value = data.title;
    if (quickComp) quickComp.value = data.company_name;
    if (quickRaw) {
        quickRaw.value = `${data.title}\nCompany: ${data.company_name}\n\n${data.description}\n\nRequirements:\n${data.requirements}\n\nBenefits:\n${data.benefits}\n\nContact: ${data.contact_email}`;
    }

    // Visual notification feedback
    const btn = event.currentTarget;
    const originalText = btn.innerHTML;
    btn.innerHTML = `<i class="fa-solid fa-check"></i> Loaded!`;
    setTimeout(() => {
        btn.innerHTML = originalText;
    }, 1200);
}

function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function copyAnalysisSummary() {
    const verdict = document.querySelector(".verdict-card h3")?.innerText || "";
    const risk = document.querySelector(".risk-percentage-label span")?.innerText || "";
    const redFlags = Array.from(document.querySelectorAll(".red-flag-item .fw-bold"))
        .map(el => "- " + el.innerText).join("\n");

    const summary = `JobShield AI - Verification Summary\n` +
        `------------------------------------\n` +
        `Verdict: ${verdict}\n` +
        `Risk Probability: ${risk}\n\n` +
        `Detected Red Flags:\n${redFlags || 'None'}\n\n` +
        `Verified with AI Fake Job Detection System`;

    navigator.clipboard.writeText(summary).then(() => {
        alert("Verification summary copied to clipboard!");
    }).catch(() => {
        prompt("Copy analysis summary:", summary);
    });
}
