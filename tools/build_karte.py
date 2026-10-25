"""Build the business-card landing pages (/karte/<slug>/) and their vCard files.

The QR code on each printed card opens one of these pages, where the visitor
chooses WhatsApp, a call, saving the contact or the website.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://royalclean-ay.de"
COMPANY_TEL = "+4917676275792"
WHATSAPP = "4917676275792"
WA_TEXT = "Hallo%2C%20ich%20habe%20Ihre%20Visitenkarte%20erhalten%20und%20interessiere%20mich%20f%C3%BCr%20ein%20Angebot."

PEOPLE = [
    {"slug": "yasin", "first": "Yasin", "last": "Yilmaz", "tel": "+4915735500310", "tel_label": "0157 35500310"},
    {"slug": "amir", "first": "Amir", "last": "Hussain Rajabi", "tel": COMPANY_TEL, "tel_label": "0176 76275792"},
]

ICONS = {
    "chat": '<path d="M20 11.5a8.5 8.5 0 0 1-12.6 7.4L3 20l1.2-4.2A8.5 8.5 0 1 1 20 11.5Z"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/>',
    "save": '<circle cx="10" cy="8" r="4"/><path d="M3 20a7 7 0 0 1 12.5-4.3M19 14v6M16 17h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}


def icon(name):
    return (f'<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def vcard(p):
    tels = [f"TEL;TYPE=CELL:{p['tel']}"]
    if p["tel"] != COMPANY_TEL:
        tels.append(f"TEL;TYPE=WORK:{COMPANY_TEL}")
    lines = [
        "BEGIN:VCARD", "VERSION:3.0",
        f"N:{p['last']};{p['first']};;;", f"FN:{p['first']} {p['last']}",
        "ORG:Royal Clean Services AY GbR", "TITLE:Gesellschafter",
        *tels,
        "EMAIL;TYPE=WORK:info@royalclean-ay.de",
        f"URL:{SITE}/",
        "ADR;TYPE=WORK:;;Mülheimer Straße 128;Oberhausen;;46045;Deutschland",
        "END:VCARD",
    ]
    return "\r\n".join(lines) + "\r\n"


def page(p):
    name = f"{p['first']} {p['last']}"
    vcf = f"{p['first']}-{p['last'].replace(' ', '-')}.vcf".lower()
    return f'''<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{name} | Royal Clean Services AY</title>
  <meta name="description" content="Kontakt zu {name}, Royal Clean Services AY: WhatsApp, Anruf, Kontakt speichern oder Angebot anfragen.">
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#0A1128">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/cormorant-garamond-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/jost-latin.woff2" as="font" type="font/woff2" crossorigin>
  <style>
    @font-face {{ font-family: "Cormorant Garamond"; src: url("/assets/fonts/cormorant-garamond-latin.woff2") format("woff2"); font-weight: 400 700; font-display: swap; }}
    @font-face {{ font-family: "Jost"; src: url("/assets/fonts/jost-latin.woff2") format("woff2"); font-weight: 300 600; font-display: swap; }}
    :root {{ --navy: #0A1128; --navy-2: #101A3A; --gold: #D6A83E; --gold-light: #F0D28A; --text: #E8EBF4; --muted: #A8B0C8; --line: rgba(214, 168, 62, .28); }}
    * {{ box-sizing: border-box; margin: 0; }}
    html {{ background: var(--navy); }}
    body {{ min-height: 100svh; display: flex; justify-content: center; background: radial-gradient(120% 60% at 50% 0%, var(--navy-2), var(--navy) 70%); color: var(--text); font: 400 1rem/1.5 "Jost", system-ui, sans-serif; padding: max(2rem, env(safe-area-inset-top)) max(1.25rem, env(safe-area-inset-right)) max(1.5rem, env(safe-area-inset-bottom)) max(1.25rem, env(safe-area-inset-left)); }}
    main {{ width: 100%; max-width: 24rem; display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .logo {{ width: 11rem; height: auto; }}
    h1 {{ font: 600 2.25rem/1.1 "Cormorant Garamond", Garamond, serif; color: #fff; margin-top: 1.5rem; text-wrap: balance; }}
    .role {{ margin-top: .5rem; font-size: .75rem; letter-spacing: .22em; text-transform: uppercase; color: var(--gold); }}
    .rule {{ width: 3rem; height: 1px; background: var(--gold); margin: 1.5rem 0; }}
    .actions {{ width: 100%; display: grid; gap: .75rem; }}
    .btn {{ display: flex; align-items: center; gap: .9rem; padding: 1rem 1.25rem; border: 1px solid var(--line); border-radius: 4px; color: var(--text); text-decoration: none; text-align: left; font-size: 1.05rem; transition: border-color .2s, background-color .2s; }}
    .btn small {{ display: block; color: var(--muted); font-size: .8rem; }}
    .btn svg {{ flex: none; color: var(--gold); }}
    .btn:hover {{ border-color: var(--gold); background: rgba(214, 168, 62, .06); }}
    .btn:focus-visible {{ outline: 2px solid var(--gold-light); outline-offset: 2px; }}
    .btn.primary {{ background: var(--gold); border-color: var(--gold); color: var(--navy); font-weight: 500; }}
    .btn.primary svg, .btn.primary small {{ color: var(--navy); }}
    .btn.primary:hover {{ background: var(--gold-light); }}
    address {{ font-style: normal; margin-top: 2rem; color: var(--muted); font-size: .9rem; }}
    footer {{ margin-top: 1.5rem; font-size: .8rem; }}
    footer a {{ color: var(--muted); }}
    @media (prefers-reduced-motion: reduce) {{ .btn {{ transition: none; }} }}
  </style>
</head>
<body>
  <main>
    <img class="logo" src="/assets/img/logo-full-720.webp" width="720" height="654" alt="Royal Clean Services AY – Gebäudereinigung Ruhrgebiet">
    <h1>{name}</h1>
    <p class="role">Gesellschafter</p>
    <div class="rule"></div>
    <nav class="actions" aria-label="Kontakt">
      <a class="btn primary" href="https://wa.me/{WHATSAPP}?text={WA_TEXT}" target="_blank" rel="noopener">{icon("chat")}<span>WhatsApp schreiben<small>0176 76275792 · erreichbar 8 bis 16 Uhr</small></span></a>
      <a class="btn" href="tel:{p['tel']}">{icon("phone")}<span>Anrufen<small>{p['tel_label']}</small></span></a>
      <a class="btn" href="/karte/{p['slug']}/{vcf}" download>{icon("save")}<span>Kontakt speichern<small>Direkt ins Adressbuch</small></span></a>
      <a class="btn" href="/kontakt/">{icon("mail")}<span>Angebot anfragen<small>Kostenlos, Festpreis in 24 Stunden</small></span></a>
      <a class="btn" href="/">{icon("globe")}<span>Webseite ansehen<small>royalclean-ay.de</small></span></a>
    </nav>
    <address>Royal Clean Services AY GbR<br>Mülheimer Straße 128 · 46045 Oberhausen<br><a href="mailto:info@royalclean-ay.de" style="color:inherit">info@royalclean-ay.de</a></address>
    <footer><a href="/impressum.html">Impressum</a> · <a href="/datenschutz.html">Datenschutz</a></footer>
  </main>
</body>
</html>
''', vcf


def main():
    for p in PEOPLE:
        html, vcf = page(p)
        out = ROOT / "karte" / p["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(html, encoding="utf-8")
        (out / vcf).write_text(vcard(p), encoding="utf-8")


if __name__ == "__main__":
    main()
