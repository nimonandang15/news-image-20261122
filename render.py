#!/usr/bin/env python3
"""Render the 22 November 2026 world-news poster (1024x1024 PNG).

A broadsheet front page drawn with PIL + DejaVu only. Deterministic:
same script, same bytes (PIL writes no timestamps into PNG data).

Stories verified against live reporting on Sunday 22 Nov 2026
(EventGraph daily brief, AP, CNN, TBS News, BBC, Reuters):
- Ukraine's biggest attack of the year: Russia fires 110 missiles and
  over 400 drones; President Zelenskyy calls Putin a "killer"; a Russian
  cruise missile violates Polish airspace.
- Gulf on edge: Bahrain says Iran set fire to a civilian industrial
  site; two oil tankers are hit near the Strait of Hormuz; Iran claims
  it struck a US F-16 over the Gulf - US Central Command denies it.
- Sparta II ablaze in the Baltic: the Russian military-linked cargo
  ship is hit by drones, catches fire and drifts into Finnish waters;
  all 16 crew are evacuated; Finland says Ukraine was likely behind it.
- COP31 runs into overtime: climate talks in Antalya, Turkey, are
  extended a second day as countries split over fossil fuels and
  funding; the EU says it wants a good deal or no deal.
- "El Chapo Isidro" captured: Mexico seizes FBI most-wanted cartel
  boss Fausto Isidro Meza Flores in Guasave, Sinaloa; 11 people are
  killed in the firefight; he is flown to Mexico City.
- Quake shakes the Andes: a magnitude 6.7-6.8 earthquake hits Peru's
  Junin region; 15 people are injured, no deaths reported.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 230)
INK = (20, 18, 16)
NAVY = (24, 38, 68)
RED = (198, 12, 48)
TEAL = (13, 102, 102)
AMBER = (178, 108, 0)
SKY = (36, 110, 168)
GREY = (96, 90, 80)
CARD = (255, 255, 255)
GOLD = (214, 164, 32)
NIGHT = (16, 24, 48)
ORANGE = (232, 116, 0)
GREEN = (34, 120, 60)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


FB = lambda s: font("DejaVuSans-Bold.ttf", s)
FR = lambda s: font("DejaVuSans.ttf", s)
FSB = lambda s: font("DejaVuSerif-Bold.ttf", s)
FSR = lambda s: font("DejaVuSerif.ttf", s)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, text, fnt, x, y, max_w, fill, leading=None, max_lines=None):
    """Draw wrapped text; return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def burst(d, cx, cy, r, color):
    """Starburst: 8 spikes + filled core."""
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(cx, cy), (cx + int(r * math.cos(a)),
                           cy + int(r * math.sin(a)))],
               fill=color, width=5)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              fill=color)


def mountains(d, x0, y_base, x1, color):
    pts = [(x0, y_base)]
    n = 5
    step = (x1 - x0) // n
    for i in range(n):
        pts.append((x0 + step * i + step // 2,
                    y_base - (46 if i % 2 == 0 else 28)))
        pts.append((x0 + step * (i + 1), y_base))
    d.polygon(pts, fill=color)


def card(d, x, y, w, h, kicker_text, kicker_color, headline_text,
         body_text, head_size=25, body_size=16, head_lines=2,
         body_lines=4):
    """One story card; returns bottom y. Warns if text would overflow."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2, fill=CARD)
    ix, iy = x + 16, y + 14
    iw = w - 32
    d.text((ix, iy), kicker_text, font=FB(14), fill=kicker_color)
    iy += 22
    iy = para(d, headline_text, FSB(head_size), ix, iy, iw, INK,
              leading=int(head_size * 1.12), max_lines=head_lines)
    iy += 4
    iy = para(d, body_text, FR(body_size), ix, iy, iw, INK,
              leading=int(body_size * 1.3), max_lines=body_lines)
    if iy > y + h - 8:
        print(f"WARNING: card '{kicker_text}' overflows by "
              f"{iy - (y + h - 8)}px")
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 44  # margin

    # ---- Masthead ----
    d.text((M, 24), "THE WORLD IN ONE DAY", font=FSB(56), fill=INK)
    rule(d, M, 96, W - M, INK, 4)
    d.text((M, 108), "SUNDAY 22 NOVEMBER 2026", font=FB(24), fill=RED)
    right_tag = "ONE DAY  \u2022  ONE IMAGE"
    d.text((W - M - d.textlength(right_tag, font=FB(24)), 108),
           right_tag, font=FB(24), fill=NAVY)
    rule(d, M, 142, W - M, INK, 2)

    # ---- Lead story: Ukraine, with night-sky missile illustration ----
    y = 158
    d.text((M, y), "LEAD  \u2022  UKRAINE", font=FB(15), fill=RED)
    y += 24
    y = para(d, "Ukraine suffers its biggest attack of the year",
             FSB(38), M, y, 580, INK, leading=44, max_lines=2)
    y += 8
    y = para(d, "Russia fires 110 missiles and more than 400 drones in "
                "one night. President Zelenskyy calls Putin a "
                "\u201ckiller\u201d; a Russian cruise missile violates "
                "Polish airspace.",
             FR(18), M, y, 560, INK, leading=24, max_lines=4)
    # illustration: night sky, missile trails, bursts — drawn on its own
    # layer so nothing can spill past the box edge.
    ix0, iy0, ix1, iy1 = 640, 158, W - M, 386
    art = Image.new("RGB", (ix1 - ix0, iy1 - iy0), NIGHT)
    a = ImageDraw.Draw(art)
    rnd = random.Random(20261122)
    for _ in range(26):
        sx = rnd.randint(8, ix1 - ix0 - 8)
        sy = rnd.randint(8, iy1 - iy0 - 60)
        a.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=CARD)
    for (tx, ty, ang) in ((60, 172, -28), (160, 142, -38), (240, 182, -18)):
        ar = math.radians(ang)
        ex, ey = tx + int(150 * math.cos(ar)), ty + int(150 * math.sin(ar))
        a.line([(tx, ty), (ex, ey)], fill=GOLD, width=4)
        a.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=GOLD)
        burst(a, tx, ty, 26, ORANGE)
    a.rectangle([0, iy1 - iy0 - 26, ix1 - ix0, iy1 - iy0],
                fill=(10, 16, 32))
    a.text((12, iy1 - iy0 - 22), "110 missiles  \u2022  400+ drones",
           font=FB(14), fill=CARD)
    img.paste(art, (ix0, iy0))
    d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=2)
    d.text((M, 398), "Zelenskyy: \u201cPutin is a killer.\u201d  Trump, by "
           "contrast, calls Putin a friend who wants to end the war.",
           font=FSR(16), fill=GREY)
    rule(d, M, 428, W - M, INK, 2)

    # ---- Grid: 2 x 2 ----
    gy = 446
    gw, gh = 452, 196
    gx2 = M + gw + 32
    card(d, M, gy, gw, gh, "MIDDLE EAST  \u2022  THE GULF", RED,
         "Gulf on edge as tankers are hit",
         "Bahrain says Iran set fire to a civilian site; two oil "
         "tankers are struck near the Strait of Hormuz. Iran claims "
         "it hit a US F-16 \u2014 US Central Command denies it.",
         head_lines=2, body_lines=4)
    card(d, gx2, gy, gw, gh, "BALTIC SEA", NAVY,
         "Russian cargo ship ablaze after drone strike",
         "The Sparta II, a military-linked cargo ship under US "
         "sanctions, catches fire and drifts into Finnish waters. "
         "All 16 crew are evacuated; Finland says Ukraine was "
         "likely behind it.", head_lines=2, body_lines=4)
    gy += gh + 14
    card(d, M, gy, gw, gh, "CLIMATE  \u2022  COP31, ANTALYA", TEAL,
         "Climate talks run into overtime",
         "Negotiators in Turkey extend the summit a second day, "
         "split over fossil fuels and funding for poorer nations. "
         "The EU says it wants a good deal or no deal.",
         head_lines=2, body_lines=4)
    card(d, gx2, gy, gw, gh, "MEXICO  \u2022  SINALOA", AMBER,
         "\u201cEl Chapo Isidro\u201d captured",
         "Mexico seizes FBI most-wanted cartel boss Fausto Isidro "
         "Meza Flores in Guasave. Eleven people are killed in the "
         "firefight; he is flown to Mexico City.",
         head_lines=2, body_lines=4)

    # ---- Bottom strip: Peru quake, with drawn mountains + crack ----
    by = gy + gh + 14
    bh = 104
    d.rectangle([M, by, W - M, by + bh], outline=INK, width=2, fill=CARD)
    bx0, bx1 = W - M - 300, W - M
    d.rectangle([bx0, by, bx1, by + bh], fill=(232, 226, 210))
    mountains(d, bx0 + 8, by + bh - 18, bx1 - 8, (90, 90, 110))
    crack = [(bx0 + 60, by + 8), (bx0 + 90, by + 34), (bx0 + 70, by + 58),
             (bx0 + 104, by + 82), (bx0 + 88, by + bh - 10)]
    d.line(crack, fill=RED, width=5)
    d.line(crack, fill=(255, 255, 255), width=1)
    d.text((M + 16, by + 10), "NATURAL DISASTER  \u2022  PERU",
           font=FB(14), fill=GREEN)
    para(d, "Quake shakes the Andes", FSB(26), M + 16, by + 34, 560, INK,
         leading=30, max_lines=1)
    para(d, "A magnitude 6.7\u20136.8 earthquake hits the Jun\u00edn "
            "region; 15 people are injured and no deaths are reported.",
         FR(15), M + 16, by + 66, 560, INK, leading=18, max_lines=2)

    # ---- Footer ----
    fy = by + bh + 10
    rule(d, M, fy, W - M, INK, 2)
    d.text((M, fy + 8), "Sources: AP, CNN, TBS News, BBC, Reuters, "
           "EventGraph daily brief \u2014 22 Nov 2026",
           font=FR(13), fill=GREY)
    d.text((M, fy + 27), "Six stories, one day. Drawn from live "
           "reporting; no invented facts.", font=FR(13), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
