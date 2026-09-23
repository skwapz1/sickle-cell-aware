# Sickle Cell Sense

A plain-English sickle cell education website for **Kwapong Health CIC** (Community Interest Company no. 17271036).

## Pages

Home, About sickle cell, Know your trait, Donate, About us, Contact, Privacy — all client-side routed in a single file, with real per-page URLs via the History API (`/donate`, `/about-sickle-cell`, etc).

Features: trait inheritance calculator, awareness quiz (3 random questions from a pool of 15, on the home page), a myth-or-fact section (3 random entries from a bank of 26, each sourced to the NHS, NHS England or NICE), expandable FAQ with NHS and gov.uk sources, and a donation flow (one-off/monthly, preset and custom amounts).

## Running it

No build step. Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server
```

## Files

| File | Purpose |
| --- | --- |
| `Sickle Cell Aware.dc.html` | Source of truth — edit this |
| `index.html`, `about-sickle-cell.html`, `know-your-trait.html`, `donate.html`, `about-us.html`, `contact.html`, `privacy.html` | One real file per route, generated from the source — see below |
| `generate-routes.py` | Regenerates all seven files above, plus `sitemap.xml`, from the source. Run after every edit to the source. |
| `support.js` | Runtime required by every route file |
| `assets/` | Images, self-hosted fonts (`fonts/`), React (`vendor/`) and the favicon/app-icon set (`icons/`) |
| `site.webmanifest` | Web app manifest (name, theme color, icons) — lets the site be "added to home screen" with a proper icon |
| `robots.txt`, `sitemap.xml` | SEO basics. `sitemap.xml` is generated — don't hand-edit it. |
| `Homepage A.dc.html`, `Homepage B.dc.html` | Early design explorations, kept for reference |
| `404.html` | GitHub Pages only — has no server-side rewrite, so a direct hit on a deep route (e.g. `/donate`) 404s. This stashes the intended route and bounces back to `index.html`, which restores it. Not needed on Render. |
| `_redirects` | Render only. Each real route maps to its own generated file (so crawlers get that route's actual title/description); anything else falls back to `index.html` for the client-side router. Not used by GitHub Pages. |

### Why seven files instead of one

This is a client-routed single-page app — historically a single `index.html` served every URL, and JavaScript swapped the content after load. The problem: a crawler that doesn't run JavaScript (most search engines, and link-preview bots like WhatsApp's) only ever sees whatever the server handed it for that exact URL. Serving `index.html` for every route meant `/donate`, `/about-sickle-cell` etc. all showed the *homepage's* title, description and social-preview image to anything that didn't execute JS.

`generate-routes.py` fixes this by producing one real HTML file per route — each is byte-identical to the source except for its `<head>`'s crawler-visible tags (title, meta description, canonical URL, Open Graph/Twitter tags, and JSON-LD) and `_redirects` routes each URL to its matching file. The app itself, and how people actually navigate the site, is completely unchanged — this only affects what a server-side crawler sees on the very first hit.

**Never hand-edit any of the seven HTML files except the source.** After changing `Sickle Cell Aware.dc.html`, run:

```
python3 generate-routes.py
```

This overwrites `index.html`, the six route files, and `sitemap.xml`. Commit all of them together.

## SEO / AEO

- **Per-route metadata** (see above) — each route has its own accurate title, description, canonical URL and social-preview tags.
- **JSON-LD structured data**: every page carries `NGO` (organisation) schema; the About sickle cell page additionally carries `FAQPage` schema for its six sourced FAQs. This helps both traditional search and AI answer engines (ChatGPT, Perplexity, Google AI Overviews) understand and accurately cite the site — note that Google's *rich-result* eligibility for FAQPage is currently restricted to certain site types, so this is about machine understanding generally, not a guaranteed search snippet.
- **`robots.txt` / `sitemap.xml`**: both new — previously the site had neither, so crawlers had no guided discovery of the seven routes.

## Third-party requests

Fonts (Bricolage Grotesque and Outfit, SIL Open Font License) and React 18.3.1 are self-hosted from `assets/`. `window.__resources` in the page head points `support.js` at the local React files, whose hashes match the pinned SRI values in `support.js`.

The one exception is **Google Analytics** (`gtag.js`, measurement ID `G-0GBTRDHRVG`) — but it is consent-gated, not loaded unconditionally. `window.__loadGA()` (defined in `<head>`) only injects the real `gtag.js` script after the visitor accepts the cookie banner (`#sca-cookie-banner`, first script after `<body>`). Rejecting, or not deciding, means the Google script never loads at all — no cookie is set. The choice is stored in `localStorage['sca_consent']` and can be reopened any time via "Cookie preferences" in the footer, which calls `window.__scaReopenCookieBanner()`. This satisfies UK PECR/GDPR's requirement for consent *before* non-essential cookies are set. If you add any further analytics, embeds or a CDN, update the privacy notice first and gate it behind the same consent mechanism rather than adding a second banner.

## Accessibility

Navigation and CTAs are real `<a href>` links, actions are `<button>`s, the FAQ uses `aria-expanded`, and focus moves to `<main>` on each page change. Keep it that way when adding UI: never use a clickable `<div>`.

## GitHub Pages

Settings → Pages → Deploy from branch → `main` / root.

## Still to replace before going live

- No contact email is live yet. `CONTACT_EMAIL` at the top of the script still holds a placeholder, but the contact page and privacy notice no longer display it — once there's a monitored address, set it there and reinstate the email card in the contact page and the "reach us" line in the privacy notice
- Donation buttons now use **live-mode** Stripe Payment Links (as of 22 September 2026), so real charges are made — double-check amounts before promoting the donate page
- Photography placeholders throughout

## Note on Gift Aid

A CIC is not a charity and cannot claim Gift Aid, so no Gift Aid option appears on the donation form. Don't add one without registering as a charity first.

## Medical disclaimer

Health information on this site is general awareness content, not medical advice. Sources are linked to the NHS and gov.uk where claims are made.
