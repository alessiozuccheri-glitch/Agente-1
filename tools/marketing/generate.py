#!/usr/bin/env python3
"""
Motore di automazione marketing per Agente-1 (FASE 8).

Da una scheda prodotto (JSON) genera:
  - marketing-calendar.csv   → import in Tailwind / Buffer / Make / n8n
  - marketing-calendar.md    → revisione umana
  - reels-scripts.md         → script video pronti
  - pins/pin-NN.png          → immagini pin Pinterest brandizzate

Uso:
    pip install pillow
    python3 tools/marketing/generate.py tools/marketing/product.budget-tracker.json \
            --giorni 30 --pin 6 --out esempi/budget-tracker/marketing

Principi:
  - Solo contenuti ORGANICI sono marcati come pubblicabili in automatico.
  - Le righe "ads" hanno approva_umano = SI (gate budget).
  - Nessun dato di mercato inventato: qui si generano asset creativi (copy/immagini).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import copy_library as lib  # noqa: E402
import pins as pinmod        # noqa: E402

# Piano settimanale: (canale, formato, giorni_settimana[0=lun]) — cadenza organica.
PIANO = [
    ("Pinterest", "Pin",   [0, 1, 2, 3, 4]),   # 5x a settimana
    ("Instagram", "Reel",  [1, 3]),            # 2x
    ("TikTok",    "Reel",  [1, 4]),            # 2x
    ("Instagram", "Story", [0, 3]),            # 2x
    ("Email",     "Newsletter", [3]),          # 1x (giovedì)
]


def carica(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fill(template, p, extra=None):
    kw1 = p["keyword"][0]
    kw2 = p["keyword"][1] if len(p["keyword"]) > 1 else kw1
    data = {
        "prodotto": p["nome"],
        "nicchia": p["nicchia"],
        "benefit": p["benefit"],
        "benefit_breve": p["benefit_breve"],
        "keyword1": kw1,
        "keyword2": kw2,
        "kw1_tag": kw1.replace(" ", ""),   # hashtag-safe (niente spazi)
        "kw2_tag": kw2.replace(" ", ""),
        "link": p["link"],
    }
    if extra:
        data.update(extra)
    try:
        return template.format(**data)
    except (KeyError, IndexError):
        return template


def costruisci_calendario(p, giorni, start, n_pin=6):
    """Ritorna lista di righe (dict) ordinate per data.

    n_pin = numero di immagini pin effettivamente generate: gli asset del
    calendario ciclano su questi (i pin si ripubblicano/repinnano nel tempo).
    """
    righe = []
    n_hook = n_pin_t = n_pin_d = n_cap = n_email = 0
    n_pin = max(1, n_pin)
    for offset in range(giorni):
        day = start + dt.timedelta(days=offset)
        wd = day.weekday()
        for canale, formato, giorni_sett in PIANO:
            if wd not in giorni_sett:
                continue
            if formato == "Pin":
                titolo = lib.PIN_TITLE[n_pin_t % len(lib.PIN_TITLE)]
                desc = fill(lib.PIN_DESC[n_pin_d % len(lib.PIN_DESC)], p)
                n_pin_t += 1
                n_pin_d += 1
                righe.append(_riga(day, canale, formato, titolo, desc,
                                   lib.HASHTAG["pinterest"], p,
                                   asset=f"pins/pin-{(n_pin_t-1) % n_pin:02d}.png",
                                   board="Budget & Risparmio"))
            elif formato == "Reel":
                hook = lib.HOOK_VIDEO[n_hook % len(lib.HOOK_VIDEO)]
                cap = fill(lib.CAPTION[n_cap % len(lib.CAPTION)], p, {"hook": hook})
                n_hook += 1
                n_cap += 1
                tag = lib.HASHTAG["tiktok"] if canale == "TikTok" else lib.HASHTAG["instagram"]
                righe.append(_riga(day, canale, formato, hook, cap, tag, p,
                                   asset="reels-scripts.md"))
            elif formato == "Story":
                hook = lib.HOOK_VIDEO[(n_hook + 2) % len(lib.HOOK_VIDEO)]
                righe.append(_riga(day, canale, formato, "Story: sondaggio/teaser",
                                   f"{hook} (sticker domanda + link allo shop)",
                                   "", p, asset=""))
            elif formato == "Newsletter":
                oggetto, _ = lib.EMAIL[n_email % len(lib.EMAIL)]
                n_email += 1
                righe.append(_riga(day, canale, formato, oggetto,
                                   fill("{benefit} Scopri {prodotto}: {link}", p),
                                   "", p, asset=""))
    return righe


def _riga(day, canale, formato, titolo, testo, hashtag, p, asset="", board=""):
    return {
        "data": day.isoformat(),
        "ora": "10:00",
        "canale": canale,
        "formato": formato,
        "titolo": titolo,
        "testo": testo,
        "hashtag": hashtag,
        "board": board,
        "asset": asset,
        "link": p["link"],
        "stato": "DRAFT",
        "approva_umano": "NO",   # organico → automatizzabile
    }


def riga_ads(p, start):
    """Una riga proposta ads, SEMPRE con gate umano (budget)."""
    return {
        "data": (start + dt.timedelta(days=14)).isoformat(),
        "ora": "—",
        "canale": "Etsy Ads",
        "formato": "Paid (proposta)",
        "titolo": "Test ads su keyword principali",
        "testo": f"Budget test 3-5€/giorno per 7-14 giorni su: {', '.join(p['keyword'][:4])}. "
                 "Attivare SOLO dopo prime vendite organiche.",
        "hashtag": "",
        "board": "",
        "asset": "mockup-prompts/08-ads-creative",
        "link": p["link"],
        "stato": "PROPOSTA",
        "approva_umano": "SI",   # 🧑 GATE BUDGET
    }


CAMPI = ["data", "ora", "canale", "formato", "titolo", "testo", "hashtag",
         "board", "asset", "link", "stato", "approva_umano"]


def scrivi_csv(righe, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPI)
        w.writeheader()
        w.writerows(righe)


def scrivi_md(righe, p, path):
    org = [r for r in righe if r["approva_umano"] == "NO"]
    ads = [r for r in righe if r["approva_umano"] == "SI"]
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Calendario marketing — {p['nome']}\n\n")
        f.write(f"Periodo: {righe[0]['data']} → {righe[-1]['data']} · "
                f"{len(org)} contenuti organici + {len(ads)} proposte ads.\n\n")
        f.write("> Organico = automatizzabile (`approva_umano=NO`). "
                "Ads = 🧑 richiede approvazione budget.\n\n")
        f.write("| Data | Canale | Formato | Titolo / Hook | Asset |\n")
        f.write("|------|--------|---------|---------------|-------|\n")
        for r in righe:
            flag = " 🧑" if r["approva_umano"] == "SI" else ""
            f.write(f"| {r['data']} | {r['canale']}{flag} | {r['formato']} | "
                    f"{r['titolo']} | {r['asset']} |\n")
        f.write("\n## Conteggio per canale\n\n")
        canali = {}
        for r in righe:
            canali[r["canale"]] = canali.get(r["canale"], 0) + 1
        for c, n in sorted(canali.items(), key=lambda x: -x[1]):
            f.write(f"- **{c}**: {n}\n")


def scrivi_reels(p, path, n=6):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Script Reels / TikTok — {p['nome']}\n\n")
        for i in range(n):
            hook = lib.HOOK_VIDEO[i % len(lib.HOOK_VIDEO)]
            f.write(f"## Reel {i+1}\n\n")
            for sezione, testo in lib.SCRIPT_SEZIONI:
                line = fill(testo, p, {"hook": hook})
                f.write(f"- **{sezione}:** {line}\n")
            cap = fill(lib.CAPTION[i % len(lib.CAPTION)], p, {"hook": hook})
            f.write(f"\n  _Caption:_ {cap}\n")
            f.write(f"\n  _Hashtag:_ {lib.HASHTAG['tiktok']}\n\n---\n\n")


def genera_pin(p, out_dir, n):
    pin_dir = os.path.join(out_dir, "pins")
    os.makedirs(pin_dir, exist_ok=True)
    creati = []
    for i in range(n):
        hook = lib.PIN_TITLE[i % len(lib.PIN_TITLE)]
        out = os.path.join(pin_dir, f"pin-{i:02d}.png")
        pinmod.make_pin(hook, p.get("cta_pin", "Scarica ora"), p["palette"], out, variant=i)
        creati.append(out)
    return creati


def main(argv=None):
    ap = argparse.ArgumentParser(description="Motore marketing — Agente-1")
    ap.add_argument("product", help="scheda prodotto JSON")
    ap.add_argument("--giorni", type=int, default=30)
    ap.add_argument("--pin", type=int, default=6, help="numero di pin immagine da generare")
    ap.add_argument("--start", default=None, help="data inizio YYYY-MM-DD (default oggi)")
    ap.add_argument("--out", default="marketing-output")
    args = ap.parse_args(argv)

    p = carica(args.product)
    start = (dt.date.fromisoformat(args.start) if args.start else dt.date.today())
    os.makedirs(args.out, exist_ok=True)

    righe = costruisci_calendario(p, args.giorni, start, n_pin=max(1, args.pin))
    righe.append(riga_ads(p, start))
    righe.sort(key=lambda r: (r["data"], r["canale"]))

    scrivi_csv(righe, os.path.join(args.out, "marketing-calendar.csv"))
    scrivi_md(righe, p, os.path.join(args.out, "marketing-calendar.md"))
    scrivi_reels(p, os.path.join(args.out, "reels-scripts.md"))
    pin_files = genera_pin(p, args.out, args.pin) if args.pin else []

    org = sum(1 for r in righe if r["approva_umano"] == "NO")
    print(f"✅ Calendario: {len(righe)} righe ({org} organiche, "
          f"{len(righe)-org} ads con gate umano)")
    print(f"✅ Pin generati: {len(pin_files)}")
    print(f"📂 Output in: {os.path.normpath(args.out)}")


if __name__ == "__main__":
    main()
