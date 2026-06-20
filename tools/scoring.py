#!/usr/bin/env python3
"""
Motore di scoring per la FASE 2 (Validazione prodotto) di Agente-1.

Calcola un punteggio pesato 0-10 su 10 criteri. Solo i prodotti con punteggio
>= 8.0 sono idonei alla creazione (FASE 3).

Uso:
    python3 tools/scoring.py tools/product_data.example.json
    python3 tools/scoring.py prodotto.json --soglia 8.0

Il file JSON deve contenere un oggetto "criteri" con i 10 punteggi 0-10.
Vedi tools/product_data.example.json per il formato.

Principio: lo script NON inventa dati. Se un criterio manca, fallisce in modo
esplicito invece di indovinare.
"""
from __future__ import annotations

import argparse
import json
import sys

# Pesi dei 10 criteri (FASE 2). Somma = 1.0.
# Tarati per prodotti digitali Etsy: domanda, margine, facilità e velocità pesano
# di più perché determinano "vendibile in fretta + alto margine".
PESI: dict[str, float] = {
    "domanda": 0.16,
    "concorrenza": 0.12,
    "evergreen": 0.10,
    "facilita_creazione": 0.12,
    "margine": 0.12,
    "differenziazione": 0.10,
    "potenziale_seo": 0.08,
    "potenziale_pinterest": 0.08,
    "potenziale_ads": 0.04,
    "velocita_pubblicazione": 0.08,
}

ETICHETTE = {
    "domanda": "Domanda",
    "concorrenza": "Concorrenza (alto = poco affollato)",
    "evergreen": "Evergreen",
    "facilita_creazione": "Facilità di creazione",
    "margine": "Margine",
    "differenziazione": "Differenziazione",
    "potenziale_seo": "Potenziale SEO",
    "potenziale_pinterest": "Potenziale Pinterest",
    "potenziale_ads": "Potenziale ads",
    "velocita_pubblicazione": "Velocità di pubblicazione",
}

SOGLIA_DEFAULT = 8.0


def valida_criteri(criteri: dict) -> list[str]:
    """Ritorna la lista di errori (vuota se tutto ok). Non indovina valori mancanti."""
    errori: list[str] = []
    for chiave in PESI:
        if chiave not in criteri:
            errori.append(f"Criterio mancante: '{chiave}'")
            continue
        val = criteri[chiave]
        if not isinstance(val, (int, float)):
            errori.append(f"'{chiave}' deve essere un numero 0-10 (trovato: {val!r})")
        elif not 0 <= val <= 10:
            errori.append(f"'{chiave}' fuori range 0-10: {val}")
    extra = set(criteri) - set(PESI)
    if extra:
        errori.append(f"Criteri non riconosciuti: {', '.join(sorted(extra))}")
    return errori


def calcola(criteri: dict) -> tuple[float, list[tuple[str, float, float, float]]]:
    """Ritorna (totale, dettaglio). dettaglio = [(etichetta, valore, peso, contributo)]."""
    dettaglio = []
    totale = 0.0
    for chiave, peso in PESI.items():
        valore = float(criteri[chiave])
        contributo = valore * peso
        totale += contributo
        dettaglio.append((ETICHETTE[chiave], valore, peso, contributo))
    return round(totale, 2), dettaglio


def verdetto(totale: float, soglia: float) -> str:
    if totale >= soglia:
        return "CREA"
    if totale >= soglia - 1.0:
        return "RICERCA ANCORA"
    return "SCARTA"


def stampa_report(nome: str, totale: float, dettaglio, soglia: float) -> None:
    print(f"\n{'=' * 56}")
    print(f"  SCORING PRODOTTO: {nome}")
    print(f"{'=' * 56}")
    print(f"  {'Criterio':<40}{'Val':>4} {'Peso':>5}")
    print(f"  {'-' * 50}")
    for etichetta, valore, peso, _ in dettaglio:
        print(f"  {etichetta:<40}{valore:>4.0f} {peso:>5.2f}")
    print(f"  {'-' * 50}")
    print(f"  {'TOTALE PESATO':<40}{totale:>4.1f} /10")
    esito = verdetto(totale, soglia)
    simbolo = "✅" if esito == "CREA" else ("🟡" if esito == "RICERCA ANCORA" else "❌")
    print(f"\n  Soglia minima: {soglia}/10")
    print(f"  VERDETTO: {simbolo} {esito}")
    print(f"{'=' * 56}\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scoring FASE 2 — Agente-1")
    parser.add_argument("file", help="file JSON del prodotto")
    parser.add_argument("--soglia", type=float, default=SOGLIA_DEFAULT,
                        help=f"punteggio minimo per CREA (default {SOGLIA_DEFAULT})")
    parser.add_argument("--json", action="store_true",
                        help="output in JSON invece del report leggibile")
    args = parser.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as f:
            dati = json.load(f)
    except FileNotFoundError:
        print(f"Errore: file non trovato: {args.file}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Errore: JSON non valido ({e})", file=sys.stderr)
        return 2

    criteri = dati.get("criteri")
    if not isinstance(criteri, dict):
        print("Errore: il file deve contenere un oggetto 'criteri'.", file=sys.stderr)
        return 2

    errori = valida_criteri(criteri)
    if errori:
        print("Validazione fallita (lo script non indovina i dati mancanti):",
              file=sys.stderr)
        for err in errori:
            print(f"  - {err}", file=sys.stderr)
        return 2

    nome = dati.get("nome_prodotto", "(senza nome)")
    totale, dettaglio = calcola(criteri)
    esito = verdetto(totale, args.soglia)

    if args.json:
        print(json.dumps({
            "nome_prodotto": nome,
            "totale": totale,
            "soglia": args.soglia,
            "verdetto": esito,
            "idoneo_creazione": totale >= args.soglia,
        }, ensure_ascii=False, indent=2))
    else:
        stampa_report(nome, totale, dettaglio, args.soglia)

    # exit code 0 se idoneo, 1 se sotto soglia → utile negli workflow automatizzati.
    return 0 if totale >= args.soglia else 1


if __name__ == "__main__":
    raise SystemExit(main())
