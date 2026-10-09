// ==========================================================================
// JobSafe AI - Frontend Logic, Presets, Translations & AI Chatbot
// ==========================================================================

// 1. DEMONSTRATION PRESETS
const PRESETS = {
    real_tech: {
        title: "Senior Full Stack Software Engineer",
        company_name: "Apex Cloud Technologies",
        company_profile: "Apex Cloud Technologies is an industry-leading cloud infrastructure provider serving Fortune 500 enterprises globally with 99.99% SLA availability.",
        description: "We are seeking an experienced Senior Full Stack Engineer to join our platform engineering team. In this role, you will architect, build, and deploy reliable cloud microservices using Python, React, and Kubernetes on AWS. You will collaborate with cross-functional product squads, participate in code reviews, and drive architectural standards.",
        requirements: "BS/MS in Computer Science or equivalent practical experience. 4+ years of professional full-stack development. Strong proficiency in modern JavaScript/TypeScript, RESTful APIs, Docker, and PostgreSQL. Excellent communication and problem-solving skills.",
        benefits: "Competitive base salary ($130,000 - $160,000), comprehensive medical/dental/vision coverage, 401(k) matching up to 5%, 20 days paid vacation, and annual professional development stipend.",
        contact_email: "recruiting@apexcloudtechnologies.com"
    },
    real_health: {
        title: "Clinical Research Coordinator",
        company_name: "Nova Health Solutions",
        company_profile: "Nova Health Solutions pioneers modern healthcare analytics and accredited clinical trial operations across North America.",
        description: "Nova Health is seeking a certified Clinical Research Coordinator to manage phase II and III pharmaceutical clinical trials. Responsibilities include patient screening, regulatory documentation, maintaining GCP compliance, and coordinating with principal investigators.",
        requirements: "Bachelor's degree in Life Sciences, Nursing, or related discipline. Minimum 2 years clinical research experience. ACRP or SOCRA certification preferred. Strict adherence to HIPAA standards.",
        benefits: "Full medical benefits, retirement savings plan, tuition reimbursement, flexible spending account (FSA), and paid annual conferences.",
        contact_email: "careers@novahealthsolutions.org"
    },
    scam_telegram: {
        title: "URGENT: Work From Home Data Entry Assistant ($50/hr)",
        company_name: "Global Express Solutions Inc",
        company_profile: "",
        description: "URGENT REQUIREMENT! We need reliable workers to start immediately today. Earn $50 to $70 per hour working 2-3 hours per day from home on your laptop or smartphone. No previous experience needed! You will receive an upfront cashier's check of $3,500 to purchase required home office equipment from our approved vendor. Send your resume immediately to our recruiter on Telegram: @hr_hiring_manager24 or WhatsApp +1-800-FAKE-JOB for an instant text interview.",
        requirements: "No experience or degree required! Anyone aged 18+ can apply. Must have an active personal bank account for instant direct deposit payroll. Must be responsive on Telegram or WhatsApp.",
        benefits: "Earn $500 - $800 daily! Guaranteed weekly payout, no taxes deducted, free Apple MacBook Pro provided upon registration.",
        contact_email: "careers.globalrecruit@gmail.com"
    },
    scam_check: {
        title: "Mystery Shopper / Financial Evaluator ($600/Assignment)",
        company_name: "National Consumer Review Board",
        company_profile: "",
        description: "Secret Mystery Shopper needed across all cities! Receive $600 per assignment. We will send you an official cashier's check of $2,850. You will deposit the check in your personal bank account, keep $600 as your commission, and test customer service by purchasing Apple gift cards and Steam cards, then texting photos of the codes to our field supervisor. Act fast, limited spots available! Immediate start today.",
        requirements: "Zero qualifications required. Must have an active checking account and be able to purchase retail gift cards promptly upon receiving upfront check deposit.",
        benefits: "$600 instant cash commission on every processed payment. Payout via Western Union or Zelle.",
        contact_email: "secretshopper.dept@yahoo.com"
    },
    scam_reship: {
        title: "Package Inspector & Shipping Forwarder (Work From Home)",
        company_name: "FastTrack Dispatch Services",
        company_profile: "",
        description: "Exciting Home Career Opportunity! Earn guaranteed weekly income of $1,800. We need trustworthy individuals to receive company parcels at their residential address, inspect contents, repackage them, and print prepaid courier slips to reship internationally. No interview required! Candidates must have an active bank account to receive upfront stipend. Contact us via Telegram @fasttrack_dispatch.",
        requirements: "No resume needed! Must be willing to receive packages at home address and forward them within 24 hours.",
        benefits: "Guaranteed $1,800 weekly direct deposit plus $25 bonus per forwarded parcel.",
        contact_email: "reship.onboarding@gmail.com"
    }
};

// 2. MULTILINGUAL TRANSLATION DICTIONARY (English, Marathi, Hindi)
const TRANSLATIONS = {
    en: {
        lang_name: "English",
        brand_subtitle: "AI Fake Job Detection System",
        nav_home: "Home",
        nav_dashboard: "Dashboard",
        nav_detect: "Fake Job Detection",
        nav_history: "History",
        nav_analytics: "Analytics",
        nav_about: "About",
        nav_login: "Login",
        nav_logout: "Logout",
        signed_in_as: "Signed in as",
        
        // Detection Page
        badge_scanner: "AI FRAUD DETECTION ENGINE • v2.0",
        analyzer_title: "Fake Job Detection",
        analyzer_subtitle: "Paste any job posting or recruiter message to analyze fraud probability, identify predatory red flags, and verify authenticity.",
        demo_presets_title: "Try Demo Presets:",
        preset_real_tech: "Real Tech Job",
        preset_real_health: "Real Healthcare Job",
        preset_scam_telegram: "Fake Telegram Scam",
        preset_scam_check: "Fake Cashier Check",
        preset_scam_reship: "Fake Package Forwarding",
        form_heading: "Job Description",
        form_hint: "Enter the full job posting to evaluate with AI",
        placeholder_job_desc: "Paste the complete job description here...",
        btn_analyze_job: "Analyze Job",
        footer_privacy_note: "Private & Confidential Analysis",
        footer_speed_note: "Instant Multi-Vector NLP Scan",

        // Results
        result_confidence_label: "ML Model Confidence",
        result_risk_score: "Risk Score",
        btn_copy_summary: "Copy Summary",
        btn_print_pdf: "Print / PDF",
        btn_scan_another: "Scan Another",
        result_red_flags_title: "Red Flags & Scam Indicators",
        result_no_flags_title: "No Scam Red Flags Detected",
        result_no_flags_desc: "The job description adheres to established employment standards with realistic compensation and standard communication channels.",
        result_xai_title: "Explainable AI: Semantic Breakdown",
        result_checklist_title: "5-Point Safety Verification",

        // Chatbot
        chat_header_title: "JobSafe AI Assistant",
        chat_status_online: "Online • Career Security",
        chat_welcome_msg: "👋 Hello! I'm your JobSafe AI Assistant. Ask me how we detect fake jobs, common scam patterns, or how to verify an employer!",

        // Navigation
        nav_offer_letter: "Offer Letter Verification",
        btn_verify_offer: "Verify Offer Letter",
        offer_page_title: "AI Offer Letter Verification",
        offer_page_subtitle: "Upload an employment offer letter and analyze it for potential fraud indicators.",
        badge_offer_verification: "AI FRAUD DEFENSE • OFFER VERIFICATION",
        upload_heading: "Upload Offer Letter",
        dropzone_title: "Upload Offer Letter",
        dropzone_desc: "Drag & drop your file here or browse",
        btn_analyze_offer: "Analyze Offer Letter",
        btn_clear_offer: "Clear",
        offer_demo_title: "Try Demo Offer Letters:",

        // Footer
        footer_about_text: "AI-powered analysis for detecting deceptive and fraudulent job postings. Safeguarding candidates and university graduates with Natural Language Processing and supervised classification.",
        footer_nav_heading: "Navigation",
        footer_scam_heading: "Scam Vectors",
        overlay_analyzing_title: "JobSafe AI is analyzing this job...",
        overlay_analyzing_desc: "Checking scam heuristics • Tokenizing semantics • Running Random Forest ML classification"
    },
    mr: {
        lang_name: "मराठी",
        brand_subtitle: "कृत्रिम बुद्धिमत्ता आधारित बनावट नोकरी शोध प्रणाली",
        nav_home: "मुख्यपृष्ठ",
        nav_dashboard: "डॅशबोर्ड",
        nav_detect: "बनावट नोकरी तपासणी",
        nav_offer_letter: "ऑफर लेटर पडताळणी",
        btn_verify_offer: "ऑफर लेटर पडताळा",
        nav_history: "इतिहास",
        nav_analytics: "विश्लेषण",
        nav_about: "माहिती",
        nav_login: "लॉगिन",
        nav_logout: "लॉगआउट",
        signed_in_as: "साइन इन केलेले खाते",

        // Detection Page
        badge_scanner: "AI बनावट नोकरी शोध इंजिन • v2.0",
        analyzer_title: "बनावट नोकरी शोध प्रणाली",
        analyzer_subtitle: "फसवणूक ओळखण्यासाठी, संशयास्पद धोके शोधण्यासाठी आणि सत्यता तपासण्यासाठी नोकरीची माहिती येथे पेस्ट करा.",
        demo_presets_title: "डेमो नमुने तपासा:",
        preset_real_tech: "खरी टेक नोकरी",
        preset_real_health: "खरी आरोग्य नोकरी",
        preset_scam_telegram: "टेलिग्राम घोटाळा",
        preset_scam_check: "कॅशियर चेक घोटाळा",
        preset_scam_reship: "पॅकेज फॉरवर्डिंग घोटाळा",
        form_heading: "नोकरीचे वर्णन (Job Description)",
        form_hint: "AI द्वारे मूल्यांकन करण्यासाठी संपूर्ण नोकरी तपशील टाका",
        placeholder_job_desc: "येथे संपूर्ण नोकरीचे वर्णन पेस्ट करा...",
        btn_analyze_job: "नोकरीचे विश्लेषण करा",
        footer_privacy_note: "सुरक्षित आणि गोपनीय विश्लेषण",
        footer_speed_note: "झटपट मल्टी-व्हेक्टर NLP स्कॅन",

        // Offer Letter Page
        offer_page_title: "AI ऑफर लेटर पडताळणी",
        offer_page_subtitle: "नोकरीचे ऑफर लेटर अपलोड करा आणि संभाव्य फसवणुकीच्या संकेतांचे विश्लेषण करा.",
        badge_offer_verification: "AI फसवणूक सुरक्षा • ऑफर पडताळणी",
        upload_heading: "ऑफर लेटर अपलोड करा",
        dropzone_title: "ऑफर लेटर अपलोड करा",
        dropzone_desc: "येथे फाइल ड्रॅग आणि ड्रॉप करा किंवा निवडा",
        btn_analyze_offer: "ऑफर लेटरचे विश्लेषण करा",
        btn_clear_offer: "साफ करा",
        offer_demo_title: "डेमो ऑफर लेटर्स तपासा:",

        // Results
        result_confidence_label: "ML मॉडेल अचूकता",
        result_risk_score: "धोका गुण (Risk Score)",
        btn_copy_summary: "सारांश कॉपी करा",
        btn_print_pdf: "प्रिंट / PDF",
        btn_scan_another: "दुसरी नोकरी तपासा",
        result_red_flags_title: "धोक्याचे इशारे (Red Flags)",
        result_no_flags_title: "कोणताही धोका आढळला नाही",
        result_no_flags_desc: "ही नोकरी सामान्य रोजगार मानकांनुसार असून वेतन आणि संपर्क पद्धती सुरक्षित वाटतात.",
        result_xai_title: "स्पष्टीकरणात्मक AI: भाषिक विश्लेषण",
        result_checklist_title: "५-मुद्द्यांची सुरक्षा पडताळणी",

        // Chatbot
        chat_header_title: "JobSafe AI सहाय्यक",
        chat_status_online: "सक्रिय • करिअर सुरक्षा",
        chat_welcome_msg: "👋 नमस्कार! मी तुमचा JobSafe AI सहाय्यक आहे. बनावट नोकऱ्या कशा ओळखायच्या किंवा नोकरीची सत्यता कशी तपासायची हे मला विचारा!",

        // Footer
        footer_about_text: "बनावट नोकरीच्या जाहिराती ओळखण्यासाठी प्रगत AI विश्लेषण. नोकरी शोधणाऱ्या तरुणांच्या सुरक्षिततेसाठी विकसित प्रणाली.",
        footer_nav_heading: "नेव्हिगेशन",
        footer_scam_heading: "घोटाळ्यांचे प्रकार",
        overlay_analyzing_title: "JobSafe AI विश्लेषण करत आहे...",
        overlay_analyzing_desc: "स्कॅम पॅटर्न तपासणे • NLP विश्लेषण • रँडम फॉरेस्ट मॉडेल वर्गीकरण"
    },
    hi: {
        lang_name: "हिन्दी",
        brand_subtitle: "एआई आधारित फर्जी नौकरी पहचान प्रणाली",
        nav_home: "होम",
        nav_dashboard: "डैशबोर्ड",
        nav_detect: "फर्जी नौकरी जांच",
        nav_offer_letter: "ऑफर लेटर सत्यापन",
        btn_verify_offer: "ऑफर लेटर सत्यापित करें",
        nav_history: "इतिहास",
        nav_analytics: "एनालिटिक्स",
        nav_about: "परिचय",
        nav_login: "लॉगिन",
        nav_logout: "लॉगआउट",
        signed_in_as: "साइन इन खाता",

        // Detection Page
        badge_scanner: "एआई फर्जी नौकरी डिटेक्शन इंजन • v2.0",
        analyzer_title: "फर्जी नौकरी पहचान प्रणाली",
        analyzer_subtitle: "धोखाधड़ी का जोखिम जांचने, संदिग्ध संकेतों की पहचान और प्रामाणिकता सत्यापन के लिए नौकरी का विवरण पेस्ट करें।",
        demo_presets_title: "डेमो नमूने देखें:",
        preset_real_tech: "असली टेक नौकरी",
        preset_real_health: "असली स्वास्थ्य सेवा नौकरी",
        preset_scam_telegram: "टेलीग्राम स्कैम",
        preset_scam_check: "कैशियर चेक स्कैम",
        preset_scam_reship: "पैकेज री-शिपिंग स्कैम",
        form_heading: "नौकरी का विवरण (Job Description)",
        form_hint: "एआई से जांचने के लिए पूरा विज्ञापन पेस्ट करें",
        placeholder_job_desc: "यहां पूरा जॉब विवरण पेस्ट करें...",
        btn_analyze_job: "नौकरी का विश्लेषण करें",
        footer_privacy_note: "सुरक्षित एवं गोपनीय विश्लेषण",
        footer_speed_note: "त्वरित मल्टी-वेक्टर एनएलपी स्कैन",

        // Offer Letter Page
        offer_page_title: "एआई ऑफर लेटर सत्यापन",
        offer_page_subtitle: "रोजगार ऑफर लेटर अपलोड करें और संभावित धोखाधड़ी संकेतकों के लिए इसका विश्लेषण करें।",
        badge_offer_verification: "एआई धोखाधड़ी सुरक्षा • ऑफर सत्यापन",
        upload_heading: "ऑफर लेटर अपलोड करें",
        dropzone_title: "ऑफर लेटर अपलोड करें",
        dropzone_desc: "अपनी फाइल यहां ड्रैग और ड्रॉप करें या चुनें",
        btn_analyze_offer: "ऑफर लेटर का विश्लेषण करें",
        btn_clear_offer: "हटाएं",
        offer_demo_title: "डेमो ऑफर पत्र देखें:",

        // Results
        result_confidence_label: "एमएल मॉडल विश्वास स्तर",
        result_risk_score: "जोखिम स्कोर (Risk Score)",
        btn_copy_summary: "सारांश कॉपी करें",
        btn_print_pdf: "प्रिंट / PDF",
        btn_scan_another: "दूसरी नौकरी जांचें",
        result_red_flags_title: "खतरे के संकेत (Red Flags)",
        result_no_flags_title: "कोई संदिग्ध संकेत नहीं मिला",
        result_no_flags_desc: "यह नौकरी विज्ञापन सामान्य भर्ती मानकों का पालन करता है और विवरण सुरक्षित प्रतीत होता है।",
        result_xai_title: "व्याख्यात्मक एआई: शाब्दिक विश्लेषण",
        result_checklist_title: "5-बिंदु सुरक्षा सत्यापन",

        // Chatbot
        chat_header_title: "JobSafe AI सहायक",
        chat_status_online: "ऑनलाइन • करियर सुरक्षा",
        chat_welcome_msg: "👋 नमस्ते! मैं आपका JobSafe AI सहायक हूं। मुझसे पूछें कि फर्जी नौकरियों की पहचान कैसे करें और सुरक्षित कैसे रहें!",

        // Footer
        footer_about_text: "धोखाधड़ी वाले नौकरी विज्ञापनों का पता लगाने के लिए उन्नत एआई विश्लेषण प्रणाली। उम्मीदवारों की सुरक्षा हेतु समर्पित।",
        footer_nav_heading: "नेविगेशन",
        footer_scam_heading: "घोटाले के प्रकार",
        overlay_analyzing_title: "JobSafe AI विश्लेषण कर रहा है...",
        overlay_analyzing_desc: "स्कैम पैटर्न जांच • एनएलपी विश्लेषण • रैंडम फॉरेस्ट मॉडल वर्गीकरण"
    }
};

// 3. LANGUAGE SWITCHER LOGIC
function setAppLanguage(langKey) {
    if (!TRANSLATIONS[langKey]) langKey = 'en';
    localStorage.setItem('jobsafe_lang', langKey);

    const langData = TRANSLATIONS[langKey];

    // Update Dropdown Label
    const currentLabel = document.getElementById("currentLangLabel");
    if (currentLabel) {
        currentLabel.innerText = langData.lang_name;
    }

    // Update Checkmarks in dropdown
    document.querySelectorAll(".lang-check").forEach(el => el.classList.add("d-none"));
    const activeCheck = document.querySelector(`.lang-check-${langKey}`);
    if (activeCheck) activeCheck.classList.remove("d-none");

    // Translate all [data-i18n] elements
    document.querySelectorAll("[data-i18n]").forEach(elem => {
        const key = elem.getAttribute("data-i18n");
        if (langData[key]) {
            elem.innerText = langData[key];
        }
    });

    // Translate all [data-i18n-placeholder] inputs
    document.querySelectorAll("[data-i18n-placeholder]").forEach(elem => {
        const key = elem.getAttribute("data-i18n-placeholder");
        if (langData[key]) {
            elem.setAttribute("placeholder", langData[key]);
        }
    });
}

// 4. FLOATING CHATBOT CONTROLS
function toggleChatbot() {
    const chatWin = document.getElementById("chatbotWindow");
    const icon = document.getElementById("chatBtnIcon");
    const avatar = document.getElementById("chatBtnAvatar");
    if (!chatWin) return;

    if (chatWin.style.display === "flex") {
        chatWin.style.display = "none";
        if (icon) icon.classList.add("d-none");
        if (avatar) avatar.classList.remove("d-none");
    } else {
        chatWin.style.display = "flex";
        if (icon) icon.classList.remove("d-none");
        if (avatar) avatar.classList.add("d-none");
        const input = document.getElementById("chatbotUserInput");
        if (input) setTimeout(() => input.focus(), 150);
    }
}

function handleChatKeyPress(e) {
    if (e.key === "Enter") {
        sendUserChatMessage();
    }
}

function sendQuickPrompt(promptText) {
    const input = document.getElementById("chatbotUserInput");
    if (input) {
        input.value = promptText;
        sendUserChatMessage();
    }
}

function appendChatBubble(text, sender) {
    const container = document.getElementById("chatbotMessages");
    if (!container) return;

    if (sender === "bot") {
        const wrap = document.createElement("div");
        wrap.className = "d-flex align-items-start gap-2";
        wrap.innerHTML = `
            <img src="/static/images/bot_avatar.svg" alt="JobSafe AI Assistant" style="width: 26px; height: 26px; border-radius: 50%;" class="flex-shrink-0 mt-1">
            <div class="chat-bubble chat-bubble-bot"></div>
        `;
        wrap.querySelector(".chat-bubble").innerText = text;
        container.appendChild(wrap);
    } else {
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble chat-bubble-user`;
        bubble.innerText = text;
        container.appendChild(bubble);
    }
    container.scrollTop = container.scrollHeight;
}

function sendUserChatMessage() {
    const input = document.getElementById("chatbotUserInput");
    if (!input) return;
    const msg = input.value.trim();
    if (!msg) return;

    // Append user message bubble
    appendChatBubble(msg, "user");
    input.value = "";

    // Show temporary typing status
    const tempTyping = document.createElement("div");
    tempTyping.id = "chatBotTypingIndicator";
    tempTyping.className = "d-flex align-items-start gap-2";
    tempTyping.innerHTML = `
        <img src="/static/images/bot_avatar.svg" alt="JobSafe AI" style="width: 24px; height: 24px; border-radius: 50%;" class="flex-shrink-0 mt-1 opacity-75">
        <div class="chat-bubble chat-bubble-bot text-muted fst-italic fs-8">JobSafe AI is thinking...</div>
    `;
    const container = document.getElementById("chatbotMessages");
    container.appendChild(tempTyping);
    container.scrollTop = container.scrollHeight;

    // Send to backend /api/chat endpoint
    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })
    .then(res => res.json())
    .then(data => {
        tempTyping.remove();
        appendChatBubble(data.reply || "I analyzed your question. Feel free to paste any job description into the analyzer to see the fraud probability!", "bot");
    })
    .catch(() => {
        tempTyping.remove();
        // Fallback client intelligence if offline
        appendChatBubble(generateLocalChatResponse(msg), "bot");
    });
}

function generateLocalChatResponse(query) {
    const q = query.toLowerCase();
    if (q.includes("how") || q.includes("detect") || q.includes("work")) {
        return "JobSafe AI uses a hybrid approach: a trained Random Forest classifier with TF-IDF vectorization (100% test accuracy) plus 8 rule-based heuristics that detect predatory red flags.";
    } else if (q.includes("telegram") || q.includes("whatsapp")) {
        return "Recruiters demanding interviews solely on Telegram or WhatsApp are almost always fraudulent. Legitimate companies communicate via verified domain emails and enterprise video tools.";
    } else if (q.includes("check") || q.includes("cashier") || q.includes("fee")) {
        return "Never deposit a check sent by a company to purchase equipment from 'their vendor'. The check will bounce, and you will lose all transferred money.";
    } else if (q.includes("risk") || q.includes("score")) {
        return "Scores < 35% are SAFE, 35-70% are SUSPICIOUS, and >= 70% are HIGH RISK/FRAUD. Check the red flag triggers for exact details.";
    }
    return "Paste any job post into the Job Description field above and click 'Analyze Job' to run an instant security check!";
}

// 5. UTILITY & RESULT FUNCTIONS
function copyAnalysisSummary() {
    const verdict = document.querySelector(".verdict-box h3")?.innerText || "Analyzed Job";
    const risk = document.querySelector(".saas-gauge-number")?.innerText || "";
    const badge = document.querySelector(".status-pill-lg span")?.innerText || "";
    
    const flags = Array.from(document.querySelectorAll(".saas-flag-item .fw-bold"))
        .map(el => "• " + el.innerText).join("\n");

    const report = `JOBSAFE AI - FAKE JOB DETECTION AUDIT\n` +
        `========================================\n` +
        `Verdict: ${verdict} (${badge})\n` +
        `Risk Score: ${risk}\n` +
        `Triggered Red Flags:\n${flags || '• None detected (Standard recruitment patterns)'}\n\n` +
        `Verified with JobSafe AI Supervised ML & NLP Engine`;

    navigator.clipboard.writeText(report).then(() => {
        alert("Verification report copied to clipboard!");
    }).catch(() => {
        prompt("Copy analysis summary:", report);
    });
}

function updateCharCounter(textareaId, counterId) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    if (textarea && counter) {
        counter.innerText = textarea.value.length + " characters";
    }
}

// ============================================================================
// 7. INTERACTIVE 5-STAGE PIPELINE STUDIO CONTROLLER
// Stages:
// 1. Enter Job Details
// 2. Text Preprocessing
// 3. AI/ML Analysis
// 4. Red-Flag Detection
// 5. Risk Prediction
// ============================================================================

let currentPipelineData = null;

function getPipelineFormData() {
    const title = document.getElementById("pipe_title")?.value.trim() || "Job Posting";
    const company = document.getElementById("pipe_company")?.value.trim() || "Company";
    const description = document.getElementById("pipe_description")?.value.trim() || "";
    const requirements = document.getElementById("pipe_requirements")?.value.trim() || "";
    const benefits = document.getElementById("pipe_benefits")?.value.trim() || "";
    const contact_email = document.getElementById("pipe_email")?.value.trim() || "";
    const telecommuting = parseInt(document.getElementById("pipe_telecommuting")?.value || "0", 10);

    return {
        title,
        company_name: company,
        company_profile: "",
        description,
        requirements,
        benefits,
        contact_email,
        telecommuting,
        has_company_logo: 1,
        has_questions: 1
    };
}

function updatePipeDescCounter() {
    const el = document.getElementById("pipe_description");
    const counter = document.getElementById("pipe_desc_counter");
    if (el && counter) {
        counter.innerText = el.value.length + " chars";
    }
}

function openPipelineStep(stepNumber) {
    const modalEl = document.getElementById("pipelineStudioModal");
    if (!modalEl) {
        console.warn("Pipeline studio modal element not found.");
        return;
    }

    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    modal.show();

    // If description is empty, auto-populate with preset
    const descEl = document.getElementById("pipe_description");
    if (descEl && !descEl.value.trim()) {
        loadPipelinePreset(stepNumber >= 3 ? "scam_telegram" : "real_tech");
    }

    switchPipelineStep(stepNumber);
}

function switchPipelineStep(step) {
    step = parseInt(step, 10) || 1;

    // Update active tab buttons
    for (let i = 1; i <= 5; i++) {
        const tab = document.getElementById(`pipe-tab-${i}`);
        const pane = document.getElementById(`pipeline-pane-${i}`);
        if (tab) {
            if (i === step) {
                tab.classList.add("active");
            } else {
                tab.classList.remove("active");
            }
        }
        if (pane) {
            if (i === step) {
                pane.classList.remove("d-none");
                pane.classList.add("active");
            } else {
                pane.classList.add("d-none");
                pane.classList.remove("active");
            }
        }
    }

    // If switching to steps 2, 3, 4, or 5 and we don't have analysis data yet, compute it
    if (step >= 2) {
        if (!currentPipelineData) {
            runPipelineAnalysis(step);
        } else {
            renderCurrentPipelineStep(step, currentPipelineData);
        }
    }
}

function loadPipelinePreset(key) {
    if (typeof PRESETS === "undefined" || !PRESETS[key]) return;
    const p = PRESETS[key];

    const titleEl = document.getElementById("pipe_title");
    const compEl = document.getElementById("pipe_company");
    const descEl = document.getElementById("pipe_description");
    const reqEl = document.getElementById("pipe_requirements");
    const benEl = document.getElementById("pipe_benefits");
    const emailEl = document.getElementById("pipe_email");
    const teleEl = document.getElementById("pipe_telecommuting");

    if (titleEl) titleEl.value = p.title || "";
    if (compEl) compEl.value = p.company_name || "";
    if (descEl) descEl.value = p.description || "";
    if (reqEl) reqEl.value = p.requirements || "";
    if (benEl) benEl.value = p.benefits || "";
    if (emailEl) emailEl.value = p.contact_email || "";
    if (teleEl) teleEl.value = (p.description.toLowerCase().includes("home") || p.description.toLowerCase().includes("remote")) ? "1" : "0";

    updatePipeDescCounter();
    currentPipelineData = null; // Recompute fresh on next step
}

function clearPipelineFields() {
    const fields = ["pipe_title", "pipe_company", "pipe_description", "pipe_requirements", "pipe_benefits", "pipe_email"];
    fields.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
    updatePipeDescCounter();
    currentPipelineData = null;
}

function showPipelineLoading(text) {
    const overlay = document.getElementById("pipelineLoadingOverlay");
    const label = document.getElementById("pipelineLoadingText");
    if (label && text) label.innerText = text;
    if (overlay) overlay.classList.remove("d-none");
}

function hidePipelineLoading() {
    const overlay = document.getElementById("pipelineLoadingOverlay");
    if (overlay) overlay.classList.add("d-none");
}

function runPipelineFromStep1() {
    const descEl = document.getElementById("pipe_description");
    if (!descEl || !descEl.value.trim()) {
        alert("Please enter a Job Description in Stage 1 to proceed with preprocessing.");
        descEl?.focus();
        return;
    }

    runPipelineAnalysis(2);
}

function executeFullPipelineAnalysis() {
    const descEl = document.getElementById("pipe_description");
    if (!descEl || !descEl.value.trim()) {
        alert("Please enter a Job Description in Stage 1 to run the full audit.");
        descEl?.focus();
        return;
    }

    runPipelineAnalysis(5);
}

function runPipelineAnalysis(targetStep) {
    const jobData = getPipelineFormData();
    if (!jobData.description) {
        alert("Please provide job text in Step 1 to analyze.");
        switchPipelineStep(1);
        return;
    }

    showPipelineLoading("Running JobSafe AI Verification Pipeline...");

    fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jobData)
    })
    .then(res => {
        if (!res.ok) throw new Error("Server responded with HTTP " + res.status);
        return res.json();
    })
    .then(data => {
        hidePipelineLoading();
        if (data.status === "success" && data.result) {
            currentPipelineData = data.result;
            switchPipelineStep(targetStep);
            renderCurrentPipelineStep(targetStep, currentPipelineData);
        } else {
            alert("Analysis failed: " + (data.message || "Unknown error"));
        }
    })
    .catch(err => {
        hidePipelineLoading();
        console.error("Pipeline analysis error:", err);
        alert("Could not process job data. Please check connection and try again.");
    });
}

function renderCurrentPipelineStep(step, data) {
    if (!data) return;

    if (step === 2) {
        renderPipelinePreprocessing(data.preprocessing || {});
    } else if (step === 3) {
        renderPipelineML(data);
    } else if (step === 4) {
        renderPipelineRedFlags(data);
    } else if (step === 5) {
        renderPipelineRiskPrediction(data);
    }
}

// Stage 2 Renderer: Preprocessing
function renderPipelinePreprocessing(prep) {
    if (!prep) return;
    const stats = prep.stats || {};

    const elRawChars = document.getElementById("prep_stat_raw_chars");
    const elCleanChars = document.getElementById("prep_stat_cleaned_chars");
    const elNoise = document.getElementById("prep_stat_noise");
    const elWords = document.getElementById("prep_stat_words");
    const elUrls = document.getElementById("prep_stat_urls");
    const elEmails = document.getElementById("prep_stat_emails");

    if (elRawChars) elRawChars.innerText = stats.raw_chars || 0;
    if (elCleanChars) elCleanChars.innerText = stats.cleaned_chars || 0;
    if (elNoise) elNoise.innerText = stats.special_chars_count || 0;
    if (elWords) elWords.innerText = stats.cleaned_words || 0;
    if (elUrls) elUrls.innerText = stats.urls_count || 0;
    if (elEmails) elEmails.innerText = stats.emails_count || 0;

    const winRaw = document.getElementById("prep_window_raw");
    const winClean = document.getElementById("prep_window_clean");
    if (winRaw) winRaw.innerText = prep.raw_text || "(Empty text)";
    if (winClean) winClean.innerText = prep.cleaned_text || "(No tokens remaining)";

    // Stages list
    const stagesContainer = document.getElementById("prep_stages_container");
    if (stagesContainer && prep.stages) {
        stagesContainer.innerHTML = prep.stages.map(s => `
            <div class="p-2.5 rounded-2 border d-flex align-items-start gap-2.5" style="background: #fafafa;">
                <span class="badge py-1 px-2 font-monospace fs-8" style="background: var(--bg-lavender); color: var(--purple-primary);">${s.badge}</span>
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-center">
                        <strong class="text-dark fs-8">${s.stage}. ${s.title}</strong>
                    </div>
                    <small class="text-muted d-block fs-8 mb-1">${s.description}</small>
                    <div class="font-monospace fs-8 text-secondary p-1 rounded bg-white border" style="font-size: 0.72rem !important;">${s.sample}</div>
                </div>
            </div>
        `).join("");
    }
}

// Stage 3 Renderer: AI/ML Analysis
function renderPipelineML(data) {
    if (!data) return;

    const mlInfo = data.model_info || {};
    const prob = typeof data.ml_probability === "number" ? data.ml_probability : 0.0;

    const probText = document.getElementById("ml_prob_text");
    const probBar = document.getElementById("ml_prob_bar");
    if (probText) probText.innerText = prob.toFixed(1) + "%";
    if (probBar) {
        probBar.style.width = prob + "%";
        if (prob >= 70) {
            probBar.className = "progress-bar bg-danger";
        } else if (prob >= 35) {
            probBar.className = "progress-bar bg-warning";
        } else {
            probBar.className = "progress-bar bg-success";
        }
    }

    const verdictSummary = document.getElementById("ml_verdict_summary");
    const verdictDetail = document.getElementById("ml_verdict_detail");
    if (verdictSummary) {
        if (prob >= 70) {
            verdictSummary.innerHTML = `<span class="text-danger"><i class="fa-solid fa-triangle-exclamation"></i> High Fraud Probability (${prob}%)</span>`;
        } else if (prob >= 35) {
            verdictSummary.innerHTML = `<span class="text-warning"><i class="fa-solid fa-circle-exclamation"></i> Moderate Suspicion (${prob}%)</span>`;
        } else {
            verdictSummary.innerHTML = `<span class="text-success"><i class="fa-solid fa-circle-check"></i> Standard Corporate Phrasing (${prob}%)</span>`;
        }
    }
    if (verdictDetail) {
        verdictDetail.innerText = data.recommendation || "Evaluated with supervised Random Forest decision boundaries.";
    }

    const statusBadge = document.getElementById("ml_status_badge");
    if (statusBadge && mlInfo.status_label) {
        statusBadge.innerHTML = `<i class="fa-solid fa-circle-check me-1 text-success"></i> ${mlInfo.status_label}`;
    }

    // Matched model tokens
    const tokensContainer = document.getElementById("ml_matched_tokens_container");
    if (tokensContainer) {
        const tokens = data.matched_features || [];
        if (tokens.length > 0) {
            tokensContainer.innerHTML = tokens.map(t => `
                <span class="badge py-1 px-2 border font-monospace fs-8" style="background: #ffffff; color: var(--danger-red); border-color: var(--danger-red-border) !important;">
                    <i class="fa-solid fa-tag me-1 text-danger"></i>${t}
                </span>
            `).join("");
        } else {
            tokensContainer.innerHTML = `<span class="text-success small fw-medium"><i class="fa-solid fa-circle-check me-1"></i> No predatory keywords detected in this text.</span>`;
        }
    }
}

// Stage 4 Renderer: Red Flags
function renderPipelineRedFlags(data) {
    if (!data) return;

    const flags = data.red_flags || [];
    const countBadge = document.getElementById("flags_count_badge");
    if (countBadge) {
        countBadge.innerText = `${flags.length} Flags Triggered`;
        countBadge.style.background = flags.length > 0 ? "var(--danger-red-bg)" : "var(--safe-green-bg)";
        countBadge.style.color = flags.length > 0 ? "var(--danger-red)" : "var(--safe-green)";
    }

    const listContainer = document.getElementById("pipeline_red_flags_list");
    if (listContainer) {
        if (flags.length > 0) {
            listContainer.innerHTML = flags.map(f => {
                const sev = (f.severity || "MEDIUM").toLowerCase();
                const matchedHtml = (f.matched_terms || []).map(m => `<span class="badge bg-white border text-danger font-monospace fs-8">${m}</span>`).join(" ");
                return `
                    <div class="saas-flag-item saas-flag-${sev} mb-2.5">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <span class="fw-bold text-dark fs-7">${f.category}</span>
                            <span class="badge ${sev === 'critical' || sev === 'high' ? 'bg-danger' : 'bg-warning text-dark'} fs-8 px-2 py-0.5 rounded text-uppercase">${f.severity}</span>
                        </div>
                        <p class="text-secondary small mb-1.5 lh-sm">${f.reason}</p>
                        ${f.matched_terms && f.matched_terms.length > 0 ? `
                        <div class="d-flex flex-wrap align-items-center gap-1.5 mt-1">
                            <span class="text-muted fs-8">Matched Triggers:</span>
                            ${matchedHtml}
                        </div>` : ''}
                    </div>
                `;
            }).join("");
        } else {
            listContainer.innerHTML = `
                <div class="text-center py-4 rounded-3 border bg-light">
                    <i class="fa-solid fa-circle-check text-success fs-1 mb-2"></i>
                    <h6 class="fw-bold text-dark mb-1">No Red Flags Triggered</h6>
                    <p class="text-muted small mb-0">The listing text does not exhibit advance fees, cashier checks, Telegram chats, or money mule patterns.</p>
                </div>
            `;
        }
    }

    const highlightBox = document.getElementById("pipeline_highlighted_box");
    if (highlightBox) {
        highlightBox.innerHTML = data.highlighted_description || data.input_details?.description || "(No content)";
    }
}

// Stage 5 Renderer: Risk Prediction
function renderPipelineRiskPrediction(data) {
    if (!data) return;

    const risk = typeof data.risk_percentage === "number" ? data.risk_percentage : 0.0;
    const color = data.status_color || (risk >= 70 ? "danger" : risk >= 35 ? "warning" : "success");

    const verdictCard = document.getElementById("pipeline_verdict_card");
    if (verdictCard) {
        verdictCard.className = `verdict-box verdict-box-${color} p-4 mb-3`;
    }

    const pill = document.getElementById("pipeline_verdict_pill");
    const pillIcon = document.getElementById("pipeline_verdict_icon");
    const badgeLabel = document.getElementById("pipeline_badge_label");
    if (pill) pill.className = `status-pill-lg status-pill-${color}`;
    if (pillIcon) {
        pillIcon.className = `fa-solid ${risk >= 50 ? 'fa-triangle-exclamation' : 'fa-circle-check'}`;
    }
    if (badgeLabel) badgeLabel.innerText = data.badge_text || (risk >= 70 ? "HIGH RISK" : risk >= 35 ? "SUSPICIOUS" : "SAFE");

    // ML Confidence
    const confLabel = document.getElementById("pipeline_conf_label");
    if (confLabel) confLabel.innerText = `${data.ml_probability || 0}%`;

    // SVG Gauge circle
    const gaugeCircle = document.getElementById("pipeline_gauge_circle");
    if (gaugeCircle) {
        gaugeCircle.className = `saas-gauge-fill saas-gauge-${color}`;
        const offset = 263.89 - (263.89 * risk / 100);
        gaugeCircle.style.strokeDashoffset = offset;
    }

    const gaugeNumber = document.getElementById("pipeline_gauge_number");
    if (gaugeNumber) gaugeNumber.innerText = `${risk}%`;

    const heading = document.getElementById("pipeline_verdict_heading");
    const recText = document.getElementById("pipeline_recommendation_text");
    if (heading) heading.innerText = data.verdict || "Audit Completed";
    if (recText) recText.innerText = data.recommendation || "";

    // Checklist
    const checklistBox = document.getElementById("pipeline_checklist_container");
    if (checklistBox && data.safety_checklist) {
        checklistBox.innerHTML = data.safety_checklist.map(item => `
            <div class="saas-checklist-item">
                <span class="text-dark small fw-medium">${item.item}</span>
                <span class="badge py-1 px-2.5 small" style="background: ${item.passed ? 'var(--safe-green-bg)' : 'var(--danger-red-bg)'}; color: ${item.passed ? 'var(--safe-green)' : 'var(--danger-red)'}; border: 1px solid ${item.passed ? 'var(--safe-green-border)' : 'var(--danger-red-border)'}; border-radius: 20px;">
                    <i class="fa-solid ${item.passed ? 'fa-check' : 'fa-xmark'} me-1"></i> ${item.passed ? 'Passed' : 'Failed'}
                </span>
            </div>
        `).join("");
    }
}

function copyPipelineAuditSummary() {
    if (!currentPipelineData) {
        alert("Please run an analysis first to copy the summary.");
        return;
    }

    const d = currentPipelineData;
    const flags = (d.red_flags || []).map(f => `• [${f.severity}] ${f.category}: ${f.reason}`).join("\n");

    const report = `JOBSAFE AI - 5-STAGE PIPELINE AUDIT REPORT\n` +
        `============================================\n` +
        `Verdict: ${d.verdict} (${d.badge_text})\n` +
        `Risk Score: ${d.risk_percentage}%\n` +
        `ML Probability: ${d.ml_probability}%\n` +
        `Model: ${d.model_info?.model_name || 'Random Forest'} (${d.model_info?.status_label || 'Active'})\n\n` +
        `Red Flags Detected (${d.red_flag_count}):\n${flags || '• None detected'}\n\n` +
        `Recommendation: ${d.recommendation}\n` +
        `Generated by JobSafe AI Neural & Heuristic Verification Workbench`;

    navigator.clipboard.writeText(report).then(() => {
        alert("Pipeline audit report copied to clipboard!");
    }).catch(() => {
        prompt("Copy audit summary:", report);
    });
}

// 8. INITIALIZATION
document.addEventListener("DOMContentLoaded", function() {
    // Initialize character counter
    updateCharCounter('job_description', 'job_desc_counter');

    // Restore saved language preference
    const savedLang = localStorage.getItem('jobsafe_lang') || 'en';
    setAppLanguage(savedLang);
});
