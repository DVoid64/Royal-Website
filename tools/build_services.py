"""Generate the service tiles on the homepage and one page per service.

Usage: python3 tools/build_services.py
Content lives in tools/services.py.
"""

import html
import re
from pathlib import Path
from urllib.parse import quote

from PIL import Image

from industries import INDUSTRY_PAGES
from services import COMPANY, MENU_GROUPS, SERVICES

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITE = "https://royalclean-ay.de"


def esc(text):
    return html.escape(text, quote=True)


def quote_url(service):
    return "/?leistung=" + quote(service["form"]) + "#anfrage"


def icon_svg(service, cls):
    # Every stroke gets pathLength=1 so CSS can redraw the icon on hover
    body = re.sub(r"<(path|rect|circle)\b", r'<\1 pathLength="1"', service["icon"])
    return f'<svg class="{cls}" viewBox="0 0 48 48" aria-hidden="true">{body}</svg>'


CHEVRON = '<svg class="nav-chevron" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5l5 5 5-5"/></svg>'
BY_SLUG = {s["slug"]: s for s in SERVICES}


def menu_link(href, title, text, icon=""):
    return f'''<li><a class="menu-link" href="{href}">{icon}<span class="menu-text"><span class="menu-title">{esc(title)}</span><span class="menu-desc">{esc(text)}</span></span></a></li>'''


def build_header():
    groups = []
    for label, slugs in MENU_GROUPS:
        links = "\n                  ".join(
            menu_link(f"/leistungen/{slug}/", BY_SLUG[slug]["name"], BY_SLUG[slug]["menu"], icon_svg(BY_SLUG[slug], "menu-icon"))
            for slug in slugs
        )
        groups.append(f'''<div class="mega-group">
                <p class="mega-heading">{esc(label)}</p>
                <ul class="mega-list">
                  {links}
                </ul>
              </div>''')
    industries = "\n              ".join(menu_link(f"/branchen/{i['slug']}/", i["name"], i["menu"]) for i in INDUSTRY_PAGES)
    company = "\n              ".join(menu_link(href, name, text) for name, text, href in COMPANY)
    return f'''<header class="site-header" data-header>
    <div class="topbar">
      <div class="container topbar-inner">
        <p>Gebäudereinigung in Oberhausen, Mülheim an der Ruhr, Duisburg, Essen und Bottrop</p>
        <ul class="topbar-links">
          <li>Erreichbar 8:00 bis 16:00 Uhr</li>
          <li><a href="tel:+4917676275792">0176 76275792</a></li>
          <li><a href="mailto:info@royalclean-ay.de">info@royalclean-ay.de</a></li>
          <li><a href="https://wa.me/4917676275792" target="_blank" rel="noopener">WhatsApp</a></li>
        </ul>
      </div>
    </div>

    <div class="container header-inner">
      <a class="brand" href="/" aria-label="Royal Clean Services AY, zur Startseite">
        <img src="/assets/img/logo-emblem-320.webp" width="160" height="119" alt="">
        <span class="brand-name">Royal Clean <span>Services AY</span></span>
      </a>

      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-toggle>
        <span class="menu-toggle-bars" aria-hidden="true"></span>
        <span class="visually-hidden">Menü</span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Hauptnavigation" data-nav>
        <ul class="nav-list">
          <li class="nav-item nav-item-mega" data-dropdown>
            <button class="nav-trigger" type="button" aria-expanded="false" aria-controls="menu-leistungen">Leistungen{CHEVRON}</button>
            <div class="nav-panel mega" id="menu-leistungen">
              <div class="mega-inner">
              {groups[0]}
              {groups[1]}
              <aside class="mega-promo">
                <img src="/assets/img/photos/einblick-team.webp" alt="" width="1400" height="934" loading="lazy">
                <div class="mega-promo-body">
                  <p class="mega-promo-title">Kostenloses Angebot in 24 Stunden</p>
                  <p>Nach der Besichtigung, mit Festpreis.</p>
                  <a class="btn btn-gold btn-small" href="/#anfrage">Angebot anfragen</a>
                  <a class="mega-phone" href="tel:+4917676275792">oder 0176 76275792 anrufen</a>
                </div>
              </aside>
              <a class="mega-all" href="/#leistungen">Alle Leistungen im Überblick</a>
              </div>
            </div>
          </li>
          <li class="nav-item" data-dropdown>
            <button class="nav-trigger" type="button" aria-expanded="false" aria-controls="menu-branchen">Branchen{CHEVRON}</button>
            <ul class="nav-panel dropdown" id="menu-branchen">
              {industries}
            </ul>
          </li>
          <li class="nav-item" data-dropdown>
            <button class="nav-trigger" type="button" aria-expanded="false" aria-controls="menu-unternehmen">Unternehmen{CHEVRON}</button>
            <ul class="nav-panel dropdown" id="menu-unternehmen">
              {company}
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="/#anfrage">Kontakt</a></li>
        </ul>
        <a class="btn btn-gold btn-small nav-cta" href="/#anfrage">Angebot anfragen</a>
      </nav>
    </div>
    <span class="scroll-progress" aria-hidden="true" data-progress></span>
  </header>'''


def inject_header(path, header):
    html_text = path.read_text(encoding="utf-8")
    new = re.sub(r'<header class="site-header".*?</header>', lambda m: header, html_text, count=1, flags=re.S)
    path.write_text(new, encoding="utf-8")


def build_tiles():
    items = []
    for i, s in enumerate(SERVICES):
        wide = " tile-wide" if i == 0 else ""
        items.append(f'''          <li class="tile{wide}">
            <a class="tile-link" href="leistungen/{s["slug"]}/">
              {icon_svg(s, "tile-icon")}
              <h3>{esc(s["name"])}</h3>
              <p>{esc(s["tile"])}</p>
              <span class="tile-more">Details ansehen</span>
            </a>
          </li>''')
    return '        <ul class="tile-grid">\n' + "\n".join(items) + "\n        </ul>"


def extract(source, start, end):
    a = source.index(start)
    b = source.index(end, a) + len(end)
    return source[a:b]


def rootify(fragment):
    """Rewrite homepage-relative links so they work from any subpage."""
    fragment = fragment.replace('href="#top"', 'href="/"')
    fragment = re.sub(r'(<a\b[^>]*?)href="#([\w-]+)"', r'\1href="/#\2"', fragment)
    fragment = fragment.replace('src="assets/', 'src="/assets/')
    fragment = re.sub(r'href="(impressum|datenschutz)\.html"', r'href="/\1.html"', fragment)
    return fragment


def build_page(s, header, footer, mobile_bar, icons):
    with Image.open(ROOT / s["photo"].lstrip("/")) as img:
        w, h = img.size
    others = "\n".join(
        f'            <li><a href="/leistungen/{o["slug"]}/">{esc(o["name"])}</a></li>'
        for o in SERVICES if o is not s
    )
    scope = "\n".join(f"              <li>{esc(x)}</li>" for x in s["scope"])
    clients = "\n".join(f"              <li>{esc(x)}</li>" for x in s["for"])
    title = f'{s["name"]} Oberhausen | Royal Clean Services AY'
    url = f'{SITE}/leistungen/{s["slug"]}/'
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(s["intro"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0A1128">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{esc(s["name"])} in Oberhausen – Royal Clean Services AY">
  <meta property="og:description" content="{esc(s["intro"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="page-service">
  <a class="skip-link" href="#main">Zum Inhalt springen</a>

  {header}

  <main id="main">
    <section class="subhero">
      <div class="container subhero-inner">
        <figure class="subhero-photo photo">
          <img src="{s["photo"]}" alt="{esc(s["photo_alt"])}" width="{w}" height="{h}" fetchpriority="high">
        </figure>
        <nav class="breadcrumb" aria-label="Brotkrümelnavigation">
          <a href="/">Startseite</a>
          <span aria-hidden="true">/</span>
          <a href="/#leistungen">Leistungen</a>
          <span aria-hidden="true">/</span>
          <span aria-current="page">{esc(s["name"])}</span>
        </nav>
        <h1 class="subhero-title">{esc(s.get("h1", s["name"] + " in Oberhausen"))}</h1>
        <p class="subhero-lead">{esc(s["intro"])}</p>
        <div class="hero-actions">
          <a class="btn btn-gold btn-large" href="{quote_url(s)}">Kostenloses Angebot in 24 Stunden</a>
          <a class="btn btn-quiet btn-large" href="tel:+4917676275792">0176 76275792 anrufen</a>
        </div>
        <ul class="hero-facts" aria-label="Unsere Kernzusagen">
          <li>Angebot in 24 Stunden</li>
          <li>Fotobericht nach jedem Einsatz</li>
          <li>Festpreis ohne versteckte Kosten</li>
        </ul>
        <p class="photo-credit">Symbolfoto: {s["photo_src"]}</p>
      </div>
    </section>

    <section class="section section-light detail" aria-labelledby="umfang-title">
      <div class="container detail-grid">
        <div>
          <h2 id="umfang-title">Leistungsumfang</h2>
          <ul class="scope-list">
{scope}
          </ul>
          <p class="detail-note">Den genauen Umfang legen wir bei der Besichtigung mit Ihnen fest.</p>
        </div>
        <aside class="detail-aside">
          <h3>Für</h3>
          <ul class="detail-clients">
{clients}
          </ul>
          <h3>Turnus</h3>
          <p>{esc(s["rhythm"])}</p>
        </aside>
      </div>
    </section>

    <section class="section cta-band" aria-labelledby="cta-title">
      <div class="container cta-inner">
        <div>
          <h2 id="cta-title">Angebot für {esc(s.get("cta", s["name"]))} anfragen</h2>
          <p>Kostenlos und unverbindlich. Innerhalb von 24 Stunden nach der Besichtigung erhalten Sie ein Angebot mit Festpreis.</p>
        </div>
        <a class="btn btn-gold btn-large" href="{quote_url(s)}">Kostenloses Angebot in 24 Stunden</a>
      </div>
    </section>

    <section class="section section-light other-services" aria-labelledby="weitere-title">
      <div class="container">
        <h2 id="weitere-title">Weitere Leistungen</h2>
        <ul class="other-list">
{others}
        </ul>
      </div>
    </section>
  </main>

  {footer}

  {mobile_bar}

  {icons}

  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


def build_industry_page(ind, header, footer, mobile_bar, icons):
    with Image.open(ROOT / ind["photo"].lstrip("/")) as img:
        w, h = img.size
    url = f'{SITE}/branchen/{ind["slug"]}/'
    title = f'{ind["h1"].replace(" in Oberhausen", "")} in Oberhausen | Royal Clean Services AY'
    needs = "\n".join(f'''          <li class="need">
            <h3>{esc(n_title)}</h3>
            <p>{esc(n_text)}</p>
          </li>''' for n_title, n_text in ind["needs"])
    scope = "\n".join(f"              <li>{esc(x)}</li>" for x in ind["scope"])
    services = "\n".join(
        f'''            <li><a class="menu-link" href="/leistungen/{slug}/">{icon_svg(BY_SLUG[slug], "menu-icon")}<span class="menu-text"><span class="menu-title">{esc(BY_SLUG[slug]["name"])}</span><span class="menu-desc">{esc(BY_SLUG[slug]["menu"])}</span></span></a></li>'''
        for slug in ind["services"]
    )
    others = "\n".join(
        f'            <li><a href="/branchen/{o["slug"]}/">{esc(o["name"])}</a></li>'
        for o in INDUSTRY_PAGES if o is not ind
    )
    first_service = BY_SLUG[ind["services"][0]]
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(ind["intro"])}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#0A1128">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="de_DE">
  <meta property="og:title" content="{esc(ind["h1"])} – Royal Clean Services AY">
  <meta property="og:description" content="{esc(ind["intro"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
</head>
<body class="page-service page-industry">
  <a class="skip-link" href="#main">Zum Inhalt springen</a>

  {header}

  <main id="main">
    <section class="subhero">
      <div class="container subhero-inner">
        <figure class="subhero-photo photo">
          <img src="{ind["photo"]}" alt="{esc(ind["photo_alt"])}" width="{w}" height="{h}" fetchpriority="high">
        </figure>
        <nav class="breadcrumb" aria-label="Brotkrümelnavigation">
          <a href="/">Startseite</a>
          <span aria-hidden="true">/</span>
          <span>Branchen</span>
          <span aria-hidden="true">/</span>
          <span aria-current="page">{esc(ind["name"])}</span>
        </nav>
        <h1 class="subhero-title">{esc(ind["h1"])}</h1>
        <p class="subhero-lead">{esc(ind["intro"])}</p>
        <div class="hero-actions">
          <a class="btn btn-gold btn-large" href="{quote_url(first_service)}">Kostenloses Angebot in 24 Stunden</a>
          <a class="btn btn-quiet btn-large" href="tel:+4917676275792">0176 76275792 anrufen</a>
        </div>
        <ul class="hero-facts" aria-label="Unsere Kernzusagen">
          <li>Angebot in 24 Stunden</li>
          <li>Fotobericht nach jedem Einsatz</li>
          <li>Festpreis ohne versteckte Kosten</li>
        </ul>
        <p class="photo-credit">Symbolfoto: {ind["photo_src"]}</p>
      </div>
    </section>

    <section class="section needs-section" aria-labelledby="needs-title">
      <div class="container">
        <h2 id="needs-title" class="needs-title">{esc(ind["needs_title"])}</h2>
        <ul class="needs">
{needs}
        </ul>
      </div>
    </section>

    <section class="section section-light detail" aria-labelledby="umfang-title">
      <div class="container detail-grid">
        <div>
          <h2 id="umfang-title">Was wir reinigen</h2>
          <ul class="scope-list">
{scope}
          </ul>
          <p class="detail-note">Den genauen Umfang legen wir bei der Besichtigung mit Ihnen fest.</p>
        </div>
        <aside class="detail-aside detail-services">
          <h3>Passende Leistungen</h3>
          <ul>
{services}
          </ul>
        </aside>
      </div>
    </section>

    <section class="section cta-band" aria-labelledby="cta-title">
      <div class="container cta-inner">
        <div>
          <h2 id="cta-title">Angebot für {esc(ind["name"])} anfragen</h2>
          <p>Kostenlos und unverbindlich. Innerhalb von 24 Stunden nach der Besichtigung erhalten Sie ein Angebot mit Festpreis.</p>
        </div>
        <a class="btn btn-gold btn-large" href="{quote_url(first_service)}">Kostenloses Angebot in 24 Stunden</a>
      </div>
    </section>

    <section class="section section-light other-services" aria-labelledby="weitere-title">
      <div class="container">
        <h2 id="weitere-title">Weitere Branchen</h2>
        <ul class="other-list">
{others}
        </ul>
      </div>
    </section>
  </main>

  {footer}

  {mobile_bar}

  {icons}

  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


def main():
    index = INDEX.read_text(encoding="utf-8")
    index = re.sub(
        r"(<!-- services:start -->).*?(\s*<!-- services:end -->)",
        lambda m: m.group(1) + "\n" + build_tiles() + m.group(2),
        index,
        flags=re.S,
    )
    INDEX.write_text(index, encoding="utf-8")

    header = build_header()
    for page in ("index.html", "impressum.html", "datenschutz.html"):
        inject_header(ROOT / page, header)
    index = INDEX.read_text(encoding="utf-8")
    footer = rootify(extract(index, '<footer class="site-footer">', "</footer>")).replace(' loading="lazy"', "")
    mobile_bar = rootify(extract(index, '<div class="mobile-bar">', "</div>"))
    icons = extract(index, '<svg width="0" height="0"', "</svg>\n\n  <script").rsplit("\n\n  <script", 1)[0]

    for s in SERVICES:
        out = ROOT / "leistungen" / s["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_page(s, header, footer, mobile_bar, icons), encoding="utf-8")

    for ind in INDUSTRY_PAGES:
        out = ROOT / "branchen" / ind["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_industry_page(ind, header, footer, mobile_bar, icons), encoding="utf-8")

    urls = [f"{SITE}/"] + [f'{SITE}/leistungen/{s["slug"]}/' for s in SERVICES]
    urls += [f'{SITE}/branchen/{i["slug"]}/' for i in INDUSTRY_PAGES]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url>\n    <loc>{u}</loc>\n  </url>\n" for u in urls)
    sitemap += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Built {len(SERVICES)} service pages and {len(INDUSTRY_PAGES)} industry pages")


if __name__ == "__main__":
    main()
