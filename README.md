# Gideon's Projekte

GitHub-Pages-Übersicht über meine Projekte:

- 📚 [Gideon's Bücherwelt](https://github.com/gschmalzhaf-cell/Gideon-s-B-cherwelt)
- 🌐 [Gideon's Übersetzer](https://github.com/gschmalzhaf-cell/Gideon-s-bersetzer)
- 🎙️ [Gideon's Autodoc](https://github.com/gschmalzhaf-cell/AutoDoc) · [getautodoc.com](https://getautodoc.com/)
- 🌿 [Gideon's RömerPlant](https://github.com/gschmalzhaf-cell/PlanzenR-mer)
- 🛒 [Gideon's Einkaufsliste](https://github.com/gschmalzhaf-cell/Einkaufsliste)
- 🧹 [Gideon's Putzplan](https://github.com/gschmalzhaf-cell/putzplan)

## Live

👉 [gschmalzhaf-cell.github.io/Gideons](https://gschmalzhaf-cell.github.io/Gideons/)

## Aufbau

Die Seite wird mit Jekyll von GitHub Pages gebaut (Quelle: Branch `gh-pages`, Pfad `/`).
Änderungen auf `main` vornehmen und nach `gh-pages` pushen –
der Push löst automatisch einen neuen Pages-Build aus.

- `_data/projects.yml` – alle Projektdaten (inkl. `slug`, `long_description`, `features`, `screenshots`)
- `_layouts/project.html` + `projekte/<slug>/index.html` – Detailseite pro Projekt
- `assets/screenshots/` – Screenshots der Apps (z. B. aus `docs/assets` der Repos)
- `index.html` – Startseite mit Projekt-Kacheln

## Automatisierung

- `.github/workflows/update-projects.yml` – läuft **montags 07:00 UTC** (manuell via *Actions → Run workflow*):
  `scripts/update_projects.py` listet alle öffentlichen Repos des Users, ergänzt neue automatisch
  in `_data/projects.yml` und pusht nach `gh-pages`. Lokal testbar: `python scripts/update_projects.py --dry-run`
- `.github/workflows/optimization-suggestions.yml` – läuft **am 1. des Monats, 09:00 UTC**:
  `scripts/audit_site.py` prüft die Seite auf Lücken (fehlende Beschreibungen, Features, Screenshots,
  Detailseiten) und legt das Ergebnis als Issue ab bzw. kommentiert das bestehende `[Optimierung]`-Issue
