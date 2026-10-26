#!/usr/bin/env python3
"""Synthetic plan sets with a known answer.

Every set is drawn from exact geometry, and the answer key is computed from the
SAME geometry objects that drew the sheets - so there is no reading, guessing
or interpretation between the drawing and its truth. If the engine's number
differs from the key, the engine is wrong (or the drawing is ambiguous, which
the trap sets are built to test on purpose).

Conventions follow TAKEOFF_METHOD.md section 7:
  floor   = polygon area - floor-standing joinery (wall-hung vanities NOT taken off)
  walls   = run x tiled height - the part of every door/window inside the tiled band
  niche   = (w x h) + 2(d x h) + 2(w x d), reported on its own
  skirting = lineal metres, door widths taken off

    python3 backtest/synthetic/make_sets.py            # writes sets + answer_key.json
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import fitz

OUT = Path(__file__).resolve().parent / "sets"

A3 = fitz.Rect(0, 0, 1190.55, 841.89)
PT_PER_MM = 72 / 25.4
PLAN_S = PT_PER_MM / 20          # 1:20 on the sheet
ELEV_S = PT_PER_MM / 50          # 1:50 on the sheet
BLACK, GREY, LIGHT = (0, 0, 0), (0.45, 0.45, 0.45), (0.86, 0.86, 0.86)

ADDRESS = "14 Example Avenue, Epping NSW 2121"


# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

@dataclass
class Opening:
    kind: str        # "door" | "window"
    off: float       # mm from the wall's start point, along the wall
    w: float
    h: float
    sill: float = 0  # mm off the floor

    @property
    def label(self):
        tag = "DOOR" if self.kind == "door" else "WINDOW"
        return f"{tag} {self.w:.0f} x {self.h:.0f}"


@dataclass
class Niche:
    off: float
    sill: float
    w: float
    h: float
    d: float

    def area(self):
        return (self.w * self.h + 2 * self.d * self.h + 2 * self.w * self.d) / 1e6


@dataclass
class Wall:
    tile: tuple | None = None     # ("full", h) | ("splash", bottom, top, x0, x1) | ("skirting", h)
    openings: list = field(default_factory=list)
    niche: Niche | None = None
    marks: list = field(default_factory=list)   # extra plan breakpoints: (off, len, label)


@dataclass
class Room:
    name: str
    pts: list                     # clockwise on screen (y down), mm, internal face
    walls: list                   # one Wall per edge pts[i] -> pts[i+1]
    ceiling: float = 2400
    deductions: list = field(default_factory=list)   # (label, x, y, w, d) floor-standing
    fixtures: list = field(default_factory=list)     # (label, x, y, w, d) NOT deducted
    lines: list = field(default_factory=list)        # ((x0,y0),(x1,y1), label) e.g. screens

    def edges(self):
        n = len(self.pts)
        return [(self.pts[i], self.pts[(i + 1) % n]) for i in range(n)]


def run_of(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def polygon_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2 / 1e6


def band_overlap(z0, z1, a0, a1):
    return max(0.0, min(z1, a1) - max(z0, a0))


def wall_truth(room: Room, i: int):
    a, b = room.edges()[i]
    run = run_of(a, b)
    w = room.walls[i]
    if not w.tile:
        return 0.0, 0.0
    kind = w.tile[0]
    if kind == "full":
        z0, z1, x0, x1 = 0, w.tile[1], 0, run
    elif kind == "splash":
        _, z0, z1, x0, x1 = w.tile
    elif kind == "skirting":
        z0, z1, x0, x1 = 0, w.tile[1], 0, run
    area = (x1 - x0) * (z1 - z0)
    for o in w.openings:
        area -= band_overlap(x0, x1, o.off, o.off + o.w) * band_overlap(z0, z1, o.sill, o.sill + o.h)
    lm = 0.0
    if kind == "skirting":
        lm = run - sum(o.w for o in w.openings if o.kind == "door")
    return area / 1e6, lm / 1000


def room_truth(room: Room) -> dict:
    floor = polygon_area(room.pts) - sum(w * d for _, _, _, w, d in room.deductions) / 1e6
    walls, skirting_m, skirting_m2, niches = 0.0, 0.0, 0.0, 0.0
    per_wall = []
    for i, w in enumerate(room.walls):
        area, lm = wall_truth(room, i)
        if w.tile and w.tile[0] == "skirting":
            skirting_m += lm
            skirting_m2 += area
        else:
            walls += area
        if w.niche:
            niches += w.niche.area()
        per_wall.append({"wall": f"E{i + 1:02d}", "run_mm": run_of(*room.edges()[i]),
                         "tile": list(w.tile) if w.tile else None, "area_m2": round(area, 4)})
    return {"floor_m2": round(floor, 4), "wall_tile_m2": round(walls, 4),
            "niche_m2": round(niches, 4),
            "niche_opening_m2": round(sum(w.niche.w * w.niche.h for w in room.walls
                                          if w.niche) / 1e6, 4),
            "skirting_m": round(skirting_m, 4), "skirting_m2": round(skirting_m2, 4),
            "ceiling_mm": room.ceiling, "per_wall": per_wall}


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------

def text(page, x, y, s, size=7, rotate=0, color=BLACK, bold=False):
    page.insert_text((x, y), s, fontsize=size, rotate=rotate, color=color,
                     fontname="hebo" if bold else "helv")


def text_w(s, size=7):
    return fitz.get_text_length(s, fontname="helv", fontsize=size)


def chain(page, p0, p1, cuts, values, offset, size=7):
    """A dimension chain along p0->p1 (page points), pushed `offset` pt along its
    outward normal. cuts = page-point distances along the line where ticks go,
    values = the printed number for each segment between consecutive cuts."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = uy, -ux                    # outward for a clockwise polygon
    q0 = (p0[0] + nx * offset, p0[1] + ny * offset)
    q1 = (p1[0] + nx * offset, p1[1] + ny * offset)
    page.draw_line(q0, q1, color=GREY, width=0.4)
    horizontal = abs(ux) > abs(uy)
    for c in cuts:
        cx, cy = q0[0] + ux * c, q0[1] + uy * c
        page.draw_line((cx - 3, cy + 3), (cx + 3, cy - 3), color=BLACK, width=0.6)
        page.draw_line((cx - nx * 4, cy - ny * 4), (cx + nx * 2, cy + ny * 2),
                       color=GREY, width=0.3)
    for k, v in enumerate(values):
        mid = (cuts[k] + cuts[k + 1]) / 2
        mx, my = q0[0] + ux * mid, q0[1] + uy * mid
        s = f"{v:.0f}"
        if horizontal:
            text(page, mx - text_w(s, size) / 2, min(q0[1], q1[1]) - 2, s, size)
        else:
            text(page, min(q0[0], q1[0]) - 2, my + text_w(s, size) / 2, s, size, rotate=90)


def dims_for_wall(page, a, b, s, origin, breaks, overall_value, inner_off, outer_off,
                  override_values=None):
    """Segment chain (breaks are mm offsets along the wall) + an overall chain."""
    pa = (origin[0] + a[0] * s, origin[1] + a[1] * s)
    pb = (origin[0] + b[0] * s, origin[1] + b[1] * s)
    run = run_of(a, b)
    pts = [0.0] + sorted(x for x in breaks if 0 < x < run) + [run]
    if len(pts) > 2:
        vals = override_values or [pts[k + 1] - pts[k] for k in range(len(pts) - 1)]
        chain(page, pa, pb, [p * s for p in pts], vals, inner_off)
        chain(page, pa, pb, [0, run * s], [overall_value], outer_off)
    else:
        chain(page, pa, pb, [0, run * s], [overall_value], inner_off)


def title_block(page, sheet_no, title, scale, set_name, rev="A"):
    x0 = 1000
    page.draw_rect(fitz.Rect(x0, 20, 1172, 822), color=BLACK, width=0.8)
    text(page, x0 + 8, 40, "RESIDENTIAL ALTERATIONS", 8, bold=True)
    text(page, x0 + 8, 52, ADDRESS, 6.5)
    text(page, x0 + 8, 64, f"Project {set_name}", 6.5)
    notes = [
        "NOTES",
        "All dimensions in millimetres.",
        "Dimensions are to the finished face",
        "of the internal wall lining.",
        "Do not scale from the drawing.",
        "Heights are above finished floor (AFF).",
        "Waterproofing to AS 3740.",
        "Wall-hung vanities: floor tile runs under.",
    ]
    for k, n in enumerate(notes):
        text(page, x0 + 8, 100 + k * 10, n, 6.5, bold=(k == 0))
    page.draw_line((x0, 700), (1172, 700), color=BLACK, width=0.6)
    text(page, x0 + 8, 716, f"SCALE {scale} @ A3", 7)
    text(page, x0 + 8, 730, f"REV {rev}   DATE 12/05/2025", 7)
    text(page, x0 + 8, 760, title, 12, bold=True)
    text(page, x0 + 8, 800, sheet_no, 18, bold=True)


# ---------------------------------------------------------------------------
# sheets
# ---------------------------------------------------------------------------

def cover_sheet(doc, set_name, schedule):
    page = doc.new_page(width=A3.width, height=A3.height)
    title_block(page, "A000", "COVER SHEET", "NTS", set_name)
    text(page, 60, 80, "RESIDENTIAL ALTERATIONS - WET AREAS", 20, bold=True)
    text(page, 60, 104, ADDRESS, 11)
    text(page, 60, 150, "DRAWING SCHEDULE", 10, bold=True)
    for k, (no, t) in enumerate(schedule):
        text(page, 60, 168 + k * 14, f"{no}    {t}", 9)
    gen = ["GENERAL NOTES",
           "1. Floor tile to all wet areas shown. Wall tile as noted on the internal elevations.",
           "2. Tiling heights are as dimensioned on the internal elevations.",
           "3. Shower screens are frameless glass. Floor waste to each shower.",
           "4. Wall-hung vanities and basins are clear of the floor.",
           "5. Floor-standing joinery sits on a plinth; no floor tile under it.",
           "6. All dimensions to the finished face of the wall lining."]
    for k, g in enumerate(gen):
        text(page, 60, 300 + k * 14, g, 9, bold=(k == 0))
    return page


def plan_sheet(doc, rooms, sheet_no, title, set_name, chain_override=None, layout=None):
    page = doc.new_page(width=A3.width, height=A3.height)
    title_block(page, sheet_no, title, "1:20", set_name)
    origins = layout or []
    if not origins:
        x = 110
        for r in rooms:
            origins.append((x, 140))
            x += max(p[0] for p in r.pts) * PLAN_S + 150
    s = PLAN_S
    for r, org in zip(rooms, origins):
        poly = [(org[0] + x * s, org[1] + y * s) for x, y in r.pts]
        # wall: the internal face thick, a lining offset outside it
        page.draw_polyline(poly + [poly[0]], color=BLACK, width=2.2)
        cx = sum(p[0] for p in poly) / len(poly)
        cy = sum(p[1] for p in poly) / len(poly)
        text(page, cx - text_w(r.name, 8) / 2, cy, r.name, 8, bold=True)
        text(page, cx - text_w("FLOOR TILE", 6) / 2, cy + 10, "FLOOR TILE", 6, color=GREY)
        for (label, x, y, w, d) in r.deductions:
            rc = fitz.Rect(org[0] + x * s, org[1] + y * s, org[0] + (x + w) * s, org[1] + (y + d) * s)
            page.draw_rect(rc, color=BLACK, width=0.8, fill=LIGHT)
            text(page, rc.x0 + 3, rc.y0 + 9, label, 5.5)
        for (label, x, y, w, d) in r.fixtures:
            rc = fitz.Rect(org[0] + x * s, org[1] + y * s, org[0] + (x + w) * s, org[1] + (y + d) * s)
            page.draw_rect(rc, color=GREY, width=0.6, dashes="[2] 0")
            text(page, rc.x0 + 2, rc.y0 + 8, label, 5.5, color=GREY)
        for (p0, p1, label) in r.lines:
            q0 = (org[0] + p0[0] * s, org[1] + p0[1] * s)
            q1 = (org[0] + p1[0] * s, org[1] + p1[1] * s)
            page.draw_line(q0, q1, color=BLACK, width=0.9)
            text(page, (q0[0] + q1[0]) / 2 + 2, (q0[1] + q1[1]) / 2 - 3, label, 5.5)

        for i, ((a, b), w) in enumerate(zip(r.edges(), r.walls)):
            run = run_of(a, b)
            ux, uy = (b[0] - a[0]) / run, (b[1] - a[1]) / run
            nx, ny = uy, -ux
            breaks = []
            for o in w.openings:
                breaks += [o.off, o.off + o.w]
                ox0 = (org[0] + (a[0] + ux * o.off) * s, org[1] + (a[1] + uy * o.off) * s)
                ox1 = (org[0] + (a[0] + ux * (o.off + o.w)) * s,
                       org[1] + (a[1] + uy * (o.off + o.w)) * s)
                page.draw_line(ox0, ox1, color=(1, 1, 1), width=3.0)   # hole in the wall
                if o.kind == "door":
                    # leaf swung into the room
                    leaf_end = (ox0[0] - nx * o.w * s, ox0[1] - ny * o.w * s)
                    page.draw_line(ox0, leaf_end, color=BLACK, width=0.8)
                    mid = ((ox0[0] + ox1[0]) / 2 - nx * 14, (ox0[1] + ox1[1]) / 2 - ny * 14)
                    text(page, mid[0] - 10, mid[1], f"D{o.w:.0f}", 5.5)
                else:
                    for k in (-2, 0, 2):
                        page.draw_line((ox0[0] + nx * k, ox0[1] + ny * k),
                                       (ox1[0] + nx * k, ox1[1] + ny * k), color=BLACK, width=0.5)
                    mid = ((ox0[0] + ox1[0]) / 2 - nx * 10, (ox0[1] + ox1[1]) / 2 - ny * 10)
                    text(page, mid[0] - 10, mid[1], f"W{o.w:.0f}", 5.5)
            for (off, ln, _label) in w.marks:
                breaks += [off, off + ln]
            override = (chain_override or {}).get((r.name, i))
            dims_for_wall(page, a, b, s, org, breaks, run, 18, 34, override)
            # elevation tag inside the wall
            mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            tx = org[0] + mid[0] * s - nx * 22
            ty = org[1] + mid[1] * s - ny * 22
            page.draw_circle((tx, ty), 7, color=BLACK, width=0.5)
            text(page, tx - 5.5, ty + 2.5, f"E{i + 1:02d}", 5)
    return page


def elevation_panel(page, room, i, x, y, show_heights=True):
    """One developed internal elevation, bottom-left at (x, y)."""
    s = ELEV_S
    a, b = room.edges()[i]
    run = run_of(a, b)
    w = room.walls[i]
    W, H = run * s, room.ceiling * s
    frame = fitz.Rect(x, y - H, x + W, y)
    if w.tile:
        kind = w.tile[0]
        if kind in ("full", "skirting"):
            z0, z1, x0, x1 = 0, w.tile[1], 0, run
        else:
            _, z0, z1, x0, x1 = w.tile
        band = fitz.Rect(x + x0 * s, y - z1 * s, x + x1 * s, y - z0 * s)
        page.draw_rect(band, color=None, fill=LIGHT)
        label = {"full": "WALL TILE", "skirting": "300 TILE SKIRTING",
                 "splash": "TILED SPLASHBACK"}[kind]
        text(page, band.x0 + 3, band.y0 + 8, label, 5.5)
    if not w.tile or w.tile[0] != "full" or w.tile[1] < room.ceiling:
        text(page, x + 3, y - H + 9, "PAINT FINISH ABOVE / NOT TILED"
             if w.tile else "PAINT FINISH - NOT TILED", 5)
    page.draw_rect(frame, color=BLACK, width=0.9)

    hbreaks, vchains = [], []
    for o in w.openings:
        r = fitz.Rect(x + o.off * s, y - (o.sill + o.h) * s, x + (o.off + o.w) * s, y - o.sill * s)
        page.draw_rect(r, color=BLACK, width=0.7, fill=(1, 1, 1))
        text(page, r.x0 + 2, r.y0 + 8, o.label, 5)
        hbreaks += [o.off, o.off + o.w]
        if show_heights:
            parts = [p for p in (o.sill, o.h, room.ceiling - o.sill - o.h) if p > 0]
            vchains.append((o.off + o.w, parts))
    if w.niche:
        n = w.niche
        r = fitz.Rect(x + n.off * s, y - (n.sill + n.h) * s, x + (n.off + n.w) * s, y - n.sill * s)
        page.draw_rect(r, color=BLACK, width=0.7, fill=(0.95, 0.95, 0.95))
        text(page, x + 2, y - H - 14,
             f"NICHE {n.w:.0f}W x {n.h:.0f}H x {n.d:.0f}D, TILED ALL FACES", 5)
        hbreaks += [n.off, n.off + n.w]
        if show_heights:
            vchains.append((n.off + n.w, [n.sill, n.h, room.ceiling - n.sill - n.h]))
    if w.tile and w.tile[0] == "splash":
        hbreaks += [w.tile[3], w.tile[4]]
    for (off, ln, label) in w.marks:
        hbreaks += [off, off + ln]
        text(page, x + (off + 30) * s, y - 4, label, 4.8, color=GREY)

    # horizontal: segments + overall, under the panel
    pts = [0.0] + sorted({v for v in hbreaks if 0 < v < run}) + [run]
    if len(pts) > 2:
        # The line runs right->left so its outward normal points down (under the
        # panel). Distances along it are measured from the right-hand end.
        cuts = [(run - p) * s for p in reversed(pts)]
        segs = [pts[k + 1] - pts[k] for k in range(len(pts) - 1)]
        chain(page, (x + W, y), (x, y), cuts, list(reversed(segs)), 12)
        chain(page, (x + W, y), (x, y), [0, W], [run], 26)
    else:
        chain(page, (x + W, y), (x, y), [0, W], [run], 12)

    # vertical: tiled height + ceiling on the right edge
    if show_heights:
        zs = [0.0]
        if w.tile:
            k = w.tile[0]
            if k in ("full", "skirting"):
                zs.append(w.tile[1])
            else:
                zs += [w.tile[1], w.tile[2]]
        zs = sorted({z for z in zs if 0 <= z <= room.ceiling} | {room.ceiling})
        segs = [zs[k + 1] - zs[k] for k in range(len(zs) - 1)]
        # line runs bottom->top on the right side; outward normal = right
        if len(segs) > 1:
            chain(page, (x + W, y), (x + W, y - H), [z * s for z in zs], segs, -12)
            chain(page, (x + W, y), (x + W, y - H), [0, H], [room.ceiling], -26)
        else:
            chain(page, (x + W, y), (x + W, y - H), [0, H], [room.ceiling], -12)
        for (xo, parts) in vchains:
            zz = [0.0]
            for p in parts:
                zz.append(zz[-1] + p)
            chain(page, (x + xo * s + 6, y), (x + xo * s + 6, y - H), [z * s for z in zz], parts, 0)
    else:
        text(page, x + W + 4, y - H / 2, "TILE FULL HEIGHT", 5.5)

    side = ["NORTH", "EAST", "SOUTH", "WEST"]
    dx, dy = b[0] - a[0], b[1] - a[1]
    nx, ny = dy, -dx
    face = side[0] if ny < 0 else side[1] if nx > 0 else side[2] if ny > 0 else side[3]
    text(page, x, y + 44, f"E{i + 1:02d}  {room.name} - {face} WALL", 7, bold=True)
    text(page, x, y + 53, "INTERNAL ELEVATION   SCALE 1:50", 5.5, color=GREY)


def elevation_sheets(doc, rooms, first_no, set_name, show_heights=True):
    jobs = [(r, i) for r in rooms for i in range(len(r.walls))]
    sheets = []
    for k in range(0, len(jobs), 6):
        page = doc.new_page(width=A3.width, height=A3.height)
        names = sorted({r.name for r, _ in jobs[k:k + 6]})
        no = f"A{first_no + k // 6}"
        title_block(page, no, "INTERNAL ELEVATIONS", "1:50", set_name)
        text(page, 60, 50, " & ".join(names) + " - INTERNAL ELEVATIONS", 11, bold=True)
        for j, (r, i) in enumerate(jobs[k:k + 6]):
            col, row = j % 3, j // 3
            elevation_panel(page, r, i, 80 + col * 300, 300 + row * 330, show_heights)
        sheets.append(page)
    return sheets


# ---------------------------------------------------------------------------
# the cases
# ---------------------------------------------------------------------------

def s1_room():
    return Room(
        "MAIN BATHROOM",
        [(0, 0), (2400, 0), (2400, 2700), (0, 2700)],
        [Wall(("full", 2400), niche=Niche(1300, 1000, 600, 300, 100),
              marks=[(1500, 900, "SHOWER")]),
         Wall(("full", 2400), marks=[(0, 1000, "SHOWER")]),
         Wall(("full", 2400), openings=[Opening("door", 1400, 820, 2040)]),
         Wall(("full", 2400), marks=[(900, 900, "WALL HUNG VANITY")])],
        ceiling=2400,
        fixtures=[("WALL HUNG VANITY 900 x 500", 0, 900, 500, 900)],
        lines=[((1500, 0), (1500, 1000), "SCREEN"), ((1500, 1000), (2400, 1000), "")],
    )


def s2_room():
    return Room(
        "ENSUITE",
        [(0, 0), (3000, 0), (3000, 1700), (2100, 1700), (2100, 2500), (0, 2500)],
        [Wall(("full", 2100), openings=[Opening("window", 300, 1200, 900, 1200)],
              marks=[(1800, 1200, "SHOWER")]),
         Wall(("full", 2100), niche=Niche(400, 1100, 400, 400, 90),
              marks=[(0, 1200, "SHOWER")]),
         Wall(("full", 1200)),
         Wall(("full", 1200)),
         Wall(("full", 1200), openings=[Opening("door", 1000, 720, 2040)]),
         Wall(("full", 1200), marks=[(800, 1200, "WALL HUNG VANITY")])],
        ceiling=2400,
        fixtures=[("WALL HUNG VANITY 1200 x 460", 0, 500, 460, 1200)],
        lines=[((1800, 0), (1800, 1200), "SCREEN"), ((1800, 1200), (3000, 1200), "")],
    )


def s3_rooms():
    laundry = Room(
        "LAUNDRY",
        [(0, 0), (2000, 0), (2000, 1800), (0, 1800)],
        [Wall(("splash", 900, 1500, 200, 2000), marks=[(200, 1800, "BENCH 900 AFF")]),
         Wall(None),
         Wall(None, openings=[Opening("door", 600, 820, 2040)]),
         Wall(None)],
        ceiling=2400,
        deductions=[("FLOOR STANDING CABINETS 1800 x 600 ON PLINTH", 200, 0, 1800, 600)],
    )
    powder = Room(
        "POWDER ROOM",
        [(0, 0), (1200, 0), (1200, 1600), (0, 1600)],
        [Wall(("skirting", 300)),
         Wall(("skirting", 300)),
         Wall(("skirting", 300), openings=[Opening("door", 200, 720, 2040)]),
         Wall(("skirting", 300), marks=[(400, 450, "WALL HUNG BASIN")])],
        ceiling=2400,
        fixtures=[("WALL HUNG BASIN", 0, 400, 350, 450)],
    )
    return [laundry, powder]


def build(name, rooms, *, elevations=True, show_heights=True, chain_override=None,
          note=""):
    doc = fitz.open()
    sched = [("A000", "COVER SHEET"), ("A101", "FLOOR PLAN")]
    if elevations:
        n_el = math.ceil(sum(len(r.walls) for r in rooms) / 6)
        sched += [(f"A{201 + k}", "INTERNAL ELEVATIONS") for k in range(n_el)]
    cover_sheet(doc, name, sched)
    plan_sheet(doc, rooms, "A101", "FLOOR PLAN", name, chain_override=chain_override)
    if elevations:
        elevation_sheets(doc, rooms, 201, name, show_heights)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.pdf"
    doc.save(path, garbage=3, deflate=True)
    return path


def rasterise(src: Path, dst: Path, dpi=110):
    """A 'phone scan' - the same sheets as pictures, no text layer."""
    srcdoc, out = fitz.open(src), fitz.open()
    for p in srcdoc:
        pix = p.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        np_ = out.new_page(width=p.rect.width, height=p.rect.height)
        np_.insert_image(np_.rect, pixmap=pix)
    out.save(dst, garbage=3, deflate=True)


def main():
    key = {}

    def add(case, rooms, expect, path, **extra):
        key[case] = {"file": path.name, "expect_gate": expect,
                     "rooms": {r.name: room_truth(r) for r in rooms}, **extra}

    r1 = [s1_room()]
    add("S1_simple_bath", r1, "PASS", build("S1_simple_bath", r1),
        what="Rectangular bathroom, full-height tile, one door, one niche, wall-hung vanity.")

    r2 = [s2_room()]
    add("S2_L_ensuite", r2, "PASS", build("S2_L_ensuite", r2),
        what="L-shaped ensuite (6 walls), two tile heights, window inside the tiled band, "
             "door partly inside a 1200 band, niche.")

    r3 = s3_rooms()
    add("S3_laundry_powder", r3, "PASS", build("S3_laundry_powder", r3),
        what="Two rooms: laundry with floor-standing cabinets (taken off the floor) and a "
             "splashback only; powder room with 300 tile skirting only.")

    add("S4_floors_only", r2, "PARTIAL", build("S4_floors_only", r2, elevations=False),
        what="The S2 floor plan with no elevations - must come back floors only, no walls.",
        expect_behaviour="No wall tile numbers anywhere. Floor = S2 floor.")

    r5 = [s1_room()]
    # south wall (edge index 2) runs east->west: true segments 1400 | 820 | 180 = 2400.
    # The drawing prints the last one as 330 -> the chain sums to 2550, 150 mm over.
    add("S5_trap_bad_chain", r5, "PASS",
        build("S5_trap_bad_chain", r5, chain_override={("MAIN BATHROOM", 2): [1400, 820, 330]}),
        what="S1 with one plan sub-chain that doesn't add up (1400 + 820 + 330 = 2550 vs 2400).",
        expect_behaviour="Must raise the 150 mm discrepancy as a question. Must not silently "
                         "use 2550 anywhere.")

    r6 = [s1_room()]
    add("S6_trap_no_heights", r6, "PASS",
        build("S6_trap_no_heights", r6, show_heights=False),
        what="S1 with every height dimension removed from the elevations - 'tile full height' "
             "is written but no ceiling height is printed anywhere.",
        expect_behaviour="Floor still measurable. Wall tile must NOT go in the order total "
                         "as a firm number; the missing height must be a question. "
                         "Importing 2400 silently is a fail.")

    src = OUT / "S1_simple_bath.pdf"
    dst = OUT / "S7_scan.pdf"
    rasterise(src, dst)
    key["S7_scan"] = {"file": dst.name, "expect_gate": "FAIL", "rooms": {},
                      "what": "S1 as a picture-only PDF (a phone scan).",
                      "expect_behaviour": "Rejected at the gate. Nothing measured."}

    (OUT / "answer_key.json").write_text(json.dumps(key, indent=2), encoding="utf-8")
    for case, k in key.items():
        print(case, k["expect_gate"])
        for rn, t in k["rooms"].items():
            print(f"   {rn:14} floor {t['floor_m2']:.3f}  walls {t['wall_tile_m2']:.3f}  "
                  f"niche {t['niche_m2']:.3f}  skirting {t['skirting_m']:.2f} m")


if __name__ == "__main__":
    main()
