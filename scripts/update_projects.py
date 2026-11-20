#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys

import yaml

DATA_FILE = "_data/projects.yml"
USER = os.environ.get("GITHUB_USER", "gschmalzhaf-cell")
EXCLUDE = {r.strip().lower() for r in os.environ.get("EXCLUDE_REPOS", "Gideons").split(",") if r.strip()}

NAME_MAP = {
    "gideon-s-b-cherwelt": "Gideon's Bücherwelt",
    "gideon-s-bersetzer": "Gideon's Übersetzer",
    "autodoc": "Gideon's Autodoc",
    "planzenr-mer": "Gideon's RömerPlant",
    "einkaufsliste": "Gideon's Einkaufsliste",
    "putzplan": "Gideon's Putzplan",
}

SLUG_MAP = {
    "gideon-s-b-cherwelt": "buecherwelt",
    "gideon-s-bersetzer": "uebersetzer",
    "autodoc": "autodoc",
    "planzenr-mer": "roemerplant",
    "einkaufsliste": "einkaufsliste",
    "putzplan": "putzplan",
}

ICON_MAP = {
    "gideon-s-b-cherwelt": "📚",
    "gideon-s-bersetzer": "🌐",
    "autodoc": "🎙️",
    "planzenr-mer": "🌿",
    "einkaufsliste": "🛒",
    "putzplan": "🧹",
}


def gh_json(path):
    out = subprocess.run(
        ["gh", "api", path, "--jq", "."],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)


def list_public_repos():
    repos = []
    page = 1
    while True:
        batch = gh_json("users/%s/repos?per_page=100&page=%d&sort=created" % (USER, page))
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def prettify(name):
    base = re.sub(r"(?i)^gideon-s-", "", name)
    words = [w for w in re.split(r"[-_]+", base) if w]
    return " ".join(w[:1].upper() + w[1:] for w in words)


def slugify(name):
    key = name.lower()
    if key in SLUG_MAP:
        return SLUG_MAP[key]
    return re.sub(r"[^a-z0-9]+", "-", key).strip("-") or "projekt"


def main():
    dry_run = "--dry-run" in sys.argv
    with open(DATA_FILE, encoding="utf-8") as fh:
        projects = yaml.safe_load(fh) or []
    known = {str(p.get("repo", "")).rstrip("/").lower() for p in projects}

    new_entries = []
    for repo in list_public_repos():
        name = repo.get("name", "")
        if name.lower() in EXCLUDE or repo.get("archived"):
            continue
        url = (repo.get("html_url") or "").rstrip("/").lower()
        if not url or url in known:
            continue
        key = name.lower()
        description = repo.get("description") or "Beschreibung folgt – siehe Repository."
        new_entries.append({
            "name": NAME_MAP.get(key, "Gideon's " + prettify(name)),
            "icon": ICON_MAP.get(key, "🚀"),
            "slug": slugify(name),
            "description": description,
            "long_description": description,
            "features": [],
            "screenshots": [],
            "language": repo.get("language") or "—",
            "repo": repo.get("html_url", ""),
            "website": repo.get("homepage") or "",
        })

    for entry in new_entries:
        print("+ %s (%s)" % (entry["name"], entry["repo"]))
    if not new_entries:
        print("Keine neuen Repos gefunden – %s bleibt unveraendert." % DATA_FILE)
        return
    if dry_run:
        print("[dry-run] keine Datei geschrieben.")
        return
    projects.extend(new_entries)
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        yaml.safe_dump(projects, fh, allow_unicode=True, sort_keys=False, width=120)
    print("%d neue(s) Projekt(e) in %s ergaenzt." % (len(new_entries), DATA_FILE))


if __name__ == "__main__":
    main()
