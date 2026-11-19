#!/usr/bin/env python3
"""Institutions icon in the eez.io mockup's isometric style (ops.svg / app.svg / infra.svg):
dark #161616 faces, #F2F2EC 1.1 outlines, one gradient element (here the pediment roof).
Projection matches the mockup: P(x,y,z) = ((x-y)*cos30, (x+y)*0.5 - z)."""
import math, sys

C, S = math.cos(math.pi / 6), 0.5
P = lambda x, y, z: ((x - y) * C, (x + y) * S - z)
STROKE = 'stroke="#F2F2EC" stroke-width="1.1" stroke-linejoin="round"'
out = []


def poly(pts, fill="#161616"):
    s = " ".join(f"{x:.2f},{y:.2f}" for x, y in (P(*p) for p in pts))
    out.append(f'<polygon points="{s}" fill="{fill}" {STROKE}/>')


def box(x0, x1, y0, y1, z0, z1, left="#161616", right="#161616", top="#161616"):
    # visible faces: +y (left on screen), +x (right on screen), top
    poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], left)
    poly([(x1, y1, z0), (x1, y0, z0), (x1, y0, z1), (x1, y1, z1)], right)
    poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top)


H = 17          # plinth half-size (same footprint as ops.svg)
box(-H, H, -H, H, 0, 5)                 # plinth
box(-H + 2, H - 2, -H + 2, H - 2, 5, 8)  # step
# columns on the step: a ring, drawn back to front
# only the two visible faces (+x and +y), so the colonnade reads cleanly
r, w = 11.5, 2.3
cols = sorted({(a, r) for a in (-r, 0, r)} | {(r, b) for b in (-r, 0, r)})
for a, b in sorted(cols, key=lambda c: c[0] + c[1]):
    box(a - w, a + w, b - w, b + w, 8, 23)
E = H - 2
box(-E, E, -E, E, 23, 27)               # entablature
# pediment: ridge along x at y=0
R = 36
poly([(-E, 0, R), (E, 0, R), (E, -E, 27), (-E, -E, 27)], "url(#eez-t)")   # back slope (seen from above)
poly([(-E, E, 27), (E, E, 27), (E, 0, R), (-E, 0, R)], "url(#eez-t)")     # front slope: the lit top, like the others
poly([(E, E, 27), (E, -E, 27), (E, 0, R)], "url(#eez-a)")                # gable end

xs, ys = [], []
import re
for p in out:
    for x, y in re.findall(r"(-?\d+\.\d+),(-?\d+\.\d+)", p):
        xs.append(float(x)); ys.append(float(y))
pad = 3
minx, maxx, miny, maxy = min(xs) - pad, max(xs) + pad, min(ys) - pad, max(ys) + pad
w_, h_ = maxx - minx, maxy - miny
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx:.2f} {miny:.2f} {w_:.2f} {h_:.2f}" width="{w_:.2f}" height="{h_:.2f}">'
       '<defs><linearGradient id="eez-t" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8CE8AB"/><stop offset="1" stop-color="#79B9B4"/></linearGradient>'
       '<linearGradient id="eez-a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#79B9B4"/><stop offset="1" stop-color="#3F2ACD"/></linearGradient>'
       '<linearGradient id="eez-b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6AA29E"/><stop offset="1" stop-color="#3725B4"/></linearGradient></defs>'
       + "".join(out) + "</svg>\n")
open(sys.argv[1] if len(sys.argv) > 1 else "inst.svg", "w").write(svg)
print(f"{w_:.1f} x {h_:.1f}")
