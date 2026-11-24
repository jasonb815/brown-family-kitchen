# brown-family-kitchen — history

Newest first. One entry per session that changes something. Format is defined in CLAUDE.md.

## 2026-11-24 — Add Chocolate Delight (Desserts)
- Why: BrownRecipesNN prompt to add Christy Shaw's Chocolate Delight to the Desserts category.
- Changed: added docs/recipes/desserts/chocolate-delight.md (verbatim from the prompt); Desserts nav entry in mkdocs.yml (before Gluten-Free Coconut Cream Cake); HISTORY.md. Rebuilt site/ and browse pages (not committed). Recipe appears under Browse > By Status > "New — Never Tried".
- Commits: CookBook-021.
- Follow-ups: none.

## 2026-11-24 — Fix truncated Shopping List in Alton Brown's Brined Turkey
- Why: BrownRecipesNN prompt; the recipe ended with an empty "###" under Shopping List and had no source footer.
- Changed: docs/recipes/poultry/alton-browns-brined-turkey.md (Shopping List contents, Supplies, source footer restored; nothing above it touched); HISTORY.md. Rebuilt site/ (not committed).
- Commits: CookBook-020.
- Follow-ups: none.

## 2026-11-24 — Add Alton Brown's Brined Turkey (new Poultry category)
- Why: BrownRecipesNN prompt to add Alton Brown's Brined Turkey under a new Poultry category.
- Changed: added docs/recipes/poultry/alton-browns-brined-turkey.md (verbatim from the prompt); new Poultry nav section between Drinks and Snacks in mkdocs.yml; HISTORY.md. Rebuilt site/ and browse pages (not committed). hooks/badges.py and scripts/generate_browse_pages.py have no hardcoded category list.
- Commits: CookBook-019.
- Follow-ups: recipe file ends with an empty "### " heading under "## Shopping List" (as supplied); fill in or remove.

## 2026-11-14 — Grandpa's Chili recipe card photos
- Why: attach the two photos of Grandpa's handwritten recipe card (front and back) to the recipe.
- Changed: docs/recipes/soups/grandpas-chili.md (new "## Photos / ### Recipe Card" section, added by scripts/add_recipe_images.py); docs/assets/recipe-images/grandpas-chili/grandpas-chili-card-01.jpg and -02.jpg; HISTORY.md. Originals (HEIC) stay in ~/.scratch/incoming/, not committed. First pass came out sideways; redone with --rotate 270, and the sideways JPEGs were quarantined.
- Commits: CookBook-018.
- Follow-ups: none.

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
