#!/usr/bin/env python3
"""Build the static site for altusresearch.com.

    python3 tools/build.py

Pages live at the same paths the WordPress site used, so old links and search
results keep working. {{ROOT}} becomes the relative path back to the site
root, so the build works on altusresearch.com and on a GitHub Pages preview
URL (https://<user>.github.io/altus-website/).
"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path

import content as C

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE = "https://altusresearch.com"
PAGES = []          # (path, html)
SITEMAP = []        # paths


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ shell
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{base}<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Altus Clinical Research">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="theme-color" content="#15294d">
<link rel="icon" href="{{{{ROOT}}}}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{{{{ROOT}}}}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{{{{ROOT}}}}assets/img/favicon-180.png">
<link rel="stylesheet" href="{{{{ROOT}}}}assets/css/site.css">
{extra}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""
FOOT = """<script src="{{ROOT}}assets/js/site.js" defer></script>
<script src="{{ROOT}}assets/js/i18n.js" defer></script>
</body>
</html>
"""


def fix_links(h):
    """Point links at old WordPress-only URLs straight at their new home."""
    def sub(m):
        path = "/" + m.group(1)
        frag = ""
        if "#" in path:
            path, frag = path.split("#", 1)
            frag = "#" + frag
        if path != "/" and not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
            fixed = path + "/"
            if fixed in C.REDIRECTS or (ROOT_DIR / fixed.lstrip("/")).exists():
                path = fixed
                if path not in C.REDIRECTS:
                    return 'href="{{ROOT}}' + path.lstrip("/") + frag + '"'
        if path in C.REDIRECTS:
            return 'href="{{ROOT}}' + C.REDIRECTS[path].lstrip("/") + '"'
        for pre, to in C.REDIRECT_PREFIXES.items():
            if path.startswith(pre):
                return 'href="{{ROOT}}' + to.lstrip("/") + '"'
        if path in ("/clinical-trials/",):
            return 'href="{{ROOT}}understanding-clinical-trials/"'
        return m.group(0)
    return re.sub(r'href="\{\{ROOT\}\}([^"]*)"', sub, h)


def page(path, title, desc, body, extra="", og_type="website", og_image=None, sitemap=True):
    depth = len([p for p in path.strip("/").split("/") if p])
    root = "../" * depth if depth else "./"
    canonical = SITE + path
    img = SITE + "/" + (og_image or "assets/img/hero-volunteers.jpg")
    header = (ROOT_DIR / "tools/partials/header.html").read_text(encoding="utf-8")
    footer = (ROOT_DIR / "tools/partials/footer.html").read_text(encoding="utf-8")
    out = (HEAD.format(base="", title=esc(title), desc=esc(desc), canonical=canonical, og_type=og_type,
                       og_image=img, extra=extra)
           + header + '\n<main id="main">\n' + body + "\n</main>\n" + footer + "\n" + FOOT)
    out = fix_links(out).replace("{{ROOT}}", root)
    assert "{{" not in out, f"unreplaced placeholder in {path}: {out[out.index('{{')-80:out.index('{{')+40]}"
    PAGES.append((path, out))
    if sitemap:
        SITEMAP.append(path)


# ------------------------------------------------------------------ components
def crumbs(*items):
    parts = ['<a href="{{ROOT}}">Home</a>']
    for label, href in items:
        parts.append(f'<a href="{{{{ROOT}}}}{href}">{esc(label)}</a>' if href else f'<span>{esc(label)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def hero(eyebrow, h1, lead="", trail=(), extra=""):
    return f"""<section class="page-hero"><div class="wrap">
  {crumbs(*trail)}
  <span class="eyebrow">{esc(eyebrow)}</span>
  <h1>{h1}</h1>
  {f'<p class="lead">{esc(lead)}</p>' if lead else ''}
  {extra}
</div></section>"""


def picture(stem, alt, ext="jpg", pos="50% 50%", lazy=True, cls="rf-img"):
    webp = (ROOT_DIR / f"{stem}.webp").exists()
    src = f"{{{{ROOT}}}}{stem}.{ext}"
    img = (f'<img class="{cls}" src="{src}" alt="{esc(alt)}" {"loading=\"lazy\" " if lazy else ""}'
           f'decoding="async" style="object-position:{pos}">')
    if webp:
        return f'<picture><source srcset="{{{{ROOT}}}}{stem}.webp" type="image/webp">{img}</picture>'
    return img


def chip(s):
    if s["status"] == "soon":
        return f'<span class="chip chip--soon">Coming soon · {esc(s["label"])}</span>'
    return f'<span class="chip">Enrolling · {esc(s["label"])}</span>'


def study_card(s):
    return f"""<a href="{{{{ROOT}}}}study/{s['slug']}/" class="study-card rf-card">
  <div class="rf-imgwrap">{picture(s['img'], s['title'], s.get('img_ext', 'jpg'), s['img_pos'])}</div>
  <div class="study-card__body">
    {chip(s)}
    <h3>{esc(s['title'])}</h3>
    <p>{esc(s['short'])}</p>
    <span class="more">Learn more →</span>
  </div>
</a>"""


def cta(eyebrow, h2, text, primary=("Enroll today →", "contact-us/"), phone=True):
    p_label, p_href = primary
    return f"""<section class="wrap" style="max-width:1100px;padding-top:72px;padding-bottom:80px">
  <div class="cta-box">
    <span class="eyebrow">{esc(eyebrow)}</span>
    <h2 class="h2">{esc(h2)}</h2>
    <p>{esc(text)}</p>
    <div class="btn-row">
      <a href="{{{{ROOT}}}}{p_href}" class="btn">{esc(p_label)}</a>
      {f'<a href="tel:{C.PHONE_TEL}" class="btn btn--light">Call {C.PHONE}</a>' if phone else ''}
    </div>
  </div>
</section>"""


def section_head(eyebrow, h2, link=None):
    l = f'<a href="{{{{ROOT}}}}{link[1]}" class="link-arrow">{esc(link[0])}</a>' if link else ""
    return f'<div class="section-head"><div><span class="eyebrow">{esc(eyebrow)}</span><h2 class="h2">{esc(h2)}</h2></div>{l}</div>'


ENROLLING = [s for s in C.STUDIES if s["status"] == "enrolling"]
AREA_BY_KEY = {a[0]: a for a in C.AREAS}


def area_card(a):
    key, slug, name, line, _ = a
    return f"""<a href="{{{{ROOT}}}}areas-of-expertise/{slug}/" class="card rf-card">
  <div class="icon-tile">{C.ICON[key]}</div>
  <h3 class="h3">{esc(name)}</h3>
  <p>{esc(line)}</p>
  <span class="link-arrow" style="display:inline-block;margin-top:14px;font-size:14px">Learn more →</span>
</a>"""


STEPS = [("Reach out", "Tell us your area of interest by form or phone."),
         ("Pre-screen", "A coordinator reviews eligibility at no cost."),
         ("Participate", "Join the study with our team at every visit."),
         ("Make an impact", "Help advance research for your community.")]


def steps_list():
    rows = "".join(f'<li><span class="steps__label">Step {i}</span><div><h3>{esc(t)}</h3><p>{esc(d)}</p></div></li>'
                   for i, (t, d) in enumerate(STEPS, 1))
    return f'<ol class="steps">{rows}</ol>'


def area_accordion(open_key="womens"):
    items = []
    for key, slug, name, line, _ in C.AREAS:
        is_open = key == open_key
        items.append(
            f'<div class="acc__item"><h3 class="acc__h"><button type="button" class="acc__btn" id="acc-b-{key}" '
            f'aria-expanded="{"true" if is_open else "false"}" aria-controls="acc-p-{key}">{esc(name)}</button></h3>'
            f'<div class="acc__panel" id="acc-p-{key}" role="region" aria-labelledby="acc-b-{key}"{"" if is_open else " hidden"}>'
            f'<p>{esc(line)}</p><a href="{{{{ROOT}}}}areas-of-expertise/{slug}/">Learn more →</a></div></div>')
    return '<div class="acc" data-accordion>' + "".join(items) + "</div>"


# ------------------------------------------------------------------ pages
def build_home():
    body = (ROOT_DIR / "pages/home.html").read_text(encoding="utf-8")
    body = (body.replace("{{AREA_ACCORDION}}", area_accordion())
                .replace("{{STEPS}}", steps_list())
                .replace("{{STUDY_CARDS}}", "\n".join(study_card(s) for s in C.STUDIES))
                .replace("{{RATING}}", esc(C.RATING))
                .replace("{{RATING_COUNT}}", esc(C.RATING_COUNT))
                .replace("{{RATING_LABEL}}", esc(C.RATING_LABEL))
                .replace("{{MAPS_URL}}", esc(C.MAPS_URL))
                .replace("{{N_ENROLLING}}", str(len(ENROLLING)))
                .replace("{{N_AREAS}}", str(len(C.AREAS))))
    org = {
        "@context": "https://schema.org", "@type": "MedicalClinic", "name": "Altus Clinical Research",
        "url": SITE + "/", "telephone": "+1-" + C.PHONE, "logo": SITE + "/assets/img/altus-logo.png",
        "address": {"@type": "PostalAddress", "streetAddress": C.ADDRESS_1, "addressLocality": "Lake Worth",
                    "addressRegion": "FL", "postalCode": "33461", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 26.607926, "longitude": -80.0902012},
        "medicalSpecialty": ["Gynecologic", "Urologic", "Dermatology"],
        "sameAs": ["https://www.facebook.com/AltusResearch/", "https://www.instagram.com/altusresearch/",
                   "https://twitter.com/altusresearch"],
    }
    extra = ('<link rel="preload" as="image" href="{{ROOT}}assets/img/hero-volunteers.webp" type="image/webp" '
             'fetchpriority="high">\n<script type="application/ld+json">' + json.dumps(org) + "</script>\n")
    page("/", "Altus Clinical Research | Clinical Trials in Lake Worth, FL",
         "Altus Clinical Research is a South Florida research site in Lake Worth, FL. See studies enrolling now "
         f"and find out if you qualify. Call {C.PHONE}.", body, extra=extra)


def build_expertise():
    n = len(C.AREAS)
    body = hero("Areas of expertise", "Research across the conditions that matter most",
                f"Eight therapeutic areas, all delivered from one trusted South Florida site. Our investigators "
                f"conduct Phase II–IV trials with the highest standards of subject safety and protocol adherence.",
                trail=[("Areas of Expertise", None)])
    body += f"""<section class="section"><div class="wrap">
  <div class="grid grid--areas">{''.join(area_card(a) for a in C.AREAS)}</div>
</div></section>"""
    body += cta("Get started", "Not sure which study fits you?",
                "Our coordinators will help you find the right trial at no cost. Reach out and we'll take it from there.",
                primary=("Talk to our team →", "contact-us/"))
    page("/areas-of-expertise/", "Areas of Expertise | Altus Clinical Research",
         "Clinical research in women's health, urology, dermatology, vaccines, internal medicine, rheumatology, "
         "aesthetic medicine and pediatrics at Altus Clinical Research in Lake Worth, FL.", body)

    guides = {"internal": ("Internal Medicine Clinical Research in Palm Springs, FL",
                           "areas-of-expertise/internal-medicine/internal-medicine-clinical-research-in-palm-springs-fl/"),
              "aesthetic": ("Aesthetic Medicine Clinical Research in Boynton Beach, FL",
                            "areas-of-expertise/aesthetic-medicine/aesthetic-medicine-clinical-research-in-boynton-beach-fl/")}
    for a in C.AREAS:
        key, slug, name, line, conditions = a
        studies = [s for s in C.STUDIES if key in s["areas"]]
        body = hero("Areas of expertise", esc(name), line,
                    trail=[("Areas of Expertise", "areas-of-expertise/"), (name, None)])
        body += f"""<section class="section"><div class="wrap">
  <span class="eyebrow">Experience</span>
  <h2 class="h2" style="margin-bottom:22px">Conditions our team has studied</h2>
  <ul class="dot-list">{''.join(f'<li>{esc(c)}</li>' for c in conditions)}</ul>
</div></section>
<section class="section section--alt"><div class="wrap">
  {section_head('Open enrollment', f'Currently enrolling {name} studies', ('View all studies →', 'current-studies/'))}
  {('<div class="grid grid--3">' + ''.join(study_card(s) for s in studies) + '</div>') if studies else
   f'<div class="card"><p style="margin:0;font-size:16px">We do not have any {esc(name)} studies enrolling right now. '
   f'Join our volunteer list and we will contact you when a study opens, or <a class="link-arrow" style="font-size:16px" href="{{{{ROOT}}}}current-studies/">see all current studies</a>.</p></div>'}
</div></section>"""
        if key in guides:
            g = guides[key]
            body += f"""<section class="section section--tight"><div class="wrap"><ul class="res-list"><li><a href="{{{{ROOT}}}}{g[1]}">{esc(g[0])}<small>Read the guide →</small></a></li></ul></div></section>"""
        body += cta("Get started", "Not sure which study fits you?",
                    "Our coordinators will help you find the right trial at no cost. Reach out and we'll take it from there.",
                    primary=("Talk to our team →", "contact-us/"))
        page(f"/areas-of-expertise/{slug}/", f"{name} Clinical Trials in Lake Worth, FL | Altus Clinical Research",
             f"{line} Altus Clinical Research, Lake Worth, FL.", body)


def build_studies():
    groups = []
    for cat in ["Women's", "Dermatology", "Vaccines", "Internal Medicine", "Rheumatology", "Urology"]:
        rows = "".join(f"<li><strong>{esc(t)}</strong><span>{esc(d)}</span></li>" for c, t, d in C.PAST if c == cat)
        if rows:
            groups.append(f'<div class="past-group"><h3>{esc(cat)}</h3><ul>{rows}</ul></div>')
    past = "".join(groups)
    body = hero("Clinical studies", "Find a study that's right for you",
                "Browse our currently enrolling trials below, or explore the studies we've completed. "
                "Pre-screening is always free.", trail=[("Studies", None)])
    body += f"""<section class="section"><div class="wrap">
  {section_head('Open enrollment', 'Currently enrolling studies')}
  <div class="grid grid--3">{''.join(study_card(s) for s in C.STUDIES)}</div>
</div></section>
<section class="section section--alt" id="past"><div class="wrap">
  {section_head('Completed', 'Past studies')}
  <div class="past-groups">{past}</div>
  <p class="muted" style="margin-top:24px;font-size:15px">Read about treatments our sites helped bring to patients on
  <a class="link-arrow" style="font-size:15px" href="{{{{ROOT}}}}results-of-past-studies/">Results of Past Studies →</a></p>
</div></section>"""
    body += cta("Get started", "See a study you're interested in?",
                "Reach out and a coordinator will check your eligibility, free and with no obligation.",
                primary=("Get pre-screened →", "contact-us/"))
    page("/current-studies/", "Current Clinical Studies in Lake Worth, FL | Altus Clinical Research",
         "Clinical trials enrolling now at Altus Clinical Research in Lake Worth, FL, plus studies we have "
         "completed. Pre-screening is always free.", body)

    for s in C.STUDIES:
        intro = "".join(f'<p class="h3" style="font-size:24px">{esc(q)}</p>' for q in s["intro"])
        crit = "".join(f"<li>{esc(c)}</li>" for c in s["criteria"])
        note = f'<p class="muted" style="font-size:14px;margin-top:14px">{esc(s["note"])}</p>' if s.get("note") else ""
        more = (f'<p style="margin-top:18px"><a class="link-arrow" href="{{{{ROOT}}}}{s["more"][1]}">{esc(s["more"][0])} →</a></p>'
                if s.get("more") else "")
        status = ("This study is coming soon. Contact us to be added to the interest list and we will reach out when "
                  "enrollment opens." if s["status"] == "soon" else "")
        body = hero("Clinical study", esc(s["title"]), s["short"],
                    trail=[("Studies", "current-studies/"), (s["title"], None)], extra=f'<div style="margin-top:18px">{chip(s)}</div>')
        body += f"""<section class="section"><div class="wrap study-layout">
  <div>
    {intro}
    <p style="font-size:17px;line-height:1.6;color:#42544f;margin-top:14px">{esc(s['body'])}</p>
    <ul class="check-list">{crit}</ul>
    <p style="font-size:15px;color:#42544f;margin-top:16px;font-weight:600">Additional criteria will apply.</p>
    {note}{more}
    {f'<div class="notice">{status}</div>' if status else ''}
    <div class="card" style="margin-top:32px"><h2 class="h3">What happens next?</h2>
      <p>A coordinator will review your eligibility at no cost and with no obligation to continue. If you qualify,
      we will explain the study, its visits and any risks in plain language before you decide.
      Participation requires in-person visits at our site in Lake Worth, FL.</p></div>
  </div>
  <aside class="aside-card">
    <div class="study-photo">{picture(s['img'], s['title'], s.get('img_ext', 'jpg'), s['img_pos'], lazy=False, cls='')}</div>
    <div class="card" style="margin-top:18px">
      <h2 class="h3">Interested in volunteering?</h2>
      <p>Tell us a little about yourself and our team will reach out about this study.</p>
      <div class="btn-row" style="margin-top:18px"><a class="btn" href="{{{{ROOT}}}}contact-us/">Enroll today →</a>
      <a class="btn btn--light" href="tel:{C.PHONE_TEL}">Call {C.PHONE}</a></div>
    </div>
  </aside>
</div></section>"""
        img_rel = f"{s['img']}.{s.get('img_ext', 'jpg')}"
        page(f"/study/{s['slug']}/", f"{s['title']} Study Volunteers Near Lake Worth, FL | Altus Clinical Research",
             f"{s['title']} clinical study at Altus Clinical Research in Lake Worth, FL. {s['short']}", body,
             og_image=img_rel)


def build_volunteers():
    benefits = [("Free pre-screening", "A coordinator reviews your eligibility at no cost and with no obligation to continue."),
                ("Learn about investigational studies",
                 "A coordinator explains the study medication, the visits and the possible risks before you decide."),
                ("Care close to home", "Compassionate, attentive care from a team that treats your time and safety as the priority.")]
    body = hero("Volunteers", "Your participation moves medicine forward",
                "Volunteers play a critical role in advancing treatment for many conditions. We guide you through every "
                "step in plain language, with compassionate care close to home.", trail=[("Volunteers", None)],
                extra='<div class="btn-row"><a class="btn" href="{{ROOT}}current-studies/">Browse studies</a>'
                      '<a class="btn btn--light" href="{{ROOT}}contact-us/">Enroll today</a></div>')
    body += ('<section class="section"><div class="wrap" style="max-width:1100px">'
             '<span class="eyebrow">Why volunteer with Altus</span><h2 class="h2" style="margin-bottom:26px">What to expect from us</h2>'
             '<ul class="benefits">' + "".join(f"<li><strong>{esc(t)}</strong><span>{esc(d)}</span></li>" for t, d in benefits)
             + '</ul></div></section>')
    body += ('<section class="section section--alt"><div class="wrap" style="max-width:1100px">'
             '<span class="eyebrow">How it works</span><h2 class="h2">Joining a study is simple</h2>'
             f'<div style="max-width:720px">{steps_list()}</div></div></section>')
    body += f"""<section class="section"><div class="wrap wrap--narrow prose">
  <span class="eyebrow">What it means to volunteer</span>
  <h2 style="margin-top:12px">Informed consent and your rights</h2>
  <p>Clinical trials are studies where volunteers are needed to test the effectiveness of investigational drugs, devices or other
  treatments that may then be approved for general use. Our physicians help recruit patients to learn more about
  certain medical conditions and the usefulness of investigational treatments.</p>
  <p>Everyone who takes part in a study must meet that study's requirements and be willing to sign an informed consent.
  Informed consent is voluntary agreement, given by you (or a responsible proxy), after you have been told the methods,
  procedures, risks and benefits of taking part. Consent must be given freely and without undue influence, and you
  have the right to withdraw from the study at any time.</p>
  <p><strong>Please note:</strong> all of our studies require face-to-face visits with our staff, so we are looking for
  volunteers who live near our site in Lake Worth, FL.</p>
  <p><a href="{{{{ROOT}}}}{C.NPP_PDF}">View our Notice of Privacy Practices (PDF)</a> ·
  <a href="{{{{ROOT}}}}volunteers/what-to-expect-when-you-volunteer-for-a-clinical-trial-in-palm-beach-fl/">What to expect when you volunteer</a></p>
</div></section>
<section class="section section--alt"><div class="wrap">
  {section_head('Open enrollment', 'Currently enrolling studies', ('View all studies →', 'current-studies/'))}
  <div class="grid grid--3">{''.join(study_card(s) for s in C.STUDIES)}</div>
</div></section>"""
    body += cta("Get started", "Ready to get started?",
                "Take the first step today. Pre-screening is always free and there's no obligation to continue.")
    page("/volunteers/", "Clinical Trial Volunteers in Lake Worth, FL | Altus Clinical Research",
         "Volunteer for a clinical trial at Altus Clinical Research in Lake Worth, FL. Free pre-screening, "
         "plain-language guidance and care close to home.", body)


def build_sponsors():
    body = hero("For research sponsors", "A quality research site, ready for your next study",
                "We offer our sponsors a trained and experienced clinical research team. The diverse Palm Beach County "
                "suburban population, exceeding 1.3 million, supports FDA standards for ethnically and racially diverse "
                "subjects, and our central location near major highways and public transportation keeps access easy "
                "for both subjects and sponsor visits.", trail=[("Sponsors", None)])
    body += f"""<section class="section"><div class="wrap">
  <span class="eyebrow">Facilities</span><h2 class="h2" style="margin-bottom:24px">About our research facilities</h2>
  <ul class="check-list" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px 32px">
  {''.join(f'<li>{esc(x)}</li>' for x in C.FACILITY)}</ul>
</div></section>
<section class="section section--alt"><div class="wrap">
  <span class="eyebrow">Equipment</span><h2 class="h2" style="margin-bottom:20px">Available resources</h2>
  <ul class="pill-list">{''.join(f'<li>{esc(x)}</li>' for x in C.RESOURCES)}</ul>
</div></section>
<section class="section section--tight"><div class="wrap"><ul class="res-list">
  <li><a href="{{{{ROOT}}}}meet-our-team/">Meet our investigator and research team<small>Our team →</small></a></li>
  <li><a href="{{{{ROOT}}}}results-of-past-studies/">Approvals our research supported<small>Results →</small></a></li>
</ul></div></section>"""
    body += cta("For sponsors", "Let's talk about your protocol",
                "Interested in placing a study with us? Let's talk about your protocol, timelines, and enrollment goals.",
                primary=("Discuss your study with us →", "contact-us/"))
    page("/sponsors/", "Clinical Research Site for Sponsors | Altus Clinical Research",
         "A 5,000 sq. ft. research site in Palm Beach County with experienced coordinators, central IRB experience, "
         "a 35,000-patient database and a proven history of rapid enrollment.", body)


def person(name, role, photo, lead=False, eyebrow="Investigator"):
    initials = "".join(w[0] for w in name.replace(",", "").replace("Dr. ", "").split()[:2] if w[0].isalpha())
    if photo:
        stem = photo.rsplit(".", 1)[0]
        img = f'<img src="{{{{ROOT}}}}{photo}" alt="{esc(name)}" loading="lazy" decoding="async">'
        ph = (f'<picture><source srcset="{{{{ROOT}}}}{stem}.webp" type="image/webp">{img}</picture>'
              if (ROOT_DIR / f"{stem}.webp").exists() else img)
    else:
        ph = initials
    return (f'<div class="person{" person--lead" if lead else ""}"><div class="person__photo">{ph}</div>'
            f'<div class="person__body">{f"<span class=eyebrow>{esc(eyebrow)}</span>" if lead else ""}'
            f'<div class="person__name"{" style=\"font-size:24px;margin-top:8px;font-family:Times New Roman,serif\"" if lead else ""}>{esc(name)}</div>'
            f'<div class="person__role">{esc(role)}</div></div></div>')


def build_team():
    body = hero("Our people", "Meet the Altus team",
                "Trained, experienced research professionals who adhere to the highest ethical, regulatory, and industry "
                "standards, and stay current through ongoing continuing education.", trail=[("Our Team", None)])
    body += f"""<section class="section"><div class="wrap">
  {person(*C.INVESTIGATOR, lead=True)}
  <div style="margin-top:22px">{person(*C.PA, lead=True, eyebrow="Investigator")}</div>
  <h2 class="h2" style="margin:56px 0 24px">Our staff</h2>
  <div class="team-grid">{''.join(person(*p) for p in C.STAFF)}</div>
</div></section>"""
    body += cta("Get started", "Ready to take the next step?",
                "Tell us a little about yourself and our team will reach out about current and upcoming studies.")
    page("/meet-our-team/", "Meet Our Team | Altus Clinical Research",
         "Meet the investigator and research staff at Altus Clinical Research in Lake Worth, FL.", body)


def build_about():
    body = hero("About us", "An independent research site in Lake Worth, Florida",
                "Altus Research is an independent, free-standing, state-of-the-art clinical research facility.",
                trail=[("About Us", None)])
    body += f"""<section class="section"><div class="wrap wrap--narrow prose">
  <p>Working closely with major pharmaceutical corporations, we help research novel and sophisticated medications,
  procedures, vaccinations and treatment regimens and, in turn, seek to promote their successful implementation into
  modern medical practice.</p>
  <p>Altus Research has a qualified and dedicated research staff. We provide comprehensive administrative management and
  experienced study coordinators to allow accurate and timely enrollment and completion of clinical trials.</p>
  <p>Our research staff has been conducting clinical trials since 1996, and more than eight community-based private
  practice physicians participate in research at our center. Our clinical staff and administrators are committed to
  efficient operations: fulfilling contractual time and budget parameters and implementing protocol, GCP and ICH
  compliance in a safe and comfortable environment.</p>
</div></section>
<section class="section section--alt"><div class="wrap"><div class="grid grid--3">
  <a class="card rf-card" href="{{{{ROOT}}}}meet-our-team/"><h2 class="h3">Meet our team</h2><p>The investigator and staff behind every study.</p></a>
  <a class="card rf-card" href="{{{{ROOT}}}}sponsors/"><h2 class="h3">For sponsors</h2><p>Our facility, equipment and enrollment track record.</p></a>
  <a class="card rf-card" href="{{{{ROOT}}}}volunteers/"><h2 class="h3">For volunteers</h2><p>How taking part works, and studies enrolling now.</p></a>
</div></div></section>"""
    body += cta("Get started", "Ready to take the next step?",
                "Tell us a little about yourself and our team will reach out about current and upcoming studies.")
    page("/about-us/", "About Us | Altus Clinical Research, Lake Worth, FL",
         "Altus Research is an independent, state-of-the-art clinical research facility in Lake Worth, FL, "
         "conducting clinical trials since 1996.", body)


def build_contact():
    if C.FORM_EMBED_URL:
        form = (f'<div class="card" style="padding:12px"><iframe class="form-frame" src="{esc(C.FORM_EMBED_URL)}" '
                f'title="Volunteer inquiry form" loading="lazy"></iframe></div>')
    else:
        areas = "".join(f'<option>{esc(a[2])}</option>' for a in C.AREAS)
        form = f"""<div class="card" style="padding:32px">
  <span class="eyebrow">Get pre-screened</span>
  <h2 class="h2" style="font-size:32px">Send us your information</h2>
  <form id="inquiry" class="inq" novalidate data-to="{C.INQUIRY_EMAIL}">
    <div class="inq__row">
      <label>First name<input name="first" autocomplete="given-name" required></label>
      <label>Last name<input name="last" autocomplete="family-name" required></label>
    </div>
    <div class="inq__row">
      <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
      <label>Email<input name="email" type="email" autocomplete="email" required></label>
    </div>
    <label>Area of interest<select name="area" required><option value="">Select an area</option>{areas}<option>Weight Loss</option><option>Not sure / any study</option></select></label>
    <label>Message (optional)<textarea name="message" rows="4"></textarea></label>
    <label class="inq__check"><input type="checkbox" name="consent" required><span>We'll never share your information. By submitting, you agree to be contacted about studies.</span></label>
    <p class="inq__err" role="alert" hidden>Please fill in every field marked above and tick the box.</p>
    <button class="btn" type="submit">Send my information →</button>
    <p class="inq__note">Clicking send opens your email app with your details filled in. Just press Send there.
    No email app? Call us at <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a>.</p>
  </form>
  <div class="inq__done" hidden>
    <h3 class="h3">Almost done: press Send in your email app.</h3>
    <p>Your email app should have opened with your details filled in. Press Send and a coordinator will reach out.
    If nothing opened, please call <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a>.</p>
  </div>
</div>"""
    body = hero("Contact", "Enroll today.",
                "Tell us a little about yourself and our team will reach out about current and upcoming studies.",
                trail=[("Contact", None)])
    body += f"""<section class="section"><div class="wrap contact-layout">
  <div>
    <span class="eyebrow">Visit or call</span>
    <h2 class="h2">Altus Clinical Research</h2>
    <ul class="info-list">
      <li><span class="icon-tile" style="margin:0;flex-shrink:0">☎</span><span>Phone<br><a href="tel:{C.PHONE_TEL}">{C.PHONE}</a></span></li>
      <li><span class="icon-tile" style="margin:0;flex-shrink:0">⌂</span><span>{C.ADDRESS_1}<br>{C.ADDRESS_2}<br>
        <a href="{C.MAPS_URL}" target="_blank" rel="noopener" style="font-size:14px;color:#14796b">Open in Google Maps →</a></span></li>
    </ul>
    <p class="muted" style="font-size:15px;line-height:1.6;margin-top:22px">Our research facility is on the campus of the
    largest hospital in Palm Beach County, minutes from Palm Beach International Airport and all major highways.</p>
    <iframe class="map" src="{C.MAP_EMBED}" title="Map to Altus Clinical Research" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  <div>{form}
    <p class="muted" style="font-size:13px;line-height:1.55;margin-top:14px"><a href="{{{{ROOT}}}}{C.NPP_PDF}" style="color:#14796b">Notice of Privacy Practices</a></p>
  </div>
</div></section>"""
    page("/contact-us/", "Contact Us | Altus Clinical Research, Lake Worth, FL",
         f"Contact Altus Clinical Research at {C.ADDRESS_1}, {C.ADDRESS_2}. Call {C.PHONE} to get pre-screened for a study.",
         body, extra='<script src="{{ROOT}}assets/js/contact.js" defer></script>\n')


FAQ = [
    ("What is a clinical trial?",
     "A clinical trial is a research study in people that tests whether a new drug, device or treatment is safe and "
     "effective. Treatments are studied in clinical trials before they can be approved for general use. "
     '<a href="{{ROOT}}understanding-clinical-trials/">Learn more about clinical trials</a>.'),
    ("Who can take part in a study?",
     "Each study has its own requirements, such as age, health history or a specific condition. A coordinator checks "
     "whether you may qualify during a free pre-screening. All of our studies require in-person visits, so volunteers "
     'should live near our site in Lake Worth, FL. <a href="{{ROOT}}current-studies/">See studies enrolling now</a>.'),
    ("Does pre-screening cost anything?",
     "No. Pre-screening is always free, and there's no obligation to continue."),
    ("What is informed consent?",
     "Before you join, the study team explains the methods, procedures, risks and benefits of taking part, and answers "
     "your questions. You decide freely and without pressure, and you can withdraw from a study at any time. "
     '<a href="{{ROOT}}what-is-informed-consent-in-medical-studies/">Read more about informed consent</a>.'),
    ("Will I be paid for taking part?",
     "Some studies offer compensation for time and travel. Whether a study does, and how much, differs by study and is "
     "explained to you before you agree to take part."),
    ("Could I receive a placebo?",
     "Some studies compare a treatment to a placebo. You will be told during informed consent whether the study uses one. "
     '<a href="{{ROOT}}what-is-a-placebo-and-should-you-be-worried-about-getting-one/">What a placebo is, and what it means for you</a>.'),
    ("How is my personal information protected?",
     "Your health information is protected under federal privacy law. "
     f'<a href="{{{{ROOT}}}}{C.NPP_PDF}">Read our Notice of Privacy Practices (PDF)</a> or '
     '<a href="{{ROOT}}how-personal-information-is-protected-in-a-research-study/">how personal information is protected in a study</a>.'),
    ("Where are you located?",
     f"{C.ADDRESS_1}, {C.ADDRESS_2}, on the campus of the largest hospital in Palm Beach County, minutes from Palm Beach "
     "International Airport."),
    ("How do I get started?",
     f'Call <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a> or <a href="{{{{ROOT}}}}contact-us/">contact us</a> and a '
     "coordinator will reach out about current and upcoming studies."),
]


def build_faq():
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="ans">{a}</div></details>' for q, a in FAQ)
    body = hero("Resources", "Frequently asked questions", trail=[("FAQ", None)])
    body += f'<section class="section"><div class="wrap wrap--narrow faq">{items}</div></section>'
    body += cta("Get started", "Still have questions?",
                "Our coordinators are happy to talk you through any study. Pre-screening is always free.")
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a.replace("{{ROOT}}", ""))}}
        for q, a in FAQ]}
    page("/faq/", "Frequently Asked Questions | Altus Clinical Research",
         "Answers about clinical trials at Altus Clinical Research: who can take part, cost, compensation, "
         "informed consent, placebos and privacy.", body,
         extra='<script type="application/ld+json">' + json.dumps(ld) + "</script>\n")


def build_resources():
    pdfs = [("What are the different types of clinical trials?", "wp-content/uploads/2020/02/for-coard-one-trial-wasnt-enough.pdf"),
            ("Who are the members of a clinical research team?", "wp-content/uploads/2020/02/Jenna-Korb-back-from-the-brink.pdf"),
            ("What is the difference between a standard treatment and a clinical trial?", "wp-content/uploads/2020/02/Issue5.pdf"),
            ("How can I make sure a clinical trial is safe?", "wp-content/uploads/2020/02/healthy-volunteer-inspired.pdf"),
            ("How can I weigh the risks in participating in a clinical trial?", "wp-content/uploads/2020/02/child-dream-for-cancer-research.pdf")]
    reads = [("Phases of clinical trials and what they mean", "phases-of-clinical-trials-and-what-they-mean/"),
             ("What is informed consent in medical studies?", "what-is-informed-consent-in-medical-studies/"),
             ("What are the rights of clinical trial participants?", "what-are-the-rights-of-clinical-trial-participants/"),
             ("Are clinical trials safe?", "are-clinical-trials-safe/"),
             ("Questions you should ask before participating", "questions-you-should-ask-before-participating-in-a-clinical-trial/"),
             ("Common myths about clinical trials, and the facts", "common-myths-about-clinical-trials-and-the-facts/")]
    li = lambda items, tag: "".join(f'<li><a href="{{{{ROOT}}}}{h}">{esc(t)}<small>{tag}</small></a></li>' for t, h in items)
    body = hero("Resources", "Understanding clinical trials",
                "Plain-language guides to how clinical research works and what taking part involves.",
                trail=[("Understanding Clinical Trials", None)])
    body += f"""<section class="section"><div class="wrap wrap--narrow">
  <span class="eyebrow">Guides</span><h2 class="h2" style="margin-bottom:22px">Questions people often ask</h2>
  <ul class="res-list">{li(pdfs, 'PDF →')}</ul>
  <h2 class="h2" style="margin:56px 0 22px">From our blog</h2>
  <ul class="res-list">{li(reads, 'Read →')}</ul>
  <p style="margin-top:22px"><a class="link-arrow" href="{{{{ROOT}}}}our-blog/">All articles →</a> &nbsp;
  <a class="link-arrow" href="{{{{ROOT}}}}faq/">Frequently asked questions →</a></p>
</div></section>"""
    body += cta("Get started", "Ready to take the next step?",
                "Tell us a little about yourself and our team will reach out about current and upcoming studies.")
    page("/understanding-clinical-trials/", "Understanding Clinical Trials | Altus Clinical Research",
         "Guides to how clinical trials work: types of trials, the research team, safety, risks and your rights.", body)

    results = [("Chemo, Laboratorios León Farma: Birth Control", "Exeltis announced FDA approval of Slynd (drospirenone) for prescription use in the United States.",
                "wp-content/uploads/2020/02/Birth-Control-Slynd-Approval-1.pdf"),
               ("AbbVie: Endometriosis", "AbbVie received U.S. FDA approval of ORILISSA (elagolix) for the management of moderate to severe pain associated with endometriosis.",
                "wp-content/uploads/2020/02/Press-Release-Elagolix-Oralissa-FDA-Approval-R..-1.pdf"),
               ("Endoceutics: Vaginal Atrophy", "Endoceutics received Health Canada approval for Intrarosa, the first innovative drug for the treatment of vulvovaginal atrophy with prasterone.",
                "wp-content/uploads/2020/02/PressRelease_EN_Intrarosa_NOC_Canada-1.pdf"),
               ("Regeneron", "Regeneron and Sanofi announced that dupilumab received FDA Breakthrough Therapy Designation in atopic dermatitis.",
                "wp-content/uploads/2020/02/Press-Release-Dupilamab-FDA-approval-1.pdf")]
    body = hero("Results", "Results of past studies",
                "Treatments that research like ours helped bring to patients.", trail=[("Results of Past Studies", None)])
    body += '<section class="section"><div class="wrap wrap--narrow"><div class="grid" style="gap:16px">' + "".join(
        f'<a class="card rf-card" href="{{{{ROOT}}}}{u}"><h2 class="h3">{esc(t)}</h2><p>{esc(d)}</p>'
        f'<span class="link-arrow" style="display:inline-block;margin-top:12px;font-size:14px">Press release (PDF) →</span></a>'
        for t, d, u in results) + "</div></div></section>"
    page("/results-of-past-studies/", "Results of Past Studies | Altus Clinical Research",
         "FDA and Health Canada approvals for treatments studied in clinical research.", body)

    body = hero("News", "In the press", trail=[("In the Press", None)])
    body += f"""<section class="section"><div class="wrap wrap--narrow"><a class="card rf-card" target="_blank" rel="noopener"
  href="https://www.fool.com/investing/2020/11/20/coronavirus-vaccine-maker-past-pfizer-moderna/">
  <span class="chip">The Motley Fool · November 2020</span>
  <h2 class="h3" style="margin-top:12px">Here's the Coronavirus Vaccine Maker That's Most Likely to Blow Past Pfizer and Moderna</h2>
  <span class="link-arrow" style="display:inline-block;margin-top:12px;font-size:14px">Read the article →</span></a></div></section>"""
    page("/in-the-press/", "In the Press | Altus Clinical Research", "Altus Clinical Research in the news.", body)

    body = hero("Patients", "Patient forms", "Download and complete these forms before your visit, or fill them in at our office.",
                trail=[("Patient Forms", None)])
    body += f"""<section class="section"><div class="wrap wrap--narrow"><ul class="res-list">
  <li><a href="{{{{ROOT}}}}wp-content/uploads/2020/02/HP_short-1.pdf">Medical history<small>PDF →</small></a></li>
  <li><a href="{{{{ROOT}}}}wp-content/uploads/2020/02/Pt-database-form-2.pdf">Patient database form<small>PDF →</small></a></li>
  <li><a href="{{{{ROOT}}}}{C.NPP_PDF}">Notice of Privacy Practices<small>PDF →</small></a></li>
</ul></div></section>"""
    page("/patient-forms/", "Patient Forms | Altus Clinical Research", "Patient forms for Altus Clinical Research.", body)

    body = hero("Accessibility", "Accessibility statement", trail=[("Accessibility", None)])
    body += f"""<section class="section"><div class="wrap wrap--narrow prose">
  <p>Altus Clinical Research wants everyone, including people with disabilities, to be able to use this website and
  learn about our studies.</p>
  <p>We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA. The site is built with semantic
  headings and landmarks, works with a keyboard, supports screen readers, respects reduced-motion settings, and offers
  English and Spanish.</p>
  <h2>Need help?</h2>
  <p>If any part of this site is hard to use, or you need information in another format, please call us at
  <a href="tel:{C.PHONE_TEL}">{C.PHONE}</a> during business hours and we will help.</p>
  <p class="muted" style="font-size:15px">Last reviewed October 2026.</p>
</div></section>"""
    page("/accessibility-statement/", "Accessibility Statement | Altus Clinical Research",
         "Accessibility statement for altusresearch.com.", body)


def thumb(img):
    """Small JPEG for list cards; full image stays for the article page."""
    if not img:
        return None
    from PIL import Image
    src = ROOT_DIR / img
    out = ROOT_DIR / "assets/thumbs" / (Path(img).stem + ".jpg")
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(src).convert("RGB")
        im.thumbnail((720, 720))
        im.save(out, "JPEG", quality=78, optimize=True, progressive=True)
    return f"assets/thumbs/{out.name}"


def nice_date(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%B %-d, %Y")


def build_articles():
    meta = json.loads((ROOT_DIR / "content/articles.json").read_text(encoding="utf-8"))
    posts = [m for m in meta if m["kind"] == "post"]
    for m in meta:
        body_html = (ROOT_DIR / "content/articles" / m["file"]).read_text(encoding="utf-8")
        is_post = m["kind"] == "post"
        trail = [("Our Blog", "our-blog/"), (m["title"], None)] if is_post else [(m["title"], None)]
        h = hero("Our blog" if is_post else "Guide", esc(m["title"]), trail=trail,
                 extra=f'<p class="article-meta">{nice_date(m["date"]) if is_post else "Altus Clinical Research"}</p>')
        img = ""
        if m["img"]:
            img = (f'<div class="wrap wrap--narrow"><div class="article-hero-img"><img src="{{{{ROOT}}}}{m["img"]}" '
                   f'alt="" decoding="async"></div></div>')
        related = [p for p in posts if p["path"] != m["path"]][:3]
        rel = "".join(post_card(p) for p in related)
        body = h + img + f"""<article class="section"><div class="wrap wrap--narrow prose">{body_html}</div></article>
<section class="section section--alt"><div class="wrap">
  {section_head('Keep reading', 'More from our blog', ('All articles →', 'our-blog/'))}
  <div class="grid grid--3">{rel}</div>
</div></section>"""
        body += cta("Get started", "Ready to take the next step?",
                    "Tell us a little about yourself and our team will reach out about current and upcoming studies.")
        ld = {"@context": "https://schema.org", "@type": "BlogPosting" if is_post else "Article", "headline": m["title"],
              "datePublished": m["date"], "dateModified": m["modified"],
              "publisher": {"@type": "Organization", "name": "Altus Clinical Research"},
              "mainEntityOfPage": SITE + m["path"]}
        if m["img"]:
            ld["image"] = SITE + "/" + m["img"]
        page(m["path"], f'{m["title"]} | Altus Clinical Research', m["desc"], body, og_type="article",
             og_image=m["img"], extra='<script type="application/ld+json">' + json.dumps(ld) + "</script>\n")

    body = hero("Our blog", "Learn about clinical research",
                "Articles from our team on how clinical trials work, what to expect, and research in South Florida.",
                trail=[("Our Blog", None)])
    body += f'<section class="section"><div class="wrap"><div class="grid grid--3">{"".join(post_card(p) for p in posts)}</div></div></section>'
    page("/our-blog/", "Our Blog | Altus Clinical Research",
         "Articles about clinical trials, volunteering and medical research from Altus Clinical Research.", body)


def post_card(p):
    t = thumb(p["img"])
    img = (f'<div class="rf-imgwrap"><img class="rf-img" src="{{{{ROOT}}}}{t}" alt="" loading="lazy" decoding="async"></div>'
           if t else "")
    return (f'<a class="post-card rf-card" href="{{{{ROOT}}}}{p["path"].lstrip("/")}">{img}<div class="post-card__body">'
            f'<h3>{esc(p["title"])}</h3><time datetime="{p["date"]}">{nice_date(p["date"])}</time></div></a>')


def build_404():
    redirects = json.dumps(C.REDIRECTS)
    prefixes = json.dumps(C.REDIRECT_PREFIXES)
    script = f"""<script>
(function(){{
  var host=location.hostname, parts=location.pathname.split('/');
  var base=/github\\.io$/.test(host)&&parts[1]?'/'+parts[1]:'';
  document.write('<base href="'+base+'/">');
  var p=location.pathname.slice(base.length)||'/';
  if(!/\\/$/.test(p)&&!/\\.[a-z0-9]+$/i.test(p))p+='/';
  p=p.toLowerCase();
  var R={redirects}, P={prefixes}, to=R[p];
  if(!to){{for(var k in P){{if(p.indexOf(k)===0){{to=P[k];break;}}}}}}
  if(to){{location.replace(base+to);}}
}})();
</script>
"""
    body = hero("Page not found", "We couldn't find that page",
                "It may have moved when we updated our website. These links will get you where you need to go.")
    body += """<section class="section"><div class="wrap wrap--narrow"><ul class="res-list">
  <li><a href="{{ROOT}}current-studies/">Studies enrolling now<small>Studies →</small></a></li>
  <li><a href="{{ROOT}}volunteers/">Volunteer for a study<small>Volunteers →</small></a></li>
  <li><a href="{{ROOT}}our-blog/">Articles about clinical research<small>Blog →</small></a></li>
  <li><a href="{{ROOT}}contact-us/">Contact us<small>Contact →</small></a></li>
</ul></div></section>"""
    header = (ROOT_DIR / "tools/partials/header.html").read_text(encoding="utf-8")
    footer = (ROOT_DIR / "tools/partials/footer.html").read_text(encoding="utf-8")
    out = (HEAD.format(base=script, title="Page not found | Altus Clinical Research", desc="Page not found.",
                       canonical=SITE + "/404.html", og_type="website", og_image=SITE + "/assets/img/hero-volunteers.jpg",
                       extra='<meta name="robots" content="noindex">\n')
           + header + '\n<main id="main">\n' + body + "\n</main>\n" + footer + "\n" + FOOT)
    out = out.replace("{{ROOT}}", "")
    PAGES.append(("/404.html", out))


def write_all():
    # remove previously generated pages (any dir holding an index.html we wrote), keep sources
    keep = {"assets", "wp-content", "tools", "pages", "content", ".git"}
    for child in ROOT_DIR.iterdir():
        if child.is_dir() and child.name not in keep and not child.name.startswith("."):
            shutil.rmtree(child)
    for path, out in PAGES:
        dest = ROOT_DIR / (path.lstrip("/") if path.endswith(".html") else path.lstrip("/") + "index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
    today = date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod></url>\n" for p in SITEMAP)
    (ROOT_DIR / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                          + urls + "</urlset>\n", encoding="utf-8")
    (ROOT_DIR / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(PAGES)} pages")


if __name__ == "__main__":
    build_home()
    build_expertise()
    build_studies()
    build_volunteers()
    build_sponsors()
    build_team()
    build_about()
    build_contact()
    build_faq()
    build_resources()
    build_articles()
    build_404()
    write_all()
