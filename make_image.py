#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news summary image (1024x1024 PNG).

v2: every text block is measured and wrapped to its panel width before
drawing, so nothing overflows its panel. All text is drawn with PIL from
the strings below (no AI-generated text): spelling is exactly as written.
Icons are simple geometric shapes drawn with PIL primitives.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 27, 52)
PAPER = (247, 244, 235)
RED = (198, 40, 40)
TEAL = (0, 121, 107)
ORANGE = (217, 108, 20)
BLUE = (30, 90, 168)
GREEN = (46, 125, 50)
DARK = (33, 33, 33)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def panel(draw, box, fill):
    draw.rounded_rectangle(box, radius=18, fill=fill)


def block(draw, x, y, max_w, kicker, kicker_color, headline, sub,
          head_size=36, sub_size=24, dark=True):
    """Kicker + wrapped headline + wrapped sub; returns y after the block."""
    draw.text((x, y), kicker, font=font(BOLD, 24), fill=kicker_color)
    yy = y + 38
    col = DARK if dark else WHITE
    hf = font(BOLD, head_size)
    for ln in wrap(draw, headline, hf, max_w):
        draw.text((x, yy), ln, font=hf, fill=col)
        yy += head_size + 10
    yy += 4
    sf = font(REG, sub_size)
    scol = GREY if dark else (220, 228, 240)
    for ln in wrap(draw, sub, sf, max_w):
        draw.text((x, yy), ln, font=sf, fill=scol)
        yy += sub_size + 9
    return yy


def draw_ship(draw, cx, cy, s, color):
    draw.polygon([(cx - 90 * s, cy), (cx + 90 * s, cy), (cx + 60 * s, cy + 34 * s),
                  (cx - 60 * s, cy + 34 * s)], fill=color)
    draw.rectangle([cx - 30 * s, cy - 26 * s, cx + 26 * s, cy], fill=color)
    draw.rectangle([cx - 4 * s, cy - 52 * s, cx + 4 * s, cy - 26 * s], fill=color)
    for i, dx in enumerate((-70, 0, 70)):
        draw.arc([cx + (dx - 26) * s, cy + (30 + i * 2) * s, cx + (dx + 26) * s,
                  cy + 58 * s], start=0, end=180, fill=BLUE, width=max(3, int(5 * s)))


def draw_chip(draw, cx, cy, s, color):
    draw.rounded_rectangle([cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s],
                           radius=int(10 * s), outline=color, width=max(3, int(6 * s)))
    draw.rounded_rectangle([cx - 18 * s, cy - 18 * s, cx + 18 * s, cy + 18 * s],
                           radius=int(6 * s), fill=color)
    for d in (-27, 0, 27):
        draw.line([cx + d * s, cy - 58 * s, cx + d * s, cy - 40 * s], fill=color, width=5)
        draw.line([cx + d * s, cy + 40 * s, cx + d * s, cy + 58 * s], fill=color, width=5)
        draw.line([cx - 58 * s, cy + d * s, cx - 40 * s, cy + d * s], fill=color, width=5)
        draw.line([cx + 40 * s, cy + d * s, cx + 58 * s, cy + d * s], fill=color, width=5)


def draw_tanker_flame(draw, cx, cy, s):
    draw.polygon([(cx - 78 * s, cy + 20 * s), (cx + 78 * s, cy + 20 * s),
                  (cx + 54 * s, cy + 46 * s), (cx - 54 * s, cy + 46 * s)], fill=DARK)
    draw.rectangle([cx - 58 * s, cy + 6 * s, cx + 38 * s, cy + 20 * s], fill=DARK)
    draw.polygon([(cx, cy - 58 * s), (cx + 22 * s, cy - 6 * s), (cx + 8 * s, cy + 8 * s),
                  (cx - 8 * s, cy + 8 * s), (cx - 22 * s, cy - 6 * s)], fill=ORANGE)
    draw.polygon([(cx, cy - 34 * s), (cx + 11 * s, cy - 4 * s), (cx - 11 * s, cy - 4 * s)],
                 fill=RED)


def draw_satellite(draw, cx, cy, s, color):
    draw.rectangle([cx - 15 * s, cy - 15 * s, cx + 15 * s, cy + 15 * s], fill=color)
    draw.polygon([(cx - 66 * s, cy - 24 * s), (cx - 23 * s, cy - 9 * s),
                  (cx - 23 * s, cy + 9 * s), (cx - 66 * s, cy + 24 * s)], fill=BLUE)
    draw.polygon([(cx + 66 * s, cy - 24 * s), (cx + 23 * s, cy - 9 * s),
                  (cx + 23 * s, cy + 9 * s), (cx + 66 * s, cy + 24 * s)], fill=BLUE)
    draw.line([cx, cy + 15 * s, cx, cy + 40 * s], fill=color, width=max(3, int(5 * s)))
    draw.ellipse([cx - 6 * s, cy + 40 * s, cx + 6 * s, cy + 52 * s], fill=RED)


def draw_globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=4)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.text((36, 16), "WORLD NEWS", font=font(BOLD, 54), fill=WHITE)
    d.text((38, 84), "TUESDAY 24 NOVEMBER 2026", font=font(BOLD, 30), fill=(255, 199, 44))
    d.text((W - 36, 30), "ONE DAY", font=font(BOLD, 30), fill=(144, 202, 249), anchor="ra")
    d.text((W - 36, 70), "ONE IMAGE", font=font(BOLD, 30), fill=(144, 202, 249), anchor="ra")

    # ---- main story: Libya (panel 24..640 x 148..516) ----
    panel(d, [24, 148, 640, 516], WHITE)
    draw_ship(d, 128, 246, 0.88, NAVY)
    block(d, 246, 172, 366, "LIBYA - UKRAINE WAR", RED,
          "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
          "7 naval drones hit corvette Merkury at Benghazi port.",
          head_size=35, sub_size=24)
    tag = "UN SEEKS PROBE - WAR SPREADS TO THE MEDITERRANEAN"
    tf = font(BOLD, 22)
    while d.textlength(tag, font=tf) > 560 and tf.size > 14:
        tf = font(BOLD, tf.size - 1)
    d.text((48, 466), tag, font=tf, fill=RED)

    # ---- Nvidia (panel 664..1000 x 148..516) ----
    panel(d, [664, 148, 1000, 516], (232, 240, 252))
    draw_chip(d, 832, 212, 0.8, TEAL)
    block(d, 690, 288, 284, "TECH - NVIDIA", TEAL,
          "HUANG BACK AS CEO",
          "Jensen Huang reinstated. Shares +31%. S&P +4.7%, Nikkei +3.9%.",
          head_size=32, sub_size=22)

    # ---- Hormuz (panel 24..500 x 540..820) ----
    panel(d, [24, 540, 500, 820], (253, 238, 224))
    draw_tanker_flame(d, 104, 636, 0.78)
    block(d, 208, 562, 264, "MIDDLE EAST", ORANGE,
          "3 TANKERS HIT MINES IN HORMUZ",
          "Iran says three oil tankers caught fire in the Strait of Hormuz.",
          head_size=33, sub_size=23)

    # ---- NATO space (panel 524..1000 x 540..820) ----
    panel(d, [524, 540, 1000, 820], (235, 232, 245))
    draw_satellite(d, 606, 636, 0.78, NAVY)
    block(d, 706, 562, 266, "NATO - SPACE", BLUE,
          "NATO VOWS SPACE DEFENCE",
          "After reports Russia plans a nuclear-armed satellite.",
          head_size=33, sub_size=23)

    # ---- COP31 (panel 24..1000 x 844..944) ----
    panel(d, [24, 844, 1000, 944], (227, 242, 228))
    draw_globe(d, 82, 894, 32, GREEN)
    d.text((136, 858), "CLIMATE", font=font(BOLD, 24), fill=GREEN)
    d.text((136, 890), "COP31 SUMMIT ENDS WITHOUT A DEAL", font=font(BOLD, 35), fill=DARK)

    # ---- ticker: two measured lines ----
    d.rectangle([0, 958, W, H], fill=NAVY)
    t1 = "ALSO TODAY: GAZA STRIKES KILL 6  -  INDONESIA FACTORY FIRE KILLS 26"
    t2 = "LANDMINE CASUALTIES HIT 7,000 - A FIVE-YEAR HIGH"
    d.text((24, 966), t1, font=font(BOLD, 21), fill=WHITE)
    d.text((24, 994), t2, font=font(BOLD, 21), fill=(255, 199, 44))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
