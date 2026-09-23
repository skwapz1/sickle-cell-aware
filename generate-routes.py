#!/usr/bin/env python3
"""
Regenerates index.html and the per-route static HTML files from the single
source of truth, "Sickle Cell Aware.dc.html".

Why this exists: the site is a client-routed single-page app, but crawlers
that don't run JavaScript (search engines, WhatsApp, many AI/answer-engine
bots) only ever see whichever file the server hands them for a given URL.
Serving the same index.html for every route means every route shows the
homepage's title/description to those crawlers. This script produces one
real HTML file per route, each byte-identical to the source except for its
<head>'s crawler-visible tags (title, description, canonical, OG/Twitter
tags) and its injected JSON-LD, so every route is accurately described.
_redirects then routes each URL to its matching file before falling back
to index.html for anything else.

Run this after editing "Sickle Cell Aware.dc.html". It overwrites
index.html and the route .html files listed below; nothing else.
"""
import json
import re

SOURCE = "Sickle Cell Aware.dc.html"
SITE = "https://www.sicklecellsense.org"

HOME_TITLE = "Sickle Cell Sense | Kwapong Health CIC"
HOME_DESC_LONG = "Clear, honest answers about sickle cell for young people and families in the UK. Learn about sickle cell, check your trait, and support Kwapong Health CIC."
HOME_DESC_SHORT = "Clear, honest answers about sickle cell for young people and families in the UK."
HOME_URL = SITE + "/"

ROUTES = [
    {
        "key": "home",
        "file": "index.html",
        "path": "/",
        "title": HOME_TITLE,
        "desc": HOME_DESC_LONG,
        "og_desc": HOME_DESC_SHORT,
    },
    {
        "key": "about",
        "file": "about-sickle-cell.html",
        "path": "/about-sickle-cell",
        "title": "About sickle cell | Sickle Cell Sense",
        "desc": "What sickle cell disorder actually is, in plain English: symptoms, genotypes, what can trigger a crisis, and answers to the questions people search for most, sourced to the NHS and NICE.",
        "og_desc": "What sickle cell disorder actually is, in plain English: symptoms, crisis triggers, and NHS/NICE-sourced answers to common questions.",
        "faq": True,
    },
    {
        "key": "trait",
        "file": "know-your-trait.html",
        "path": "/know-your-trait",
        "title": "Know your trait | Sickle Cell Sense",
        "desc": "Find out if you carry sickle cell trait with a free NHS blood test, and use our inheritance calculator to see the odds for your children if you and your partner both carry it.",
        "og_desc": "One blood test, free on the NHS. Use our inheritance calculator to see the odds for your children.",
    },
    {
        "key": "donate",
        "file": "donate.html",
        "path": "/donate",
        "title": "Donate | Sickle Cell Sense",
        "desc": "Support Kwapong Health CIC, a newly formed Community Interest Company working on practical support, awareness and community for people living with sickle cell across the UK.",
        "og_desc": "Help Kwapong Health CIC get its work off the ground: practical support, awareness and community for people living with sickle cell.",
    },
    {
        "key": "org",
        "file": "about-us.html",
        "path": "/about-us",
        "title": "About us | Sickle Cell Sense",
        "desc": "Kwapong Health CIC is a Community Interest Company supporting young people with sickle cell and their families across the UK, working on practical support, awareness and belonging.",
        "og_desc": "A Community Interest Company supporting young people with sickle cell and their families across the UK.",
    },
    {
        "key": "contact",
        "file": "contact.html",
        "path": "/contact",
        "title": "Contact | Sickle Cell Sense",
        "desc": "Get in touch with Kwapong Health CIC, the Community Interest Company behind Sickle Cell Sense.",
        "og_desc": "Get in touch with Kwapong Health CIC, the Community Interest Company behind Sickle Cell Sense.",
    },
    {
        "key": "privacy",
        "file": "privacy.html",
        "path": "/privacy",
        "title": "Privacy notice | Sickle Cell Sense",
        "desc": "How Sickle Cell Sense and Kwapong Health CIC collect, use and protect your personal data, including our use of Google Analytics and Stripe.",
        "og_desc": "How Sickle Cell Sense and Kwapong Health CIC collect, use and protect your personal data.",
    },
    {
        "key": "terms",
        "file": "terms.html",
        "path": "/terms",
        "title": "Terms and conditions | Sickle Cell Sense",
        "desc": "The terms and conditions for using the Sickle Cell Sense website and making a donation to Kwapong Health CIC.",
        "og_desc": "The terms and conditions for using the Sickle Cell Sense website and making a donation to Kwapong Health CIC.",
    },
]

FAQS = [
    ("Is sickle cell contagious?",
     "No. It is entirely genetic, passed from parents to child through haemoglobin genes. You cannot catch it from someone, give it to someone, or develop it later in life. A child inherits one haemoglobin gene from each parent: two sickle genes means sickle cell disease, one means they carry the trait and are healthy. Nothing either parent did caused it."),
    ("Can it be cured?",
     "For most people it is managed rather than cured, but that is changing. A stem cell transplant can be curative where a matched donor is available. Since January 2025 the NHS in England also offers a one-off gene-editing therapy, exa-cel (Casgevy), to people aged 12 and over who have recurrent sickle cell crises and would be suitable for a stem cell transplant but have no available donor. In the trial, researchers reported a 'functional cure' in 96.6% of participants who received it. It is not suitable or available for everyone, so speak to your specialist team about whether you are eligible."),
    ("Should my child be tested?",
     "In the UK every newborn is offered blood spot screening at around five days old, and sickle cell is one of the conditions it looks for, so most children born here are already screened. If your child was born abroad, or you are unsure whether the result was ever explained to you, ask your GP. Older children and adults can be tested at any age with a single blood sample. It is worth doing before starting a family, because two carriers have a one in four chance of a child with sickle cell disease in every pregnancy."),
    ("What should I do during a crisis?",
     "Start early rather than waiting to see if it passes. Take your prescribed pain relief at the first sign, drink plenty of fluids, keep warm and rest. Many people manage milder crises at home with a written care plan agreed with their team. Go to hospital if the pain is not controlled, or straight away if there is a fever, chest pain, breathlessness, sudden weakness, severe headache or a change in vision. On arrival, say clearly that you have sickle cell disease and are in a pain crisis, and ask for your care plan to be followed. NICE says people arriving at hospital with a painful sickle cell episode should be assessed and given appropriate pain relief within 30 minutes, so it is reasonable to ask for the relief you normally need."),
    ("How is it treated day to day?",
     "Most care is about preventing crises rather than reacting to them. That usually means staying well hydrated, keeping warm, taking folic acid, keeping up with vaccinations and penicillin where prescribed, and attending annual review with a specialist team. Many people take hydroxyurea, a daily medicine that reduces how often crises happen. Some have regular blood transfusions. Children are offered scans to check the risk of stroke. None of this is optional extra: consistent routine care is what protects organs over a lifetime."),
    ("What should a school or employer know?",
     "That sickle cell is a fluctuating condition, not a run of unexplained absences. Practical adjustments make a real difference: easy access to water and the toilet, staying warm, avoiding sudden temperature changes, rest after exertion, catching up on missed work without penalty, and flexibility around hospital appointments. In the UK, sickle cell disease is generally treated as a disability under the Equality Act 2010, so reasonable adjustments are a legal duty rather than a favour. As we grow, we hope to support schools and employers directly."),
]

ORG_JSONLD = {
    "@context": "https://schema.org",
    "@type": "NGO",
    "name": "Sickle Cell Sense",
    "alternateName": "Kwapong Health CIC",
    "legalName": "Kwapong Health CIC",
    "url": HOME_URL,
    "logo": SITE + "/assets/og-image.png",
    "description": HOME_DESC_SHORT,
    "areaServed": "GB",
    "location": {"@type": "Place", "address": {"@type": "PostalAddress", "addressCountry": "GB"}},
}


def faq_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQS
        ],
    }


def jsonld_script(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def main():
    with open(SOURCE, "r", encoding="utf-8") as f:
        src = f.read()

    assert src.count(f"<title>{HOME_TITLE}</title>") == 2
    assert src.count(f'<meta name="description" content="{HOME_DESC_LONG}" />') == 2
    assert src.count(f'<link rel="canonical" href="{HOME_URL}" />') == 1
    assert src.count(f'<meta property="og:url" content="{HOME_URL}" />') == 2
    assert src.count(f'<meta property="og:title" content="{HOME_TITLE}" />') == 2
    assert src.count(f'<meta property="og:description" content="{HOME_DESC_SHORT}" />') == 2
    assert src.count(f'<meta name="twitter:title" content="{HOME_TITLE}" />') == 1
    assert src.count(f'<meta name="twitter:description" content="{HOME_DESC_SHORT}" />') == 1
    assert src.count("</head>") == 1

    for route in ROUTES:
        out = src
        url = SITE + route["path"] if route["path"] != "/" else HOME_URL
        out = out.replace(f"<title>{HOME_TITLE}</title>", f'<title>{route["title"]}</title>')
        out = out.replace(
            f'<meta name="description" content="{HOME_DESC_LONG}" />',
            f'<meta name="description" content="{route["desc"]}" />',
        )
        out = out.replace(f'<link rel="canonical" href="{HOME_URL}" />', f'<link rel="canonical" href="{url}" />')
        out = out.replace(f'<meta property="og:url" content="{HOME_URL}" />', f'<meta property="og:url" content="{url}" />')
        out = out.replace(
            f'<meta property="og:title" content="{HOME_TITLE}" />',
            f'<meta property="og:title" content="{route["title"]}" />',
        )
        out = out.replace(
            f'<meta property="og:description" content="{HOME_DESC_SHORT}" />',
            f'<meta property="og:description" content="{route["og_desc"]}" />',
        )
        out = out.replace(
            f'<meta name="twitter:title" content="{HOME_TITLE}" />',
            f'<meta name="twitter:title" content="{route["title"]}" />',
        )
        out = out.replace(
            f'<meta name="twitter:description" content="{HOME_DESC_SHORT}" />',
            f'<meta name="twitter:description" content="{route["og_desc"]}" />',
        )

        jsonld_blocks = [jsonld_script(ORG_JSONLD)]
        if route.get("faq"):
            jsonld_blocks.append(jsonld_script(faq_jsonld()))
        out = out.replace("</head>", "\n".join(jsonld_blocks) + "\n</head>")

        with open(route["file"], "w", encoding="utf-8") as f:
            f.write(out)
        print("wrote", route["file"])

    sitemap_urls = "\n".join(
        f"  <url><loc>{SITE + r['path'] if r['path'] != '/' else HOME_URL}</loc></url>" for r in ROUTES
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_urls}\n"
        "</urlset>\n"
    )
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
