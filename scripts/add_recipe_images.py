#!/usr/bin/env python3
"""Attach photos to a recipe page.

Converts each image (HEIC/HEIF/JPG/PNG) to a web-ready JPEG (EXIF orientation
applied, longest edge <= 1600px, quality 82, progressive, all metadata
stripped), saves it as docs/assets/recipe-images/<slug>/<slug>-<kind>-<NN>.jpg,
and adds a figure under "## Photos" in the recipe, creating the section and the
kind subheading (Recipe Card / Finished Dish / Preparation Steps) if needed.
Nothing else in the recipe file is changed. Re-running is safe: images whose
converted bytes already exist for that recipe are skipped.

Needs pillow and pillow-heif (requirements-tools.txt).
"""
import argparse
import hashlib
import html
import io
import os
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageCms, ImageOps
import pillow_heif

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
KINDS = {  # kind -> (subheading, default alt)
    "card": ("Recipe Card", "Original recipe card"),
    "dish": ("Finished Dish", "Finished dish"),
    "step": ("Preparation Steps", "Preparation step {n}"),
}
ORDER = [KINDS[k][0] for k in KINDS]
MAX_EDGE, QUALITY = 1600, 82


def fail(msg):
    sys.exit(f"error: {msg}")


def find_recipe(arg):
    p = Path(arg)
    if p.suffix == ".md" or p.is_file():
        if not p.is_file():
            fail(f"recipe file not found: {arg}")
        return p.resolve()
    hits = sorted((ROOT / "docs" / "recipes").glob(f"*/{arg}.md"))
    if not hits:
        fail(f"no recipe with slug '{arg}' under docs/recipes/*/")
    if len(hits) > 1:
        fail("ambiguous slug '%s': %s" % (arg, ", ".join(str(h) for h in hits)))
    return hits[0].resolve()


def convert(path, rotate):
    """Return (jpeg bytes, (w, h)) for one source image."""
    try:
        img = Image.open(path)
        img.load()
    except Exception as e:
        fail(f"cannot read image {path}: {e}")
    profile = img.info.get("icc_profile")
    img = ImageOps.exif_transpose(img)
    if rotate:
        img = img.rotate(-rotate, expand=True)  # clockwise
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGB", img.size, "white")
        bg.paste(img, mask=img.split()[-1])
        img = bg
    img = img.convert("RGB") if img.mode != "RGB" else img
    if profile:  # e.g. iPhone Display P3 -> sRGB, since the profile is stripped
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(profile))
            img = ImageCms.profileToProfile(img, src, ImageCms.createProfile("sRGB"))
        except Exception:
            pass
    if max(img.size) > MAX_EDGE:
        img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=QUALITY, progressive=True, optimize=True)  # no exif/icc
    return buf.getvalue(), img.size


def figure(rel, alt, caption):
    alt = alt.replace("[", "(").replace("]", ")")
    lines = ["<figure markdown>", f"  ![{alt}]({rel}){{ loading=lazy }}"]
    if caption:
        lines.append(f"  <figcaption>{html.escape(caption, quote=False)}</figcaption>")
    lines.append("</figure>")
    return lines


def footer_index(lines):
    """Index of the closing '---' footer line, or None."""
    start = 0
    if lines and lines[0].strip() == "---":  # skip front matter
        start = next((i + 1 for i in range(1, len(lines)) if lines[i].strip() == "---"), 0)
    for i in range(len(lines) - 1, start - 1, -1):
        if lines[i].strip() == "---":
            return i if not any(l.startswith("#") for l in lines[i + 1:]) else None
    return None


def last_content(lines, lo, hi):
    """Index just after the last non-blank line in lines[lo:hi]."""
    i = hi
    while i > lo and not lines[i - 1].strip():
        i -= 1
    return i


def add_figures(text, new_by_kind):
    """new_by_kind: {subheading: [figure line lists]} -> new recipe text."""
    lines = text.split("\n")
    foot = footer_index(lines)
    ph = next((i for i, l in enumerate(lines) if l.strip() == "## Photos"), None)

    def block(heading, figs):
        out = ["### " + heading, ""]
        for f in figs:
            out += f + [""]
        return out

    if ph is None:
        new = ["## Photos", ""]
        for h in ORDER:
            if h in new_by_kind:
                new += block(h, new_by_kind[h])
        if foot is None:
            base = text if text.endswith("\n") else text + "\n"
            if not base.endswith("\n\n"):
                base += "\n"
            return base + "\n".join(new)
        pre = [""] if lines[foot - 1].strip() else []
        return "\n".join(lines[:foot] + pre + new + lines[foot:])

    for h in ORDER:
        figs = new_by_kind.get(h)
        if not figs:
            continue
        end = foot if foot is not None and foot > ph else next(
            (i for i in range(ph + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        subs = {lines[i].strip()[4:]: i for i in range(ph + 1, end) if lines[i].startswith("### ")}
        ins = []
        for f in figs:
            ins += [""] + f
        if h in subs:
            nxt = min([i for i in range(subs[h] + 1, end) if lines[i].startswith("### ")] or [end])
            at = last_content(lines, subs[h] + 1, nxt)
            lines[at:at] = ins
        else:
            later = [subs[x] for x in ORDER[ORDER.index(h) + 1:] if x in subs]
            if later:
                lines[later[0]:later[0]] = block(h, figs)
            else:
                at = last_content(lines, ph + 1, end)
                lines[at:at] = [""] + block(h, figs)[:-1]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Attach photos to a recipe page (see module docstring).",
        epilog="Put originals in .scratch/incoming/ (git-ignored). Then rebuild with ./rebuild.sh.")
    ap.add_argument("recipe", help="path to the recipe .md, or its slug")
    ap.add_argument("kind", choices=list(KINDS), help="card | dish | step")
    ap.add_argument("images", nargs="+", help="HEIC/HEIF/JPG/PNG files")
    ap.add_argument("--caption", help="caption (and alt text) for these images")
    ap.add_argument("--rotate", type=int, choices=(90, 180, 270),
                    help="extra clockwise rotation, applied after EXIF orientation")
    ap.add_argument("--assets-dir", type=Path, default=ROOT / "docs/assets/recipe-images",
                    help="image root (default docs/assets/recipe-images; mainly for testing)")
    a = ap.parse_args()

    recipe = find_recipe(a.recipe)
    slug = recipe.stem
    outdir = a.assets_dir.resolve() / slug
    heading, default_alt = KINDS[a.kind]
    text = recipe.read_bytes().decode("utf-8")

    seen = {hashlib.sha256(p.read_bytes()).hexdigest()
            for p in outdir.glob("*.jpg")} if outdir.is_dir() else set()
    nums = [int(m.group(1)) for p in outdir.glob(f"{slug}-{a.kind}-*.jpg")
            if (m := re.fullmatch(rf"{re.escape(slug)}-{a.kind}-(\d+)\.jpg", p.name))] \
        if outdir.is_dir() else []
    n = max(nums, default=0)

    to_write, figs = [], []
    for src in a.images:
        sp = Path(src)
        if not sp.is_file():
            fail(f"image not found: {src}")
        data, size = convert(sp, a.rotate)
        digest = hashlib.sha256(data).hexdigest()
        if digest in seen:
            print(f"skip   {sp.name}: duplicate of an image already attached to {slug}")
            continue
        seen.add(digest)
        n += 1
        name = f"{slug}-{a.kind}-{n:02d}.jpg"
        rel = Path(os.path.relpath(outdir / name, recipe.parent)).as_posix()
        alt = a.caption or default_alt.format(n=n)
        figs.append(figure(rel, alt, a.caption))
        to_write.append((outdir / name, data))
        print(f"wrote  {name}: {sp.stat().st_size:,} B -> {len(data):,} B, {size[0]}x{size[1]}")

    if not to_write:
        print("nothing to add")
        return
    new_text = add_figures(text, {heading: figs})

    written = []
    try:
        outdir.mkdir(parents=True, exist_ok=True)
        for path, data in to_write:
            path.write_bytes(data)
            written.append(path)
        fd, tmp = tempfile.mkstemp(dir=recipe.parent, suffix=".tmp")
        with os.fdopen(fd, "wb") as f:
            f.write(new_text.encode("utf-8"))
        os.replace(tmp, recipe)
    except Exception as e:
        for p in written:
            p.unlink(missing_ok=True)
        fail(f"could not update recipe, rolled back images: {e}")
    print(f"updated {recipe} under '### {heading}':")
    for f in figs:
        print("\n".join("  + " + l for l in f))


if __name__ == "__main__":
    main()
