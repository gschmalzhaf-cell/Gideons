#!/usr/bin/env python3
import json
import os
import pathlib
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
    "autodoc": "Gideon's Notizen",
    "gideon-s-notizen": "Gideon's Notizen",
    "planzenr-mer": "Gideon's RömerPlant",
    "einkaufsliste": "Gideon's Einkaufsliste",
    "putzplan": "Gideon's Putzplan",
    "gideon-s-tamagotschi": "Gideon's Tamagot(s)chi",
}

SLUG_MAP = {
    "gideon-s-b-cherwelt": "buecherwelt",
    "gideon-s-bersetzer": "uebersetzer",
    "autodoc": "notizen",
    "gideon-s-notizen": "notizen",
    "planzenr-mer": "roemerplant",
    "einkaufsliste": "einkaufsliste",
    "putzplan": "putzplan",
    "gideon-s-tamagotschi": "tamagotschi",
}

ICON_MAP = {
    "gideon-s-b-cherwelt": "📚",
    "gideon-s-bersetzer": "🌐",
    "autodoc": "📝",
    "gideon-s-notizen": "📝",
    "planzenr-mer": "🌿",
    "einkaufsliste": "🛒",
    "putzplan": "🧹",
    "gideon-s-tamagotschi": "🐣",
}


def gh_json(path):
    res = subprocess.run(
        ["gh", "api", path, "--jq", "."],
        capture_output=True,
        text=True,
    )
    if res.returncode != 0:
        return None
    return json.loads(res.stdout)


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


def fetch_latest_release(repo_url):
    match = re.match(r"https?://github\.com/([^/]+/[^/]+?)(?:\.git)?/?$", str(repo_url).strip())
    if not match:
        return None
    owner_repo = match.group(1)
    rel = gh_json("repos/%s/releases/latest" % owner_repo)
    if not rel or not rel.get("tag_name"):
        return None

    assets = rel.get("assets") or []
    download_url = ""
    download_label = "Download"
    for ext, label in (
        (".apk", "APK laden"),
        (".exe", "Windows-Installer"),
        (".dmg", "macOS laden"),
        (".appimage", "Linux laden"),
    ):
        for asset in assets:
            name = (asset.get("name") or "").lower()
            if name.endswith(ext):
                download_url = asset.get("browser_download_url") or ""
                download_label = label
                break
        if download_url:
            break

    published = (rel.get("published_at") or "")[:10]
    return {
        "release_version": rel.get("tag_name") or "",
        "release_date": published,
        "release_url": rel.get("html_url") or "",
        "download_url": download_url,
        "download_label": download_label if download_url else "",
    }


def prettify(name):
    base = re.sub(r"(?i)^gideon-s-", "", name)
    words = [w for w in re.split(r"[-_]+", base) if w]
    return " ".join(w[:1].upper() + w[1:] for w in words)


def slugify(name):
    key = name.lower()
    if key in SLUG_MAP:
        return SLUG_MAP[key]
    return re.sub(r"[^a-z0-9]+", "-", key).strip("-") or "projekt"


def infer_platform(language):
    lang = (language or "").lower()
    if lang == "kotlin":
        return ("Android", "android")
    return ("Desktop", "desktop")


def ensure_detail_page(slug, dry_run):
    page_path = pathlib.Path("projekte") / slug / "index.html"
    if page_path.exists():
        return False
    if dry_run:
        print("[dry-run] wuerde Detailseite anlegen: %s" % page_path)
        return True
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text("---\nlayout: project\nslug: %s\n---\n" % slug, encoding="utf-8")
    print("+ Detailseite angelegt: %s" % page_path)
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    with open(DATA_FILE, encoding="utf-8") as fh:
        projects = yaml.safe_load(fh) or []
    known = {str(p.get("repo", "")).rstrip("/").lower() for p in projects}

    changed = False
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
        platform, platform_group = infer_platform(repo.get("language"))
        slug = slugify(name)
        new_entries.append({
            "name": NAME_MAP.get(key, "Gideon's " + prettify(name)),
            "icon": ICON_MAP.get(key, "🚀"),
            "slug": slug,
            "app_icon": "",
            "tagline": "",
            "platform": platform,
            "platform_group": platform_group,
            "category": "Werkzeuge",
            "privacy": "Lokal & Open Source",
            "description": description,
            "long_description": description,
            "features": [],
            "language": repo.get("language") or "—",
            "repo": repo.get("html_url", ""),
            "website": repo.get("homepage") or "",
        })

    for entry in new_entries:
        print("+ %s (%s)" % (entry["name"], entry["repo"]))
        ensure_detail_page(entry["slug"], dry_run)
        changed = True

    projects.extend(new_entries)

    for project in projects:
        rel_info = fetch_latest_release(project.get("repo", ""))
        if not rel_info:
            continue
        for field, val in rel_info.items():
            if project.get(field) != val:
                print("~ %s: %s -> %s" % (project.get("name"), field, val))
                project[field] = val
                changed = True

    if not changed:
        print("Keine Aenderungen gefunden – %s bleibt unveraendert." % DATA_FILE)
        return
    if dry_run:
        print("[dry-run] keine Datei geschrieben.")
        return
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        yaml.safe_dump(projects, fh, allow_unicode=True, sort_keys=False, width=120)
    print("Aktualisierung in %s gespeichert." % DATA_FILE)


if __name__ == "__main__":
    main()
