#!/usr/bin/env python3
"""Generate the home-page drawing: a shoe sole seen from below, split into
mold pockets, with a grid of spouts (green = fits, dashed red = rejected).
Writes layouts/_partials/home_info.html."""
import math, pathlib

W, H = 800, 400
X0, X1, CY, VS = 50, 750, 190, 1.7   # sole spans x0..x1, centre line y, vertical scale

TOP = [(0, 44), (.10, 47), (.25, 50), (.40, 48), (.55, 56), (.72, 70), (.85, 66), (.94, 46), (1, 40)]
BOT = [(0, 44), (.10, 45), (.25, 41), (.40, 17), (.50, 13), (.60, 33), (.72, 63), (.85, 70), (.94, 52), (1, 40)]

def interp(pts, t):
    for (a, ya), (b, yb) in zip(pts, pts[1:]):
        if a <= t <= b:
            u = (t - a) / (b - a)
            u = (1 - math.cos(math.pi * u)) / 2
            return ya + (yb - ya) * u
    return 0

def end(t):
    def cap(u):  # quarter-ellipse rounding, u in 0..1
        u = max(0.0, min(1.0, u))
        return math.sqrt(1 - (1 - u) ** 2)
    return min(cap(t / .09), cap((1 - t) / .16))

def yt(x):
    t = (x - X0) / (X1 - X0)
    return CY - interp(TOP, t) * VS * end(t)

def yb(x):
    t = (x - X0) / (X1 - X0)
    return CY + interp(BOT, t) * VS * end(t)

def tx(t): return X0 + t * (X1 - X0)

# sole outline
xs = [X0 + i * (X1 - X0) / 240 for i in range(241)]
outline = [(x, yt(x)) for x in xs] + [(x, yb(x)) for x in reversed(xs)]

# pockets: (name, t_start, t_end)
M = 11
POCKETS = [("HEEL", .07, .31), ("ARCH", .37, .50), ("FOREFOOT", .56, .93)]
def inside(px, py, a, b):
    return a + M <= px <= b - M and yt(px) + M <= py <= yb(px) - M

o = []
A = o.append
A(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The sole of a shoe seen from below, drawn in the style of AutoCAD: three mold pockets filled with a grid of pouring spouts, valid positions circled in green">')
A(f'<rect width="{W}" height="{H}" fill="#000"/>')
for x in range(20, W, 20):
    for y in range(20, H - 30, 20):
        A(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#303030"/>')
A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in outline) + '" fill="none" stroke="#f0f0f0" stroke-width="1.8"/>')

r, pitch = 9, 23
for name, ta, tb in POCKETS:
    a, b = tx(ta), tx(tb)
    sx = [a + M + i * (b - a - 2 * M) / 80 for i in range(81)]
    top = [(x, yt(x) + M) for x in sx]
    bot = [(x, yb(x) - M) for x in reversed(sx)]
    A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in top + bot) + '" fill="none" stroke="#00e5e5" stroke-width="1.5"/>')
    A(f'<text x="{(a + b) / 2:.0f}" y="{CY + 150}" fill="#e040e0" font-size="15" text-anchor="middle">{name}</text>')
    x = a + M + r
    while x < b - M:
        y = CY - 150
        while y < CY + 150:
            ring = [(x + r * math.cos(k * math.pi / 4), y + r * math.sin(k * math.pi / 4)) for k in range(8)]
            if all(inside(px, py, a, b) for px, py in ring):
                A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#00e000" stroke-width="1.4"/>')
                A(f'<path d="M{x-3:.0f} {y:.0f}h6M{x:.0f} {y-3:.0f}v6" stroke="#00e000" stroke-width="1"/>')
            elif inside(x, y, a - 4, b + 4) or any(inside(px, py, a, b) for px, py in ring):
                A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="none" stroke="#ff3030" stroke-width="1" stroke-dasharray="3 3"/>')
            y += pitch
        x += pitch

A('<path d="M60 380h23M60 374v12M83 374v12" stroke="#f5e400"/>')
A('<text x="92" y="386" fill="#f5e400" font-size="16">spout pitch</text>')
A('<text x="48" y="28" fill="#e040e0" font-size="17">LAYER: POCKETSURF / CELL</text>')
A('<text x="560" y="28" fill="#c8c8c8" font-size="17">AME SOLINT area test</text>')
A('<path d="M14 390V354M14 390H50" stroke="#f0f0f0" stroke-width="1.5"/>')
A('<path d="M14 354l-4 8M14 354l4 8M50 390l-8-4M50 390l-8 4" stroke="#f0f0f0"/>')
A('<text x="54" y="386" fill="#f0f0f0" font-size="15">X</text><text x="19" y="360" fill="#f0f0f0" font-size="15">Y</text>')
A('</svg>')

html = '''<article class="first-entry home-info">
    <header class="entry-header">
        <h1>{{ site.Params.homeInfoParams.Title | markdownify }}</h1>
    </header>
    <figure class="cad-screen">
''' + "\n".join(o) + '''
        <figcaption>A shoe sole seen from below, split into heel, arch and forefoot pockets. Green circles are spouts that fit; dashed red ones were rejected. Redrawn after the program's method.</figcaption>
    </figure>
    <div class="entry-content md-content">
        {{ $opts := dict "display" "block" }}
        {{ site.Params.homeInfoParams.Content | $.Page.RenderString $opts }}
    </div>
</article>
'''
(pathlib.Path(__file__).parent / "layouts/_partials/home_info.html").write_text(html)
print("wrote", len(html), "bytes")
