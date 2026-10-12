#!/usr/bin/env python3
"""Shared SVG art fragments for the portfolio (constellations, rings, landmarks)."""
import random

def constellation(seed, w=520, h=420, n=14, label=None, cls="constellation"):
    rnd = random.Random(seed)
    pts = [(rnd.uniform(30, w - 30), rnd.uniform(30, h - 30)) for _ in range(n)]
    # connect each point to its 2 nearest neighbours
    edges = set()
    for i, (x, y) in enumerate(pts):
        d = sorted(((x - a) ** 2 + (y - b) ** 2, j) for j, (a, b) in enumerate(pts) if j != i)
        for _, j in d[:2]:
            edges.add(tuple(sorted((i, j))))
    out = [f'<svg viewBox="0 0 {w} {h}" class="{cls}" aria-hidden="true">']
    for i, j in sorted(edges):
        out.append(f'<line class="edge" x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[j][0]:.0f}" y2="{pts[j][1]:.0f}"/>')
    accent = rnd.randrange(n)
    for k, (x, y) in enumerate(pts):
        c = "node is-accent" if k == accent else "node"
        r = 4 if k == accent else rnd.choice([2.5, 3, 3.5])
        out.append(f'<circle class="{c}" cx="{x:.0f}" cy="{y:.0f}" r="{r}"/>')
    if label:
        ax, ay = pts[accent]
        out.append(f'<text class="label" x="{ax + 10:.0f}" y="{ay - 8:.0f}">{label}</text>')
    out.append("</svg>")
    return "".join(out)

def rings():
    return ('<svg viewBox="0 0 400 400" aria-hidden="true">'
            '<circle cx="200" cy="200" r="60"/><circle cx="200" cy="200" r="110"/>'
            '<circle cx="200" cy="200" r="160"/><circle cx="200" cy="200" r="196"/>'
            '<circle class="n" cx="200" cy="40" r="4"/><circle class="n" cx="310" cy="200" r="3"/>'
            '</svg>')

# BlazePose's 33 landmarks placed by hand on aditya-la.jpg (1104x1380 pixels).
POSE_33 = [
    (564, 359), (550, 336), (544, 336), (537, 336), (577, 334), (584, 334), (590, 333),
    (524, 352), (620, 355), (552, 372), (585, 370),
    (465, 447), (705, 455), (437, 650), (725, 650), (462, 775), (695, 775),
    (452, 792), (706, 792), (466, 800), (690, 800), (474, 782), (684, 782),
    (492, 810), (668, 810), (505, 1060), (660, 1060), (500, 1290), (670, 1290),
    (482, 1322), (680, 1322), (452, 1348), (705, 1348),
]
POSE_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8), (9, 10),
    (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
    (27, 29), (28, 30), (29, 31), (30, 32), (27, 31), (28, 32),
]


def pose_svg():
    """The scan overlay: points appear top to bottom as --scan rises, then the bones draw."""
    out = ['<svg class="pose" viewBox="0 0 1104 1380" preserveAspectRatio="xMidYMid slice" aria-hidden="true">']
    for a, b in POSE_EDGES:
        (x1, y1), (x2, y2) = POSE_33[a], POSE_33[b]
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" pathLength="1"/>')
    for i, (x, y) in enumerate(POSE_33):
        t = 0.04 + (y - 330) / 1020 * 0.42
        r = 5 if i <= 10 or 17 <= i <= 22 else 8
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="--t:{t:.3f}"/>')
    out.append("</svg>")
    return "".join(out)


def portrait_landmarks():
    """Rough pose landmarks over the hero portrait (4:5 box, coords in %)."""
    P = {
        "nose": (52, 24), "ls": (36, 43), "rs": (70, 43), "le": (28, 60), "re": (80, 58),
        "lw": (62, 66), "rw": (44, 66), "lh": (42, 82), "rh": (64, 82),
    }
    E = [("ls", "rs"), ("ls", "le"), ("le", "lw"), ("rs", "re"), ("re", "rw"), ("ls", "lh"), ("rs", "rh"), ("lh", "rh"), ("nose", "ls"), ("nose", "rs")]
    out = ['<svg viewBox="0 0 100 125" preserveAspectRatio="none" aria-hidden="true">']
    for a, b in E:
        out.append(f'<line class="edge" x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" vector-effect="non-scaling-stroke"/>')
    for i, (k, (x, y)) in enumerate(P.items()):
        out.append(f'<circle class="node" cx="{x}" cy="{y}" r="1.1" style="animation-delay:{1.4 + i * 0.12:.2f}s"/>')
    out.append("</svg>")
    return "".join(out)

if __name__ == "__main__":
    print(constellation(7, label="tracking")[:200])
