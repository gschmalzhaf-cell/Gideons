#!/usr/bin/env python3
import datetime
import pathlib

import yaml

ROOT = pathlib.Path(".")


def main():
    with open(ROOT / "_data/projects.yml", encoding="utf-8") as fh:
        projects = yaml.safe_load(fh) or []
    with open(ROOT / "_config.yml", encoding="utf-8") as fh:
        config = yaml.safe_load(fh) or {}

    findings = []

    for p in projects:
        name = p.get("name", "?")
        slug = p.get("slug", "")
        if not p.get("description"):
            findings.append("**%s**: Kurzbeschreibung fehlt" % name)
        if not p.get("long_description"):
            findings.append("**%s**: Langbeschreibung fehlt – README des Repos einarbeiten" % name)
        features = p.get("features") or []
        if len(features) < 3:
            findings.append("**%s**: nur %d Feature(s) – Feature-Liste aus dem Repo-README ergaenzen" % (name, len(features)))
        if not (p.get("screenshots") or []):
            findings.append("**%s**: keine Screenshots – Bilder aus dem Repo (z. B. docs/assets) uebernehmen oder eigene aufnehmen und unter assets/screenshots/ ablegen" % name)
        if not p.get("website"):
            findings.append("**%s**: keine Website verlinkt – Repo-Homepage oder Demo-Seite nachtragen" % name)
        if not str(p.get("repo", "")).startswith("https://github.com/"):
            findings.append("**%s**: Repo-Link fehlt oder ist ungueltig" % name)
        if slug and not (ROOT / "projekte" / slug / "index.html").exists():
            findings.append("**%s**: Detailseite fehlt (projekte/%s/index.html)" % (name, slug))

    if not (ROOT / "index.html").exists():
        findings.append("index.html fehlt")
    if config.get("baseurl") != "/Gideons":
        findings.append("_config.yml: baseurl ist nicht /Gideons (aktuell: %r)" % config.get("baseurl"))
    if not (ROOT / "404.html").exists():
        findings.append("404.html fehlt")

    lines = []
    lines.append("Automatischer Audit der GitHub-Pages-Seite vom %s." % datetime.date.today().isoformat())
    lines.append("")
    lines.append("## Befunde")
    lines.append("")
    if findings:
        for f in findings:
            lines.append("- [ ] %s" % f)
    else:
        lines.append("Keine Luecken gefunden – alle Projekte vollstaendig gepflegt.")
    lines.append("")
    lines.append("## Allgemeine Optimierungsideen")
    lines.append("")
    lines.append("- [ ] OG-Image (og:image) hinterlegen, damit Links in sozialen Medien eine Vorschaukarte zeigen")
    lines.append("- [ ] Lighthouse-Audit (Performance, Accessibility, SEO) durchfuehren und Ergebnisse umsetzen")
    lines.append("- [ ] Eigenen Domain-Namen (CNAME) fuer die Pages-Seite einrichten")
    lines.append("- [ ] Screenshots der uebrigen Apps nachtragen, sobald verfuegbar")
    lines.append("- [ ] Projekt-Kacheln um Release-Version oder Sterne ergaenzen")
    lines.append("- [ ] Dunkel/Hell-Wechsel als manueller Schalter (aktuell nur prefers-color-scheme)")
    lines.append("")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
