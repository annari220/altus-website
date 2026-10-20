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
- Patient inquiries must go to a HIPAA-covered service. The contact form posts to a Power Automate
  flow in Altus's Microsoft 365 (covered by Microsoft's HIPAA BAA), never to a third-party form service.

## Volunteer form

The form on `/contact-us/` (layout from the Claude Design "Altus - Bold" Contact screen) sends each
inquiry to a Power Automate flow, which emails the coordinators from Altus's Microsoft 365.
Its URL lives in `FORM_FLOW_URL` in `tools/content.py`. While that is empty the form opens the
visitor's own email app with their details addressed to `INQUIRY_EMAIL`, and they press Send there.
The same happens if the flow ever fails (for example the Premium trial ends), so no inquiry is lost.

Setting up the flow (once, signed in with an Altus Microsoft 365 account; the web trigger is a
Power Automate **Premium** feature, so that account needs a Premium license or trial):

1. make.powerautomate.com → **Create** → **Instant cloud flow** → trigger
   **When an HTTP request is received**. Name it "Website volunteer inquiries".
2. In the trigger set **Who can trigger the flow?** to **Anyone**. Leave the JSON schema empty:
   the site sends plain form data, not JSON.
3. Add **Send an email (V2)** (Office 365 Outlook).
   - **To:** `info@altusresearch.com` and anyone else who should get inquiries
   - **Subject:** `Volunteer inquiry: @{triggerFormDataValue('area')} - @{triggerFormDataValue('first')} @{triggerFormDataValue('last')}`
   - **Body:** one line per field: `first`, `last`, `phone`, `email`, `area`, `message`, `language`,
     each as `@{triggerFormDataValue('phone')}` and so on. If pasting `@{...}` doesn't turn into a
     token, add it with the **fx** (expression) button as `triggerFormDataValue('phone')`.
   - **Reply To** (advanced parameters): `@{triggerFormDataValue('email')}` so a reply goes to the volunteer.
4. Add **Response**: status code `200`, header `Access-Control-Allow-Origin` = `https://altusresearch.com`,
   body `{"ok":true}`. Without that header the page says "couldn't send" even though the email went out.
5. Save, copy the trigger's **HTTP URL** into `FORM_FLOW_URL`, run the build, commit and push.
6. Test on altusresearch.com/contact-us/ with obvious test details: the page should say
   "Thank you, we got your information." and the email should arrive.
