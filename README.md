# royalclean-ay.de

Website der Royal Clean Services AY GbR, Gebäudereinigung in Oberhausen.

Reines HTML, CSS und JavaScript, ohne Build-Schritt. Schriften (Cormorant Garamond, Jost) liegen lokal in `assets/fonts/`, es werden keine externen Dienste geladen.

## Dateien

- `index.html` – Startseite
- `leistungen/<leistung>/index.html` – je eine Unterseite pro Leistung (generiert, siehe unten)
- `impressum.html`, `datenschutz.html` – Pflichtseiten
- `assets/css/style.css` – Gestaltung
- `assets/js/main.js` – Menü und Anfrageformular (öffnet WhatsApp oder das E-Mail-Programm mit fertiger Nachricht)
- `assets/img/` – Logo, Icons, Vorschaubild für Social Media
- `assets/img/photos/` – Symbolfotos von Unsplash (Unsplash-Lizenz, Nachweis im Impressum)
- `.htaccess` – Weiterleitung auf https://royalclean-ay.de und Browser-Caching (Apache bei IONOS)

## Leistungen bearbeiten

Texte der sieben Leistungen stehen in `tools/services.py`. Nach einer Änderung:

```
cd tools && python3 build_services.py
```

Das Skript aktualisiert die Kacheln auf der Startseite, alle Unterseiten unter `leistungen/` und die `sitemap.xml`. Kopfzeile und Footer der Unterseiten werden aus `index.html` übernommen, also nach Änderungen daran ebenfalls neu erzeugen.

## Lokal ansehen

```
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen.

## Veröffentlichen

Die Seite läuft über GitHub Pages. Jeder Push auf `main` startet den Workflow `.github/workflows/pages.yml`, der nur die Webseiten-Dateien veröffentlicht (ohne `.claude`, README usw.).

Einmalige Einrichtung:

1. GitHub: Settings → Pages → Source „GitHub Actions“ wählen, Custom domain `royalclean-ay.de` eintragen, „Enforce HTTPS“ aktivieren, sobald verfügbar.
2. IONOS: Domains & SSL → royalclean-ay.de → DNS:
   - A-Einträge für `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - CNAME für `www`: `dvoid64.github.io`
   - Bestehende MX-Einträge für E-Mail nicht ändern.

Die `.htaccess` wird von GitHub Pages ignoriert. Sie ist nur für den Fall gedacht, dass die Seite später auf einen Apache-Webspace (z. B. IONOS Webhosting) umzieht.

## Vor dem Livegang

- Im Impressum die markierten Platzhalter (Umsatzsteuer-ID, Handwerkskammer) ergänzen oder entfernen.
- Impressum und Datenschutzerklärung rechtlich prüfen lassen.
- SSL-Zertifikat für die Domain im IONOS-Kundenbereich aktivieren.
