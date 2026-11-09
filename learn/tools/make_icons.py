"""Generate PWA icons into icons/. Needs Pillow:  python learn/tools/make_icons.py"""
import math, os
from PIL import Image, ImageDraw
def draw(size, maskable=False):
    S = size * 4
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    # background gradient (vertical) clipped to a rounded square (full-bleed when maskable)
    bg = Image.new('RGBA', (S, S))
    px = bg.load()
    for y in range(S):
        t = y / S
        c = (int(8 + 22 * t), int(11 + 22 * t), int(23 + 70 * t), 255)
        for x in range(S): px[x, y] = c
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=0 if maskable else int(S * 0.22), fill=255)
    img.paste(bg, (0, 0), mask)
    k = 0.66 if maskable else 0.8            # safe zone for maskable icons
    cx = cy = S / 2; w = S * k
    # axes
    ax = (255, 255, 255, 55)
    d.line([(cx - w / 2, cy), (cx + w / 2, cy)], fill=ax, width=int(S * 0.008))
    d.line([(cx - w / 2, cy - w * 0.36), (cx - w / 2, cy + w * 0.36)], fill=ax, width=int(S * 0.008))
    # sine wave, colour sweeps indigo -> cyan
    n = 400; amp = w * 0.30; lw = int(S * 0.045)
    pts = [(cx - w / 2 + w * i / n, cy - amp * math.sin(2 * math.pi * 1.5 * i / n)) for i in range(n + 1)]
    for i in range(n):
        t = i / n
        col = (int(124 + (34 - 124) * t), int(140 + (211 - 140) * t), int(255 + (238 - 255) * t), 255)
        d.line([pts[i], pts[i + 1]], fill=col, width=lw)
        d.ellipse([pts[i][0] - lw / 2, pts[i][1] - lw / 2, pts[i][0] + lw / 2, pts[i][1] + lw / 2], fill=col)
    return img.resize((size, size), Image.LANCZOS)
os.makedirs('icons', exist_ok=True)
for name, size, m in [('icon-192.png', 192, False), ('icon-512.png', 512, False), ('icon-maskable-512.png', 512, True), ('apple-touch-icon.png', 180, True)]:
    draw(size, m).save('icons/' + name)
print('ok')
