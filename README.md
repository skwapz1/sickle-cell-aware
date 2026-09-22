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
| `index.html` | The site (entry point, for GitHub Pages) |
| `Sickle Cell Aware.dc.html` | Source of truth — edit this |
| `support.js` | Runtime required by both |
| `assets/` | Images, self-hosted fonts (`fonts/`) and React (`vendor/`) |
| `Homepage A.dc.html`, `Homepage B.dc.html` | Early design explorations, kept for reference |
| `404.html` | GitHub Pages only — has no server-side rewrite, so a direct hit on a deep route (e.g. `/donate`) 404s. This stashes the intended route and bounces back to `index.html`, which restores it. Not needed on Render. |
| `_redirects` | Render only — rewrites every path to `index.html` (200) so the client-side router can take over. Not used by GitHub Pages. |

`index.html` is a copy of `Sickle Cell Aware.dc.html`. After editing the source, re-copy it over `index.html` (and `404.html`, if editing routes).

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
