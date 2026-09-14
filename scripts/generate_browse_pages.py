#!/usr/bin/env python3
"""Generates docs/browse/by-status.md and docs/browse/favorites.md from
every recipe's own frontmatter under docs/recipes/. Both files are
generated output -- regenerate by running this script (rebuild.sh does
so automatically before every mkdocs build) rather than editing them by
hand; docs/browse/ is gitignored for the same reason.

Uses PyYAML directly rather than declaring it in requirements.txt --
it's already a hard, transitive dependency of mkdocs itself (mkdocs
can't run without it), so anywhere this script's venv has mkdocs
installed, PyYAML is already guaranteed present.
"""
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = REPO_ROOT / "docs" / "recipes"
BROWSE_DIR = REPO_ROOT / "docs" / "browse"

# Canonical order + display labels -- must match hooks/badges.py's own
# STATUS_LABELS exactly (single source of truth would be nicer, but
# these live in two different kinds of file for two different tools;
# keep both in sync by hand if the status list ever changes).
STATUS_LABELS = {
    "new": "New — Never Tried",
    "tried-disliked": "Tried Once – Didn't Like",
    "tried-ok": "Tried Once – OK",
    "tried-loved": "Tried Once – Loved",
    "basic": "Basic Recipe",
    "in-rotation": "In Rotation",
    "family": "Family Recipe",
}

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?\n)---\s*\n", re.DOTALL)


def load_recipes():
    """Every docs/recipes/**/*.md file's frontmatter, plus its path
    relative to docs/browse/ (for markdown links) and title (falling
    back to the filename if a page has no title: field)."""
    recipes = []
    for path in sorted(RECIPES_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = _FRONTMATTER_RE.match(text)
        meta = yaml.safe_load(match.group(1)) if match else {}
        meta = meta or {}
        title = meta.get("title") or path.stem.replace("-", " ").title()
        rel_from_browse = Path("..") / path.relative_to(REPO_ROOT / "docs")
        recipes.append({
            "title": title,
            "status": meta.get("status"),
            "faves": meta.get("faves") is True,
            "link": rel_from_browse.as_posix(),
        })
    return recipes


def write_by_status(recipes):
    lines = ["# Browse by Status", ""]
    any_section = False
    for slug, label in STATUS_LABELS.items():
        matches = sorted(
            (r for r in recipes if r["status"] == slug),
            key=lambda r: r["title"].lower(),
        )
        if not matches:
            continue
        any_section = True
        lines.append(f"## {label}")
        lines.append("")
        for r in matches:
            lines.append(f"- [{r['title']}]({r['link']})")
        lines.append("")
    if not any_section:
        lines.append("No recipes have a recognized status yet.")
        lines.append("")
    (BROWSE_DIR / "by-status.md").write_text("\n".join(lines), encoding="utf-8")


def write_favorites(recipes):
    lines = ["# Favorites", ""]
    faves = sorted((r for r in recipes if r["faves"]), key=lambda r: r["title"].lower())
    if faves:
        for r in faves:
            lines.append(f"- [{r['title']}]({r['link']})")
        lines.append("")
    else:
        lines.append("No favorites marked yet -- set `faves: true` on a recipe to add it here.")
        lines.append("")
    (BROWSE_DIR / "favorites.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    BROWSE_DIR.mkdir(parents=True, exist_ok=True)
    recipes = load_recipes()
    write_by_status(recipes)
    write_favorites(recipes)
    print(f"Generated browse pages from {len(recipes)} recipe(s).")


if __name__ == "__main__":
    main()
