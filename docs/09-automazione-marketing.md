# 9 — Automazione del marketing (FASE 8 operativa)

Questo modulo rende **continuo e automatico** il marketing dei prodotti pubblicati. Genera i
contenuti, li programma e li distribuisce sui canali — mantenendo **gate umani su tutto ciò
che costa denaro** (ads) e sul tono del brand.

> Principio: **organico prima, paid dopo**. L'agente automatizza al 100% l'organico
> (Pinterest, contenuti social, email), mentre lo spend pubblicitario resta sempre dietro
> 🧑 GATE BUDGET.

## Cosa fa il motore (`tools/marketing/`)
1. Legge una scheda prodotto (JSON) con angoli, keyword, link.
2. Genera un **calendario editoriale di 30 giorni** multi-canale con copy pronto.
3. Esporta:
   - `marketing-calendar.csv` → import diretto in **Tailwind / Buffer / Later / Make / n8n**
   - `marketing-calendar.md` → revisione umana leggibile
4. Genera automaticamente le **immagini dei pin Pinterest** (2:3, brandizzate).

```bash
pip install pillow
python3 tools/marketing/generate.py tools/marketing/product.budget-tracker.json \
        --giorni 30 --pin 6 --out esempi/budget-tracker/marketing
```

## Canali e cadenza (default)
| Canale | Frequenza | Formato | Automazione | Gate |
|--------|-----------|---------|-------------|------|
| **Pinterest** | 5×/settimana | Pin statici/idea pin | piena (API/Tailwind) | no |
| **Instagram/TikTok Reels** | 2×/settimana | video 15-30s | semi (script+caption auto, upload manuale o Make) | no |
| **Instagram feed/story** | 2×/settimana | carosello/story | semi | no |
| **Etsy** | eventi (sale, novità) | promo shop | manuale | 🧑 se sconto |
| **Email** (se hai lista) | 1×/settimana | newsletter | piena | no |
| **Etsy Ads / Pinterest Ads** | a test | paid | preparazione auto | 🧑 **BUDGET** |

## Architettura dell'automazione

```
                ┌────────────────────────────────────────────┐
                │  Scheda prodotto (JSON): angoli, keyword,    │
                │  link listing, hashtag, palette              │
                └───────────────┬──────────────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  CONTENT ENGINE         │
                    │  • copy_library (angoli,│
                    │    hook, template)      │
                    │  • calendar builder     │
                    │  • pin image generator  │
                    └───────────┬────────────┘
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
   marketing-calendar.csv   pins/*.png      marketing-calendar.md
              │                 │                  │
   ┌──────────▼─────────┐  ┌────▼─────┐    ┌───────▼────────┐
   │ Scheduler           │  │ Pinterest│    │ 🧑 revisione    │
   │ (Make/n8n/Tailwind) │  │ /Tailwind│    │ umana tono     │
   │ pubblica organico   │  │ upload   │    │ brand          │
   └─────────────────────┘  └──────────┘    └────────────────┘
```

## Flussi schedulati (si agganciano ai job di [05-automazioni](05-automazioni.md))
| ID | Job | Frequenza | Cosa fa | Gate |
|----|-----|-----------|---------|------|
| M1 | **Content Refresh** | lunedì 10:00 | rigenera il calendario settimana successiva | no |
| M2 | **Pinterest Auto-Pin** | gg feriali | pubblica i pin programmati del giorno | no |
| M3 | **Reel Prep** | mar/gio | prepara script+caption+hashtag del Reel | no |
| M4 | **Email Weekly** | giovedì | invia newsletter (se lista presente) | no |
| M5 | **Ads Proposal** | a richiesta | prepara campagna ads (keyword, budget, creatività) | 🧑 **BUDGET** |
| M6 | **Perf → Content loop** | settimanale | i contenuti che convertono diventano template | no |

## Come collegarlo agli strumenti (no-code)
- **Make/n8n:** un modulo "Watch CSV/Sheets" legge `marketing-calendar.csv` riga per riga e,
  alla data/ora schedulata, chiama l'API del canale (Pinterest, IG Graph, email).
- **Tailwind:** import diretto del CSV per i pin Pinterest (campi: image, board, title,
  description, date).
- **Buffer/Later:** import del CSV per IG/TikTok.

## Cosa resta SEMPRE umano
- 🧑 **Budget ads** (M5): l'agente prepara tutto, tu approvi la spesa.
- 🧑 **Sconti/promo Etsy** che cambiano il prezzo.
- 🧑 **Tono di voce** la prima settimana: rivedi il calendario `.md` prima di automatizzare.

## Metriche e loop di ottimizzazione
Il job M6 chiude il cerchio con la [FASE 7](04-moduli-agente.md): i pin/hook con più
salvataggi e click diventano **template vincenti** riusati e variati, quelli deboli vengono
ritirati. Così il marketing migliora da solo nel tempo.
