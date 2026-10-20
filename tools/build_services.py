"""Generate the service tiles on the homepage and one page per service.

Usage: python3 tools/build_services.py
Content lives in tools/services.py.
"""

import html
import re
from pathlib import Path
from urllib.parse import quote

from services import SERVICES

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITE = "https://royalclean-ay.de"


def esc(text):
    return html.escape(text, quote=True)


def quote_url(service):
    return "/?leistung=" + quote(service["form"]) + "#anfrage"


def build_tiles():
    items = []
    for i, s in enumerate(SERVICES):
        wide = " tile-wide" if i == 0 else ""
        items.append(f'''          <li class="tile{wide}">
            <a class="tile-link" href="leistungen/{s["slug"]}/">
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
      <div class="container">
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


def main():
    index = INDEX.read_text(encoding="utf-8")
    index = re.sub(
        r"(<!-- services:start -->).*?(\s*<!-- services:end -->)",
        lambda m: m.group(1) + "\n" + build_tiles() + m.group(2),
        index,
        flags=re.S,
    )
    INDEX.write_text(index, encoding="utf-8")

    header = rootify(extract(index, '<header class="site-header"', "</header>"))
    footer = rootify(extract(index, '<footer class="site-footer">', "</footer>")).replace(' loading="lazy"', "")
    mobile_bar = rootify(extract(index, '<div class="mobile-bar">', "</div>"))
    icons = extract(index, '<svg width="0" height="0"', "</svg>\n\n  <script").rsplit("\n\n  <script", 1)[0]

    for s in SERVICES:
        out = ROOT / "leistungen" / s["slug"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build_page(s, header, footer, mobile_bar, icons), encoding="utf-8")

    urls = [f"{SITE}/"] + [f'{SITE}/leistungen/{s["slug"]}/' for s in SERVICES]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "".join(f"  <url>\n    <loc>{u}</loc>\n  </url>\n" for u in urls)
    sitemap += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Built {len(SERVICES)} service pages")


if __name__ == "__main__":
    main()
