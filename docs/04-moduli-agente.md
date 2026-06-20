# 4 — Moduli dell'agente (sotto-agenti)

Ogni modulo è un "ruolo" con obiettivo, input, output e prompt dedicato (cartella
[`prompts/`](../prompts/)). L'orchestratore li attiva nell'ordine del workflow.

| Modulo | Ruolo umano equivalente | Obiettivo | Prompt |
|--------|------------------------|-----------|--------|
| **M1 · Market Research** | Market Research Analyst | Trovare opportunità reali | `prompts/fase1-ricerca-mercato.md` |
| **M2 · Validator** | Strategist | Scoring 8/10 oggettivo | `prompts/fase2-validazione.md` |
| **M3 · Product Builder** | Digital Product Creator | Creare il prodotto finito | `prompts/fase3-creazione-prodotto.md` |
| **M4 · Mockup Designer** | Mockup Designer | Immagini ad alta conversione | `prompts/fase4-mockup-immagini.md` |
| **M5 · Etsy SEO Writer** | Etsy SEO Expert | Titolo/tag/descrizione/prezzo | `prompts/fase5-seo-etsy.md` |
| **M6 · Performance Tracker** | E-commerce Manager + CRO | Leggere metriche, trovare problemi | `prompts/fase7-monitoraggio.md` |
| **M7 · Growth/Ads** | Pinterest Growth + Ads Strategist | Traffico organico e paid | `prompts/fase8-ads-traffico.md` |
| **M0 · Orchestrator** | Responsabile operativo | Coordinare, gestire i gate umani | — (logica in [05-automazioni](05-automazioni.md)) |

## Dettaglio moduli

### M1 — Market Research
- **Input:** nicchie target, data.
- **Fa:** interroga eRank/Marmalead, legge autocomplete Etsy, bestseller, trend
  Pinterest/Google/TikTok, recensioni competitor.
- **Output:** schede `ProductOpportunity` con fonte di ogni dato.
- **Guardrail:** se non trova dati reali per un campo → lo marca `IPOTESI_DA_VALIDARE`, non
  inventa.

### M2 — Validator
- **Input:** scheda opportunità.
- **Fa:** compila i 10 criteri, esegue `tools/scoring.py`.
- **Output:** punteggio + raccomandazione (crea / scarta / serve più ricerca).

### M3 — Product Builder
- **Input:** idea approvata (≥8/10).
- **Fa:** struttura, testo, file finale, copertina, varianti, bonus, istruzioni, naming.
- **Output:** cartella prodotto pronta + checklist QA premium.

### M4 — Mockup Designer
- **Input:** prodotto + brand style.
- **Fa:** genera prompt immagine (Midjourney/DALL·E/Ideogram) e/o layout Canva per gli 8 tipi
  di immagine richiesti.
- **Output:** set immagini listing + pin + ads, con prompt riproducibili.

### M5 — Etsy SEO Writer
- **Input:** prodotto + keyword dalla FASE 1.
- **Fa:** titolo ≤140, 13 tag, descrizione, bullet, materiali, categoria, prezzo, sconto,
  bundle, upsell.
- **Output:** `templates/etsy-listing.md` compilato.

### M6 — Performance Tracker
- **Input:** metriche giornaliere (Etsy stats / API).
- **Fa:** calcola CTR e conversion, confronta con benchmark, individua underperformer,
  propone A/B test.
- **Output:** report + lista azioni prioritizzate.

### M7 — Growth/Ads
- **Input:** prodotto pubblicato + obiettivo traffico.
- **Fa:** pin Pinterest, caption/hook TikTok-IG, idee Etsy Ads, target, budget test.
- **Output:** piano traffico + creatività.

### M0 — Orchestrator
- Pianifica i job (cron), instrada i task, **accoda le approvazioni umane** in un unico
  riepilogo, aggiorna lo stato in DB, garantisce idempotenza.

## Come comunicano

Tutti leggono/scrivono lo stesso oggetto `ProductOpportunity`/`Product`/`Listing` (vedi
[01-architettura](01-architettura-tecnica.md)). Questo rende i moduli **intercambiabili**:
puoi sostituire Midjourney con Ideogram senza toccare gli altri.
