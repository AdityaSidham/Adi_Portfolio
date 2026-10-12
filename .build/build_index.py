#!/usr/bin/env python3
"""Render index.html from index_template.html. Run: python3 .build/build_index.py"""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import art

# Bump after any CSS, JS or hero image change so browsers fetch fresh files.
V = "20261012p"

# The public address (on the résumé). Canonical links and social cards point here.
SITE = "https://adityasidham.site/"

# One mobile menu for every page; case studies prefix the anchors with index.html.
MOBILE = [("work", "Work"), ("about", "About"), ("training", "Training"),
          ("experience", "Experience"), ("highlights", "Highlights"), ("contact", "Contact")]


def mobile_links(prefix=""):
    return "\n    ".join(f'<a href="{prefix}#{i}">{label}</a>' for i, label in MOBILE)

# Where each zoom layer's child sits inside it, measured from the Runway stills
# with a template match (box), plus how each child enters while the camera
# pushes through (enter). See design-package.md and hero_layers.py.
RUNNER = {"x": .345, "y": .18, "w": .31, "h": .65}
HERO_LAYERS = [
    {"name": "z0", "box": {"w": .16, "cx": .755, "cy": .44}, "chip": "downtown_la 0.98"},
    {"name": "z1", "box": {"w": .300, "cx": .504, "cy": .502}, "chip": "tower 0.96",
     "enter": {"fade": [.55, .88], "mask": {"type": "ellipse", "f": .6}, "solid": .9}},
    {"name": "z2", "box": {"w": .226, "cx": .5, "cy": .5}, "chip": "window_21f 0.94",
     "enter": {"fade": [.12, .55], "mask": {"type": "rect", "f": .12}, "solid": .72}},
    {"name": "z3", "box": {"w": .302, "cx": .5, "cy": .488}, "chip": "phone 0.97",
     "enter": {"fade": [.30, .72], "mask": {"type": "rect", "f": .035}, "solid": .78}},
    {"name": "z4", "box": {"w": .602, "cx": .5, "cy": .5}, "chip": "landmarks 33", "lock": RUNNER,
     "enter": {"fade": [.08, .45], "mask": {"type": "rect", "f": .05}, "solid": .62}},
    {"name": "z5", "chip": "pose 33/33", "lock": RUNNER,
     "enter": {"fade": [.10, .85], "mask": {"type": "ellipse", "f": .5}, "solid": .86}},
]

def main():
    t = (HERE / "index_template.html").read_text(encoding="utf-8")
    t = t.replace("{{SPRITE}}", (HERE / "sprite.html").read_text(encoding="utf-8"))
    t = t.replace("{{HERO_LAYERS}}", json.dumps(HERO_LAYERS, separators=(",", ":")))
    t = t.replace("{{POSE}}", art.pose_svg())
    t = t.replace("{{V}}", V)
    t = t.replace("{{SITE}}", SITE)
    t = t.replace("{{MOBILE_LINKS}}", mobile_links())
    assert "{{" not in t, t[t.index("{{"):t.index("{{") + 60]
    (HERE.parent / "index.html").write_text(t, encoding="utf-8")
    print("wrote index.html", len(t))


if __name__ == "__main__":
    main()
