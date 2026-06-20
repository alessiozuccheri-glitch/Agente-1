#!/usr/bin/env python3
"""
Genera gli asset visivi del prodotto "Smart Budget Tracker" con Pillow:
  1) Guida rapida in PDF (multi-pagina, brandizzata)
  2) Hero image per il listing Etsy (1:1, leggibile da mobile)
  3) "What's included" image

Uso:
    pip install pillow
    python3 src/build_assets.py
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
OUT_PROD = os.path.normpath(os.path.join(HERE, "..", "file-prodotto"))
OUT_IMG = os.path.normpath(os.path.join(HERE, "..", "mockup-prompts"))
os.makedirs(OUT_PROD, exist_ok=True)
os.makedirs(OUT_IMG, exist_ok=True)

# palette brand (coerente con lo spreadsheet)
NAVY = (31, 42, 68)
TEAL = (43, 179, 163)
LIGHT = (234, 246, 244)
GREY = (107, 114, 128)
WHITE = (255, 255, 255)
INK = (40, 48, 66)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(size, bold=False):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------- PDF GUIDE ----
def page(w=1240, h=1754):  # A4 @150dpi
    img = Image.new("RGB", (w, h), WHITE)
    return img, ImageDraw.Draw(img)


def header_band(d, w, title, subtitle=None):
    d.rectangle([0, 0, w, 150], fill=NAVY)
    d.rectangle([0, 150, w, 158], fill=TEAL)
    d.text((70, 45), title, font=font(40, True), fill=WHITE)
    if subtitle:
        d.text((70, 100), subtitle, font=font(22), fill=(200, 210, 220))


def footer(d, w, h, n):
    d.text((70, h - 60), "Smart Budget Tracker — Guida rapida", font=font(18), fill=GREY)
    d.text((w - 120, h - 60), f"{n}", font=font(18), fill=GREY)


def build_pdf_guide():
    pages = []
    W, H = 1240, 1754

    # ---- Pagina 1: copertina
    img, d = page()
    d.rectangle([0, 0, W, H], fill=NAVY)
    d.rectangle([0, 760, W, 768], fill=TEAL)
    # emoji-free badge
    d.rounded_rectangle([W // 2 - 90, 320, W // 2 + 90, 500], 30, fill=TEAL)
    d.text((W // 2 - 52, 360), "€", font=font(120, True), fill=WHITE)
    t = "SMART BUDGET TRACKER"
    d.text(((W - text_w(d, t, font(58, True))) // 2, 600), t, font=font(58, True), fill=WHITE)
    s = "Guida rapida all'uso"
    d.text(((W - text_w(d, s, font(30))) // 2, 690), s, font=font(30), fill=(190, 200, 215))
    foot = "Controlla entrate, spese e risparmi in pochi minuti al mese"
    for i, line in enumerate(wrap(d, foot, font(26), 800)):
        d.text(((W - text_w(d, line, font(26))) // 2, 880 + i * 40), line,
               font=font(26), fill=(170, 180, 195))
    pages.append(img)

    # ---- Pagina 2: come iniziare
    img, d = page()
    header_band(d, W, "Come iniziare", "3 passi, 5 minuti")
    steps = [
        ("1", "Apri il foglio  Setup",
         "Inserisci le tue categorie di spesa e il budget mensile che vuoi "
         "rispettare per ciascuna. Aggiungi le tue fonti di entrata."),
        ("2", "Registra ogni mese",
         "Apri il foglio del mese (es. Gennaio) e scrivi le entrate e le spese "
         "reali. Le differenze Budget vs Speso si calcolano da sole."),
        ("3", "Leggi la Dashboard",
         "Il foglio Dashboard mostra il riepilogo annuale con grafico entrate "
         "vs spese e il tuo risparmio mese per mese. Tutto automatico."),
    ]
    y = 230
    for num, title, body in steps:
        d.rounded_rectangle([70, y, 150, y + 80], 16, fill=TEAL)
        d.text((98, y + 12), num, font=font(48, True), fill=WHITE)
        d.text((180, y + 6), title, font=font(32, True), fill=NAVY)
        for i, line in enumerate(wrap(d, body, font(24), 990)):
            d.text((180, y + 56 + i * 34), line, font=font(24), fill=INK)
        y += 220
    footer(d, W, H, 2)
    pages.append(img)

    # ---- Pagina 3: cosa c'è dentro + suggerimenti
    img, d = page()
    header_band(d, W, "Cosa c'e dentro")
    feats = [
        "Dashboard annuale automatica con grafico entrate vs spese",
        "12 fogli mensili con Budget vs Speso e differenza a colori",
        "Tasso di risparmio calcolato automaticamente",
        "Tracker degli obiettivi di risparmio con barre di avanzamento",
        "Categorie e budget completamente personalizzabili",
        "Compatibile con Microsoft Excel e Google Sheets",
    ]
    y = 220
    for fdesc in feats:
        d.ellipse([74, y + 8, 96, y + 30], fill=TEAL)
        d.line([80, y + 19, 85, y + 25], fill=WHITE, width=3)
        d.line([85, y + 25, 92, y + 13], fill=WHITE, width=3)
        for i, line in enumerate(wrap(d, fdesc, font(26), 1000)):
            d.text((120, y + i * 34), line, font=font(26), fill=INK)
        y += 84

    d.rounded_rectangle([70, y + 10, W - 70, y + 250], 18, fill=LIGHT)
    d.text((100, y + 35), "Suggerimenti", font=font(30, True), fill=NAVY)
    tips = [
        "Le celle verdi/rosse ti dicono a colpo d'occhio se sei dentro o fuori budget.",
        "Non modificare le celle con le formule (sfondo chiaro): si aggiornano da sole.",
        "Su Google Sheets: File > Importa > Carica e scegli 'Sostituisci foglio'.",
    ]
    yy = y + 85
    for tip in tips:
        d.text((100, yy), "•", font=font(26, True), fill=TEAL)
        for i, line in enumerate(wrap(d, tip, font(24), 980)):
            d.text((125, yy + i * 32), line, font=font(24), fill=INK)
        yy += 56
    footer(d, W, H, 3)
    pages.append(img)

    out = os.path.join(OUT_PROD, "Guida-Smart-Budget-Tracker.pdf")
    # Questo build di Pillow non ha l'encoder JPEG: converto le pagine in modalita
    # palette ("P") cosi il PDF usa la compressione Flate invece di DCT/JPEG.
    # Downscale leggero per contenere il peso del file mantenendo nitidezza.
    scale = 0.66
    pal = []
    for p in pages:
        small = p.resize((int(p.width * scale), int(p.height * scale)), Image.LANCZOS)
        # dither=NONE evita il rumore che gonfia il file su aree a tinta piatta
        pal.append(small.convert("P", palette=Image.ADAPTIVE, colors=64,
                                 dither=Image.Dither.NONE))
    pal[0].save(out, save_all=True, append_images=pal[1:], resolution=100.0,
                optimize=True)
    print(f"✅ PDF guida: {out} ({len(pages)} pagine)")


# --------------------------------------------------------------- HERO IMAGE ---
def rounded_panel(d, box, radius, fill):
    d.rounded_rectangle(box, radius, fill=fill)


def build_hero():
    W = H = 1500  # 1:1 Etsy
    img = Image.new("RGB", (W, H), LIGHT)
    d = ImageDraw.Draw(img)
    # banda titolo in alto
    d.rectangle([0, 0, W, 470], fill=NAVY)
    title = "SMART BUDGET"
    title2 = "TRACKER"
    d.text(((W - text_w(d, title, font(96, True))) // 2, 90), title,
           font=font(96, True), fill=WHITE)
    d.text(((W - text_w(d, title2, font(96, True))) // 2, 200), title2,
           font=font(96, True), fill=TEAL)
    sub = "Excel  +  Google Sheets  •  Aggiornamento automatico"
    d.text(((W - text_w(d, sub, font(34))) // 2, 340), sub, font=font(34), fill=(190, 200, 215))

    # mock "schermata" dashboard
    panel = [180, 540, W - 180, 1150]
    d.rounded_rectangle([panel[0] + 12, panel[1] + 14, panel[2] + 12, panel[3] + 14],
                        28, fill=(0, 0, 0))  # ombra
    rounded_panel(d, panel, 28, WHITE)
    d.rounded_rectangle([panel[0], panel[1], panel[2], panel[1] + 70], 28, fill=TEAL)
    d.rectangle([panel[0], panel[1] + 40, panel[2], panel[1] + 70], fill=TEAL)
    d.text((panel[0] + 40, panel[1] + 18), "Dashboard 2026", font=font(34, True), fill=WHITE)

    # KPI cards
    labels = [("Entrate", "32.400 €", (27, 127, 92)),
              ("Spese", "24.180 €", (192, 57, 43)),
              ("Risparmio", "8.220 €", NAVY)]
    cw = (panel[2] - panel[0] - 160) // 3
    cx = panel[0] + 40
    for lab, val, col in labels:
        d.rounded_rectangle([cx, panel[1] + 110, cx + cw, panel[1] + 250], 18, fill=LIGHT)
        d.text((cx + 24, panel[1] + 130), lab, font=font(26), fill=GREY)
        d.text((cx + 24, panel[1] + 170), val, font=font(40, True), fill=col)
        cx += cw + 40

    # mini bar chart
    base_y = panel[3] - 60
    bx = panel[0] + 60
    bars = [120, 180, 150, 210, 170, 240, 200, 260, 220, 280, 250, 300]
    bw = 56
    for i, hgt in enumerate(bars):
        col = TEAL if i % 2 == 0 else NAVY
        d.rectangle([bx, base_y - hgt, bx + bw, base_y], fill=col)
        bx += bw + 30

    # benefit strip
    d.rounded_rectangle([180, 1210, W - 180, 1360], 22, fill=WHITE)
    benefits = "Budget vs Speso  •  Tasso di risparmio  •  Obiettivi"
    d.text(((W - text_w(d, benefits, font(36, True))) // 2, 1255), benefits,
           font=font(36, True), fill=NAVY)

    # download badge
    badge = "DOWNLOAD DIGITALE ISTANTANEO"
    bf = font(26, True)
    bw = text_w(d, badge, bf)
    d.rounded_rectangle([W // 2 - bw // 2 - 45, 1400, W // 2 + bw // 2 + 45, 1470], 35, fill=TEAL)
    d.text(((W - bw) // 2, 1420), badge, font=bf, fill=WHITE)

    out = os.path.join(OUT_IMG, "01-hero-image.png")
    img.save(out)
    print(f"✅ Hero image: {out}")


# ----------------------------------------------------------- WHAT'S INCLUDED --
def build_whats_included():
    W = H = 1500
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 200], fill=NAVY)
    d.text((70, 60), "Cosa ricevi", font=font(70, True), fill=WHITE)
    d.rectangle([0, 200, W, 208], fill=TEAL)

    items = [
        ("Foglio Dashboard", "Riepilogo annuale automatico + grafico"),
        ("12 fogli mensili", "Budget vs Speso con differenza a colori"),
        ("Foglio Setup", "Categorie e budget personalizzabili"),
        ("Obiettivi di risparmio", "Barre di avanzamento automatiche"),
        ("Guida PDF", "Istruzioni passo-passo per iniziare"),
        ("Excel + Google Sheets", "Funziona su entrambi, nessuna app"),
    ]
    y = 280
    for i, (t, sub) in enumerate(items):
        box = [70, y, W - 70, y + 160]
        d.rounded_rectangle(box, 22, fill=LIGHT)
        d.rounded_rectangle([90, y + 30, 200, y + 130], 18, fill=TEAL)
        d.text((128, y + 48), str(i + 1), font=font(56, True), fill=WHITE)
        d.text((240, y + 38), t, font=font(40, True), fill=NAVY)
        d.text((240, y + 92), sub, font=font(28), fill=GREY)
        y += 190

    out = os.path.join(OUT_IMG, "05-whats-included.png")
    img.save(out)
    print(f"✅ What's included: {out}")


if __name__ == "__main__":
    build_pdf_guide()
    build_hero()
    build_whats_included()
