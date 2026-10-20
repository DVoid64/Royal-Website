# royalclean-ay.de

Website der Royal Clean Services AY GbR, Gebäudereinigung in Oberhausen.

Reines HTML, CSS und JavaScript, ohne Build-Schritt. Schriften (Marcellus, Figtree) liegen lokal in `assets/fonts/`, es werden keine externen Dienste geladen.

## Dateien

- `index.html` – Startseite
- `impressum.html`, `datenschutz.html` – Pflichtseiten
- `assets/css/style.css` – Gestaltung
- `assets/js/main.js` – Menü und Anfrageformular (öffnet WhatsApp oder das E-Mail-Programm mit fertiger Nachricht)
- `assets/img/` – Logo, Icons, Vorschaubild für Social Media
- `.htaccess` – Weiterleitung auf https://royalclean-ay.de und Browser-Caching (Apache bei IONOS)

## Lokal ansehen

```
python3 -m http.server 8000
```

Dann http://localhost:8000 öffnen.

## Veröffentlichen bei IONOS

Alle Dateien dieses Ordners (ohne `.git`, `.claude`, `skills-lock.json`, `README.md`) per SFTP in das Webspace-Verzeichnis der Domain laden, oder IONOS „Deploy Now“ mit diesem GitHub-Repository verbinden.

## Vor dem Livegang

- Im Impressum die markierten Platzhalter (Umsatzsteuer-ID, Handwerkskammer) ergänzen oder entfernen.
- Impressum und Datenschutzerklärung rechtlich prüfen lassen.
- SSL-Zertifikat für die Domain im IONOS-Kundenbereich aktivieren.
