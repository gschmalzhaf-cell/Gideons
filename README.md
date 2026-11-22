# Gideon's Projekte

GitHub-Pages-Übersicht über meine Projekte:

- 📚 [Gideon's Bücherwelt](https://github.com/gschmalzhaf-cell/Gideon-s-B-cherwelt)
- 🌐 [Gideon's Übersetzer](https://github.com/gschmalzhaf-cell/Gideon-s-bersetzer)
- 📝 [Gideon's Notizen](https://github.com/gschmalzhaf-cell/AutoDoc)
- 🌿 [Gideon's RömerPlant](https://github.com/gschmalzhaf-cell/PlanzenR-mer)
- 🛒 [Gideon's Einkaufsliste](https://github.com/gschmalzhaf-cell/Einkaufsliste)
- 🧹 [Gideon's Putzplan](https://github.com/gschmalzhaf-cell/putzplan)
- 🐣 [Gideon's Tamagot(s)chi](https://github.com/gschmalzhaf-cell/Gideon-s-Tamagotschi)

## Live

👉 [gschmalzhaf-cell.github.io/Gideons](https://gschmalzhaf-cell.github.io/Gideons/)

## Aufbau

Die Seite wird mit Jekyll von GitHub Pages gebaut (Quelle: Branch `gh-pages`, Pfad `/`).
Änderungen auf `main` vornehmen und nach `gh-pages` pushen –
der Push löst automatisch einen neuen Pages-Build aus.

- `_data/projects.yml` – alle Projektdaten (inkl. `slug`, `app_icon`, `platform`, `tagline`, `privacy`, `long_description`, `features`, `release_version`, `download_url`)
- `_includes/head.html`, `header.html`, `footer.html` – gemeinsamer SEO-/OG-Header, Navigation mit Hell/Dunkel-Umschalter und Footer
- `_layouts/project.html` + `projekte/<slug>/index.html` – Detailseite pro Projekt mit Direkt-Download, Faktenleiste, Feature-Karten und Vor/Zurück-Navigation
- `assets/icons/<slug>/` – App-Icons der Projekte (aus den jeweiligen Repos)
- `assets/img/` – Hero-Illustration (`hero-atelier.jpg`), OG-Preview (`og-preview.jpg`) und SVG-Favicon (`favicon.svg`)
- `assets/js/main.js` – Plattform-Filter, Live-Suche (`/`-Shortcut) und Hell/Dunkel-Modus
- `index.html` – Startseite mit Editorial-Hero, Filterleiste, Projekt-Kacheln und Prinzipien

## Automatisierung

- `.github/workflows/update-projects.yml` – läuft **montags 07:00 UTC** (manuell via *Actions → Run workflow*):
  `scripts/update_projects.py` listet alle öffentlichen Repos des Users, ergänzt neue automatisch
  in `_data/projects.yml`, legt fehlende Detailseiten unter `projekte/<slug>/` an, aktualisiert
  Release-Versionen sowie APK-/Installer-Downloadlinks und pusht nach `gh-pages`.
  Lokal testbar: `python scripts/update_projects.py --dry-run`
- `.github/workflows/optimization-suggestions.yml` – läuft **am 1. des Monats, 09:00 UTC**:
  `scripts/audit_site.py` prüft die Seite auf Lücken (fehlende Beschreibungen, Features, Icons,
  Release-Daten, OG-Image, Detailseiten) und legt das Ergebnis als Issue ab bzw. kommentiert
  das bestehende `[Optimierung]`-Issue
