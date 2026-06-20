# 2 — Strumenti consigliati

Tre profili di stack in base a budget/competenze. Puoi partire dal **Profilo A (no-code)**
e migrare verso il C quando i volumi crescono.

## Profilo A — No-code (start veloce, ~0-50 €/mese)

| Funzione | Strumento | Note |
|----------|-----------|------|
| Cervello/LLM | **Claude** (Opus/Sonnet) | ricerca, scrittura SEO, idee, prompt mockup |
| Orchestrazione | **Make.com** o **n8n (cloud)** | scenari visuali, scheduling |
| Database/Stato | **Airtable** o **Notion DB** | backlog, pipeline, metriche |
| Mockup/Immagini | **Canva** + **Midjourney/DALL·E** | mockup e creatività |
| Trend | **Google Trends** (UI), **Pinterest Trends** (UI) | lettura manuale assistita |
| SEO Etsy | **eRank** o **Marmalead** | keyword, tag, stime domanda *reali* |
| Pubblicazione | **Etsy** (manuale, supervisionata) | l'agente prepara, tu pubblichi |
| Reporting | **Google Sheets** + Looker Studio | dashboard performance |

## Profilo B — Low-code (scala media, ~50-150 €/mese)

| Funzione | Strumento | Note |
|----------|-----------|------|
| Orchestrazione | **n8n self-hosted** | costi marginali bassi, controllo totale |
| LLM via API | **Anthropic API** (Claude) | chiamate programmatiche dai workflow |
| Database | **Supabase / Postgres** | query SQL, time-series metriche |
| Etsy data | **Etsy Open API v3** | listing, stats shop (con OAuth, vedi sotto) |
| Trend data | **Google Trends** via `pytrends` | rispettando rate limit |
| Immagini | **API Midjourney/Ideogram** + **Bannerbear** | mockup automatizzati con testo |
| Pinterest | **Pinterest API** | pubblicazione pin programmata |

## Profilo C — Custom (scala alta)

Microservizi Python + coda (Celery/Redis) + Postgres + dashboard dedicata. Da valutare solo
quando hai decine di listing e volumi che giustificano lo sviluppo.

---

## API ufficiali (preferire sempre alle scorciatoie)

- **Etsy Open API v3** — `https://developers.etsy.com/` — OAuth 2.0. Permette: gestione
  listing, lettura statistiche shop, immagini, inventario. ✅ canale legittimo, niente
  scraping.
- **Pinterest API** — pubblicazione pin, analytics.
- **Google Trends** — non ha API ufficiale stabile; usare `pytrends` con cautela e rate
  limit, oppure lettura manuale dalla UI.
- **TikTok** — per i trend usare la UI / Creative Center; nessuno scraping non autorizzato.

## Cosa NON usare

- ❌ Scraper che violano i ToS di Etsy/Pinterest/TikTok/Google.
- ❌ Tool che promettono "dati nascosti" aggirando le piattaforme.
- ❌ Auto-pubblicazione senza gate umano.

> **Per la stima di domanda/concorrenza su Etsy** usa **eRank/Marmalead**: forniscono dati
> reali (volumi di ricerca, competizione, engagement) in modo conforme. Sono la fonte
> primaria della FASE 1 per evitare di inventare numeri.

## Credenziali e segreti

Tutte le chiavi (Anthropic, Etsy OAuth, Pinterest, eRank) vanno in un **secret manager**
(variabili d'ambiente, `.env` mai committato, o il vault del tuo orchestratore). Vedi
[06-permessi-sicurezza](06-permessi-sicurezza.md).

## Stack minimo consigliato per partire OGGI

1. **Claude** (cervello)
2. **eRank** (dati keyword/domanda reali)
3. **Airtable** (stato/pipeline) — importa lo schema da `templates/`
4. **Canva** (mockup)
5. **Etsy** (pubblicazione manuale supervisionata)

Con questi 5 sei operativo senza scrivere codice. L'automazione (Make/n8n) si aggiunge dopo.
