# Motore di automazione marketing (FASE 8)

Genera un **calendario editoriale multi-canale** + le **immagini dei pin Pinterest** da una
scheda prodotto JSON. Output pronti per gli scheduler (Tailwind/Buffer/Make/n8n).

Architettura e flussi schedulati: vedi [docs/09-automazione-marketing.md](../../docs/09-automazione-marketing.md).

## Uso
```bash
pip install pillow
python3 tools/marketing/generate.py tools/marketing/product.budget-tracker.json \
        --giorni 30 --pin 6 --start 2026-07-01 --out esempi/budget-tracker/marketing
```

| Opzione | Default | Descrizione |
|---------|---------|-------------|
| `--giorni` | 30 | durata del calendario |
| `--pin` | 6 | numero di immagini pin da generare (riusate/repinnate nel calendario) |
| `--start` | oggi | data di inizio `YYYY-MM-DD` |
| `--out` | `marketing-output` | cartella di output |

## Output generati
| File | Uso |
|------|-----|
| `marketing-calendar.csv` | import diretto in Tailwind / Buffer / Later / Make / n8n |
| `marketing-calendar.md` | revisione umana leggibile (tono brand) |
| `reels-scripts.md` | script video TikTok/Reels pronti (hook → CTA) |
| `pins/pin-NN.png` | pin Pinterest brandizzati 2:3 (1000×1500) |

Colonne CSV: `data, ora, canale, formato, titolo, testo, hashtag, board, asset, link, stato,
approva_umano`.

## File del motore
| File | Ruolo |
|------|-------|
| `generate.py` | CLI: costruisce calendario, CSV/MD, script, pin |
| `copy_library.py` | angoli, hook, template copy, hashtag (personalizzabili) |
| `pins.py` | generazione immagini pin con Pillow (3 layout) |
| `product.budget-tracker.json` | scheda prodotto di esempio (input) |

## Adattarlo a un nuovo prodotto
Copia `product.budget-tracker.json`, cambia `nome`, `nicchia`, `benefit`, `keyword`, `link`,
`palette` e rilancia. Per nicchie diverse dalla finanza, aggiorna gli hook/angoli in
`copy_library.py`.

## Sicurezza / gate
- Le righe **organiche** hanno `approva_umano = NO` → automatizzabili.
- La riga **ads** ha `approva_umano = SI` → 🧑 **GATE BUDGET**: l'agente prepara la campagna
  ma la spesa la approvi tu.
- Rivedi il `.md` la prima settimana per validare il tono prima di automatizzare del tutto.
