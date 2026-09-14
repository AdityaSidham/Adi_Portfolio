#!/usr/bin/env python3
"""Render index.html from index_template.html. Run: python3 .build/build_index.py"""
import pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import art

t = (HERE / "index_template.html").read_text(encoding="utf-8")
t = t.replace("{{SPRITE}}", (HERE / "sprite.html").read_text(encoding="utf-8"))
t = t.replace("{{ART_HERO}}", art.constellation(11, label="pose · 33 pts"))
t = t.replace("{{ART_EXP}}", art.constellation(29, label="2020 → now"))
t = t.replace("{{ART_HL}}", art.constellation(43, n=11, label="milestones"))
t = t.replace("{{ART_RINGS}}", art.rings())
assert "{{" not in t, t[t.index("{{"):t.index("{{") + 60]
(HERE.parent / "index.html").write_text(t, encoding="utf-8")
print("wrote index.html", len(t))
