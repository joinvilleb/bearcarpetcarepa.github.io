#!/usr/bin/env python3
"""Generates every HTML page for bearcarpetcare.com.

The site is plain static HTML, but the header, footer, call bar, icon
sprite and business facts are identical on nine pages. Keeping them in one
place is why the phone number, hours and service area can no longer drift
apart the way bearcarpetcare.com and carpetcleanerharrisburg.com did.

Edit the data below, then:  python3 build-pages.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SITE = "https://bearcarpetcare.com"
TODAY = "2026-10-01"

# ---------------------------------------------------------------- facts
BIZ = {
    "name": "Bear Carpet Care",
    "phone_display": "(717) 454-7347",
    "phone_href": "tel:+17174547347",
    "phone_schema": "+1-717-454-7347",
    "email": "bearcarpetcarepa@gmail.com",
    "city": "Harrisburg",
    "region": "PA",
    "zip": "17112",
    "lat": 40.2732,
    "lng": -76.8867,
    "years": "30+",
    "hours_text": "Mon–Fri 8am–7pm · Sat 10am–3pm · Sun 11am–3pm",
}

HOURS = [("Mon – Fri", "8am – 7pm"), ("Saturday", "10am – 3pm"), ("Sunday", "11am – 3pm")]

HOURS_SCHEMA = [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
     "opens": "08:00", "closes": "19:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "15:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "11:00", "closes": "15:00"},
]

AREAS = ["Harrisburg", "Carlisle", "Hershey", "Lancaster", "Lebanon", "York"]

SOCIALS = [
    ("facebook", "Facebook", "https://www.facebook.com/profile.php?id=61577586021295"),
    ("instagram", "Instagram", "https://www.instagram.com/bearcarpetcare/"),
    ("tiktok", "TikTok", "https://www.tiktok.com/@bearcarpetcare"),
    ("youtube", "YouTube", "https://www.youtube.com/@BearCarpetCare"),
    ("yelp", "Yelp", "https://www.yelp.com/biz/bear-carpet-care-harrisburg"),
    ("google", "Google", "https://maps.app.goo.gl/8CSvEHzdW2A2sdau7"),
]

NAV = [
    ("Home", "index.html", None),
    ("Services", None, [("Carpet Cleaning", "carpet-cleaning.html"),
                        ("Upholstery Cleaning", "upholstery-cleaning.html"),
                        ("Rug Cleaning", "oriental-rug-cleaning.html")]),
    ("Pricing", "index.html#pricing", None),
    ("Reviews", "reviews.html", None),
    ("Gallery", "gallery.html", None),
    ("Contact", "contact.html", None),
]

# Prices as advertised on carpetcleanerharrisburg.com.
PRICES = [
    dict(name="2 Rooms", amount="79.95", unit="up to 250 sq ft",
         notes=["Hot-water extraction", "Deodorising included", "Stairs quoted separately"], feature=False),
    dict(name="4 Rooms", amount="149.95", unit="up to 500 sq ft",
         notes=["Hot-water extraction", "Deodorising included", "Best value per room"], feature=True),
    dict(name="Upholstery", amount="39.95", unit="from, per chair",
         notes=["Sofa $79.95", "Love seat $59.95", "Chair $39.95"], feature=False),
    dict(name="Oriental Rugs", amount="15", unit="% off", currency=False,
         notes=["Free pick-up and delivery", "Cleaned at our facility", "Repairs quoted separately"], feature=False),
]

# Transcribed verbatim from the Google reviews shown on
# carpetcleanerharrisburg.com/testimonials. Do not paraphrase these: they are
# attributed to named people. `short` marks the ones used on the home page.
REVIEWS = [
    ("Celeste Chicoine", "2025-07-24", True,
     "Bear Carpet Care did a great job for us. They were very nice and care about the work they do. They were very thorough. We would definitely use them again"),
    ("gary barnes", "2025-07-09", True,
     "The job they did was INCREDIBLE. With having six dogs our carpets were in BAD shape and now they look brand new. We highly recommend this company!"),
    ("Julie Myers", "2025-07-17", True,
     "This was first time using Bear Carpet Care. Carpets look great and smell fresh! Great job! Appreciate your hard work in getting out stains too!"),
    ("Jen", "2025-07-08", True,
     "Dave was quick to respond and set up an appointment. He arrived early and went over my options. He was super quick, professional and reasonably priced!"),
    ("Bertie Spalding", "2025-07-19", False,
     "I picked this business after Googling for a professional cleaning of a house I was purchasing. Quick call back, met, measured, agreed on price, whole house cleaned &amp; scotchguarded today while I sat on the front porch. Very friendly! Highly recommend!"),
    ("Mor Ovadia", "2025-07-21", False,
     "Hey These guys were just great. They cleaned my chairs, my couch and picked up my 8x11 oriental rug to clean. They were Very good. I was very happy with the service. I will recommend them to my family and friends."),
    ("E E", "2025-07-10", False,
     "Thanks, Dave &amp; Corey! Carpet looks great! Thank you for the time you spent working on those oil stains! There all gone! Excellent work! We highly recommend Bear Carpet Care."),
    ("Francis family", "2025-07-15", False,
     "We had an amazing experience with this family-owned carpet cleaning company! They cleaned all our carpets and stairs, and the results were outstanding. Every stain and pet odor we were worried about is completely gone \u2014 it looks and smells like new again! The team was professional, friendly, and clearly took pride in their work. It\u2019s refreshing to find a company that truly cares about quality and customer satisfaction. Highly recommend them to anyone needing carpet or upholstery cleaning. We\u2019ll definitely be using them again!"),
    ("Lauren", "2025-07-05", False,
     "They were very professional and efficient, and they did a great job cleaning out the carpets in our bedrooms before we moved into our house. The carpets looked and smelled great afterwards, and I will definitely use them in the future for steam cleaning carpets and rugs."),
    ("Marisa Francis", "2025-07-01", False,
     "Professional and quick. We have 2 dogs and 4 cats so needless to say, regular carpet cleaning is required. First time using Bear Carpetcare and we will use them again. Highly recommend!"),
    ("Roni C.", "2025-06-03", False,
     "Dave did an amazing job cleaning the carpets in two rooms and the steps in my home. He was professional, on time, and super friendly. The carpets look brand new and smell fresh, and he took extra care to make sure everything was done right. You can tell he really takes pride in his work. I highly recommend Dave if you\u2019re looking for quality carpet cleaning and great service!"),
]

SPRITE = (ROOT / "_sprite.html").read_text().strip()

# Header photo for each inner page. Generated at 960 and 1600 wide.
PAGE_PHOTO = {
    "carpet-cleaning.html": "ph-carpet",
    "upholstery-cleaning.html": "ph-upholstery",
    "oriental-rug-cleaning.html": "ph-rug",
    "reviews.html": "ph-reviews",
    "gallery.html": "ph-gallery",
    "contact.html": "ph-contact",
}


# ---------------------------------------------------------------- helpers
def icon(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>'


def photo_preload(name):
    """Preload for a full-width photo served at 960 and 1600 wide."""
    return [dict(href=f"img/{name}-1600.webp",
                 srcset=f"img/{name}-960.webp 960w, img/{name}-1600.webp 1600w", sizes="100vw")]


def head(page):
    """<head> for one page."""
    pre = ""
    for p in page.get("preload", []):
        attrs = f' href="{p["href"]}"'
        if p.get("srcset"):
            attrs += f' imagesrcset="{p["srcset"]}" imagesizes="{p["sizes"]}"'
        if p.get("media"):
            attrs += f' media="{p["media"]}"'
        pre += f'\n    <link rel="preload" as="image"{attrs} fetchpriority="high">'
    extra = "".join(f"\n{s}" for s in page.get("head_extra", []))
    return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{page['title']}</title>
    <meta name="description" content="{page['desc']}">
    <link rel="canonical" href="{SITE}/{page['slug']}">
    <meta name="robots" content="{page.get('robots', 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1')}">
    <meta name="theme-color" content="#0d4671">
    <meta name="author" content="{BIZ['name']}">
    <meta name="geo.region" content="US-PA">
    <meta name="geo.placename" content="{BIZ['city']}">
    <meta name="geo.position" content="{BIZ['lat']};{BIZ['lng']}">
    <meta name="ICBM" content="{BIZ['lat']}, {BIZ['lng']}">

    <meta property="og:type" content="website">
    <meta property="og:url" content="{SITE}/{page['slug']}">
    <meta property="og:title" content="{page['title']}">
    <meta property="og:description" content="{page['desc']}">
    <meta property="og:image" content="{SITE}/img/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="{BIZ['name']}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page['title']}">
    <meta name="twitter:description" content="{page['desc']}">
    <meta name="twitter:image" content="{SITE}/img/og-image.jpg">

    <link rel="icon" href="img/favicon-32.png" sizes="32x32" type="image/png">
    <link rel="apple-touch-icon" href="img/apple-touch-icon.png">
    <link rel="preload" href="fonts/league-spartan-latin-var.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="fonts/questrial-latin.woff2" as="font" type="font/woff2" crossorigin>{pre}
    <link rel="stylesheet" href="css/site.min.css">
    <script>(function(d){{d.classList.add("js");setTimeout(function(){{if(!window.bccReady)d.classList.remove("js")}},3000)}})(document.documentElement)</script>
{page['schema']}{extra}
</head>
"""


def brand(sub):
    return (f'<a href="index.html" class="brand"><img src="img/logo-220.webp" alt="" width="58" height="58">'
            f'<span><b>{BIZ["name"]}</b><small>{sub}</small></span></a>')


def header(active):
    items = []
    for label, href, sub in NAV:
        if sub:
            links = "".join(
                f'<li><a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{t}</a></li>'
                for t, h in sub)
            cur = ' aria-current="page"' if active in [h for _, h in sub] else ""
            items.append(
                f'<li class="has-sub"><button class="subnav-toggle" aria-expanded="false"{cur}>{label}'
                f'{icon("chev")}</button><ul class="subnav">{links}</ul></li>')
        else:
            cur = ' aria-current="page"' if href == active else ""
            items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return f"""<body>

{SPRITE}

<a href="#main" class="skip-link">Skip to main content</a>

<header class="site-header">
    <div class="wrap">
        {brand(f"{BIZ['city']}, {BIZ['region']}")}
        <nav id="nav" class="nav" aria-label="Main">
            <ul>{''.join(items)}</ul>
            <div class="nav-cta">
                <a href="{BIZ['phone_href']}" class="nav-phone"><span>{icon('phone')}</span>{BIZ['phone_display']}</a>
                <a href="contact.html" class="btn btn-teal">Free Quote</a>
            </div>
        </nav>
        <a href="{BIZ['phone_href']}" class="head-call" aria-label="Call {BIZ['phone_display']}">{icon('phone')}</a>
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span></button>
    </div>
</header>

<main id="main">
"""


FOOTER_NAV = [("Home", "index.html"), ("Carpet", "carpet-cleaning.html"),
              ("Upholstery", "upholstery-cleaning.html"), ("Rugs", "oriental-rug-cleaning.html"),
              ("Pricing", "index.html#pricing"), ("Reviews", "reviews.html"),
              ("Gallery", "gallery.html"), ("Contact", "contact.html")]


def footer(active=""):
    socs = "".join(
        f'<a href="{url}" target="_blank" rel="noopener" aria-label="{BIZ["name"]} on {label}">{icon(k)}</a>'
        for k, label, url in SOCIALS)
    links = "".join(
        f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{t}</a>'
        for t, h in FOOTER_NAV)
    return f"""</main>

<footer class="site-footer navy">
    <div class="wrap">
        {brand("Family-owned for " + BIZ["years"] + " years")}
        <nav class="footer-nav" aria-label="Footer">{links}</nav>
        <div class="footer-info">
            <a href="{BIZ['phone_href']}">{icon('handset')}{BIZ['phone_display']}</a>
            <a href="mailto:{BIZ['email']}">{icon('envelope')}{BIZ['email']}</a>
            <span>{icon('time')}{BIZ['hours_text']}</span>
        </div>
        <div class="footer-info">
            <span>{icon('marker')}Serving {', '.join(AREAS[:-1])} and {AREAS[-1]}, PA</span>
        </div>
        <div class="socials">{socs}</div>
        <div class="footer-bottom">
            &copy; <span id="year">2026</span> <a href="index.html">{BIZ['name']}</a>. All rights reserved.
            Maintained by <a href="https://webeaze.io" rel="noopener">WebEaze</a>.
        </div>
    </div>
</footer>

<div class="callbar">
    <a href="{BIZ['phone_href']}" class="btn btn-call">{icon('phone')}Call Now</a>
    <a href="contact.html" class="btn btn-teal">Free Quote</a>
</div>

<a href="#" class="to-top" aria-label="Back to top">{icon('up')}</a>

<script src="js/main.min.js" defer></script>
{{scripts}}<script src="https://portal.webeaze.io/track.js" data-key="65995a53-f1e8-4ff1-a0d4-3b15b126d1ca" defer></script>

</body>
</html>
"""


def section_head(eyebrow, title, sub=None, level="h2"):
    p = f"<p>{sub}</p>" if sub else ""
    return (f'<div class="section-head" data-reveal><span class="eyebrow">{eyebrow}</span>'
            f'<{level}>{title}</{level}>{p}</div>')


def page_head_block(eyebrow, title, crumbs, slug):
    trail = "".join(
        (f'<li><a href="{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>')
        for t, h in crumbs)
    ph = PAGE_PHOTO[slug]
    return f"""    <div class="page-head">
        <img src="img/{ph}-1600.webp" srcset="img/{ph}-960.webp 960w, img/{ph}-1600.webp 1600w" sizes="100vw"
             alt="" width="1600" height="667" fetchpriority="high">
        <div class="wrap">
            <span class="eyebrow">{eyebrow}</span>
            <h1>{title}</h1>
            <nav aria-label="Breadcrumb"><ol class="crumbs">{trail}</ol></nav>
        </div>
    </div>
"""


def pricing_block():
    cards = []
    for i, p in enumerate(PRICES):
        tag = '<span class="tag">Most booked</span>' if p["feature"] else ""
        amount = (f'<p class="amount">${p["amount"]}</p><p class="unit">{p["unit"]}</p>'
                  if p.get("currency", True)
                  else f'<p class="amount">{p["amount"]}{p["unit"]}</p><p class="unit">with free pick-up</p>')
        notes = "".join(f"<li>{n}</li>" for n in p["notes"])
        btn = "btn-teal" if p["feature"] else "btn-line"
        cards.append(f'<div class="price" data-reveal="{i + 1}">{tag}'
                     f'<h3>{p["name"]}</h3>{amount}<ul>{notes}</ul>'
                     f'<a href="contact.html" class="btn {btn}">Book Now</a></div>')
    return f"""    <section class="cream section" id="pricing">
        <div class="wrap">
            {section_head("special offers", "Straightforward Pricing", "What most jobs cost. Call for an exact figure on yours.")}
            <div class="prices">{''.join(cards)}</div>
            <p class="price-note">Prices are starting points for standard cleaning and cover the room sizes shown.
               Heavily soiled carpet, stairs, hallways and rug repairs are quoted separately, and we will always
               confirm the total before starting. Call <a href="{BIZ['phone_href']}">{BIZ['phone_display']}</a> for a firm quote.</p>
        </div>
    </section>
"""


def review_cards():
    return "".join(
        f'<figure class="review" data-reveal="{i % 3 + 1}">{icon("quote")}'
        f'<blockquote>{t}</blockquote>'
        f'<div class="stars" aria-hidden="true">★★★★★</div><span class="visually-hidden">Rated 5 out of 5</span>'
        f'<figcaption>{n}<time datetime="{d}">{d}</time></figcaption></figure>'
        for i, (n, d, _, t) in enumerate(REVIEWS))


def testimonial_slides():
    return "".join(
        f'<figure class="slide"><blockquote>{t}</blockquote>'
        f'<div class="stars" aria-hidden="true">★★★★★</div><span class="visually-hidden">Rated 5 out of 5</span>'
        f'<figcaption>{n}<time datetime="{d}">Google review</time></figcaption></figure>'
        for n, d, short, t in REVIEWS if short)


def cta(title, sub):
    return f"""    <section class="navy section on-dark cta-band">
        <div class="wrap" data-reveal>
            <span class="eyebrow">free quotes</span>
            <h2>{title}</h2>
            <p>{sub}</p>
            <div class="btn-row stack">
                <a href="contact.html" class="btn btn-teal">Get a Free Quote</a>
                <a href="{BIZ['phone_href']}" class="btn btn-white">{icon('phone')}Call {BIZ['phone_display']}</a>
            </div>
        </div>
    </section>
"""


def faq_items(qs, open_first=False):
    return "".join(
        f"<details{' open' if open_first and i == 0 else ''}><summary><h3>{q}</h3></summary>"
        f"<div class=\"answer\"><p>{a}</p></div></details>"
        for i, (q, a) in enumerate(qs))


def faq_block(qs):
    return f"""    <section class="cream section">
        <div class="wrap narrow">
            {section_head("good to know", "Frequently Asked Questions")}
            <div class="faq" data-reveal>{faq_items(qs, open_first=True)}</div>
        </div>
    </section>
"""


def contact_details():
    return f"""<ul class="contact-details">
                    <li>{icon('marker')}Based in {BIZ['city']}, {BIZ['region']} {BIZ['zip']}</li>
                    <li><a href="{BIZ['phone_href']}">{icon('handset')}<span class="big">{BIZ['phone_display']}</span></a></li>
                    <li><a href="mailto:{BIZ['email']}">{icon('envelope')}{BIZ['email']}</a></li>
                    <li>{icon('time')}{BIZ['hours_text']}</li>
                </ul>"""


FORM_ACTION = "https://gmgzhjxfypuyzzgqwona.supabase.co/functions/v1/form-lead/65995a53-f1e8-4ff1-a0d4-3b15b126d1ca"


def contact_block(details=True):
    """Contact copy and the quote form. Used on the home and contact pages."""
    return f"""    <section class="cream section" id="quote">
        <div class="wrap split top">
            <div class="split-copy" data-reveal>
                <span class="eyebrow">contact us</span>
                <h2>Have Questions? Get in Touch!</h2>
                <p class="muted">Free, no-obligation quotes across Harrisburg and Central PA.
                   Tell us what needs cleaning and we usually reply the same business day.</p>
                {contact_details() if details else ""}
            </div>
            <div data-reveal="2">
                <div id="form-status" aria-live="polite"></div>
                <form id="quote-form" class="form" novalidate method="POST" action="{FORM_ACTION}">
                    <div class="field">
                        <label for="name">{icon('user')}Your name</label>
                        <input type="text" id="name" name="name" autocomplete="name" required data-msg="Please enter your name">
                        <span class="err" id="name-err"></span>
                    </div>
                    <div class="field">
                        <label for="email">{icon('envelope')}Email address</label>
                        <input type="email" id="email" name="email" autocomplete="email" required data-msg="Please enter your email">
                        <span class="err" id="email-err"></span>
                    </div>
                    <div class="field full">
                        <label for="phone">{icon('handset')}Phone <span class="muted">(optional)</span></label>
                        <input type="tel" id="phone" name="phone" autocomplete="tel">
                        <span class="err"></span>
                    </div>
                    <div class="field full">
                        <label for="message">{icon('pencil')}What needs cleaning?</label>
                        <textarea id="message" name="message" required data-msg="Please tell us what needs cleaning"></textarea>
                        <span class="err" id="message-err"></span>
                    </div>
                    <div class="form-foot full">
                        <button type="submit" class="btn btn-teal">Get In Touch</button>
                        <p>Or call <a href="{BIZ['phone_href']}">{BIZ['phone_display']}</a></p>
                    </div>
                </form>
            </div>
        </div>
    </section>
"""


def clean_urls(out):
    """Extensionless URLs, which Cloudflare Pages serves natively (it 308s
    /page.html to /page) and GitHub Pages also resolves. Canonicals, schema
    and links all point at the final address so nothing goes via a redirect."""
    out = re.sub(rf'{re.escape(SITE)}/index\.html', f'{SITE}/', out)
    out = re.sub(rf'{re.escape(SITE)}/([a-z0-9-]+)\.html', rf'{SITE}/\1', out)
    out = re.sub(r'href="/?index\.html', 'href="/', out)
    out = re.sub(r'href="/?([a-z0-9-]+)\.html', r'href="/\1', out)
    return out


def write(slug, page, body, scripts=""):
    active = page.get("active", slug)
    out = clean_urls(head(page) + header(active) + body + footer(active).replace("{scripts}", scripts))
    (ROOT / slug).write_text(out)
    text = re.sub(r"<[^>]+>", " ", re.search(r"<main.*?</main>", out, re.S).group(0))
    return len(text.split())


# ---------------------------------------------------------------- schema
def ld(*nodes):
    import json
    graph = {"@context": "https://schema.org", "@graph": [n for n in nodes if n]}
    return ('    <script type="application/ld+json">\n'
            + json.dumps(graph, indent=2, ensure_ascii=False) + "\n    </script>")


def business():
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": f"{SITE}/#business",
        "name": BIZ["name"],
        "url": f"{SITE}/",
        "logo": f"{SITE}/img/bearcarpetcare-logo.jpg",
        "image": f"{SITE}/img/og-image.jpg",
        "telephone": BIZ["phone_schema"],
        "email": BIZ["email"],
        "description": ("Family-owned carpet, upholstery and oriental rug cleaning company serving "
                        "Harrisburg, Pennsylvania and Central PA. Over 30 years of experience using "
                        "non-toxic, hypoallergenic solutions that are safe for children and pets."),
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "paymentAccepted": "Cash, Check, Credit Card",
        "address": {"@type": "PostalAddress", "addressLocality": BIZ["city"],
                    "addressRegion": BIZ["region"], "postalCode": BIZ["zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "areaServed": [{"@type": "City", "name": a,
                        "containedInPlace": {"@type": "State", "name": "Pennsylvania"}} for a in AREAS],
        "openingHoursSpecification": HOURS_SCHEMA,
        "sameAs": [u for _, _, u in SOCIALS],
        "knowsAbout": ["Carpet cleaning", "Hot water extraction", "Upholstery cleaning",
                       "Oriental rug cleaning", "Area rug repair", "Pet stain and odour removal",
                       "Scotchgard fabric protection"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Cleaning services",
            "itemListElement": [
                {"@type": "Offer", "name": "Carpet cleaning, 2 rooms up to 250 sq ft",
                 "price": "79.95", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Carpet Cleaning",
                                 "url": f"{SITE}/carpet-cleaning.html"}},
                {"@type": "Offer", "name": "Carpet cleaning, 4 rooms up to 500 sq ft",
                 "price": "149.95", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Carpet Cleaning",
                                 "url": f"{SITE}/carpet-cleaning.html"}},
                {"@type": "Offer", "name": "Sofa cleaning", "price": "79.95", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Upholstery Cleaning",
                                 "url": f"{SITE}/upholstery-cleaning.html"}},
                {"@type": "Offer", "name": "Love seat cleaning", "price": "59.95", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Upholstery Cleaning",
                                 "url": f"{SITE}/upholstery-cleaning.html"}},
                {"@type": "Offer", "name": "Chair cleaning", "price": "39.95", "priceCurrency": "USD",
                 "itemOffered": {"@type": "Service", "name": "Upholstery Cleaning",
                                 "url": f"{SITE}/upholstery-cleaning.html"}},
                {"@type": "Offer", "name": "Oriental and area rug cleaning, 15% off with free pick-up and delivery",
                 "itemOffered": {"@type": "Service", "name": "Oriental and Area Rug Cleaning",
                                 "url": f"{SITE}/oriental-rug-cleaning.html"}},
            ]},
    }


def website():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
            "name": BIZ["name"], "publisher": {"@id": f"{SITE}/#business"}, "inLanguage": "en-US"}


def webpage(slug, name, types=("WebPage",), faqs=None, about=None, speakable=True):
    node = {"@type": list(types), "@id": f"{SITE}/{slug}#webpage",
            "url": f"{SITE}/{slug}", "name": name,
            "isPartOf": {"@id": f"{SITE}/#website"},
            "about": {"@id": about or f"{SITE}/#business"},
            "inLanguage": "en-US", "dateModified": TODAY}
    if speakable:
        node["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".hero p", ".lead"]}
    if faqs:
        node["mainEntity"] = [{"@type": "Question", "name": html.unescape(q),
                               "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r"<[^>]+>", "", a))}}
                              for q, a in faqs]
    return node


def crumbs_ld(slug, trail):
    return {"@type": "BreadcrumbList", "@id": f"{SITE}/{slug}#breadcrumb",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t,
                                 "item": f"{SITE}/{h}" if h else f"{SITE}/{slug}"}
                                for i, (t, h) in enumerate(trail)]}


def service_ld(slug, name, stype, desc, offers=None):
    node = {"@type": "Service", "@id": f"{SITE}/{slug}#service", "name": name,
            "serviceType": stype, "description": desc,
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": [{"@type": "City", "name": a} for a in AREAS]}
    if offers:
        node["offers"] = offers
    return node


# ---------------------------------------------------------------- services
SERVICES = {
"carpet-cleaning.html": dict(
  nav="Carpet Cleaning",
  eyebrow="wall-to-wall, stairs &amp; pet stains",
  h2="Deep Cleaning for Every Room",
  h1="Carpet Cleaning in Harrisburg, PA",
  title="Carpet Cleaning in Harrisburg, PA | Bear Carpet Care",
  desc="Carpet cleaning in Harrisburg, PA from $79.95 for two rooms. Hot-water extraction, stain and pet-odour removal, Scotchgard. Call (717) 454-7347.",
  head_class="head-carpet",
  preload=[("img/hdr-carpet-960.webp", "(max-width: 991px)"), ("img/hdr-carpet-1920.webp", "(min-width: 992px)")],
  lead="We deep clean wall-to-wall carpet, stairs and hallways across Harrisburg and Central PA, and treat spots, stains and pet odours. <strong>Two rooms from $79.95.</strong>",
  stats=[("Typical room","20–30 min"),("Whole home","2–4 hours"),("Dry time","6–12 hours"),("From","$79.95")],
  included=["Wall-to-wall carpet","Hot-water extraction","Spot and stain removal","Pet odour treatment",
            "Stairs and hallways","Sanitising and deodorising","Scotchgard&reg; protection","Pre-conditioning for heavy soil"],
  band=("carpet-cleaning-3", 1280, 864, "Hot-water extraction on a living room carpet",
        "Bear Carpet Care cleaning a living room carpet in Harrisburg, PA"),
  steps=[("We look first","Fibre type, traffic patterns and problem spots get checked before anything is switched on."),
         ("Pre-treat the trouble","Heavy soil, spots and pet areas are treated on their own so the main pass is not doing all the work."),
         ("Hot-water extraction","Solution goes in hot and comes straight back out, taking the dirt and the residue with it."),
         ("Protect and dry","Optional Scotchgard&reg;, then airflow so you are walking on it in a few hours.")],
  notes=[("leaf","Non-toxic throughout","Self-neutralising, biodegradable solutions. Hypoallergenic and safe around children and pets on every job."),
         ("paw","Pet odour at the source","Surface cleaning does not fix it. We locate the source and treat it with enzymes that neutralise odour at fibre level."),
         ("shield","Scotchgard&reg; protection","An invisible barrier that resists dirt and stains and makes routine vacuuming work harder for you.")],
  faqs=[("How often should carpets be professionally cleaned?","Most homes benefit every 12 to 18 months. With pets, children or allergies, every 6 to 12 months. Hallways and living rooms may need it sooner."),
        ("Is it safe for pets and children?","Yes. We use non-toxic, hypoallergenic, biodegradable solutions. No harsh chemicals and no residue left behind."),
        ("How long does it take?","Most rooms take 20 to 30 minutes. A whole home is usually 2 to 4 hours depending on size and condition."),
        ("How long before I can walk on it?","Two to four hours for light traffic, 6 to 12 hours to be fully dry. Opening windows or running a fan speeds it up."),
        ("Can you remove pet odours?","Yes. Enzyme treatments neutralise odour at the source rather than masking it. We find urine hotspots and treat them directly."),
        ("What does carpet cleaning cost?","Two rooms up to 250 sq ft is $79.95 and four rooms up to 500 sq ft is $149.95. Stairs, hallways and heavily soiled areas are quoted separately.")],
  cta=("Ready for cleaner carpets?","Two rooms from $79.95. Free quotes across Harrisburg and Central PA."),
  stype="Carpet Cleaning",
  sdesc="Hot-water extraction carpet cleaning, spot and stain removal, pet odour treatment and Scotchgard protection for homes in Harrisburg, PA and Central Pennsylvania.",
  offers={"@type":"Offer","price":"79.95","priceCurrency":"USD",
          "description":"Two rooms up to 250 square feet","url":f"{SITE}/carpet-cleaning.html"}),

"upholstery-cleaning.html": dict(
  nav="Upholstery Cleaning",
  eyebrow="sofas, chairs &amp; sectionals",
  h2="Furniture That Feels New Again",
  h1="Upholstery Cleaning in Harrisburg, PA",
  title="Upholstery Cleaning in Harrisburg, PA | Bear Carpet Care",
  desc="Upholstery cleaning in Harrisburg, PA. Sofas $79.95, love seats $59.95, chairs $39.95. Non-toxic and pet-safe. Call (717) 454-7347.",
  head_class="head-upholstery",
  preload=[("img/hdr-upholstery-960.webp", "(max-width: 991px)"), ("img/hdr-upholstery-1920.webp", "(min-width: 992px)")],
  lead="We steam clean sofas, sectionals, chairs, recliners and dining chairs across Harrisburg and Central PA. <strong>Sofas $79.95, chairs from $39.95.</strong>",
  stats=[("Single piece","30–60 min"),("Living room set","2–3 hours"),("Dry time","2–6 hours"),("Sofa","$79.95")],
  included=["Sofas, loveseats and sectionals","Chairs and armchairs","Recliners","Ottomans",
            "Dining room chairs","Microfibre, cotton, linen and velvet","Scotchgard&reg; protection","Food, drink and pet stains"],
  band=("svc-upholstery", 1280, 608, "Upholstery cleaned and ready to use the same day",
        "A clean upholstered sofa in a Harrisburg, PA living room"),
  steps=[("Fabric test","Every piece is tested first so the method matches the fabric, weave and dyes."),
         ("Dry soil removal","Loose grit comes out first. Left in, it turns to mud the moment moisture is added."),
         ("Steam clean","Low-moisture extraction lifts embedded dirt, allergens and odour without soaking the padding."),
         ("Groom and dry","Pile is groomed back and airflow brings drying down to a few hours.")],
  notes=[("couch","Safe on delicate pieces","We test first and match the method to the fabric, so antiques and delicate weaves are treated accordingly."),
         ("drop","Stains lifted, not spread","Food, drink and pet stains are treated with solutions matched to the fabric rather than scrubbed."),
         ("shield","Scotchgard&reg; protection","Applied after cleaning so the next spill sits on the surface instead of soaking straight in.")],
  faqs=[("What furniture do you clean?","Sofas, sectionals, loveseats, armchairs, recliners, ottomans and dining chairs, in microfibre, cotton, linen, velvet and most blends."),
        ("Is it safe for delicate or antique fabrics?","Yes. We test each piece and choose the method from the fabric type and construction, so freshness is restored without damaging the piece."),
        ("How long does it take?","A single piece takes 30 to 60 minutes and a full living room set 2 to 3 hours. Drying is usually 2 to 6 hours."),
        ("Can you remove coffee, wine or pet stains?","Yes, using solutions matched to the fabric. Results depend on the age and nature of the stain, but most come out well."),
        ("Do you offer Scotchgard protection?","Yes. Applied after cleaning, it resists future stains and makes routine upkeep easier."),
        ("What does upholstery cleaning cost?","Sofas are $79.95, love seats $59.95 and chairs $39.95. Sectionals are quoted by the piece.")],
  cta=("Ready to refresh your furniture?","Sofas $79.95. Free quotes across Harrisburg and Central PA."),
  stype="Upholstery Cleaning",
  sdesc="Steam upholstery cleaning for sofas, sectionals, chairs, recliners, ottomans and dining chairs, with optional Scotchgard protection. Harrisburg, PA and Central Pennsylvania.",
  offers={"@type":"Offer","price":"39.95","priceCurrency":"USD",
          "description":"From, per chair. Sofa $79.95, love seat $59.95.","url":f"{SITE}/upholstery-cleaning.html"}),

"oriental-rug-cleaning.html": dict(
  nav="Rug Cleaning",
  eyebrow="free pick-up &amp; delivery",
  h2="Rugs Cleaned, Repaired &amp; Restored",
  h1="Oriental &amp; Area Rug Cleaning in Harrisburg, PA",
  title="Oriental &amp; Area Rug Cleaning in Harrisburg, PA | Bear Carpet Care",
  desc="Oriental and area rug cleaning in Harrisburg, PA. 15% off with free pick-up and delivery. Repairs in-house. Call (717) 454-7347.",
  head_class="head-rug",
  preload=[("img/hdr-rug2-640.webp", "(max-width: 991px)"), ("img/hdr-rug2-960.webp", "(min-width: 992px)")],
  lead="We clean, repair and restore oriental and area rugs across Harrisburg and Central PA. <strong>15% off, with free pick-up and delivery.</strong>",
  stats=[("Turnaround","5–7 days"),("Pick-up","Free"),("Fibres","Wool, silk, cotton"),("Offer","15% off")],
  included=["Free pick-up and delivery","Hand and machine cleaning","Oriental, Persian and Turkish",
            "Karastan, Chinese and Indian","Braided, shag and machine-made","Wool, silk, cotton and synthetic",
            "Scotchgard&reg; protection","Full repair service"],
  band=("oriental-rug-cleaning-3", 1024, 929, "Fringes cleaned by hand, off the floor and out of the house",
        "An oriental rug fringe being cleaned by hand at the Bear Carpet Care facility"),
  steps=[("Collected from you","We pick the rug up free of charge and log it in when it reaches the facility."),
         ("Assessed by fibre","Fibre content, weave and dye stability decide the method. Antique and hand-woven pieces get gentler handling."),
         ("Dusted, washed, dried","Dry soil comes out first, then a wash matched to the rug, then controlled drying so it keeps its shape."),
         ("Repaired and returned","Fringe or structural work happens before we deliver it back, usually within 5 to 7 days.")],
  notes=[("home","Cleaned off-site","Rugs are cleaned at our facility, not on your floor, so the dirt leaves the building instead of moving around it."),
         ("shield","Antique-safe handling","Fibre, weave and dye composition are assessed individually. Hand-woven and antique rugs are treated by hand."),
         ("broom","Full repair service","Reweaving, moth damage, fringe repair and replacement, renapping, colour retouching, serging and binding.")],
  faqs=[("Do you offer free pick-up and delivery?","Yes, free on all rug cleaning in the Harrisburg area. We handle the rug from your door to our facility and back."),
        ("What types of rug do you clean?","Oriental, Persian, Turkish, Indian, Chinese, Karastan, braided, shag, machine-made and hand-woven, in wool, silk, cotton and synthetic fibres."),
        ("How long does it take?","Most rugs are cleaned and returned within 5 to 7 business days, depending on size, fibre and any repair work."),
        ("Do you repair rugs as well?","Yes. Reweaving, moth damage, fringe repair and replacement, renapping, colour retouching, serging, binding and size reduction."),
        ("Is it safe for antique or valuable rugs?","Yes. Each rug is assessed on fibre content, weave and dye composition first. Antique and hand-woven rugs are treated by hand."),
        ("What does rug cleaning cost?","Rug cleaning is currently 15% off with free pick-up and delivery. Price depends on size and fibre, so we quote each rug after assessing it.")],
  cta=("Ready to restore your rugs?","15% off with free pick-up and delivery across Harrisburg and Central PA."),
  stype="Rug Cleaning",
  sdesc="Cleaning, repair and restoration of oriental and area rugs in wool, silk, cotton and synthetic fibres, with free pick-up and delivery. Harrisburg, PA and Central Pennsylvania.",
  offers={"@type":"Offer","description":"15% off rug cleaning with free pick-up and delivery",
          "url":f"{SITE}/oriental-rug-cleaning.html"}),
}


def service_page(slug, s):
    inc = "".join(f"<li>{icon('check')}<span>{i}</span></li>" for i in s["included"])
    steps = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in s["steps"])
    notes = "".join(
        f'<div class="note" data-reveal="{n + 1}">{icon("l-" + i)}<h3>{t}</h3><p>{d}</p></div>'
        for n, (i, t, d) in enumerate(s["notes"]))
    src, w, h, cap, alt = s["band"]
    trail = [("Home", "index.html"), (s["nav"], None)]

    body = page_head_block(s["eyebrow"], s["h1"], trail, slug) + f"""
    <section class="section">
        <div class="wrap split">
            <div class="split-copy" data-reveal>
                <span class="eyebrow">what's included</span>
                <h2>{s['h2']}</h2>
                <p class="lead">{s['lead']}</p>
                <ul class="checklist two">{inc}</ul>
                <div class="btn-row stack">
                    <a href="contact.html" class="btn btn-teal">Get a Free Quote</a>
                    <a href="{BIZ['phone_href']}" class="btn btn-line">{icon('phone')}{BIZ['phone_display']}</a>
                </div>
            </div>
            <figure class="feature-img" data-reveal="2">
                <img src="img/{src}-{w}.webp" srcset="img/{src}-{w // 2}.webp {w // 2}w, img/{src}-{w}.webp {w}w"
                     sizes="(min-width: 900px) 50vw, 100vw" alt="{alt}"
                     width="{w}" height="{h}" loading="lazy" decoding="async">
            </figure>
        </div>
    </section>

    <section class="cream section">
        <div class="wrap split top">
            <div class="split-copy" data-reveal>
                <span class="eyebrow">how it works</span>
                <h2>Four Steps, Start to Finish</h2>
                <p class="muted">{cap}. Every job follows the same process, so you know what to expect
                   before we arrive.</p>
            </div>
            <ol class="steps" data-reveal="2">{steps}</ol>
        </div>
    </section>

    <section class="section">
        <div class="wrap">
            {section_head("why choose us", "The Bear Carpet Care Difference")}
            <div class="notes">{notes}</div>
        </div>
    </section>
""" + faq_block(s["faqs"]) + cta(*s["cta"])

    page = dict(slug=slug, title=s["title"], desc=s["desc"], preload=photo_preload(PAGE_PHOTO[slug]),
                schema=ld(business(), website(),
                          service_ld(slug, s["nav"], s["stype"], s["sdesc"], s.get("offers")),
                          crumbs_ld(slug, trail),
                          webpage(slug, s["title"], ("WebPage", "FAQPage"), s["faqs"],
                                  about=f"{SITE}/{slug}#service")))
    return write(slug, page, body)


# ---------------------------------------------------------------- home
def home():
    slug = "index.html"
    services = [
        ("carpet-cleaning.html", "l-wand", "Carpet Cleaning", "Two rooms from $79.95"),
        ("upholstery-cleaning.html", "l-sofa", "Upholstery Cleaning", "Sofas, chairs &amp; sectionals"),
        ("oriental-rug-cleaning.html", "l-rug", "Oriental Rug Cleaning", "Free pick-up &amp; delivery"),
        ("carpet-cleaning.html", "l-paw", "Pet Stain &amp; Odor Removal", "Treated at the source"),
    ]
    svc = "".join(
        f'<div class="service" data-reveal="{i + 1}">{icon(ic)}<h3><a href="{href}">{t}</a></h3>'
        f'<p>{d}</p><span class="arrow-link">{icon("arrow")}</span></div>'
        for i, (href, ic, t, d) in enumerate(services))

    work = [
        ("g-carpet", "Carpet Cleaning", "Hot-water extraction that lifts the dirt and the residue with it."),
        ("g-sofa", "Upholstery Cleaning", "Fabric-tested steam cleaning for sofas, chairs and sectionals."),
        ("g-rugfringe", "Rug Cleaning", "Oriental and area rugs washed by hand at our own facility."),
    ]
    circles = "".join(
        f'<div class="circle-item" data-reveal="{i + 1}">'
        f'<img src="img/{im}-380.webp" srcset="img/{im}-380.webp 380w, img/{im}-760.webp 760w" sizes="200px" '
        f'alt="" width="200" height="200" loading="lazy" decoding="async">'
        f'<small>Our work</small><h3><a href="gallery.html">{t}</a></h3><p>{d}</p>'
        f'<span class="arrow-link">{icon("arrow")}</span></div>'
        for i, (im, t, d) in enumerate(work))

    socials = "".join(
        f'<li><a href="{url}" target="_blank" rel="noopener">{icon(k)}{label}</a></li>'
        for k, label, url in SOCIALS)

    faqs = [
        ("What does carpet cleaning cost?", "Two rooms up to 250 sq ft is $79.95 and four rooms up to 500 sq ft is $149.95. Sofas are $79.95, love seats $59.95 and chairs $39.95. Oriental rugs are 15% off with free pick-up and delivery."),
        ("What areas do you serve?", "Harrisburg, Carlisle, Hershey, Lancaster, Lebanon and York, Pennsylvania, and the surrounding Central PA area."),
        ("Are your products safe for pets and children?", "Yes. We use non-toxic, hypoallergenic, biodegradable solutions on every job, with no harsh chemicals and no residue left behind."),
        ("How long has Bear Carpet Care been in business?", "Over 30 years. We are family-owned and locally operated in Harrisburg, Pennsylvania."),
        ("Do you offer free pick-up and delivery for rugs?", "Yes, free on all area rug cleaning in the Harrisburg area."),
        ("How do I get a quote?", "Call (717) 454-7347 or use the contact form. Quotes are free with no obligation and we usually reply the same business day."),
    ]

    body = f"""    <section class="hero">
        <picture>
            <source media="(max-width: 639px)" srcset="img/hero-m-720.webp">
            <img src="img/hero-1600.webp" srcset="img/hero-960.webp 960w, img/hero-1600.webp 1360w" sizes="100vw"
                 alt="A carpet being deep cleaned with a hot-water extraction wand" width="1360" height="765" fetchpriority="high">
        </picture>
        <div class="wrap">
            <span class="eyebrow">carpet cleaning in Harrisburg, PA</span>
            <h1>Enjoy Your Freshly Cleaned Home</h1>
            <p>Carpets, furniture and rugs, deep cleaned by a family business with {BIZ['years']} years in Central PA.
               Non-toxic, pet-safe, and two rooms from $79.95.</p>
            <div class="btn-row stack">
                <a href="contact.html" class="btn btn-teal">Get a Free Quote</a>
                <a href="{BIZ['phone_href']}" class="btn btn-white">{icon('phone')}Call {BIZ['phone_display']}</a>
            </div>
            <ul class="ticks">
                <li>{icon('check')}{BIZ['years']} years, family-owned</li>
                <li>{icon('check')}Pet &amp; kid safe</li>
                <li>{icon('check')}Free quotes</li>
            </ul>
        </div>
    </section>

    <section class="cream section">
        <div class="wrap">
            {section_head("what we do", "Our Services")}
            <div class="services">{svc}</div>
        </div>
    </section>

    <section class="section">
        <div class="wrap split">
            <div class="split-copy" data-reveal>
                <span class="eyebrow">good to know</span>
                <h2>Keeping Central PA Homes Fresh and Clean</h2>
                <div class="faq">{faq_items(faqs, open_first=True)}</div>
            </div>
            <div class="stat-photo" data-reveal="2">
                <img src="img/pet-1100.webp" srcset="img/pet-640.webp 640w, img/pet-1100.webp 698w"
                     sizes="(min-width: 900px) 45vw, 100vw" alt="A small dog relaxing on a freshly cleaned carpet"
                     width="698" height="559" loading="lazy" decoding="async">
                <div class="stats">
                    <div class="stat"><b>Years</b><strong><span data-count="30">30</span>+</strong>Family-owned and locally run.</div>
                    <div class="stat"><b>Towns</b><strong>{len(AREAS)}</strong>Harrisburg to Lancaster and York.</div>
                </div>
            </div>
        </div>
    </section>

{pricing_block()}
    <section class="testimonials">
        <div class="navy t-panel on-dark" data-reveal>
            <span class="eyebrow">testimonials</span>
            <h2>What They Say</h2>
            {icon('quote', 'icon quote-mark')}
            <div class="slider" tabindex="0" role="region" aria-label="Customer reviews">{testimonial_slides()}</div>
            <div class="dots" role="group" aria-label="Choose a review"></div>
            <a class="more" href="reviews.html">Read all reviews</a>
        </div>
        <img src="img/spot-1000.webp" srcset="img/spot-560.webp 560w, img/spot-1000.webp 881w"
             sizes="(min-width: 900px) 50vw, 100vw" alt="Spot-treating a stain on a cream carpet"
             width="881" height="1102" loading="lazy" decoding="async">
    </section>

    <section class="social-strip" aria-label="Find us online">
        <div class="wrap"><ul>{socials}</ul></div>
    </section>

    <section class="section">
        <div class="wrap split">
            <div class="photo-card" data-reveal>
                <img src="img/facility-900.webp" srcset="img/facility-560.webp 560w, img/facility-900.webp 765w"
                     sizes="(min-width: 900px) 45vw, 100vw" alt="Oriental rugs hanging to dry at the Bear Carpet Care facility"
                     width="765" height="957" loading="lazy" decoding="async">
                <div class="tag-box">Free Rug Pick-Up &amp; Delivery<small>Rugs are washed at our own facility, then brought back to your door.</small></div>
            </div>
            <div class="split-copy" data-reveal="2">
                <span class="eyebrow">save your time</span>
                <h2>We Make Clean Carpets Easy</h2>
                <p class="muted">Bear Carpet Care is family-owned and locally operated in Harrisburg. Dave and the team
                   have been cleaning carpet, upholstery and rugs across Central PA for more than three decades.</p>
                <ol class="numbered">
                    <li><span>01.</span><div>Non-Toxic &amp; Pet-Safe<small>Biodegradable, hypoallergenic solutions on every job.</small></div></li>
                    <li><span>02.</span><div>Honest, Upfront Pricing<small>We confirm the total before we start. No surprises.</small></div></li>
                    <li><span>03.</span><div>Quick Replies<small>Most quotes answered the same business day.</small></div></li>
                </ol>
                <div class="btn-row"><a href="contact.html" class="btn btn-teal">Get a Free Quote</a></div>
            </div>
        </div>
    </section>

    <section class="cream section">
        <div class="wrap">
            {section_head("find help now", "Recent Work", "A few jobs from around Harrisburg and Central PA. There is more in the gallery.")}
            <div class="circles">{circles}</div>
        </div>
    </section>

    <section class="band">
        <img src="img/band-1440.webp" srcset="img/band-960.webp 960w, img/band-1440.webp 1440w" sizes="100vw"
             alt="" width="1440" height="617" loading="lazy" decoding="async">
        <a href="https://www.youtube.com/@BearCarpetCare" target="_blank" rel="noopener" data-reveal>
            <span class="play">{icon('play')}</span>
            <p>Watch us work on YouTube</p>
        </a>
    </section>

{contact_block(details=False)}"""

    page = dict(slug=slug, title=f"Carpet Cleaning in Harrisburg, PA from $79.95 | {BIZ['name']}",
                desc="Family-owned carpet, upholstery and oriental rug cleaning in Harrisburg, PA. Two rooms from $79.95. 30+ years, non-toxic and pet-safe. Call (717) 454-7347.",
                preload=[dict(href="img/hero-m-720.webp", media="(max-width: 639px)"),
                         dict(href="img/hero-1600.webp", media="(min-width: 640px)",
                              srcset="img/hero-960.webp 960w, img/hero-1600.webp 1360w", sizes="100vw")],
                schema=ld(business(), website(),
                          webpage(slug, "Carpet Cleaning in Harrisburg, PA", ("WebPage", "FAQPage"), faqs)))
    return write(slug, page, body, scripts='<script src="js/contact.min.js" defer></script>\n')


# ---------------------------------------------------------------- reviews
def reviews_page():
    slug = "reviews.html"
    trail = [("Home", "index.html"), ("Reviews", None)]
    body = page_head_block("testimonials", "Customer Reviews", trail, slug) + f"""
    <section class="cream section">
        <div class="wrap">
            {section_head("what they say", "Straight From Our Customers", "What people in Harrisburg and Central PA say after we have been out. These are collected from our Google listing.")}
            <div class="reviews">{review_cards()}</div>
            <p class="price-note">
                Reviews are reproduced from our
                <a href="https://maps.app.goo.gl/8CSvEHzdW2A2sdau7" target="_blank" rel="noopener">Google Business Profile</a>
                and <a href="https://www.yelp.com/biz/bear-carpet-care-harrisburg" target="_blank" rel="noopener">Yelp page</a>,
                where you can read them in full.</p>
        </div>
    </section>

{cta('Join Them?', 'Free quotes across Harrisburg and Central Pennsylvania.')}"""
    page = dict(slug=slug, title=f"Customer Reviews | {BIZ['name']}, Harrisburg PA",
                desc="Read reviews from Bear Carpet Care customers across Harrisburg and Central PA. Carpet, upholstery and rug cleaning, family-owned for over 30 years.",
                preload=photo_preload(PAGE_PHOTO[slug]),
                schema=ld(business(), website(), crumbs_ld(slug, trail),
                          webpage(slug, "Customer Reviews", ("CollectionPage",))))
    return write(slug, page, body)


# ---------------------------------------------------------------- gallery
GALLERY = [
    ("g-carpet", "Hot-water extraction on a living room carpet"),
    ("g-sofa", "An upholstered sofa after cleaning"),
    ("g-rugfringe", "Oriental rug fringe cleaned by hand"),
    ("g-facility", "Rugs drying at our cleaning facility"),
    ("g-pet", "Carpet after pet odour treatment"),
    ("rug-facility", "Oriental rugs hung to dry after washing"),
]
GALLERY_SRC = {"rug-facility": (640, 1280)}
# Wider than the grid tiles, so it runs full width underneath them.
GALLERY_WIDE = ("before-and-after", 500, 181, "An oriental rug before and after cleaning")


def gallery():
    slug = "gallery.html"
    trail = [("Home", "index.html"), ("Gallery", None)]
    figs = []
    for i, (name, cap) in enumerate(GALLERY):
        a, b = GALLERY_SRC.get(name, (380, 760))
        figs.append(
            f'<figure data-reveal="{i % 3 + 1}"><img src="img/{name}-{a}.webp" '
            f'srcset="img/{name}-{a}.webp {a}w, img/{name}-{b}.webp {b}w" '
            f'sizes="(min-width: 900px) 33vw, (min-width: 560px) 50vw, 100vw" alt="{cap}" '
            f'width="380" height="285" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>')
    wn, ww, wh, wcap = GALLERY_WIDE
    wide = (f'<figure class="wide" data-reveal><img src="img/{wn}.webp" alt="{wcap}" '
            f'width="{ww}" height="{wh}" loading="lazy" decoding="async">'
            f'<figcaption>{wcap}</figcaption></figure>')
    body = page_head_block("before &amp; after", "Our Work", trail, slug) + f"""
    <section class="section">
        <div class="wrap">
            {section_head("recent jobs", "Carpet, Upholstery &amp; Rugs", "Work from around Harrisburg and Central PA.")}
            <div class="gallery">{''.join(figs)}{wide}</div>
            <p class="price-note">More on
                <a href="https://www.instagram.com/bearcarpetcare/" target="_blank" rel="noopener">Instagram</a>,
                <a href="https://www.tiktok.com/@bearcarpetcare" target="_blank" rel="noopener">TikTok</a> and
                <a href="https://www.youtube.com/@BearCarpetCare" target="_blank" rel="noopener">YouTube</a>.</p>
        </div>
    </section>

{cta('Want Yours Looking Like This?', 'Free quotes across Harrisburg and Central Pennsylvania.')}"""
    page = dict(slug=slug, title=f"Gallery | {BIZ['name']}, Harrisburg PA",
                preload=photo_preload(PAGE_PHOTO[slug]),
                desc="Photos of carpet, upholstery and oriental rug cleaning by Bear Carpet Care in Harrisburg, PA and Central Pennsylvania.",
                schema=ld(business(), website(), crumbs_ld(slug, trail),
                          webpage(slug, "Our Work", ("CollectionPage",))))
    return write(slug, page, body)


# ---------------------------------------------------------------- contact
def contact():
    slug = "contact.html"
    trail = [("Home", "index.html"), ("Contact", None)]
    MAP = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d495471.83057429155!2d-77.10622490514357"
           "!3d40.274299078759906!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c9c132db7bfb3f"
           "%3A0x3fc7795a8d802f20!2sHarrisburg%2C%20PA!5e0!3m2!1sen!2sus!4v1716574863725!5m2!1sen!2sus")
    hours = "".join(f"<div><dt>{d}</dt><dd>{t}</dd></div>" for d, t in HOURS)
    body = page_head_block("free quotes", "Contact Bear Carpet Care", trail, slug) + contact_block() + f"""
    <section class="section">
        <div class="wrap split top">
            <div class="split-copy" data-reveal>
                <span class="eyebrow">when &amp; where</span>
                <h2>Hours &amp; Service Area</h2>
                <dl class="hours" style="margin-top:1.5rem">{hours}</dl>
                <p class="muted" style="margin-top:1.5rem">We serve {', '.join(AREAS[:-1])} and {AREAS[-1]},
                   and the surrounding Central PA area. Times are Eastern.</p>
            </div>
            <div class="map" data-reveal="2">
                <button type="button" data-map="{MAP}">{icon('marker')}<strong>View our service area</strong>
                    <span>Tap to load the map of Harrisburg, PA</span></button>
            </div>
        </div>
    </section>
"""
    page = dict(slug=slug, title=f"Contact Us for a Free Quote | {BIZ['name']}",
                desc="Contact Bear Carpet Care in Harrisburg, PA for carpet, upholstery or rug cleaning. Free quotes, no obligation. Call (717) 454-7347.",
                preload=photo_preload(PAGE_PHOTO[slug]),
                schema=ld(business(), website(), crumbs_ld(slug, trail),
                          webpage(slug, "Contact Bear Carpet Care", ("ContactPage",))))
    return write(slug, page, body, scripts='<script src="js/contact.min.js" defer></script>\n')


# ---------------------------------------------------------------- 404
def notfound():
    slug = "404.html"
    body = f"""    <section class="cream section notfound">
        <div class="wrap">
            <div class="section-head">
                <span class="eyebrow">page not found</span>
                <h1>We Couldn't Find That Page</h1>
                <p>It may have moved, or the link may be out of date.</p>
            </div>
            <div class="notes">
                <a class="note" href="/carpet-cleaning.html">{icon('l-wand')}<h3>Carpet Cleaning</h3><p>From $79.95 for two rooms.</p></a>
                <a class="note" href="/upholstery-cleaning.html">{icon('l-sofa')}<h3>Upholstery Cleaning</h3><p>Sofas from $79.95.</p></a>
                <a class="note" href="/oriental-rug-cleaning.html">{icon('l-rug')}<h3>Rug Cleaning</h3><p>15% off, free pick-up.</p></a>
            </div>
        </div>
    </section>

{cta('Need a Quote Right Now?', 'Free quotes across Harrisburg and Central Pennsylvania.')}"""
    page = dict(slug=slug, title=f"Page Not Found | {BIZ['name']}",
                desc="That page could not be found. Browse carpet, upholstery and rug cleaning in Harrisburg, PA or call (717) 454-7347.",
                robots="noindex, follow",
                schema=ld(business(), website()))
    out = head(page) + header("") + body + footer().replace("{scripts}", "")
    # 404 is served from any path, so its links and assets must be absolute
    out = clean_urls(out)
    out = re.sub(r'(href|src)="(?!https?:|#|/|mailto:|tel:)', r'\1="/', out)
    out = re.sub(r'(srcset="|, )(img/)', r'\1/\2', out)
    (ROOT / slug).write_text(out)
    return len(re.sub(r"<[^>]+>", " ", out).split())


# ---------------------------------------------------------------- run
if __name__ == "__main__":
    counts = {"index.html": home()}
    for slug, s in SERVICES.items():
        counts[slug] = service_page(slug, s)
    counts["reviews.html"] = reviews_page()
    counts["gallery.html"] = gallery()
    counts["contact.html"] = contact()
    counts["404.html"] = notfound()
    for k, v in counts.items():
        print(f"  {k:30} {v:>4} words")
    print(f"\n{len(counts)} pages written")
