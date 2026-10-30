"""Pixel-art assets for Deep Cut, all drawn here so every sprite comes from one reproducible source.

Each image is drawn on a small canvas with aliased primitives and Bayer dithering, then enlarged 4x with
nearest-neighbour (S = 4). The site shows them with image-rendering: pixelated and whole-number scales.

    python3 tools/pixel/gen_pixel.py            # writes into web/src/assets/pixel/
    python3 tools/pixel/gen_pixel.py OUTDIR     # or somewhere else

Starter assets (court.png, ball.png, dunker.png) are produced exactly as first drawn; the rest (court_bare.png, rim and
net frames, two more shooter poses, spotlight beams, crowd sparkle) extend the same drawing code and palette.
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "web", "src", "assets", "pixel")
OUT = os.path.abspath(OUT) + os.sep
os.makedirs(OUT, exist_ok=True)

S = 4
W, H = 172, 215
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def thr(x, y):
    return (BAYER[y % 4][x % 4] + 0.5) / 16


def dither(a, b, t, x, y):
    return b if thr(x, y) < t else a


# palette (see docs/pixel-art.md)
INK, PANEL, LINE = hx("#0a0a0a"), hx("#141414"), hx("#3a3a3a")
CREAM = hx("#f4ead6")
ORANGE = hx("#ff6a13")
AMBER = hx("#ffb347")
DEEP = hx("#8a3c0a")


def save(im, name, scale=S):
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(OUT + name)


# ======================================================================================================== the court
def build_court(hoop=True):
    """The half court. hoop=False leaves the rim and the net off, so the site can animate them on top."""
    rnd = random.Random(11)
    img = Image.new("RGB", (W, H), hx("#060606"))
    px = img.load()
    d = ImageDraw.Draw(img)

    def poly_mask(pts):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).polygon(pts, fill=255)
        return m.load()

    # ---- stands
    for y in range(6, 80):
        for x in range(W):
            band = (y // 13) % 2
            px[x, y] = hx("#0e0e0f") if band == 0 else hx("#171718")
            if rnd.random() < 0.17:
                c = rnd.choices(
                    ["#3a2414", "#5a3418", "#7a4a22", "#2a2a30", "#ff6a13", "#ffb347", "#46464e"],
                    weights=[6, 5, 3, 6, 2, 1, 4],
                )[0]
                px[x, y] = hx(c)
    for yy in (19, 32, 45, 58, 71):
        d.line((0, yy, W, yy), fill=hx("#040404"))

    # ---- spotlight cones
    for pts, t in (
        ([(16, 0), (34, 0), (72, 86), (0, 86)], 0.34),
        ([(138, 0), (156, 0), (172, 86), (100, 86)], 0.34),
        ([(68, 0), (104, 0), (124, 86), (48, 86)], 0.2),
    ):
        m = poly_mask(pts)
        for y in range(86):
            for x in range(W):
                if m[x, y] and thr(x, y) < t:
                    px[x, y] = mix(px[x, y], hx("#ffd9a0"), 0.4)

    # ---- LED ribbon
    d.rectangle((0, 78, W, 84), fill=hx("#090909"))
    d.line((0, 78, W, 78), fill=ORANGE)
    for x in range(3, W, 7):
        d.rectangle((x, 81, x + 3, 81), fill=ORANGE)

    # ---- floor
    FL = 85
    wood_dark, wood_mid, wood_light = hx("#4a240a"), hx("#7a3f14"), hx("#b36a2a")
    for y in range(FL, H):
        for x in range(W):
            dx = (x - 86) / 98.0
            dy = (y - 150) / 88.0
            t = max(0.0, 1 - math.sqrt(dx * dx + dy * dy))
            if t > 0.55:
                px[x, y] = dither(wood_mid, wood_light, (t - 0.55) / 0.45, x, y)
            else:
                px[x, y] = dither(wood_dark, wood_mid, t / 0.55, x, y)

    # plank lines toward vanishing point
    lm = Image.new("L", (W, H), 0)
    ld = ImageDraw.Draw(lm)
    for xb in range(-320, 500, 13):
        x0 = 86 + (xb - 86) * 0.0511
        ld.line((x0, FL, xb, H - 1), fill=255)
    lmp = lm.load()
    for y in range(FL, H):
        for x in range(W):
            if lmp[x, y]:
                px[x, y] = mix(px[x, y], hx("#1a0a02"), 0.42)
    for yy in (90, 96, 104, 114, 126, 141, 160, 184, 211):
        for x in range(W):
            px[x, yy] = mix(px[x, yy], hx("#1a0a02"), 0.28)

    # lane paint
    lane = [(60, 85), (112, 85), (130, 150), (42, 150)]
    m = poly_mask(lane)
    for y in range(FL, 152):
        for x in range(W):
            if m[x, y]:
                px[x, y] = mix(px[x, y], hx("#5b1d04"), 0.55)

    # court lines
    d.line(lane + [lane[0]], fill=CREAM, width=1)
    d.line((0, FL, W, FL), fill=CREAM)
    d.arc((42, 138, 130, 162), 180, 360, fill=CREAM)
    for a in range(0, 180, 24):
        d.arc((42, 138, 130, 162), a, a + 12, fill=CREAM)
    pts = [(18, 85), (18, 125)]
    for a in range(180, -1, -4):
        r = math.radians(a)
        pts.append((86 + 68 * math.cos(r), 125 + 82 * math.sin(r)))
    pts += [(154, 125), (154, 85)]
    d.line(pts, fill=CREAM, width=1)
    rp = []
    for a in range(0, 181, 6):
        r = math.radians(a)
        rp.append((86 + 14 * math.cos(r), 85 + 9 * math.sin(r)))
    d.line(rp, fill=CREAM, width=1)
    # hoop shadow
    for y in range(86, 94):
        for x in range(64, 108):
            if ((x - 86) / 22.0) ** 2 + ((y - 90) / 4.0) ** 2 < 1:
                px[x, y] = mix(px[x, y], (0, 0, 0), 0.5)

    # ---- backboard rig
    d.rectangle((84, 0, 88, 28), fill=hx("#1b1b1b"))
    d.line((84, 0, 84, 28), fill=hx("#2e2e2e"))
    d.rectangle((80, 28, 92, 31), fill=hx("#222222"))
    for y in range(29, 62):
        for x in range(65, 108):
            px[x, y] = dither(hx("#1a1a1e"), hx("#35353b"), 0.3, x, y)
    d.rectangle((64, 28, 108, 62), outline=CREAM)
    for i in range(7):
        px[69 + i, 33 + i] = hx("#8a8a92")
        px[72 + i, 33 + i] = hx("#5a5a62")
    d.rectangle((78, 44, 94, 56), outline=ORANGE)
    d.rectangle((64, 60, 108, 62), fill=ORANGE)
    if hoop:
        d.line((78, 68, 94, 68), fill=hx("#8a3c0a"))
        d.ellipse((77, 68, 95, 72), outline=ORANGE)
        d.line((78, 70, 94, 70), fill=ORANGE)
        NET = hx("#e8e0d0")
        for x0 in range(77, 96, 3):
            x1 = 81 + (x0 - 77) * 8 / 18.0
            d.line((x0, 71, x1, 83), fill=NET)
        for yy in (74, 77, 80):
            t = (yy - 71) / 12.0
            xl, xr = 77 + (81 - 77) * t, 95 + (89 - 95) * t
            d.line((xl, yy, xr, yy), fill=hx("#9d9686"))

    # ---- vignette
    for y in range(H):
        for x in range(W):
            r = max(abs(x - 86) / 86.0, abs(y - 118) / 125.0)
            t = max(0.0, min(1.0, (r - 0.6) / 0.4))
            if t > 0 and thr(x, y) < t:
                px[x, y] = mix(px[x, y], hx("#040404"), 0.75)
    return img


save(build_court(True), "court.png")
save(build_court(False), "court_bare.png")

# ======================================================================================================== the ball
bw = 13
ball = Image.new("RGBA", (bw, bw), (0, 0, 0, 0))
bd = ImageDraw.Draw(ball)
bd.ellipse((0, 0, 12, 12), fill=ORANGE + (255,), outline=hx("#1a0902") + (255,))
bp = ball.load()
for y in range(13):
    for x in range(13):
        if bp[x, y][3] and bp[x, y][:3] == ORANGE and x + y > 14 and thr(x, y) < 0.6:
            bp[x, y] = hx("#c2410c") + (255,)
bd.line((1, 6, 11, 6), fill=hx("#1a0902") + (255,))
bd.line((6, 1, 6, 11), fill=hx("#1a0902") + (255,))
bd.arc((-5, 1, 6, 11), -80, 80, fill=hx("#1a0902") + (255,))
bd.arc((6, 1, 17, 11), 100, 260, fill=hx("#1a0902") + (255,))
for (x, y) in ((3, 3), (4, 2), (2, 4)):
    bp[x, y] = AMBER + (255,)
save(ball, "ball.png")

# ======================================================================================================== the players
SW, SH = 56, 76
SKIN, SKIN_HI, SKIN_SH = hx("#b87a45"), hx("#d9a066"), hx("#8a5528")
JER, JER_SH, SHORTS, SHOE, HAIR = hx("#ff6a13"), hx("#c2410c"), hx("#111111"), hx("#f2e6d0"), hx("#1a1a1a")
OUTL = hx("#050505")


def sprite(draw_figure):
    """A 56 x 76 sprite: draw the figure with limb() and poly() (in the 0.15-scaled units), then outline and highlight it."""
    spr = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    sd = ImageDraw.Draw(spr)
    s = 0.15

    def P(x, y):
        return (x * s + 2, y * s + 2)

    def limb(pts, w, col):
        pp = [P(*p) for p in pts]
        sd.line(pp, fill=col + (255,), width=w)
        for p in pp:
            sd.ellipse((p[0] - w / 2.0, p[1] - w / 2.0, p[0] + w / 2.0, p[1] + w / 2.0), fill=col + (255,))

    def poly(pts, col):
        sd.polygon([P(*p) for p in pts], fill=col + (255,))

    draw_figure(sd, P, limb, poly)
    sp = spr.load()
    alpha = [[sp[x, y][3] for x in range(SW)] for y in range(SH)]
    res = spr.copy()
    rp_ = res.load()
    for y in range(SH):
        for x in range(SW):
            if alpha[y][x] == 0:
                near = False
                for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ddx, y + ddy
                    if 0 <= nx < SW and 0 <= ny < SH and alpha[ny][nx]:
                        near = True
                if near:
                    rp_[x, y] = OUTL + (255,)
            else:
                if x + 1 < SW and alpha[y][x + 1] == 0:
                    rp_[x, y] = mix(sp[x, y][:3], AMBER, 0.55) + (255,)
    return res


def head(sd, P, cx, cy):
    hc = P(cx, cy)
    sd.ellipse((hc[0] - 4, hc[1] - 4, hc[0] + 4, hc[1] + 4), fill=SKIN + (255,))
    sd.pieslice((hc[0] - 4.5, hc[1] - 5, hc[0] + 4.5, hc[1] + 3), 180, 360, fill=HAIR + (255,))


def dunker(sd, P, limb, poly):
    limb([(168, 330), (156, 388), (134, 440)], 4, SKIN_SH)
    poly([(122, 436), (148, 436), (160, 452), (120, 454)], SHOE)
    limb([(206, 318), (252, 352), (226, 418)], 4, SKIN)
    poly([(218, 414), (244, 420), (256, 436), (224, 438)], SHOE)
    poly([(154, 266), (206, 260), (220, 326), (176, 340), (148, 330)], SHORTS)
    poly([(146, 152), (208, 146), (214, 206), (204, 268), (154, 274), (148, 206)], JER)
    poly([(146, 206), (214, 206), (204, 268), (154, 274)], JER_SH)
    sd.line([P(150, 262), P(206, 256)], fill=AMBER + (255,), width=1)
    limb([(150, 160), (116, 190), (92, 222)], 3, SKIN_SH)
    limb([(172, 136), (176, 150)], 3, SKIN)
    head(sd, P, 172, 118)
    limb([(204, 156), (238, 108), (262, 56)], 3, SKIN)
    hp = P(266, 46)
    sd.ellipse((hp[0] - 2.5, hp[1] - 2.5, hp[0] + 2.5, hp[1] + 2.5), fill=SKIN_HI + (255,))


def torso(sd, P, limb, poly, lean=0):
    """Shorts and jersey, upright, for the standing and shooting poses."""
    poly([(150, 262), (206, 262), (214, 330), (180, 338), (146, 330)], SHORTS)
    poly([(144, 150 + lean), (210, 150 + lean), (214, 206), (206, 268), (152, 268), (144, 206)], JER)
    poly([(146, 208), (212, 208), (206, 268), (152, 268)], JER_SH)
    sd.line([P(152, 262), P(206, 262)], fill=AMBER + (255,), width=1)


def shooter_stand(sd, P, limb, poly):
    """Knees bent, the ball held at the chest, ready to shoot (the ball is a separate sprite)."""
    limb([(160, 330), (140, 392), (136, 446)], 4, SKIN_SH)
    poly([(122, 442), (150, 442), (160, 458), (120, 460)], SHOE)
    limb([(200, 330), (226, 392), (222, 446)], 4, SKIN)
    poly([(210, 442), (238, 442), (250, 458), (208, 460)], SHOE)
    torso(sd, P, limb, poly)
    limb([(150, 164), (140, 206), (172, 214)], 3, SKIN_SH)
    limb([(172, 136), (176, 150)], 3, SKIN)
    head(sd, P, 176, 118)
    limb([(204, 164), (216, 206), (186, 216)], 3, SKIN)


def shooter_shoot(sd, P, limb, poly):
    """In the air at the release: both arms up and the wrist flicked."""
    limb([(164, 330), (150, 380), (150, 420)], 4, SKIN_SH)
    poly([(138, 416), (164, 416), (172, 434), (134, 436)], SHOE)
    limb([(200, 330), (216, 372), (214, 416)], 4, SKIN)
    poly([(202, 412), (228, 412), (238, 430), (200, 432)], SHOE)
    torso(sd, P, limb, poly)
    limb([(150, 158), (150, 100), (170, 52)], 3, SKIN_SH)
    limb([(172, 136), (176, 150)], 3, SKIN)
    head(sd, P, 176, 118)
    limb([(206, 158), (214, 100), (200, 54)], 3, SKIN)
    hp = P(196, 44)
    sd.ellipse((hp[0] - 2.5, hp[1] - 2.5, hp[0] + 2.5, hp[1] + 2.5), fill=SKIN_HI + (255,))


save(sprite(dunker), "dunker.png")
save(sprite(shooter_stand), "shooter_stand.png")
save(sprite(shooter_shoot), "shooter_shoot.png")

# ======================================================================================================== the hoop
# The rim and the net as their own sprites, so they can move: a back half of the rim (behind the ball), a front half
# (in front of it), and three net frames (at rest, stretched by the ball, snapped back).
HX0, HY0, HW, HH = 74, 66, 24, 28  # where the sprite sits on the court, in low-res pixels


def hoop_canvas():
    return Image.new("RGBA", (HW, HH), (0, 0, 0, 0))


def rim_halves():
    full = hoop_canvas()
    fd = ImageDraw.Draw(full)
    fd.ellipse((77 - HX0, 68 - HY0, 95 - HX0, 72 - HY0), outline=ORANGE + (255,))
    fd.line((78 - HX0, 70 - HY0, 94 - HX0, 70 - HY0), fill=ORANGE + (255,))
    back, front = hoop_canvas(), hoop_canvas()
    fp, bp_, ft = full.load(), back.load(), front.load()
    for y in range(HH):
        for x in range(HW):
            if fp[x, y][3]:
                (bp_ if y + HY0 <= 69 else ft)[x, y] = fp[x, y]
    ImageDraw.Draw(back).line((78 - HX0, 68 - HY0, 94 - HX0, 68 - HY0), fill=DEEP + (255,))
    return back, front


def net(stretch, narrow):
    """The net: stretch makes it longer (the ball pulling it down), narrow pinches the bottom."""
    im = hoop_canvas()
    nd = ImageDraw.Draw(im)
    NET, NET_DIM = hx("#e8e0d0"), hx("#9d9686")
    bottom = 83 + stretch
    for x0 in range(77, 96, 3):
        x1 = 81 + (x0 - 77) * (8 - narrow * 2) / 18.0 + narrow
        nd.line((x0 - HX0, 71 - HY0, x1 - HX0, bottom - HY0), fill=NET + (255,))
    for yy in (74, 77, 80, 83):
        if yy > bottom:
            continue
        t = (yy - 71) / float(bottom - 71)
        xl, xr = 77 + (81 + narrow - 77) * t, 95 + (89 - narrow - 95) * t
        nd.line((xl - HX0, yy - HY0, xr - HX0, yy - HY0), fill=NET_DIM + (255,))
    return im


rim_back, rim_front = rim_halves()
save(rim_back, "rim_back.png")
save(rim_front, "rim_front.png")
save(net(0, 0), "net_0.png")
save(net(3, 1), "net_1.png")
save(net(6, 2), "net_2.png")

# ======================================================================================================== the room
# Spotlight beams (dithered, so they stay pixels) and two frames of crowd sparkle for the stands.
beam = Image.new("RGBA", (60, 90), (0, 0, 0, 0))
bpx = beam.load()
for y in range(90):
    half = 4 + y * 0.32
    for x in range(60):
        if abs(x - 30) <= half and thr(x, y) < 0.34 * (1 - y / 100.0):
            bpx[x, y] = hx("#ffd9a0") + (255,)
save(beam, "beam.png")

for name, seed in (("crowd_a.png", 5), ("crowd_b.png", 9)):
    r = random.Random(seed)
    sp = Image.new("RGBA", (W, 74), (0, 0, 0, 0))
    spp = sp.load()
    for y in range(74):
        for x in range(W):
            if r.random() < 0.035:
                spp[x, y] = (r.choice([ORANGE, AMBER, CREAM]) + (255,))
    save(sp, name)

# ======================================================================================================== the icon
icon = Image.new("RGBA", (16, 16), INK + (255,))
idr = ImageDraw.Draw(icon)
idr.rectangle((0, 0, 15, 15), outline=ORANGE + (255,))
b16 = ball.resize((13, 13), Image.NEAREST)
icon.paste(b16, (1, 1), b16)
save(icon, "icon.png", 16)
print("wrote", OUT)
