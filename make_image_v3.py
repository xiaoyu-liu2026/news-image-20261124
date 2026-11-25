#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news summary image, v3 (1024x1024 PNG).

v3 redesign after round-2 judging (win rate 0.447): from a flat pastel
card layout to a bold breaking-news poster. A large illustrated hero
scene (warship on fire at night, seven drone boats approaching) carries
the main story; the other four stories sit in deep saturated panels on
a near-black band; a red ticker closes the page. All text is drawn with
PIL from the strings below (no AI-generated text). Deterministic: the
only randomness uses a fixed seed.
"""
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
CB = "/usr/share/fonts/truetype/noto/NotoSansDisplay-CondensedBlack.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

INK = (8, 10, 16)
WHITE = (255, 255, 255)
AMBER = (255, 199, 44)
RED = (206, 32, 32)
SHIP = (5, 8, 14)


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


def vgrad(img, y0, y1, top, bottom):
    d = ImageDraw.Draw(img)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)


# ---------- icons (drawn on the card layer, light colours) ----------

def draw_chip(d, cx, cy, s, color):
    d.rounded_rectangle([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s],
                        radius=int(9 * s), outline=color, width=max(3, int(6 * s)))
    d.rounded_rectangle([cx - 15 * s, cy - 15 * s, cx + 15 * s, cy + 15 * s],
                        radius=int(5 * s), fill=color)
    for dd in (-23, 0, 23):
        d.line([cx + dd * s, cy - 50 * s, cx + dd * s, cy - 34 * s], fill=color, width=5)
        d.line([cx + dd * s, cy + 34 * s, cx + dd * s, cy + 50 * s], fill=color, width=5)
        d.line([cx - 50 * s, cy + dd * s, cx - 34 * s, cy + dd * s], fill=color, width=5)
        d.line([cx + 34 * s, cy + dd * s, cx + 50 * s, cy + dd * s], fill=color, width=5)


def draw_tanker_flame(d, cx, cy, s):
    d.polygon([(cx - 62 * s, cy + 18 * s), (cx + 62 * s, cy + 18 * s),
               (cx + 42 * s, cy + 40 * s), (cx - 42 * s, cy + 40 * s)], fill=WHITE)
    d.rectangle([cx - 46 * s, cy + 6 * s, cx + 30 * s, cy + 18 * s], fill=WHITE)
    d.polygon([(cx, cy - 52 * s), (cx + 19 * s, cy - 4 * s), (cx + 7 * s, cy + 8 * s),
               (cx - 7 * s, cy + 8 * s), (cx - 19 * s, cy - 4 * s)], fill=(255, 138, 42))
    d.polygon([(cx, cy - 30 * s), (cx + 9 * s, cy - 2 * s), (cx - 9 * s, cy - 2 * s)],
              fill=(255, 213, 74))


def draw_satellite(d, cx, cy, s):
    d.rectangle([cx - 13 * s, cy - 13 * s, cx + 13 * s, cy + 13 * s], fill=WHITE)
    d.polygon([(cx - 58 * s, cy - 21 * s), (cx - 20 * s, cy - 8 * s),
               (cx - 20 * s, cy + 8 * s), (cx - 58 * s, cy + 21 * s)], fill=(147, 197, 253))
    d.polygon([(cx + 58 * s, cy - 21 * s), (cx + 20 * s, cy - 8 * s),
               (cx + 20 * s, cy + 8 * s), (cx + 58 * s, cy + 21 * s)], fill=(147, 197, 253))
    d.line([cx, cy + 13 * s, cx, cy + 34 * s], fill=WHITE, width=max(3, int(5 * s)))
    d.ellipse([cx - 5 * s, cy + 34 * s, cx + 5 * s, cy + 44 * s], fill=(255, 110, 110))


def draw_globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=6)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=WHITE, width=4)
    d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=4)


# ---------- hero scene pieces ----------

def draw_ship(d, base_y):
    """Warship silhouette, bow to the right, waterline at base_y."""
    d.polygon([(318, base_y), (922, base_y), (884, base_y + 38), (372, base_y + 38)], fill=SHIP)
    d.rectangle([470, base_y - 52, 668, base_y], fill=SHIP)            # main block
    d.rectangle([540, base_y - 96, 636, base_y - 52], fill=SHIP)      # bridge
    d.rectangle([700, base_y - 78, 742, base_y], fill=SHIP)           # funnel
    d.rectangle([742, base_y - 60, 806, base_y], fill=SHIP)           # aft block
    d.rectangle([806, base_y - 30, 872, base_y], fill=SHIP)           # turret
    d.line([500, base_y - 150, 500, base_y - 52], fill=SHIP, width=7)  # mast
    d.line([452, base_y - 128, 548, base_y - 128], fill=SHIP, width=5)
    d.line([468, base_y - 100, 532, base_y - 100], fill=SHIP, width=5)
    d.line([636, base_y - 96, 700, base_y - 118], fill=SHIP, width=5)  # crane arm
    # fire on the bridge / funnel area
    fx, fy = 640, base_y - 92
    d.polygon([(fx - 52, fy + 26), (fx - 18, fy - 34), (fx + 2, fy + 4),
               (fx + 22, fy - 48), (fx + 46, fy + 26)], fill=(255, 110, 20))
    d.polygon([(fx - 28, fy + 26), (fx - 6, fy - 18), (fx + 10, fy + 2),
               (fx + 24, fy - 22), (fx + 32, fy + 26)], fill=(255, 176, 32))
    d.polygon([(fx - 12, fy + 26), (fx + 2, fy - 6), (fx + 16, fy + 26)],
              fill=(255, 226, 110))


def main():
    img = Image.new("RGB", (W, H), INK)
    rng = random.Random(20261124)

    # ================= hero scene (96..566) =================
    vgrad(img, 96, 424, (9, 18, 44), (25, 66, 104))
    vgrad(img, 424, 566, (11, 40, 68), (5, 18, 36))
    d = ImageDraw.Draw(img)

    # stars + moon (glow on its own layer)
    for _ in range(90):
        x, y = rng.uniform(8, 1016), rng.uniform(106, 300)
        r = rng.uniform(0.8, 2.0)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 214, 235))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([826, 106, 934, 214], fill=(235, 240, 245, 90))
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    glow.filter(ImageFilter.GaussianBlur(18))).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([846, 126, 914, 194], fill=(232, 238, 244))

    # fire glow + smoke (soft layers under the ship silhouette)
    soft = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(soft)
    sd.ellipse([520, 268, 800, 448], fill=(255, 120, 30, 120))       # fire glow
    for i in range(9):                                                # smoke column
        t = i / 8
        cx = 660 + 66 * t + rng.uniform(-8, 8)
        cy = 330 - 178 * t
        r = 30 + 62 * t
        sd.ellipse([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72],
                   fill=(148, 152, 160, 105))
    soft = soft.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), soft).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    draw_ship(d, 452)

    # sea sparkle + seven drone boats with wakes
    sea = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(sea)
    for _ in range(46):
        x, y = rng.uniform(10, 990), rng.uniform(432, 556)
        ln = rng.uniform(14, 44)
        wd.line([x, y, x + ln, y], fill=(150, 190, 220, 110), width=3)
    drone_x = [86, 218, 350, 482, 614, 746, 878]
    for i, x in enumerate(drone_x):
        y = 502 + (i % 3) * 16 + rng.uniform(-3, 3)
        wd.line([x - 66, y + 16, x - 8, y + 7], fill=(210, 228, 240, 150), width=4)
        wd.line([x - 66, y + 24, x - 8, y + 12], fill=(210, 228, 240, 90), width=3)
        wd.ellipse([x - 16, y + 8, x + 44, y + 18], fill=(190, 214, 235, 70))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sea).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    for i, x in enumerate(drone_x):
        y = 502 + (i % 3) * 16
        d.polygon([(x - 14, y), (x + 40, y), (x + 30, y + 11), (x - 6, y + 11)], fill=(3, 5, 9))
        d.rectangle([x + 4, y - 7, x + 22, y], fill=(3, 5, 9))

    # hero text (shadow first, then white)
    def shadow_text(x, y, text, fnt, fill, anchor=None):
        d.text((x + 3, y + 3), text, font=fnt, fill=(0, 0, 0), anchor=anchor)
        d.text((x, y), text, font=fnt, fill=fill, anchor=anchor)

    kick = "BREAKING · LIBYA — UKRAINE WAR"
    kf = font(BOLD, 23)
    kw = d.textlength(kick, font=kf)
    d.rectangle([30, 118, 30 + kw + 28, 156], fill=RED)
    d.text((44, 125), kick, font=kf, fill=WHITE)
    hf = font(CB, 88)
    shadow_text(30, 168, "UKRAINE SINKS", hf, WHITE)
    shadow_text(30, 262, "RUSSIAN WARSHIP", hf, WHITE)
    sf = font(BOLD, 25)
    shadow_text(32, 372, "7 naval drones hit corvette Merkury at Benghazi port.", sf, (238, 243, 248))
    shadow_text(32, 406, "UN seeks probe as the war spreads to the Mediterranean.", sf, AMBER)

    # ================= masthead (0..96) =================
    d.rectangle([0, 0, W, 96], fill=INK)
    d.rectangle([0, 94, W, 97], fill=RED)
    d.text((30, 14), "WORLD NEWS", font=font(CB, 58), fill=WHITE)
    d.text((994, 16), "24 NOVEMBER 2026", font=font(BOLD, 30), fill=AMBER, anchor="ra")
    d.text((994, 56), "TUESDAY · ONE DAY, ONE IMAGE", font=font(BOLD, 19),
           fill=(170, 190, 210), anchor="ra")

    # ================= story cards (566..962) =================
    d.rectangle([0, 566, W, 962], fill=(10, 14, 24))

    def card(x, y, w_, h_, fill, kicker, kcol, headline, sub, icon):
        d.rounded_rectangle([x, y, x + w_, y + h_], radius=16, fill=fill)
        icon(x + 56, y + h_ // 2)
        tx = x + 116
        d.text((tx, y + 15), kicker, font=font(BOLD, 20), fill=kcol)
        hf2 = font(CB, 38)
        yy = y + 42
        for ln in wrap(d, headline, hf2, w_ - 116 - 16):
            d.text((tx, yy), ln, font=hf2, fill=WHITE)
            yy += 44
        yy += 4
        sf2 = font(REG, 19)
        for ln in wrap(d, sub, sf2, w_ - 116 - 16):
            d.text((tx, yy), ln, font=sf2, fill=(226, 232, 240))
            yy += 24

    cw, ch = 481, 186
    card(24, 580, cw, ch, (0, 66, 54), "TECH · NVIDIA", (110, 231, 183),
         "HUANG BACK AS CEO",
         "Jensen Huang reinstated. Shares +31%. S&P +4.7%, Nikkei +3.9%.",
         lambda cx, cy: draw_chip(d, cx, cy, 0.85, (167, 243, 208)))
    card(519, 580, cw, ch, (133, 52, 16), "MIDDLE EAST", (253, 186, 116),
         "3 TANKERS HIT MINES IN HORMUZ",
         "Iran says three oil tankers caught fire in the Strait of Hormuz.",
         lambda cx, cy: draw_tanker_flame(d, cx, cy, 0.8))
    card(24, 780, cw, ch, (30, 42, 110), "NATO · SPACE", (147, 197, 253),
         "NATO VOWS SPACE DEFENCE",
         "After reports Russia plans a nuclear-armed satellite.",
         lambda cx, cy: draw_satellite(d, cx, cy, 0.88))
    card(519, 780, cw, ch, (16, 74, 34), "CLIMATE", (134, 239, 172),
         "COP31 ENDS WITHOUT A DEAL",
         "Climate summit closes with no agreement.",
         lambda cx, cy: draw_globe(d, cx, cy, 36))

    # ================= ticker (962..1024) =================
    d.rectangle([0, 962, W, H], fill=RED)
    t1 = "ALSO TODAY: GAZA STRIKES KILL 6  ·  INDONESIA FACTORY FIRE KILLS 26"
    t2 = "LANDMINE CASUALTIES HIT 7,000 — A FIVE-YEAR HIGH"
    d.text((24, 968), t1, font=font(BOLD, 21), fill=WHITE)
    d.text((24, 995), t2, font=font(BOLD, 21), fill=AMBER)

    img.save("entry_v3.png", optimize=True)
    print("saved entry_v3.png")


if __name__ == "__main__":
    main()
