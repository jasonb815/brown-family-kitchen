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

## Tres Dias cookbook

Tres Dias recipes should ultimately live in a separate repository and site. This keeps institutional recipes, large-batch scaling, permissions, and family content independent while allowing both sites to use the same template and publishing system.
