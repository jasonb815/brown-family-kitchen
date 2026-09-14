"""MkDocs hook: renders a small status/faves badge block right after a
recipe page's first H1 heading, driven entirely by that page's own
frontmatter (status / faves).

Deliberately a hook (the documented `hooks:` mechanism), not a theme
template override -- overriding mkdocs-material's page template ties
this to that theme's internal structure and tends to break on upgrades;
on_page_markdown just edits the page's own Markdown source before it's
rendered, same as any other content.

If status is missing or not one of STATUS_LABELS below, and faves isn't
exactly True, nothing is inserted and the page is returned unchanged --
this must never raise on a page that simply doesn't opt in.
"""

STATUS_LABELS = {
    "new": "New — Never Tried",
    "tried-disliked": "Tried Once – Didn't Like",
    "tried-ok": "Tried Once – OK",
    "tried-loved": "Tried Once – Loved",
    "basic": "Basic Recipe",
    "in-rotation": "In Rotation",
    "family": "Family Recipe",
}


def on_page_markdown(markdown, page, config, files):
    status = page.meta.get("status")
    faves = page.meta.get("faves")

    badges = []
    label = STATUS_LABELS.get(status)
    if label:
        badges.append(f'<span class="recipe-badge recipe-badge--{status}">{label}</span>')
    if faves is True:
        badges.append('<span class="recipe-badge recipe-badge--faves">&#9733; Favorite</span>')

    if not badges:
        return markdown

    badge_block = f'<p class="recipe-badges">{"".join(badges)}</p>'

    lines = markdown.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines[i + 1:i + 1] = ["", badge_block]
            return "\n".join(lines)

    # No H1 found on this page -- prepend rather than silently dropping
    # the badge (better a badge with no H1 than a status nobody sees).
    return badge_block + "\n\n" + markdown
