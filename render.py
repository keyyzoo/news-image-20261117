#!/usr/bin/env python3
"""Render the 17 November 2026 world-news infographic (1024x1024 PNG).

Fully deterministic: all news text is baked in as constants, no network,
no randomness, no current time. Running this script twice produces
byte-identical output. Requires Pillow (build time only); the entry
program main.py is standard-library only.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "image.png")

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (248, 244, 233)
INK = (25, 25, 25)
RED = (180, 35, 24)
GRAY = (90, 90, 90)
DARK = (30, 30, 30)
SKY = (220, 233, 242)
SEA = (47, 111, 159)
ORANGE = (228, 87, 46)
GOLD = (242, 160, 7)
BLUE = (37, 99, 235)
GREEN = (46, 125, 50)
PURPLE = (124, 58, 237)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 56)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_DATE = font("DejaVuSans-Bold.ttf", 30)
F_HERO_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HERO_HEAD = font("DejaVuSerif-Bold.ttf", 42)
F_HERO_SUM = font("DejaVuSans.ttf", 17)
F_KICK = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSerif-Bold.ttf", 23)
F_SUM = font("DejaVuSans.ttf", 15)
F_JAPAN_HEAD = font("DejaVuSerif-Bold.ttf", 24)
F_TICK_TITLE = font("DejaVuSans-Bold.ttf", 14)
F_TICK = font("DejaVuSans.ttf", 13)
F_FOOT = font("DejaVuSans.ttf", 12)
F_CAP = font("DejaVuSerif.ttf", 12)


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(fnt):
    box = fnt.getbbox("Ay")
    return box[3] - box[1]


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_bridge(draw, x0, y0, x1, y1):
    """Stylised Kerch Bridge with a collapsed middle span."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    sea_y = y0 + int((y1 - y0) * 0.72)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    # waves
    for wx in range(x0 + 8, x1 - 8, 34):
        draw.arc([wx, sea_y - 6, wx + 26, sea_y + 10], 180, 360,
                 fill=(255, 255, 255), width=2)
    deck_y = y0 + int((y1 - y0) * 0.46)
    deck_h = 10
    gap_cx = (x0 + x1) // 2
    gap = 52
    # pylons
    for px in (x0 + 58, x1 - 58):
        draw.rectangle([px - 5, deck_y - 74, px + 5, deck_y], fill=INK)
        draw.line([px, deck_y - 74, px - 46, deck_y], fill=INK, width=2)
        draw.line([px, deck_y - 74, px + 46, deck_y], fill=INK, width=2)
    # deck, with the middle span missing
    draw.rectangle([x0, deck_y, gap_cx - gap // 2, deck_y + deck_h], fill=INK)
    draw.rectangle([gap_cx + gap // 2, deck_y, x1, deck_y + deck_h], fill=INK)
    # broken ends, tilted
    draw.polygon([(gap_cx - gap // 2, deck_y),
                  (gap_cx - gap // 2 - 14, deck_y + 26),
                  (gap_cx - gap // 2 - 6, deck_y + 28),
                  (gap_cx - gap // 2 + 4, deck_y + 8)], fill=INK)
    draw.polygon([(gap_cx + gap // 2, deck_y),
                  (gap_cx + gap // 2 + 14, deck_y + 26),
                  (gap_cx + gap // 2 + 6, deck_y + 28),
                  (gap_cx + gap // 2 - 4, deck_y + 8)], fill=INK)
    # explosion burst at the gap
    bx, by = gap_cx, deck_y - 6
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 12, 30
        a = math.radians(ang)
        x_a, y_a = bx + r1 * math.cos(a), by + r1 * math.sin(a)
        x_b, y_b = bx + r2 * math.cos(a), by + r2 * math.sin(a)
        draw.line([x_a, y_a, x_b, y_b], fill=ORANGE, width=5)
    draw.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=GOLD)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=ORANGE)
    # smoke puffs
    draw.ellipse([bx - 34, by - 52, bx - 10, by - 28], fill=(154, 160, 166))
    draw.ellipse([bx + 8, by - 58, bx + 34, by - 32], fill=(120, 126, 132))
    # debris in the water
    draw.rectangle([bx - 20, sea_y + 12, bx - 8, sea_y + 18], fill=INK)
    draw.rectangle([bx + 10, sea_y + 20, bx + 26, sea_y + 25], fill=INK)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 24

    # ---- top red rule -------------------------------------------------
    d.rectangle([M, y, M + CW, y + 3], fill=RED)
    y += 14

    # ---- masthead -----------------------------------------------------
    title = "THE WORLD IN ONE DAY"
    d.text(((W - F_TITLE.getlength(title)) / 2, y), title,
           font=F_TITLE, fill=INK)
    y += text_h(F_TITLE) + 8
    tag = "ONE DAY'S WORLD NEWS IN ONE IMAGE"
    d.text(((W - F_TAG.getlength(tag)) / 2, y), tag, font=F_TAG, fill=GRAY)
    y += text_h(F_TAG) + 10

    # ---- date band ----------------------------------------------------
    band_h = 56
    d.rectangle([M, y, M + CW, y + band_h], fill=RED)
    date = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - F_DATE.getlength(date)) / 2,
            y + (band_h - text_h(F_DATE)) // 2 - 2),
           date, font=F_DATE, fill=PAPER)
    y += band_h + 12

    # ---- hero: Kerch Bridge ------------------------------------------
    hero_text_w = 612
    hero_kick = "UKRAINE · CRIMEA"
    hero_head = "Ukraine strikes the Kerch Bridge"
    hero_sum = ("Missiles and drones hit the bridge linking Russia to "
                "occupied Crimea on Tuesday; part of a road section "
                "collapsed into the water and traffic was suspended. "
                "Kyiv says the attack took weeks to plan — the second "
                "straight day of strikes on the bridge.")
    head_lines = wrap(hero_head, F_HERO_HEAD, hero_text_w)
    sum_lines = wrap(hero_sum, F_HERO_SUM, hero_text_w)
    text_h_total = (text_h(F_HERO_KICK) + 10
                    + len(head_lines) * 48 + 8
                    + len(sum_lines) * 22)
    illus_w = 300
    illus_h = 196
    cap_h = 18
    hero_h = max(text_h_total, illus_h + cap_h) + 12
    hero_y0 = y
    tx = M + 4
    ty = y + 8
    d.text((tx, ty), hero_kick, font=F_HERO_KICK, fill=RED)
    ty += text_h(F_HERO_KICK) + 10
    ty = draw_lines(d, tx, ty, head_lines, F_HERO_HEAD, INK, 48)
    ty += 8
    draw_lines(d, tx, ty, sum_lines, F_HERO_SUM, INK, 22)
    ix0 = M + CW - illus_w
    iy0 = y + 8
    draw_bridge(d, ix0, iy0, ix0 + illus_w, iy0 + illus_h)
    d.text((ix0, iy0 + illus_h + 2), "The Kerch Bridge, Crimea.",
           font=F_CAP, fill=GRAY)
    y = hero_y0 + hero_h
    d.line([M, y, M + CW, y], fill=INK, width=2)
    y += 14

    # ---- stories grid, 2 columns x 2 rows ----------------------------
    stories = [
        ("ASIA · APEC SUMMIT", BLUE, "circle",
         "Trump arrives in Asia for APEC",
         "Donald Trump arrived in Asia for the APEC summit in Shenzhen. "
         "A trilateral meeting with Xi Jinping and Vladimir Putin on "
         "nuclear issues and Ukraine is planned."),
        ("MIDDLE EAST · STRAIT OF HORMUZ", ORANGE, "triangle",
         "Tankers hit by mines near Hormuz",
         "Oil tankers struck naval mines near the Strait of Hormuz and "
         "caught fire. The US struck Iran's Qeshm Island; Iran denies "
         "damage and claims retaliatory attacks on US assets in Bahrain."),
        ("EUROPE · MIGRATION", GREEN, "diamond",
         "Five nations plan Rwanda return hub",
         "Germany, Denmark, Austria, Greece and the Netherlands announced "
         "a joint return facility in Rwanda for rejected asylum seekers. "
         "Transfers could begin in 2027."),
        ("TECH · CHIPS", PURPLE, "bars",
         "US tightens chip curbs; Nvidia reports bumper earnings",
         "The US introduced new licensing rules for advanced processor "
         "sales to data centres in Southeast Asia. Nvidia reported strong "
         "earnings on Tuesday after Jensen Huang's exit."),
    ]
    col_w = (CW - 20) // 2
    cells = []
    for kick, colour, shape, head, summ in stories:
        hl = wrap(head, F_HEAD, col_w - 24)
        sl = wrap(summ, F_SUM, col_w - 24)
        cells.append((kick, colour, shape, hl, sl))
    for row in range(2):
        row_cells = cells[row * 2:(row + 1) * 2]
        row_h = 0
        for _, _, _, hl, sl in row_cells:
            hh = (text_h(F_KICK) + 8 + len(hl) * 29 + 6
                  + len(sl) * 20 + 8)
            row_h = max(row_h, hh)
        for col, (kick, colour, shape, hl, sl) in enumerate(row_cells):
            cx = M + col * (col_w + 20)
            cy = y
            mx, my = cx, cy + 2
            if shape == "circle":
                d.ellipse([mx, my, mx + 15, my + 15], fill=colour)
            elif shape == "triangle":
                d.polygon([(mx + 8, my), (mx + 16, my + 15),
                           (mx, my + 15)], fill=colour)
            elif shape == "diamond":
                d.polygon([(mx + 8, my), (mx + 16, my + 8),
                           (mx + 8, my + 16), (mx, my + 8)], fill=colour)
            else:  # bars
                for i, bh in enumerate((7, 12, 16)):
                    d.rectangle([mx + i * 6, my + 16 - bh,
                                 mx + i * 6 + 4, my + 16], fill=colour)
            d.text((mx + 22, cy), kick, font=F_KICK, fill=RED)
            cy += text_h(F_KICK) + 8
            cy = draw_lines(d, cx, cy, hl, F_HEAD, INK, 29)
            cy += 6
            draw_lines(d, cx, cy, sl, F_SUM, INK, 20)
        y += row_h
        if row == 0:
            y += 12

    # ---- Japan, full width -------------------------------------------
    y += 8
    d.line([M, y, M + CW, y], fill=INK, width=1)
    y += 12
    d.ellipse([M, y + 2, M + 15, y + 17], fill=RED)
    d.text((M + 22, y), "JAPAN · AIRSPACE", font=F_KICK, fill=RED)
    y += text_h(F_KICK) + 8
    japan_head = "Japan scrambles jets after Russian airspace violation"
    d.text((M, y), japan_head, font=F_JAPAN_HEAD, fill=INK)
    y += text_h(F_JAPAN_HEAD) + 6
    japan_sum = ("Japan scrambled fighter jets after two suspected Russian "
                 "aircraft violated its airspace on Tuesday morning. Tokyo "
                 "lodged a strong protest with Moscow.")
    jl = wrap(japan_sum, F_SUM, CW)
    y = draw_lines(d, M, y, jl, F_SUM, INK, 20)
    y += 10

    # ---- ticker band --------------------------------------------------
    tick_items = [
        ("UK, Australia, Canada and Italy urged Israel to open Gaza "
         "crossings for aid.", "Bitcoin stalled below $65,000 after a selloff."),
        ("US lost measles elimination status after 26 years; "
         "5,400+ cases.",
         "Gérard Depardieu pleaded guilty to a sexual assault charge "
         "in Paris."),
    ]
    tick_lines = []
    for left, right in tick_items:
        tick_lines.append(left + "  ▪  " + right)
    # safety: every ticker line must fit inside the dark band
    for line in tick_lines:
        assert F_TICK.getlength(line) <= CW - 28, "ticker overflow: %s" % line
    band_top = y
    band_h = (text_h(F_TICK_TITLE) + 8
              + len(tick_lines) * 19 + 8)
    d.rectangle([M, band_top, M + CW, band_top + band_h], fill=DARK)
    ty = band_top + 8
    d.text((M + 14, ty), "ALSO ON 17 NOVEMBER", font=F_TICK_TITLE, fill=GOLD)
    ty += text_h(F_TICK_TITLE) + 8
    for line in tick_lines:
        d.text((M + 14, ty), line, font=F_TICK, fill=PAPER)
        ty += 19
    y = band_top + band_h + 10

    # ---- footer -------------------------------------------------------
    foot = "All stories are events of Tuesday, 17 November 2026, as reported that day."
    d.text(((W - F_FOOT.getlength(foot)) / 2, y), foot,
           font=F_FOOT, fill=GRAY)
    y += text_h(F_FOOT) + 8
    assert y <= H - 8, "layout overflow: y=%d" % y

    img.save(OUT, format="PNG")
    data = open(OUT, "rb").read()
    print("wrote %s (%d bytes) sha256=%s"
          % (OUT, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
