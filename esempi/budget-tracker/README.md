# Smart Budget Tracker — Scheda operativa completa

> Primo prodotto creato end-to-end da Agente-1, seguendo il
> [formato output standard a 11 punti](../../docs/output-template.md) e le FASI 3-5 del
> [workflow](../../docs/03-workflow-completo.md). È un **esempio funzionante e riproducibile**.

## Contenuto di questa cartella
```
budget-tracker/
├── README.md                      ← questa scheda (11 punti)
├── listing-etsy.md                ← SEO Etsy pronto da copiare (FASE 5)
├── file-prodotto/
│   ├── Smart-Budget-Tracker.xlsx  ← IL PRODOTTO (16 fogli, formule)  [FASE 3]
│   └── Guida-Smart-Budget-Tracker.pdf  ← guida cliente PDF           [FASE 3]
├── mockup-prompts/
│   ├── 01-hero-image.png          ← immagine hero generata           [FASE 4]
│   ├── 05-whats-included.png      ← immagine "cosa ricevi" generata  [FASE 4]
│   └── prompts-immagini.md        ← prompt per le altre 6 immagini
└── src/
    ├── build_budget_tracker.py    ← genera il .xlsx (riproducibile)
    └── build_assets.py            ← genera PDF + immagini
```
Rigenerare tutto: `pip install openpyxl pillow && python3 src/build_budget_tracker.py && python3 src/build_assets.py`

---

## 1. Opportunità trovata
Prodotto **#1** della [lista di validazione](../../docs/08-prima-lista-10-prodotti.md):
**budget tracker / planner finanziario** in formato foglio di calcolo. Categoria evergreen,
costo marginale ~0, intenzione d'acquisto alta (inizio mese/anno, propositi). Angolo di
differenziazione scelto: **lingua italiana** (mercato meno saturo del corrispettivo inglese)
+ **automazione reale** (dashboard, formule, tasso di risparmio) vs i molti PDF statici.

## 2. Analisi mercato
| Segnale | Valore | Fonte | Stato |
|---------|--------|-------|-------|
| Domanda | alta, evergreen, picchi a gennaio/settembre | Google Trends "budget planner" | **IPOTESI_DA_VALIDARE** con eRank |
| Concorrenza (EN) | molto alta | Etsy search | nota |
| Concorrenza (IT) | medio-bassa | Etsy search "budget planner italiano" | **IPOTESI_DA_VALIDARE** |
| Saturazione | media (alta su EN, bassa su IT) | — | da confermare |
| Margine | altissimo (file digitale) | — | VERIFICATO (struttura costi) |

> ⚠️ I volumi vanno confermati su **eRank/Marmalead** prima del lancio (principio "non
> inventare dati"). L'angolo IT è un'ipotesi di posizionamento, non un dato di vendita.

## 3. Punteggio prodotto
**8,6 / 10** (soglia 8 superata → CREA). Calcolato con il motore di scoring:
```bash
python3 ../../tools/scoring.py ../../tools/product_data.example.json   # → 8.6 ✅ CREA
```
Punti di forza: margine 10, evergreen 10, domanda 9, facilità 9, velocità 9. Punto debole:
concorrenza 6 (mitigato dall'angolo lingua IT + automazione).

## 4. Strategia prodotto
- **Posizionamento:** "il budget che si compila da solo, in italiano".
- **Differenziazione:** automazione vera (formule, dashboard, grafico, tasso di risparmio)
  contro i PDF statici da stampare; lingua italiana.
- **Varianti utili:** versione EN (scaling), versione Coppia/Famiglia (doppio reddito).
- **Bonus incluso:** tracker obiettivi di risparmio + guida PDF.
- **Premium feel:** palette coerente, fogli con intestazioni a colori, celle verde/rosso.

## 5. File da creare → ✅ CREATI
- `Smart-Budget-Tracker.xlsx` — 16 fogli: Read Me, Setup, Dashboard, 12 mesi, Obiettivi;
  con formule (Budget vs Speso, totali, tasso di risparmio), formattazione condizionale e
  grafico. **Generato e validato** (ricaricato con openpyxl senza errori).
- `Guida-Smart-Budget-Tracker.pdf` — 3 pagine brandizzate (copertina, come iniziare, cosa
  c'è dentro). **Generato.**
- Naming ordinato e professionale ✅.

## 6. Mockup necessari
8 immagini definite in [`mockup-prompts/prompts-immagini.md`](mockup-prompts/prompts-immagini.md).
**2 già generate** (Hero, What's included); per le altre 6 (Lifestyle, Detail, Benefit,
Thumbnail, Pin, Ads) ci sono i prompt riproducibili per Midjourney/Ideogram/Canva.

## 7. SEO Etsy
Pacchetto completo in [`listing-etsy.md`](listing-etsy.md):
- **Titolo** 128/140 caratteri, keyword in testa
- **13 tag** tutti ≤20 caratteri
- Descrizione con gancio + benefici + materiali + FAQ + CTA
- Categoria + keyword primarie/secondarie

## 8. Prezzo consigliato
- **€ 7,90** di listino · **-30% lancio** (7 giorni) → ~€5,50
- **Bundle** "Money Bundle" € 14,90 · **Upsell** versione Famiglia / Planner obiettivi

## 9. Piano pubblicazione
1. 🤖 Carica `.xlsx` + `.pdf` come *digital download* su Etsy.
2. 🤖 Carica le 5 immagini listing nell'ordine corretto.
3. 🤖 Incolla titolo, tag, descrizione, prezzo da `listing-etsy.md`.
4. 🤖 Imposta categoria + flag digitale.
5. 🧑 **GATE 2 + PUBBLICA** — l'agente mostra il riepilogo e attende il tuo OK. *Niente
   pubblicazione automatica.*

## 10. Piano traffico
- **Pinterest (canale n°1):** 3 pin/settimana usando il prompt pin (#7). Board "Budget &
  Risparmio", "Finanze personali".
- **TikTok/Reels:** hook "Da caos a controllo in 5 minuti al mese" → demo schermo 15s.
- **Etsy Ads:** **dopo** le prime vendite organiche; budget test €3-5/giorno per 7-14 giorni
  sulle keyword principali. 🧑 **GATE BUDGET** prima di attivare.
- Sequenza: **organico prima, paid dopo** i primi dati.

## 11. Prossima azione consigliata
**Una cosa sola:** apri `file-prodotto/Smart-Budget-Tracker.xlsx` in **Google Sheets** e
verifica che le formule calcolino (inserisci qualche numero di prova nel foglio « Gennaio »).
Poi decidi il mercato: **IT** (lanciamo così) o **EN** (creo la variante inglese del file in
~10 min). Da lì → GATE 2 e pubblicazione.

---
### Note di trasparenza (principi dell'agente)
- I numeri di mercato sono etichettati `IPOTESI_DA_VALIDARE` finché non confermati su eRank.
- Nessuna azione irreversibile è stata eseguita: il prodotto è **pronto**, non pubblicato.
- Il prodotto è originale: nessun marchio/contenuto di terzi.
