#!/usr/bin/env python3
"""Generate the home-page drawing from the prototype sole photograph.

The pink, teal and purple regions of the photo are traced into outlines, the
sole is turned on its side, and a grid of spouts is laid over it the way the
original program did: a spout is accepted (green) only if its whole circle
fits inside one region, otherwise it is rejected (dashed red).

Needs: pillow, numpy, scipy, matplotlib (for contourpy).
Writes layouts/_partials/home_info.html.
"""
import pathlib
import numpy as np
from PIL import Image
from matplotlib.colors import rgb_to_hsv
from scipy import ndimage as ndi
from contourpy import contour_generator

HERE = pathlib.Path(__file__).parent
PHOTO = HERE / "content/gallery/prototype-sole.jpg"

SCALE = 0.5            # photo px -> drawing units
OX, OY = 75, 48        # placement of the sole in the drawing
W, H = 820, 480
R, PITCH = 9, 23       # spout radius and pitch, drawing units

# ---- segment the photo ------------------------------------------------------
a = np.asarray(Image.open(PHOTO).convert("RGB")).astype(float) / 255
h = rgb_to_hsv(a)
Hh, S, V = h[..., 0], h[..., 1], h[..., 2]
Rr, Gg, Bb = a[..., 0], a[..., 1], a[..., 2]
pink = (Rr > .5) & (Rr - Gg > .18) & (Rr > Bb)
teal = (Bb > .30) & (Rr < .32) & (Gg > .22) & (Bb > Rr + .15) & (Hh > .45) & (Hh < .62)
purple = (Hh > .62) & (Hh < .80) & (S > .2) & (V > .28) & ~teal

def clean(m, close=3, open_=3):
    m = ndi.binary_closing(m, iterations=close)
    m = ndi.binary_fill_holes(m)
    m = ndi.binary_opening(m, iterations=open_)
    return m

pink = clean(pink)
teal = clean(teal)
# the logo band is a slightly bluish grey against the brown paper: pick it out on a lightly blurred copy
bl = np.stack([ndi.gaussian_filter(a[..., i] * 255, 2.0) for i in range(3)], -1)
d = bl[..., 2] - bl[..., 0]
purple = (d > 0) & (d < 32) & (bl[..., 2] > 42) & (bl[..., 1] < bl[..., 0] + 8)
purple[:560] = False
purple[960:] = False
purple = ndi.binary_opening(ndi.binary_fill_holes(ndi.binary_closing(purple, iterations=5)), iterations=4)
lab, n = ndi.label(purple)
sizes = ndi.sum(purple, lab, range(1, n + 1))
purple = np.isin(lab, [i + 1 for i, sz in enumerate(sizes) if sz > 2500])
purple &= ~(pink | teal)
shape = ndi.binary_fill_holes(ndi.binary_closing(pink | teal | purple, iterations=14))
shape = ndi.binary_opening(shape, iterations=6)

# lay the sole on its side (clockwise quarter turn)
rot = lambda m: np.rot90(m, k=-1)
layers = [("pink", rot(pink), "#e040e0"), ("teal", rot(teal), "#00e5e5"), ("purple", rot(purple), "#f5e400")]
shape = rot(shape)

def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a_, b_ = pts[0], pts[-1]
    v = b_ - a_
    d = np.abs(v[0] * (pts[:, 1] - a_[1]) - v[1] * (pts[:, 0] - a_[0])) / (np.linalg.norm(v) + 1e-9)
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([rdp(pts[: i + 1], eps)[:-1], rdp(pts[i:], eps)])
    return np.vstack([a_, b_])

def polygons(mask, min_area=500, eps=1.2):
    z = ndi.gaussian_filter(mask.astype(float), 1.2)
    out = []
    for line in contour_generator(z=z).lines(0.5):
        line = np.asarray(line)
        x, y = line[:, 0], line[:, 1]
        area = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        if area < min_area:
            continue
        k = int(np.argmax(np.linalg.norm(line - line[0], axis=1)))   # closed ring: split at the far point
        out.append(np.vstack([rdp(line[: k + 1], eps)[:-1], rdp(line[k:], eps)]))
    return out

def svgpts(p):
    return " ".join(f"{OX + x * SCALE:.1f},{OY + y * SCALE:.1f}" for x, y in p)

# ---- draw -------------------------------------------------------------------
o = []
A = o.append
A(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="The prototype sole drawn in the style of AutoCAD: each colored region is a mold pocket outlined on its own layer and filled with a grid of pouring spouts, valid positions circled in green">')
A(f'<rect width="{W}" height="{H}" fill="#000"/>')
for x in range(20, W, 20):
    for y in range(20, H - 30, 20):
        A(f'<rect x="{x}" y="{y}" width="1" height="1" fill="#303030"/>')
for p in polygons(shape, min_area=5000, eps=1.6):
    A(f'<polygon points="{svgpts(p)}" fill="none" stroke="#f0f0f0" stroke-width="1.8"/>')
for name, m, col in layers:
    for p in polygons(m):
        A(f'<polygon points="{svgpts(p)}" fill="none" stroke="{col}" stroke-width="1.5"/>')

# spouts: distance of each grid point to the edge of the region it sits in
union = layers[0][1] | layers[1][1] | layers[2][1]
dist = ndi.distance_transform_edt(union)
r_px, pitch_px = R / SCALE, PITCH / SCALE
margin = 3 / SCALE
hh, ww = union.shape
y = pitch_px / 2
while y < hh:
    x = pitch_px / 2
    while x < ww:
        d = dist[int(y), int(x)]
        cx, cy = OX + x * SCALE, OY + y * SCALE
        if d >= r_px + margin:
            A(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R}" fill="none" stroke="#00e000" stroke-width="1.4"/>')
            A(f'<path d="M{cx-3:.0f} {cy:.0f}h6M{cx:.0f} {cy-3:.0f}v6" stroke="#00e000" stroke-width="1"/>')
        elif d >= r_px * 0.55:
            A(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R}" fill="none" stroke="#ff3030" stroke-width="1" stroke-dasharray="3 3"/>')
        x += pitch_px
    y += pitch_px

A(f'<path d="M80 {H-18}h23M80 {H-24}v12M103 {H-24}v12" stroke="#f5e400"/>')
A(f'<text x="112" y="{H-12}" fill="#f5e400" font-size="16">spout pitch</text>')
A('<text x="48" y="28" fill="#e040e0" font-size="17">LAYER: POCKETSURF / CELL</text>')
A('<text x="590" y="28" fill="#c8c8c8" font-size="17">AME SOLINT area test</text>')
A(f'<path d="M14 {H-10}V{H-46}M14 {H-10}H50" stroke="#f0f0f0" stroke-width="1.5"/>')
A(f'<path d="M14 {H-46}l-4 8M14 {H-46}l4 8M50 {H-10}l-8-4M50 {H-10}l-8 4" stroke="#f0f0f0"/>')
A(f'<text x="54" y="{H-14}" fill="#f0f0f0" font-size="15">X</text><text x="19" y="{H-40}" fill="#f0f0f0" font-size="15">Y</text>')
A('</svg>')

html = '''<article class="first-entry home-info">
    <header class="entry-header">
        <h1>{{ site.Params.homeInfoParams.Title | markdownify }}</h1>
    </header>
    <figure class="cad-screen">
''' + "\n".join(o) + '''
        <figcaption>The prototype sole, traced from a photograph: each colored region is a mold pocket, and every green circle is a spout that fits entirely inside it. Dashed red ones were rejected. Redrawn after the program's method.</figcaption>
    </figure>
    <div class="entry-content md-content">
        {{ $opts := dict "display" "block" }}
        {{ site.Params.homeInfoParams.Content | $.Page.RenderString $opts }}
    </div>
</article>
'''
(HERE / "layouts/_partials/home_info.html").write_text(html)
print("wrote", len(html), "bytes")
