# The Brown Family Kitchen

A durable family recipe system built with Markdown, Material for MkDocs, GitHub Actions, and GitHub Pages.

## How it works

1. Rough recipes enter `recipe-inbox/`.
2. Cleaned recipes use `templates/recipe-template.md`.
3. Published recipes live under `docs/recipes/`.
4. GitHub Actions validates every recipe and rebuilds the website after each commit to `main`.

## First-time GitHub setup

1. Create a public repository named `brown-family-kitchen`.
2. Upload this package to the repository.
3. Confirm `mkdocs.yml` contains your GitHub username.
4. Commit to `main`.
5. Open **Settings > Pages**.
6. Set Pages to deploy from the `gh-pages` branch and `/ (root)`.

The published address will be:

`https://jasonb815.github.io/brown-family-kitchen/`

## Add or update a recipe

See [CONTRIBUTING.md](CONTRIBUTING.md). The usual flow is:

```bash
python scripts/validate_recipes.py
mkdocs serve
```

Then commit the change to `main`.

## Adding photos

Each recipe can have a "Photos" section at the bottom with the original recipe card, finished-dish photos and preparation-step photos.

1. Drop the originals (HEIC from an iPhone is fine; also JPG/PNG) into `.scratch/incoming/`. This folder is git-ignored, and originals are never committed.
2. Run the helper from the repo root with the project venv:

   ```bash
   source .venv/bin/activate
   python scripts/add_recipe_images.py RECIPE KIND IMAGE [IMAGE ...] [--caption "text"] [--rotate 90|180|270]
   ```

   `RECIPE` is the recipe slug (e.g. `grandpas-chili`) or a path. `KIND` is `card` (original recipe card), `dish` (finished dish) or `step` (preparation steps). `--rotate` turns the image clockwise if it came out sideways.
3. The script converts each photo to a web-ready JPEG (max 1600px, all EXIF/GPS data stripped), saves it under `docs/assets/recipe-images/<slug>/`, and adds it to the recipe. Re-running with the same photo is skipped as a duplicate.
4. Rebuild with `./rebuild.sh`, then commit the new JPEGs and the changed recipe.

The script needs `pip install -r requirements-tools.txt` in the venv (already done on the server).
