"""The site's three pictures: favicon.png (64 x 64), apple-touch-icon.png (180 x 180) and social.png (1200 x 630).

    python3 tools/icons/gen_icons.py            # writes into web/public/
    python3 tools/icons/gen_icons.py OUTDIR     # or somewhere else

Flat shapes only (no gradients, no blur, no logos): the ball, the shot chart and the six tier squares in the site's palette.
The share image uses the site's two fonts, so run `npm install` in web/ first. Needs Pillow.
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "web", "public"))
FONTS = os.path.join(HERE, "..", "..", "web", "node_modules", "@fontsource")
os.makedirs(OUT, exist_ok=True)

INK, CREAM, ORANGE, AMBER, MUTED, LINE = "#0a0a0a", "#f4ead6", "#ff6a13", "#ffb347", "#a8a8a8", "#3a3a3a"
TIERS = ["#6e6e6e", "#a8a8a8", "#ededed", "#ffb020", "#ff6a13", "#ff3b1f"]
TIER_TEXT = ["#ffffff"] + [INK] * 5


def ball(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float) -> None:
    """A flat orange ball with two straight seams and two curved ones."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ORANGE, outline=INK, width=max(2, int(r / 8)))
    w = max(2, int(r / 9))
    d.line((cx - r, cy, cx + r, cy), fill=INK, width=w)
    d.line((cx, cy - r, cx, cy + r), fill=INK, width=w)
    d.arc((cx - 1.9 * r, cy - r, cx - 0.1 * r, cy + r), -60, 60, fill=INK, width=w)
    d.arc((cx + 0.1 * r, cy - r, cx + 1.9 * r, cy + r), 120, 240, fill=INK, width=w)


def icon(size: int) -> Image.Image:
    im = Image.new("RGB", (size, size), INK)
    d = ImageDraw.Draw(im)
    b = max(2, size // 16)
    d.rectangle((0, 0, size - 1, size - 1), outline=ORANGE, width=b)
    ball(d, size / 2, size / 2, size * 0.3)
    return im


def font(name: str, file: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONTS, name, "files", file), size)


def social() -> Image.Image:
    press = lambda n: font("press-start-2p", "press-start-2p-latin-400-normal.woff", n)
    vt = lambda n: font("vt323", "vt323-latin-400-normal.woff", n)
    im = Image.new("RGB", (1200, 630), INK)
    d = ImageDraw.Draw(im)
    d.rectangle((10, 10, 1189, 619), outline=ORANGE, width=8)
    # the shot chart, right side: court lines, tier rings around the hoop, six markers
    hx, hy, u = 900, 110, 0.78  # hoop and scale
    d.rectangle((690, 60, 1130, 560), outline=CREAM, width=4)
    rings = Image.new("RGB", (440, 500), INK)  # drawn on their own and cut to the court, so they stop at its lines
    rd = ImageDraw.Draw(rings)
    for r in (112, 190, 266, 358, 440):
        rr = r * u
        for a in range(0, 360, 12):
            rd.arc((hx - 690 - rr, hy - 60 - rr, hx - 690 + rr, hy - 60 + rr), a, a + 6, fill="#6e6e6e", width=3)
    im.paste(rings, (690, 60))
    d.rectangle((690, 60, 1130, 560), outline=CREAM, width=4)
    d.rectangle((830, 60, 970, 230), outline=CREAM, width=4)
    d.line((hx - 36, hy - 12, hx + 36, hy - 12), fill=CREAM, width=7)
    d.ellipse((hx - 14, hy - 14, hx + 14, hy + 14), outline=ORANGE, width=6)
    for i, (dist, ang) in enumerate(((70, 60), (150, 120), (230, 70), (310, 110), (400, 80), (470, 100))):
        x, y = hx + dist * u * math.cos(math.radians(ang)), hy + dist * u * math.sin(math.radians(ang))
        d.line((hx, hy, x, y), fill=MUTED, width=2)
        d.rectangle((x - 5, y - 5, x + 27, y + 27), fill="#000000")
        d.rectangle((x - 16, y - 16, x + 16, y + 16), fill=TIERS[i])
        d.text((x, y), str(i + 1), font=press(18), fill=TIER_TEXT[i], anchor="mm")
    # the words
    d.text((64, 70), "NBA", font=press(40), fill=ORANGE)
    d.text((64, 140), "DEEP", font=press(96), fill=CREAM)
    d.text((64, 262), "CUT", font=press(96), fill=AMBER)
    d.text((64, 400), "THE OBVIOUS ANSWER LOSES", font=press(22), fill=AMBER)
    d.text((64, 450), "A daily basketball trivia game.", font=vt(46), fill=CREAM)
    d.text((64, 500), "Seven prompts, 25 seconds each.", font=vt(46), fill=MUTED)
    for i, c in enumerate(TIERS):
        x = 64 + i * 72
        d.rectangle((x + 5, 552 + 5, x + 56 + 5, 552 + 56 + 5), fill="#000000")
        d.rectangle((x, 552, x + 56, 552 + 56), fill=c)
        d.text((x + 28, 552 + 28), str(i + 1), font=press(22), fill=TIER_TEXT[i], anchor="mm")
    return im


icon(64).save(os.path.join(OUT, "favicon.png"), optimize=True)
icon(180).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
if os.path.isdir(FONTS):
    social().save(os.path.join(OUT, "social.png"), optimize=True)
else:
    print("skipped social.png: run `npm install` in web/ for the fonts")
print("wrote", OUT)
