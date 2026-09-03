# -*- coding: utf-8 -*-
"""
QPEDIA — 16:9 featured-image generator, DARK CYBER / NEON variant.
Matches the site's existing house style (dark navy + neon blue/cyan glow,
analyzed from images/q_01..q_160). Reuses icons + text engine from generate.py.
"""
import os, math, random, csv, zipfile
from PIL import Image, ImageDraw, ImageFilter
import generate as G

W, H = G.W, G.H
OUT = os.path.join(G.REPO, "featured-images-dark")
FONTS = G.FONTS
F = G.F
ARTICLES = G.ARTICLES
ICONS = G.ICONS
icon_layer = G.icon_layer
fade = G.fade
layout_en = G.layout_en
layout_fa = G.layout_fa
fa_display = G.fa_display
gradient_text = G.gradient_text
dashed_ellipse = G.dashed_ellipse
ellipse_pts = G.ellipse_pts
sine_pts = G.sine_pts

# ------------------------------------------------------------------ dark palette
BG_TOP = (8, 21, 40)
BG_BOT = (16, 40, 68)
GRID = (62, 146, 208, 22)
DOT = (110, 165, 220, 38)
KW = (120, 175, 225, 120)
CIRC = (82, 165, 230, 95)
WM = (180, 200, 226, 135)
INK_FA = (240, 244, 250)

NEON = {
    "blue":   ((92, 208, 255), (70, 120, 250)),
    "orange": ((255, 178, 92), (255, 108, 52)),
    "purple": ((192, 152, 255), (122, 82, 242)),
}

# ------------------------------------------------------------------ cached effects
_bg_cache = None
def dark_grain():
    noise = Image.effect_noise((W, H), 24).convert("L")
    alpha = noise.point(lambda v: (int(abs(v - 128) / 128 * 10) // 2) * 2)
    g = Image.new("RGBA", (W, H), (150, 190, 230, 0))
    g.putalpha(alpha)
    return g

_glow_cache = {}
def radial_glow(color, radius=300, peak=110):
    key = (color, radius, peak)
    if key in _glow_cache:
        return _glow_cache[key]
    size = radius * 2
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for r in range(radius, 0, -2):
        a = peak * (1 - r / radius) ** 2
        d.ellipse([radius - r, radius - r, radius + r, radius + r], fill=(*color, int(a)))
    img = img.filter(ImageFilter.GaussianBlur(8))
    _glow_cache[key] = img
    return img

def glow_layer(layer, radius=16, strength=0.85):
    b = layer.filter(ImageFilter.GaussianBlur(radius))
    r, g, bb, a = b.split()
    a = a.point(lambda v: int(v * strength))
    return Image.merge("RGBA", (r, g, bb, a))

# ------------------------------------------------------------------ background
def draw_background(img, rnd, c1):
    d = ImageDraw.Draw(img, "RGBA")
    # vertical gradient
    for y in range(H):
        t = y / max(H - 1, 1)
        c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=(*c, 255))
    # soft center glow
    glow = radial_glow(c1, 420, 70)
    img.alpha_composite(glow, (int(W/2 - 420), int(360 - 420)))
    # cyber grid
    step = 96
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=GRID, width=1)
    # dotted grid
    for y in range(0, H, 48):
        for x in range(0, W, 48):
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(90, 150, 205, 55))
    # circuit traces with glowing nodes
    for _ in range(5):
        x, y = rnd.randint(50, W - 50), rnd.randint(50, H - 50)
        for _s in range(rnd.randint(2, 4)):
            nx = max(30, min(W - 30, x + rnd.choice([-1, 1]) * rnd.randint(60, 190)))
            ny = max(30, min(H - 30, y + rnd.choice([-1, 1]) * rnd.randint(40, 150)))
            d.line([(x, y), (nx, y)], fill=CIRC, width=1)
            d.line([(nx, y), (nx, ny)], fill=CIRC, width=1)
            d.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(c1[0], c1[1], c1[2], 160))
            d.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=(c1[0], c1[1], c1[2], 40))
            x, y = nx, ny
    img.alpha_composite(dark_grain())

# ------------------------------------------------------------------ scatter
def scatter(img, slug, icon, keywords, rnd, c1):
    d = ImageDraw.Draw(img, "RGBA")
    kf_sizes = [30, 34, 40, 46]
    for kw in keywords:
        size = rnd.choice(kf_sizes)
        f = F("Montserrat-Medium.ttf", size)
        tw = f.getlength(kw)
        for _ in range(60):
            x = rnd.randint(40, W - 40 - int(tw))
            y = rnd.randint(40, H - 70)
            if math.hypot(x - W/2, y - 360) < 300: continue
            if 540 < y < 1010 and 430 < x < 1490: continue
            break
        ang = rnd.choice([-8, -5, -3, 0, 0, 3, 5, 8])
        layer = Image.new("RGBA", (int(tw) + 20, size + 20), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.text((10, 10), kw, font=f, fill=KW)
        layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(layer, (x, y))
    for _ in range(2):
        s = rnd.randint(70, 110)
        sub = icon_layer(s, (96, 168, 220), (60, 120, 180), ICONS[icon])
        sub = fade(sub, 0.55)
        for _ in range(40):
            x = rnd.randint(30, W - 30 - s); y = rnd.randint(30, H - 30 - s)
            if math.hypot(x - W/2, y - 360) < 320: continue
            if 540 < y < 1010: continue
            break
        img.alpha_composite(sub, (x, y))
    for k, pos in [("atom", (60, 90)), ("wave", (W - 170, H - 200))]:
        sub = icon_layer(100, (96, 168, 220), (60, 120, 180), ICONS[k])
        sub = fade(sub, 0.5)
        img.alpha_composite(sub, pos)

# ------------------------------------------------------------------ branding
def watermark_block(text_lines, size, anchor_right=False):
    rendered = []
    maxw = 0
    for i, ln in enumerate(text_lines):
        f = F("Montserrat-Black.ttf", size) if i == 0 else F("Montserrat-SemiBold.ttf", int(size * 0.78))
        bbox = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), ln, font=f)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        rendered.append((ln, f, w, h, bbox))
        maxw = max(maxw, w)
    total_h = sum(r[3] for r in rendered) + (len(rendered) - 1) * 4
    layer = Image.new("RGBA", (maxw + 6, total_h + 6), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    yy = 3
    for ln, f, w, h, bbox in rendered:
        xx = maxw - w if anchor_right else 0
        ld.text((xx - bbox[0] + 3, yy - bbox[1]), ln, font=f, fill=WM)
        yy += h + 4
    return layer

def draw_branding(img, rnd, c1):
    d = ImageDraw.Draw(img, "RGBA")
    tr = watermark_block(["QPEDIA", "QUANTUM PEDIA"], 46, anchor_right=True)
    img.alpha_composite(tr, (W - tr.width - 64, 48))
    bl = watermark_block(["QPEDIA", "QUANTUM PEDIA"], 46)
    img.alpha_composite(bl, (64, H - bl.height - 52))
    f = F("Montserrat-SemiBold.ttf", 34)
    for (x, y) in [(64, 42), (W - 220, H - 46)]:
        d.text((x, y), "qpedia.ir", font=f, fill=(160, 180, 205, 140))
    # faint name repeats inside background
    f3 = F("Montserrat-SemiBold.ttf", 26)
    for (x, y) in [(W*0.20, H*0.10), (W*0.80, H*0.86), (W*0.50, H*0.04)]:
        d.text((x, y), "qpedia.ir", font=f3, fill=(140, 170, 200, 70))
    a = icon_layer(46, (150, 190, 230), (110, 150, 200), G.I_atom)
    a = fade(a, 0.8)
    img.alpha_composite(a, (W - 64 - tr.width - 52, 48))

# ------------------------------------------------------------------ build
def build(art):
    slug, fa, en, mood, icon, kw = art
    c1, c2 = NEON[mood]
    rnd = random.Random(slug + "-dark")

    img = Image.new("RGBA", (W, H), BG_TOP)
    draw_background(img, rnd, c1)
    scatter(img, slug, icon, kw, rnd, c1)
    draw_branding(img, rnd, c1)

    d = ImageDraw.Draw(img, "RGBA")

    # ---- center icon with glow + dashed circles
    cx, cy = W/2, 360
    r1, r2 = 176, 208
    dashed_ellipse(d, cx, cy, r1, r1, (c1[0], c1[1], c1[2], 150), 2, dash=16, gap=12)
    dashed_ellipse(d, cx, cy, r2, r2, (c1[0], c1[1], c1[2], 90), 2, dash=10, gap=16)
    for ang in [0, 90, 180, 270]:
        a = math.radians(ang)
        d.ellipse([cx + r1*math.cos(a)-4, cy + r1*math.sin(a)-4,
                   cx + r1*math.cos(a)+4, cy + r1*math.sin(a)+4], fill=(c1[0], c1[1], c1[2], 200))
    icon_img = icon_layer(300, c1, c2, ICONS[icon])
    gl = glow_layer(icon_img, 20, 0.8)
    img.alpha_composite(gl, (int(cx - 150), int(cy - 150)))
    img.alpha_composite(icon_img, (int(cx - 150), int(cy - 150)))

    # ---- titles
    max_w = 1560
    en_lines, en_size = layout_en(en, 76, max_w, 2)
    fa_lines, fa_size = layout_fa(fa, 46, max_w, 2)
    en_f = F("Montserrat-ExtraBold.ttf", en_size)
    fa_f = F("Vazirmatn-ExtraBold.ttf", fa_size)
    en_h = en_size * 1.25
    fa_h = fa_size * 1.45
    gap = 26
    block_h = en_h * len(en_lines) + gap + fa_h * len(fa_lines)
    top = 760 - block_h / 2

    y = top
    for ln in en_lines:
        g = gradient_text(ln, en_f, c1, c2)
        gl = glow_layer(g, 12, 0.6)
        img.alpha_composite(gl, (int(W/2 - g.width/2), int(y)))
        img.alpha_composite(g, (int(W/2 - g.width/2), int(y)))
        y += en_h
    y += gap
    for k in range(3):
        x = W/2 + (k - 1) * 30
        d.ellipse([x - 3, y - 14, x + 3, y - 8], fill=(c1[0], c1[1], c1[2], 230))
    for ln in fa_lines:
        disp = fa_display(ln)
        bbox = fa_f.getbbox(disp)
        w = bbox[2] - bbox[0]
        mask = Image.new("L", (w + 4, int(fa_h) + 4), 0)
        md = ImageDraw.Draw(mask)
        md.text((2 - bbox[0], 2 - bbox[1]), disp, font=fa_f, fill=255)
        ink = Image.new("RGBA", mask.size, INK_FA)
        ink.putalpha(mask)
        gl = glow_layer(ink, 8, 0.5)
        img.alpha_composite(gl, (int(W/2 - w/2), int(y)))
        img.alpha_composite(ink, (int(W/2 - w/2), int(y)))
        y += fa_h

    return img.convert("RGB")

def main():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for i, art in enumerate(ARTICLES, 1):
        slug = art[0]
        img = build(art)
        out = os.path.join(OUT, f"{slug}.png")
        q = img.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
        q.save(out, optimize=True)
        rows.append([i, slug, art[1], art[2], art[3]])
        print(f"[{i:02d}/74] {slug}")
    with open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["#", "slug", "title_fa", "title_en", "mood"])
        wr.writerows(rows)
    zp = os.path.join(OUT, "QPEDIA-74-thumbnails-dark.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(OUT, "manifest.csv"), "manifest.csv")
        for art in ARTICLES:
            z.write(os.path.join(OUT, f"{art[0]}.png"), f"{art[0]}.png")
    print("done ->", OUT)
    print("zip  ->", zp)

if __name__ == "__main__":
    main()
