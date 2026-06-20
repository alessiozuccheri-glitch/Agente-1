# 1 — Architettura tecnica dell'agente

## Visione d'insieme

Agente-1 è un **agente orchestratore** che coordina più moduli specializzati (sotto-agenti).
Non è un singolo prompt: è un sistema a livelli, dove ogni livello ha una responsabilità
chiara e passa output strutturato al successivo. L'umano è inserito come **gate di
approvazione** nei punti irreversibili.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LIVELLO 0 — ORCHESTRATORE                       │
│  Pianifica la giornata, instrada i task ai moduli, raccoglie output,  │
│  gestisce la coda di approvazioni umane e lo stato (memoria).         │
└───────────────┬───────────────────────────────────────┬─────────────┘
                │                                         │
   ┌────────────▼─────────────┐              ┌───────────▼────────────┐
   │  LIVELLO 1 — RICERCA      │              │  LIVELLO 4 — GROWTH    │
   │  • Market Research        │              │  • Pinterest           │
   │  • Trend Scanner          │              │  • Ads Strategist      │
   │  • Competitor Analyst     │              │  • Social/Content      │
   └────────────┬─────────────┘              └───────────▲────────────┘
                │                                         │
   ┌────────────▼─────────────┐              ┌───────────┴────────────┐
   │  LIVELLO 2 — VALIDAZIONE  │              │  LIVELLO 5 — MONITOR   │
   │  • Scoring Engine (8/10)  │              │  • Performance Tracker │
   └────────────┬─────────────┘              │  • Optimizer           │
                │                             └───────────▲────────────┘
   ┌────────────▼─────────────┐                          │
   │  LIVELLO 3 — CREAZIONE    │              ┌───────────┴────────────┐
   │  • Product Builder        │──────────────▶  GATE UMANO            │
   │  • Mockup/Image Designer  │   APPROVA?   │  pubblicazione, budget │
   │  • Etsy SEO Writer        │              └────────────────────────┘
   └───────────────────────────┘
```

## Livelli e responsabilità

### Livello 0 — Orchestratore
- **Scheduler**: avvia i job giornalieri (vedi [05-automazioni](05-automazioni.md)).
- **Router**: decide quale modulo gestisce ogni task.
- **State/Memory**: tiene traccia di idee, punteggi, prodotti in pipeline, performance
  storiche. Persistenza su un DB semplice (Airtable / Google Sheets / SQLite / Notion DB).
- **Human-in-the-loop queue**: accumula le azioni che richiedono approvazione e te le
  presenta in un unico riepilogo (no decisioni sparse).

### Livello 1 — Ricerca (FASE 1)
Raccoglie segnali **reali** da fonti consentite e li normalizza in "schede opportunità".
Mai inferenza spacciata per dato: ogni numero ha fonte + timestamp.

### Livello 2 — Validazione (FASE 2)
Applica il [motore di scoring](../tools/scoring.py). Solo punteggio ≥ 8/10 prosegue.

### Livello 3 — Creazione (FASI 3-5)
Genera prodotto, mockup/prompt immagine e pacchetto SEO. Output "pronto all'uso".

### Livello 4 — Growth (FASE 8)
Produce pin Pinterest, creatività ads, script TikTok/Reels, angoli e target.

### Livello 5 — Monitoraggio (FASE 7)
Legge le metriche, individua underperformer, propone ottimizzazioni A/B.

## Flusso dati (data contract)

Ogni passaggio tra livelli usa un **oggetto strutturato** (JSON) per evitare ambiguità.
Schema dell'oggetto `ProductOpportunity`:

```json
{
  "id": "opp_2026_0001",
  "stato": "ricerca | validato | in_creazione | pronto | in_attesa_approvazione | pubblicato | archiviato",
  "nome_prodotto": "string",
  "nicchia": "string",
  "cliente_ideale": "string",
  "problema_risolto": "string",
  "segnali": {
    "domanda": {"valore": "string", "fonte": "Etsy autocomplete | Google Trends | ...", "data": "2026-06-20", "stato": "IPOTESI_DA_VALIDARE | VERIFICATO"},
    "concorrenza": {"n_listing": null, "fonte": "...", "stato": "..."},
    "saturazione": "bassa | media | alta",
    "trend": {"direzione": "su | stabile | giu", "fonte": "Google Trends", "stato": "..."}
  },
  "keyword_principali": [],
  "keyword_secondarie": [],
  "margine_potenziale": "string",
  "difficolta_creazione": "1-10",
  "scoring": {"totale": 0, "soglia": 8, "dettaglio": {}},
  "rischi": [],
  "priorita": "1-10"
}
```

Questo contratto è la "spina dorsale": qualsiasi tool (Make, n8n, script Python, Notion)
può leggere/scrivere lo stesso oggetto.

## Memoria e stato

- **Backlog idee** → tabella `opportunities`
- **Prodotti in pipeline** → tabella `products`
- **Listing pubblicati** → tabella `listings`
- **Metriche giornaliere** → tabella `metrics` (time-series)
- **Log decisioni umane** → tabella `approvals` (audit trail di chi ha approvato cosa e quando)

## Principi architetturali non negoziabili

1. **Human gate prima dell'irreversibile** (pubblicazione, spesa, delete, modifica prezzo).
2. **Provenienza del dato sempre tracciata** — niente numeri "a sensazione".
3. **Idempotenza**: rieseguire un job non crea duplicati (chiave = `id` opportunità).
4. **Output strutturato** ovunque, così i moduli sono intercambiabili.
5. **Rispetto dei Terms of Service** delle piattaforme (no scraping vietato): vedi
   [06-permessi-sicurezza](06-permessi-sicurezza.md).
