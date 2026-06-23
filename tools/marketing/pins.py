"""
Generatore di immagini per i pin Pinterest (formato 2:3, 1000x1500).
Crea pin brandizzati e diversi tra loro combinando hook + palette del prodotto.
Usa solo Pillow (nessuna dipendenza pesante).
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def _font(size, bold=True):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textbbox((0, 0), trial, font=f)[2] <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _center(draw, text, f, w, y, fill):
    tw = draw.textbbox((0, 0), text, font=f)[2]
    draw.text(((w - tw) // 2, y), text, font=f, fill=fill)


def make_pin(hook, cta, palette, out_path, variant=0):
    """Genera un pin 1000x1500. variant cambia il layout per varietà visiva."""
    W, H = 1000, 1500
    navy = _hex(palette["navy"])
    teal = _hex(palette["teal"])
    light = _hex(palette["light"])
    white = (255, 255, 255)

    img = Image.new("RGB", (W, H), light)
    d = ImageDraw.Draw(img)

    if variant % 3 == 0:
        # Layout A: foto/mock in alto, banda hook al centro, CTA in basso
        d.rectangle([0, 0, W, 560], fill=navy)
        _mock_dashboard(d, 80, 120, W - 80, 480, teal, white, light)
        d.rectangle([0, 560, W, 1080], fill=teal)
        y = 640
        for line in _wrap(d, hook, _font(60), W - 160):
            _center(d, line, _font(60), W, y, white)
            y += 78
        _cta(d, W, 1180, cta, navy, teal, white)
    elif variant % 3 == 1:
        # Layout B: banda hook in alto su navy, mock al centro, CTA in basso
        d.rectangle([0, 0, W, 620], fill=navy)
        y = 110
        for line in _wrap(d, hook, _font(64), W - 140):
            _center(d, line, _font(64), W, y, white)
            y += 84
        _mock_dashboard(d, 90, 700, W - 90, 1120, teal, navy, white)
        _cta(d, W, 1230, cta, teal, navy, white)
    else:
        # Layout C: full teal, grande "€", hook, CTA
        d.rectangle([0, 0, W, H], fill=teal)
        d.ellipse([W // 2 - 110, 150, W // 2 + 110, 370], fill=white)
        _center(d, "€", _font(150), W, 175, teal)
        y = 470
        for line in _wrap(d, hook, _font(66), W - 140):
            _center(d, line, _font(66), W, y, white)
            y += 86
        _mock_dashboard(d, 110, 950, W - 110, 1280, navy, white, light)
        _cta(d, W, 1360, cta, navy, white, white)

    img.save(out_path)
    return out_path


def _mock_dashboard(d, x0, y0, x1, y1, accent, header_text_color, bg):
    """Disegna un finto pannello dashboard per dare l'idea del prodotto."""
    d.rounded_rectangle([x0, y0, x1, y1], 22, fill=(255, 255, 255))
    d.rounded_rectangle([x0, y0, x1, y0 + 60], 22, fill=accent)
    d.rectangle([x0, y0 + 35, x1, y0 + 60], fill=accent)
    d.text((x0 + 28, y0 + 14), "Budget 2026", font=_font(30), fill=(255, 255, 255))
    # tre KPI
    cw = (x1 - x0 - 80) // 3
    cx = x0 + 30
    vals = [("Entrate", (27, 127, 92)), ("Spese", (192, 57, 43)), ("Saldo", accent)]
    for lab, col in vals:
        d.rounded_rectangle([cx, y0 + 80, cx + cw - 10, y0 + 170], 12, fill=bg)
        d.text((cx + 14, y0 + 92), lab, font=_font(20, False), fill=(107, 114, 128))
        d.rectangle([cx + 14, y0 + 124, cx + cw - 30, y0 + 140], fill=col)
        cx += cw
    # mini barre
    by = y1 - 30
    bx = x0 + 30
    heights = [40, 70, 55, 90, 65, 110]
    for i, h in enumerate(heights):
        col = accent if i % 2 == 0 else (31, 42, 68)
        d.rectangle([bx, by - h, bx + 40, by], fill=col)
        bx += 60


def _cta(d, W, y, text, pill, ring, txt):
    f = _font(40)
    tw = d.textbbox((0, 0), text, font=f)[2]
    pad = 50
    d.rounded_rectangle([(W - tw) // 2 - pad, y, (W + tw) // 2 + pad, y + 90], 45, fill=pill)
    d.text(((W - tw) // 2, y + 22), text, font=f, fill=txt)
