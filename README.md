# altusresearch.com

Static site for Altus Clinical Research, built from the Claude Design project
"Website discussion" (Altus - Bold). Hosted free on GitHub Pages.

- `pages/` page bodies (edit these), `tools/partials/` shared header and footer
- `assets/` CSS, JS (mobile menu, EN/ES switch) and images
- `design-src/` the original Claude Design files, for reference
- Build: `python3 tools/build.py` writes each page's `index.html`

Content notes
- Rating shows the Google Business listing figure (4.6, 62 reviews, checked 2026-10-08).
  Update it in `pages/home.html` and `assets/js/i18n.js` when it changes.
- No patient testimonials are published unless they are real, attributable reviews.
- Do not add the Meta/Facebook pixel to study or contact pages.
