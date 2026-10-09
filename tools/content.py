"""Site content. Edit here, then run: python3 tools/build.py

Text comes from the live WordPress site (Oct 2026) and the Claude Design
"Altus - Bold" copy. Paths keep the old WordPress URLs so links and search
results keep working after the move.
"""

PHONE = "561-641-0404"
PHONE_TEL = "+15616410404"
ADDRESS_1 = "4671 S. Congress Ave., Suite 100-B"
ADDRESS_2 = "Lake Worth, FL 33461"
MAPS_URL = ("https://www.google.com/maps/place/Altus+Clinical+Research/@26.607926,-80.0902012,17z/"
            "data=!4m6!3m5!1s0x88d8d8719fa74f25:0xdb0401542aef1652")
MAP_EMBED = ("https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d1936.8902918757742!2d-80.0936157!"
             "3d26.6093169!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x88d8d8719fa74f25%3A0xdb0401542aef1652!"
             "2sAltus%20Clinical%20Research!5e1!3m2!1sen!2sus!4v1731074305924!5m2!1sen!2sus")
NPP_PDF = "wp-content/uploads/2020/02/notice-of-privacy-practice-1.pdf"

# Review rating shown on the homepage (hero, stat bar, reviews band). One figure everywhere.
# Google listing checked 2026-10-08: 4.6 from 62 reviews. If you switch to a combined figure,
# say which sites it covers in RATING_LABEL (e.g. "reviews on Google and Facebook").
RATING = "4.6"
RATING_COUNT = "62"
RATING_LABEL = "Google reviews"
FACEBOOK_REVIEWS = "https://www.facebook.com/AltusResearch/reviews"

# Patient inquiry form. Paste the Microsoft Forms embed URL here
# (Forms > Collect responses > Embed > copy the src="..." value).
# While empty, the contact page shows call / visit options instead of a form.
FORM_EMBED_URL = ""
# Where the built-in inquiry form sends (used while FORM_EMBED_URL is empty).
INQUIRY_EMAIL = "yperez@altusresearch.com"

# ---------------------------------------------------------------- icons
ICON = {
    "womens": '♀',
    "urology": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3C4.7 3 3 5.9 3 9.5S5 16 8 16c1.6 0 2.3-1 2.6-2 .4-1.4 1.4-2 1.4-4S11 3 8 3Z"></path><path d="M16 21c3.3 0 5-2.9 5-6.5S19 8 16 8c-1.6 0-2.3 1-2.6 2-.4 1.4-1.4 2-1.4 4s1 7 4 7Z"></path></svg>',
    "dermatology": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"></path><path d="M5 12h14"></path></svg>',
    "vaccines": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 2 4 4"></path><path d="m17 7 3-3"></path><path d="M19 9 8.7 19.3c-1 1-2 1-3 0l-1-1c-1-1-1-2 0-3L15 5"></path><path d="m9 11 4 4"></path><path d="m5 19-3 3"></path><path d="m14 4 6 6"></path></svg>',
    "internal": '♥',
    "rheumatology": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"></path></svg>',
    "aesthetic": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19.6 2.2l.5 1.5 1.5.5-1.5.5-.5 1.5-.5-1.5L17.6 4.2l1.5-.5z" fill="#14796b" stroke="none"></path><path d="M18 11c-1.5 0-2.5.5-3 2"></path><path d="M4 6a2 2 0 0 0-2 2v4a5 5 0 0 0 5 5 8 8 0 0 1 5 2 8 8 0 0 1 5-2 5 5 0 0 0 5-5V8a2 2 0 0 0-2-2h-3a8 8 0 0 0-5 2 8 8 0 0 0-5-2z"></path><path d="M6 11c1.5 0 2.5.5 3 2"></path></svg>',
    "pediatrics": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#14796b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"></circle><path d="M6 21v-1a6 6 0 0 1 12 0v1"></path></svg>',
}

# ---------------------------------------------------------------- areas
# key, slug, name, design one-liner, conditions studied (from WordPress)
AREAS = [
    ("womens", "womens-studies", "Women's Studies",
     "Contraception, hormone health, uterine fibroids and more, in partnership with our OB/GYN practice.",
     ["HRT in Postmenopausal Women", "Menopausal Vasomotor Symptoms", "Endometrial Hyperplasia",
      "Oral Contraceptives", "Cycle Control", "Bleeding Patterns in Postmenopausal Women",
      "Hot Flash Relief in Women", "Fibrocystic Disorder of the Breast",
      "Low Libido in Hysterectomized and Oophorectomized Women", "Contraceptive Efficacy",
      "Iron Deficiency for Benign Gynecologic Disease", "Low-Grade Squamous Intraepithelial Lesions",
      "Moderate to Severe Ichthyosis Vulgaris", "Vulvovaginal Candidiasis", "Vaginal Atrophy",
      "Osteoporosis in Women", "Osteopenia", "Genital Herpes",
      "High Grade Cervical Intraepithelial Lesions", "Heavy Menstrual Bleeding (Menorrhagia)",
      "Prevention of Bone Loss in Postmenopausal Women", "Postpartum Anemia",
      "Premenstrual Dysphoric Disorder", "Symptomatic Endometriosis", "Uterine Leiomyomata",
      "Fracture Incidence in Women with Osteoporosis", "Female Sexual Dysfunction",
      "Prevention of Osteoporotic Fractures After a Hip Fracture", "Breast Cancer Prevention"]),
    ("urology", "urology", "Urology",
     "Urinary incontinence, overactive bladder and related conditions, supported by on-site uroflow.",
     ["Overactive Bladder", "Urge Incontinence", "Nocturia", "Mixed Urinary Incontinence",
      "Benign Prostatic Hyperplasia", "Urinary Tract Infection", "Premature Ejaculation"]),
    ("dermatology", "dermatology", "Dermatology",
     "Plaque psoriasis, actinic keratosis and other skin conditions evaluated with state-of-the-art tools.",
     ["Plaque Psoriasis", "Moderate to Severe Psoriasis", "Adhesion Tolerability", "Herpes Labialis Infections",
      "Reduction of Length of Cold Sore Episodes", "Tinea Pedis", "Acne Vulgaris", "Onychomycosis of Toenails",
      "Non-Hyperkeratotic Actinic Keratoses of the Face and Scalp", "Tinea (Pityriasis) Versicolor",
      "Solar Lentigines"]),
    ("vaccines", "vaccines", "Vaccines",
     "Vaccine trials including meningococcal and COVID-19, with cold-chain storage and IATA-certified staff.",
     ["Smallpox Vaccine", "Japanese Encephalitis Vaccine", "HPV", "RSV", "Influenza", "Meningitis", "UTI"]),
    ("internal", "internal-medicine", "Internal Medicine",
     "High blood pressure, diabetes and fatty liver, and other chronic conditions managed by our investigators.",
     ["Smoking Cessation", "Primary Hypercholesterolemia", "Weight Loss in Obese Subjects",
      "Elevated Low-Density Lipoprotein Cholesterol", "Diabetes and Erectile Dysfunction", "Type II Diabetes",
      "Chronic Non-Malignant Pain", "Hypertension", "Diabetic Weight Loss", "Mixed Dyslipidemia"]),
    ("rheumatology", "rheumatology", "Rheumatology",
     "Osteoarthritis of the knee and inflammatory conditions, with on-site imaging and DEXA.",
     ["Osteoarthritis", "Rheumatoid Arthritis", "Fibromyalgia"]),
    ("aesthetic", "aesthetic-medicine", "Aesthetic Medicine",
     "Cosmetic and aesthetic dermatology trials evaluating investigational treatments and devices.",
     ["Laser Skin Rejuvenation Surgery", "Breast Scar Revision", "Cellulite of the Upper Thighs"]),
    ("pediatrics", "pediatrics", "Pediatrics",
     "Past pediatric studies include trials for ear infections.",
     ["Acute Otitis Externa", "Acute Otitis Media"]),
]

# ---------------------------------------------------------------- studies
# status: enrolling | soon
STUDIES = [
    dict(slug="birth-control-contraceptive-patch", title="Birth Control: Contraceptive Patch",
         status="enrolling", areas=["womens"], label="Women's",
         img="assets/img/study-birth-control", img_pos="50% 32%",
         short="Exploring estrogen-free options? A patch trial may be right for you.",
         intro=["Not ready for parenthood?", "Need estrogen-free birth control?",
                "Exploring new birth control options?", "Stress from daily pills or IUDs?"],
         body="Consider a clinical trial for an investigational birth control patch.",
         criteria=["18 years of age or older"],
         more=None),
    dict(slug="urinary-incontinence", title="Urinary Incontinence",
         status="enrolling", areas=["urology", "womens"], label="Urology",
         img="assets/img/study-urinary-incontinence", img_pos="50% 42%",
         short="You may be able to join this study. Additional criteria apply.",
         intro=["Can I join this study?"],
         body="You may be able to join the study if you:",
         criteria=["Are aged 18 years and over",
                   "Are a woman (assigned female at birth)",
                   "Have a BMI* of 27 or higher",
                   "Have not lost or gained more than 5 kg of your body weight in the last 3 months",
                   "Have daily episodes of urinary incontinence, either stress urinary incontinence (SUI) only, "
                   "or mixed urinary incontinence with mainly stress symptoms",
                   "Do not have diabetes",
                   "Do not take any anti-obesity, stress urinary incontinence or overactive bladder medication"],
         note="*BMI stands for body mass index. It compares a person's weight to their height. "
              "If you do not know your BMI, you can ask your doctor.",
         more=("Study flyer (PDF)", "wp-content/uploads/2026/03/GZPS_Flyer_Master_v1_29Jul2025_EN-1.pdf")),
    dict(slug="weight-loss", title="Weight Loss",
         status="enrolling", areas=["internal"], label="Internal Medicine",
         img="wp-content/uploads/2026/08/Weight-Loss-Clinical-Trial-Volunteers-Lake-Worth-FL-1-768x768", img_ext="jpg",
         img_pos="50% 50%",
         short="Adults 18 to 75 with a BMI of 30 or higher may qualify. Additional criteria apply.",
         intro=["Inclusion criteria"],
         body="This study is open to men and women. You may be able to join if you are:",
         criteria=["18 to 75 years of age (inclusive) at the time of screening",
                   "BMI of 30.0 kg/m² or higher at screening, OR",
                   "BMI of 27.0 to under 30.0 kg/m² at screening with at least one weight-related condition: "
                   "high blood pressure, dyslipidemia, obstructive sleep apnea, cardiovascular disease, or MASLD"],
         note="BMI is calculated as weight in kilograms divided by the square of height in meters.",
         more=None),
    dict(slug="hot-flash-study", title="Hot Flash Study",
         status="soon", areas=["womens"], label="Women's",
         img="assets/img/study-hot-flash", img_pos="40% 38%",
         short="Healthy participants may qualify. Additional criteria apply.",
         intro=["Who can join the study?"],
         body="You may be able to join the study if you meet the following requirements:",
         criteria=["Healthy menopausal women 40 to 65 years of age",
                   "Have moderate to severe hot flashes daily"],
         more=None),
]

# Completed studies (study hub). Text from the design; extra items from WordPress.
PAST = [
    ("Dermatology", "Actinic Keratosis", "Evaluated a topical treatment for actinic keratosis skin lesions."),
    ("Dermatology", "Atopic Dermatitis / Eczema", "Studied adults with moderate to severe atopic dermatitis."),
    ("Dermatology", "Plaque Psoriasis", "Enrolled adults with moderate-to-severe plaque psoriasis."),
    ("Dermatology", "Psoriasis Study", "Evaluated an investigational treatment for men and women living with psoriasis."),
    ("Vaccines", "COVID-19 Study", "Tested a candidate vaccine for the prevention of COVID-19."),
    ("Vaccines", "Moderna Vaccine", "Assessed an mRNA vaccine candidate in eligible adult participants."),
    ("Vaccines", "Meningococcal Vaccine", "Evaluated a vaccine for the prevention of meningococcal disease."),
    ("Vaccines", "HPV Treatment Vaccine", "Studied an investigational vaccine for high-grade HPV."),
    ("Internal Medicine", "Diabetes & Fatty Liver", "Investigated a therapy for adults living with diabetes and fatty liver."),
    ("Internal Medicine", "High Blood Pressure", "Enrolled men and women with high blood pressure to assess an investigational treatment."),
    ("Rheumatology", "Osteoarthritis of the Knee", "Examined an investigational drug for osteoarthritis of the knee."),
    ("Women's", "Pelvic Pain", "Studied an investigational drug for women experiencing pelvic pain."),
    ("Women's", "Endometriosis Pain", "Studied women with endometriosis-related pain."),
    ("Women's", "Uterine Fibroids", "Investigated a treatment option for women with uterine fibroids."),
    ("Women's", "Hot Flashes", "Evaluated a treatment to relieve menopausal hot flashes."),
    ("Women's", "Menopause", "Studied a probiotic supplement for menopause symptoms."),
    ("Women's", "Yeast Infections", "Studied women with recurring yeast infections."),
    ("Women's", "Birth Control Pill", "Tested an investigational birth control pill."),
    ("Urology", "UTI (Urinary Tract Infections)", "Evaluated a treatment for women with urinary tract infections."),
]

# ---------------------------------------------------------------- team (from /meet-our-team/)
INVESTIGATOR = ("Samuel N. Lederman, MD, FACOG", "Medical Director & Lead Investigator",
                "assets/img/dr-lederman.jpg")
STAFF = [
    ("Jessica Ravelo", "Director of Operations", "wp-content/uploads/2024/06/Jessica-Ravelo-1.png"),
    ("Yanelys Perez", "Assistant Site Director", None),
    ("Teresa Carmona", "Office Manager", "wp-content/uploads/2024/06/Teresa-2.png"),
    ("Axel Hernandez", "Regulatory Specialist", None),
    ("Florinda Francisco", "Lead Research Coordinator", None),
    ("Stephanie Feliz", "Research Pharmacist and CRC", "wp-content/uploads/2024/06/Stephanie-Feliz.png"),
    ("Junieth Leyes", "Recruitment Specialist and CRC", "wp-content/uploads/2024/06/Junieth-Leyes.png"),
    ("Elena Miguel-Thomas", "Research Assistant", "wp-content/uploads/2024/06/Elena-Miguel-Thomas.png"),
    ("Jessica Francisco", "Research Assistant", None),
    ("Matthew DeBoer", "Data Entry Specialist", "wp-content/uploads/2024/06/Matthew-DeBoer.png"),
]

# ---------------------------------------------------------------- sponsors (design copy)
FACILITY = [
    "5,000 sq. ft. state-of-the-art facility integrated with clinical practice",
    "Board Certified physicians with years of clinical experience",
    "Investigators on-site daily",
    "Experienced Certified Clinical Research Coordinators",
    "Access to a 35,000-patient database",
    "Associated with a large OB/GYN private practice",
    "Academic site utilizing Central IRBs",
    "Proven history of rapid enrollment",
    "Secured drug room & study files with restricted access",
    "Locked, explosion-proof refrigerator monitored 24 hours a day",
    "IATA Certified staff with daily access to dry ice",
    "Multiple patient exam rooms with gowns & drapes",
    "Sonogram with 4D imaging, digital capture & 52″ display",
    "GE DEXA machine with digital reporting",
    "State-of-the-art colposcope & CLIA certified laboratory",
    "Private monitoring area with phone, T-1 line, internet & email",
    "Daily DHL & FedEx pick-up; electronic data entry experience",
    "On-site archiving & 24-hour access to on-call physician",
    "Knowledgeable of GCP and NIH standards",
    "HIPAA compliant, centrally located near freeways, hotels & airport",
]
RESOURCES = ["Centrifuge", "Clinical Laboratory", "Crash Cart", "DEXA Scanner", "Dry Ice", "EKG Equipment",
             "Fax / Scanner", "Freezer (−20°C)", "Freezer (−70°C)", "Refrigerator (2–8°C)", "Gram Stain Testing",
             "Wright Stain Testing", "High Speed Internet", "Microscope", "Pharmacy", "Phlebotomy",
             "Radiology Equipment", "Secure Medication Storage", "Secure Records Retention", "Ultrasound",
             "Uroflow", "Institutional Bio-safety", "Committee Certification", "Written SOPs"]

# ---------------------------------------------------------------- old URLs with no page of their own
# (GitHub Pages has no server redirects; 404.html sends these on.)
REDIRECTS = {
    "/study_archive/": "/current-studies/",
    "/studies/": "/current-studies/",
    "/expertise/": "/areas-of-expertise/",
    "/team/": "/meet-our-team/",
    "/contact/": "/contact-us/",
    "/thank-you/": "/contact-us/",
    "/thank-you-2/": "/contact-us/",
    "/sitemap/": "/",
    "/covid-19-study/": "/current-studies/#past",
    "/coronavirus-letter-to-our-patients/": "/",
    "/dlm-internal/": "/contact-us/",
    "/which-clinical-study-is-right-for-you/": "/current-studies/",
    "/pages/studies.html": "/current-studies/",
    "/pages/questionaire.html": "/contact-us/",
    "/study/birth-control/": "/current-studies/#past",
    "/study/covid-19-study/": "/current-studies/#past",
    "/study/covid-19-vaccine/": "/current-studies/#past",
    "/study/moderna-vaccine/": "/current-studies/#past",
    "/study/meningococcal-vaccine-study/": "/current-studies/#past",
    "/study/actinic-keratosis/": "/current-studies/#past",
    "/study/atopic-dermatitis-eczema/": "/current-studies/#past",
    "/study/diabetes-and-fatty-liver/": "/current-studies/#past",
    "/study/endometriosis-pain/": "/current-studies/#past",
    "/study/high-blood-pressure/": "/current-studies/#past",
    "/study/hot-flashes/": "/study/hot-flash-study/",
    "/study/hpv-treatment-vaccine/": "/current-studies/#past",
    "/study/menopause/": "/current-studies/#past",
    "/study/osteoarthritis-of-the-knee/": "/current-studies/#past",
    "/study/osteoarthritis-of-the-knee-2/": "/current-studies/#past",
    "/study/pelvic-pain/": "/current-studies/#past",
    "/study/plaque-psoriasis/": "/current-studies/#past",
    "/study/psoriasis-study/": "/current-studies/#past",
    "/study/uterine-fibroids/": "/current-studies/#past",
    "/study/uti-study/": "/current-studies/#past",
    "/study/uti-urinary-tract-infection/": "/current-studies/#past",
    "/study/yeast-infections/": "/current-studies/#past",
    "/study/infant-formula/": "/current-studies/#past",
    "/paid-vs-unpaid-clinical-trial-patients-does-money-encourage-better-results/": "/our-blog/",
}
# Prefix rules (WordPress archives): category, tag, author, page/N, feeds.
REDIRECT_PREFIXES = {
    "/category/": "/our-blog/",
    "/tag/": "/our-blog/",
    "/author/": "/our-blog/",
    "/study_category/": "/current-studies/",
    "/feed/": "/our-blog/",
    "/our-blog/page/": "/our-blog/",
}
