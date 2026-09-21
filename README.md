# Sickle Cell Aware

A sickle cell awareness and support website for **Kwapong Health CIC** (Community Interest Company no. 17271036).

## Pages

Home, About sickle cell, Know your trait, Donate, About us, Contact — all client-side routed in a single file, with real per-page URLs via the History API (`/donate`, `/about-sickle-cell`, etc).

Features: trait inheritance calculator, awareness quiz (3 random questions from a pool of 15, on the home page), expandable FAQ with NHS and gov.uk sources, and a donation flow (one-off/monthly, preset and custom amounts).

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
| `assets/` | Images |
| `Homepage A.dc.html`, `Homepage B.dc.html` | Early design explorations, kept for reference |
| `404.html` | GitHub Pages only — has no server-side rewrite, so a direct hit on a deep route (e.g. `/donate`) 404s. This stashes the intended route and bounces back to `index.html`, which restores it. Not needed on Render. |
| `_redirects` | Render only — rewrites every path to `index.html` (200) so the client-side router can take over. Not used by GitHub Pages. |

`index.html` is a copy of `Sickle Cell Aware.dc.html`. After editing the source, re-copy it over `index.html` (and `404.html`, if editing routes).

## GitHub Pages

Settings → Pages → Deploy from branch → `main` / root.

## Still to replace before going live

- `hello@kwaponghealth.org` is a placeholder email address
- Donation buttons are wired to Stripe Payment Links in **test mode** — switch to live-mode Products/Prices/Payment Links before accepting real donations (see the donate footnote, which says "Test mode" until then)
- Photography placeholders throughout

## Note on Gift Aid

A CIC is not a charity and cannot claim Gift Aid, so no Gift Aid option appears on the donation form. Don't add one without registering as a charity first.

## Medical disclaimer

Health information on this site is general awareness content, not medical advice. Sources are linked to the NHS and gov.uk where claims are made.
