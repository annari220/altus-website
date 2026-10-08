# altusresearch.com

Static site for Altus Clinical Research, built from the Claude Design "Altus - Bold"
pages with content migrated from the WordPress site (Oct 2026). Hosted on GitHub Pages.

## Editing

- Studies, areas, team, sponsor facility list, redirects: `tools/content.py`
- Homepage layout: `pages/home.html`
- Blog posts: `content/articles/*.html` (+ metadata in `content/articles.json`)
- Shared header/footer: `tools/partials/`
- Styles: `assets/css/site.css`; Spanish text: `assets/js/i18n.js` and `tools/i18n_extra.py`

Then run `python3 tools/build.py` and commit. The build writes every page's `index.html`,
`404.html` (which forwards old WordPress-only URLs), `sitemap.xml` and `robots.txt`.

## Content rules

- Old WordPress URLs are kept as real pages wherever possible; everything else is listed in
  `REDIRECTS` in `tools/content.py`.
- Images and PDFs keep their original `/wp-content/uploads/...` paths.
- Rating shown is the Google listing figure (4.6, 62 reviews, checked 2026-10-08).
- No invented testimonials. No Meta/Facebook pixel on study or contact pages.
- Patient inquiries must go to a HIPAA-covered service (Microsoft Forms in Altus's Microsoft 365).
  Paste its embed URL into `FORM_EMBED_URL` in `tools/content.py`.
