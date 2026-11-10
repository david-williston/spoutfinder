#!/usr/bin/env python3
"""Draw the two figures on the Architecture page as CAD-style SVG."""
import math, pathlib

HERE = pathlib.Path(__file__).parent / "content/architecture"
FONT = 'font-family="VT323, monospace"'

def frame(w, h, body):
    dots = "".join(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#303030"/>'
                   for x in range(20, w, 20) for y in range(20, h, 20))
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" {FONT} role="img" '
            f'aria-label="__ALT__"><rect width="{w}" height="{h}" fill="#000"/>{dots}{body}</svg>')

def circ(cx, cy, r, col, dash=False):
    d = ' stroke-dasharray="4 3"' if dash else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="1.6"{d}/>'

def text(x, y, s, col="#c8c8c8", size=17, anchor="middle"):
    return f'<text x="{x}" y="{y}" fill="{col}" font-size="{size}" text-anchor="{anchor}">{s}</text>'

# ---- Figure 1: the area test ----------------------------------------------
W, H = 820, 330
R = 42
cases = [
    ("1  FITS", 150, "#00e000", "overlap = 100% of the circle", "difference 0%  <  2%  ->  VALID", "inside"),
    ("2  STRADDLES THE EDGE", 410, "#ff3030", "overlap = 62% of the circle", "difference 38%  >  2%  ->  REJECTED", "edge"),
    ("3  OUTSIDE", 670, "#ff3030", "no overlap: SOLINT returns nil", "nothing to measure  ->  REJECTED", "out"),
]
b = []
for title, cx, col, l1, l2, kind in cases:
    cy = 130
    # pocket surface region: a slab whose right edge is at x_edge
    left, top, bot = cx - 105, 50, 210
    if kind == "inside":
        xe = cx + 95
    elif kind == "edge":
        xe = cx + 12
    else:
        xe = cx - 75
    b.append(f'<rect x="{left}" y="{top}" width="{xe-left}" height="{bot-top}" fill="none" stroke="#00e5e5" stroke-width="1.6"/>')
    # overlap region hatched
    cxs = cx + (0 if kind != "out" else 0)
    cc = cx
    if kind == "inside":
        b.append(f'<circle cx="{cc}" cy="{cy}" r="{R}" fill="{col}" fill-opacity="0.22" stroke="none"/>')
    elif kind == "edge":
        b.append(f'<clipPath id="c{cx}"><rect x="{left}" y="{top}" width="{xe-left}" height="{bot-top}"/></clipPath>')
        b.append(f'<circle cx="{cc}" cy="{cy}" r="{R}" fill="#f5e400" fill-opacity="0.30" clip-path="url(#c{cx})"/>')
    b.append(circ(cc, cy, R, col, dash=(kind != "inside")))
    b.append(f'<path d="M{cc-5} {cy}h10M{cc} {cy-5}v10" stroke="{col}"/>')
    b.append(text(cx, 36, title, "#e040e0", 18))
    b.append(text(cx, 236, l1, "#c8c8c8", 16))
    b.append(text(cx, 258, l2, col, 16))
b.append(text(410, 300, "area test in CHECK:  VALID if  (valid area - overlap area)  <  valid area x accuracy      valid area = pi d^2 / 4      default accuracy = 0.02", "#f5e400", 15))
open(HERE / "area-test.svg", "w").write(frame(W, H, "".join(b)).replace("__ALT__", "Three spouts against a pocket: one fully inside is valid, one straddling the pocket edge is rejected because its overlap is short of a full circle, one fully outside is rejected"))

# ---- Figure 2: how the grid is walked --------------------------------------
W, H = 820, 330
b = []
x0, y0 = 120, 70
pitch, inc = 44, 76
cols, rows = 4, 6   # incs columns (x) by spouts rows (y)
# pocket outline (a tilted polygon to suggest a pocket)
poly = [(100, 56), (470, 40), (520, 230), (260, 262), (100, 200)]
b.append('<polygon points="' + " ".join(f"{x},{y}" for x, y in poly) + '" fill="none" stroke="#00e5e5" stroke-width="1.6"/>')
def inside(px, py):
    n = len(poly); c = False
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        if (ya > py) != (yb > py) and px < (xb - xa) * (py - ya) / (yb - ya) + xa:
            c = not c
    return c
pts = []
for i in range(cols + 2):
    for j in range(rows):
        px, py = x0 + i * inc, 62 + j * pitch
        pts.append((i, j, px, py))
for i, j, px, py in pts:
    ok = inside(px, py) and all(inside(px + 14 * math.cos(t), py + 14 * math.sin(t)) for t in [k * math.pi / 3 for k in range(6)])
    b.append(circ(px, py, 14, "#00e000" if ok else "#ff3030", dash=not ok))
# walk arrows: down each column by pitch, then step right by inc
b.append(f'<path d="M{x0} 62 v{(rows-1)*pitch} m0 -{(rows-1)*pitch} h{inc} v{(rows-1)*pitch}" fill="none" stroke="#f5e400" stroke-width="1" stroke-dasharray="5 4"/>')
b.append(f'<path d="M{x0-8} 94 l8 8 l8 -8" fill="none" stroke="#f5e400"/>')
b.append(f'<path d="M{x0+30} 54 l8 8 l-8 8" fill="none" stroke="#f5e400"/>')
b.append(text(x0 - 12, 50, "stp = (0,0)", "#f5e400", 15, "end"))
# legend / labels on the right
lx = 560
b.append(text(lx, 52, "NEXTSPOUT", "#e040e0", 18, "start"))
b.append(text(lx, 72, "y = y + pitch", "#c8c8c8", 16, "start"))
b.append(text(lx, 108, "NEXTROW", "#e040e0", 18, "start"))
b.append(text(lx, 128, "x = x + inc,  y = 0", "#c8c8c8", 16, "start"))
b.append(text(lx, 164, "BUILDLIST", "#e040e0", 18, "start"))
b.append(text(lx, 184, "append pocket id or 0", "#c8c8c8", 16, "start"))
b.append(text(lx, 220, "repeat spouts x increments", "#f5e400", 16, "start"))
b.append(text(lx, 240, "times, for each pocket", "#f5e400", 16, "start"))
b.append(text(410, 300, "green = valid location (pocket id stored)    dashed red = invalid (0 stored)", "#c8c8c8", 15))
open(HERE / "grid-walk.svg", "w").write(frame(W, H, "".join(b)).replace("__ALT__", "A grid of spouts walked column by column across a pocket outline; circles that fit are green and the rest are dashed red"))
print("figures written")
