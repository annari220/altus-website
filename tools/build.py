#!/usr/bin/env python3
"""Build the static site.

Each page in PAGES is a body fragment in pages/. This wraps it with the
shared <head>, header and footer partials and writes <out>/index.html.
{{ROOT}} is replaced with the relative path back to the site root, so the
site works both at https://altusresearch.com/ and at a GitHub Pages
project URL (https://<user>.github.io/altus-website/).

Run from the repo root:  python3 tools/build.py
"""
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE = "https://altusresearch.com"

PAGES = [
    # (body fragment, output dir, <title>, meta description)
    ("home.html", "", "Altus Clinical Research | Clinical Trials in Lake Worth, FL",
     "Altus Clinical Research is a South Florida research site in Lake Worth, FL. "
     "See studies enrolling now and find out if you qualify. Call 561-641-0404."),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Altus Clinical Research">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/hero-volunteers.jpg">
<meta name="theme-color" content="#15294d">
<link rel="icon" href="{{{{ROOT}}}}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{{{{ROOT}}}}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{{{{ROOT}}}}assets/img/favicon-180.png">
<link rel="stylesheet" href="{{{{ROOT}}}}assets/css/site.css">
{extra_head}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

FOOT = """<script src="{{ROOT}}assets/js/site.js" defer></script>
<script src="{{ROOT}}assets/js/i18n.js" defer></script>
</body>
</html>
"""


def build():
    header = (ROOT_DIR / "tools/partials/header.html").read_text(encoding="utf-8")
    footer = (ROOT_DIR / "tools/partials/footer.html").read_text(encoding="utf-8")
    for frag, out, title, desc in PAGES:
        depth = len([p for p in out.split("/") if p])
        root = "../" * depth if depth else "./"
        body = (ROOT_DIR / "pages" / frag).read_text(encoding="utf-8")
        extra = ""
        if frag == "home.html":
            extra = ('<link rel="preload" as="image" href="{{ROOT}}assets/img/hero-volunteers.webp" '
                     'type="image/webp" fetchpriority="high">\n')
        canonical = f"{SITE}/{out}" if out else f"{SITE}/"
        html = (HEAD.format(title=title, desc=desc, canonical=canonical, site=SITE, extra_head=extra)
                + header + '\n<main id="main">\n' + body + "</main>\n" + footer + "\n" + FOOT)
        html = html.replace("{{ROOT}}", root)
        assert "{{" not in html, f"unreplaced placeholder in {frag}"
        dest = ROOT_DIR / out / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")
        print("built", dest.relative_to(ROOT_DIR))


if __name__ == "__main__":
    build()
