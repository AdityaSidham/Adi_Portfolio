#!/usr/bin/env python3
"""Export the six hero zoom layers from the raw Runway generations.

Needs Pillow (not part of the site; run it from any venv that has it):
    python .build/hero_layers.py

Reads review/raw/ (gitignored, never shipped) and writes assets/img/hero/:
    z{n}-d.webp   full frame, 2560 wide        (large or high-DPI landscape screens)
    z{n}-m.webp   full frame, 1600 wide        (smaller landscape screens)
    z{n}-p.webp   center half of the frame, full height, native resolution
                  (portrait screens only ever see the middle of a 16:9 frame)
    hero-poster.jpg / hero-poster-p.jpg        first frame, painted before any JS
    hero-rest.jpg                              the resting frame, reused in Contact

The soft masks that blend each layer into its parent are drawn live in
assets/js/hero.js, so these files stay opaque. The geometry the page needs lives
in HERO_LAYERS in build_index.py; keep the two in step.
"""
import pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "review" / "raw"
OUT = ROOT / "assets" / "img" / "hero"

LAYERS = [
    ("z0", "L0hills-v1.png"),
    ("z1", "L1skyline-v1.png"),
    ("z2", "L2facade-v1.png"),
    ("z3", "L3desk-v1.png"),
    ("z4", "L4field-v1.png"),
    ("z5", "L4-v1.png"),
]
P_CROP = 0.5  # keep in step with HERO_P_CROP in the template


def save(img, path, q):
    img.save(path, "WEBP", quality=q, method=6)
    print(f"  {path.relative_to(ROOT)}  {path.stat().st_size // 1024} KB")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, raw in LAYERS:
        src = Image.open(RAW / raw).convert("RGB").resize((2752, 1536), Image.LANCZOS)
        cw = round(2752 * P_CROP)
        centre = src.crop(((2752 - cw) // 2, 0, (2752 + cw) // 2, 1536))
        print(name)
        save(src.resize((2560, 1429), Image.LANCZOS), OUT / f"{name}-d.webp", 80)
        save(src.resize((1600, 893), Image.LANCZOS), OUT / f"{name}-m.webp", 78)
        save(centre, OUT / f"{name}-p.webp", 78)
        if name == "z0":
            src.resize((1600, 893), Image.LANCZOS).save(OUT / "hero-poster.jpg", quality=82, optimize=True, progressive=True)
            centre.resize((688, 768), Image.LANCZOS).save(OUT / "hero-poster-p.jpg", quality=80, optimize=True, progressive=True)
        if name == "z5":
            src.resize((1920, 1072), Image.LANCZOS).save(OUT / "hero-rest.jpg", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    main()
