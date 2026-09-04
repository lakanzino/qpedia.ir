# -*- coding: utf-8 -*-
"""
QPedia — article featured-image generator (new formula, owner-approved spec).
900x450 · white felt/fabric texture · faint but bold multi-color line motif
in an imaginary square · EN title top · FA keyword (Yekan-style) · dark fonts.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops
import arabic_reshaper
from bidi.algorithm import get_display

FONTS = "/home/user/qpedia.ir/.thumbnails/fonts"
OUT = "/home/user/qpedia.ir/article-thumbs"
W, H = 900, 450

INK = (26, 33, 51)  # dark navy text


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def fa(s):
    return get_display(arabic_reshaper.reshape(s))


def felt_background(size, seed=11, strength=0.07):
    """White canvas with a soft thick-fabric / fleece grain."""
    img = Image.new("RGB", size, (255, 255, 255))
    noise = Image.effect_noise(size, 26).convert("L")
    noise = noise.filter(ImageFilter.GaussianBlur(1.1))
    noise = ImageOps.autocontrast(noise)
    # subtle darkening where noise is darker -> felt grain
    tint = noise.point(lambda p: 255 - int((255 - p) * strength))
    return ImageChops.multiply(img, tint.convert("RGB"))


def spring(d, a, b, color, width=6, coils=5, amp=12):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux  # perpendicular
    pts = []
    n = coils * 2
    for i in range(n + 1):
        t = i / n
        x = ax + dx * t + nx * amp * math.sin(math.pi * coils * t)
        y = ay + dy * t + ny * amp * math.sin(math.pi * coils * t)
        pts.append((x, y))
    d.line(pts, fill=color, width=width, joint="curve")


def motif_quark(d, cx, cy, R, c1, c2):
    """Proton with three quarks + gluon springs (2 colors)."""
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=c1, width=9)
    qr = 34
    q = [
        (cx - R * 0.42, cy + R * 0.30),
        (cx + R * 0.42, cy + R * 0.30),
        (cx, cy - R * 0.55),
    ]
    for (x, y), col in zip(q, [c1, c1, c2]):
        d.ellipse([x - qr, y - qr, x + qr, y + qr], outline=col, width=8)
    for a, b in [(q[0], q[1]), (q[1], q[2]), (q[2], q[0])]:
        spring(d, a, b, c2, width=5, coils=3, amp=10)


def build(slug, fa_keyword, en_title, c1, c2, motif):
    img = felt_background((W, H))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    a1 = c1 + (168,)
    a2 = c2 + (168,)

    # motif inside an imaginary square on the right side
    if motif == "quark":
        motif_quark(d, 645, 225, 128, a1, a2)

    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")

    dr = ImageDraw.Draw(img)
    # accent bar (uses one of the two colors, not the text)
    dr.rectangle([40, 82, 92, 92], fill=c1 + (255,))
    # English title (top)
    f_en = font("Montserrat-ExtraBold.ttf", 66)
    dr.text((112, 60), en_title, font=f_en, fill=INK)
    # Persian keyword (Yekan-style) — already shaped & visual-ordered via reshaper+bidi
    f_fa = font("Vazirmatn-Bold.ttf", 58)
    dr.text((112, 150), fa(fa_keyword), font=f_fa, fill=INK)

    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "png"), exist_ok=True)
    img = build(
        "quark",
        "کوارک",
        "QUARK",
        c1=(22, 101, 209),   # blue
        c2=(245, 124, 0),    # orange
        motif="quark",
    )
    img.save(os.path.join(OUT, "png", "quark.png"))
    print("saved", os.path.join(OUT, "png", "quark.png"), img.size)
