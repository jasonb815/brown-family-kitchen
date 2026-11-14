# brown-family-kitchen — history

Newest first. One entry per session that changes something. Format is defined in CLAUDE.md.

## 2026-11-14 — Recipe image support
- Why: BrownRecipesNN prompt; let recipes carry photos of the original card, the finished dish and prep steps.
- Changed: added scripts/add_recipe_images.py (HEIC/JPG/PNG -> stripped, <=1600px JPEG + "## Photos" figures) and requirements-tools.txt (pillow, pillow-heif); enabled mkdocs-glightbox (pinned in requirements.txt, plugin in mkdocs.yml); figure/figcaption rules in docs/stylesheets/extra.css; *.heic/*.heif in .gitignore; "Adding photos" in README.md; comment in templates/recipe-template.md. No real recipe was given photos.
- Commits: CookBook-017.
- Follow-ups: Jason adds the Grandpa's Chili card photos (originals go in .scratch/incoming/). glightbox adds one extra search-index entry per page (page title).

## 2026-11-14 — Add Grandpa's Chili
- Why: BrownRecipesNN prompt to add Grandpa's handwritten chili recipe (Michael Brown, Sr.).
- Changed: added docs/recipes/soups/grandpas-chili.md; added nav entry under Soups in mkdocs.yml; HISTORY.md. Rebuilt site/ (not committed).
- Commits: CookBook-016.
- Follow-ups: none.

## 2026-10-22 — Baseline applied
- Why: standardize layout and tooling across the droplet (hub Phase C1 batch).
- Changed: added CLAUDE.md and HISTORY.md; .gitignore gained the baseline lines. README.md already existed and was kept.
- Checked: 17 tracked files, no credential-like names, no key patterns in files or history.
- Commits: CookBook-015.
- Follow-ups: none.
