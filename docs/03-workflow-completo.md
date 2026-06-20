# 3 — Workflow completo (le 8 fasi)

Legenda: 🤖 = azione agente · 🧑 = **approvazione umana richiesta** · 📦 = output prodotto

```
FASE 1 ──▶ FASE 2 ──▶ [🧑 gate idea] ──▶ FASE 3 ──▶ FASE 4 ──▶ FASE 5 ──▶ [🧑 gate listing]
ricerca   scoring        approva?         prodotto   mockup     SEO          approva pubbl.?
                                                                                  │
                                                                                  ▼
                                                          FASE 6 ──▶ [🧑 PUBBLICA] ──▶ FASE 7 ──▶ FASE 8
                                                          prepara     conferma        monitora    traffico
                                                                                          │
                                                                                          ▼
                                                                                   ottimizza (loop)
```

## FASE 1 — Ricerca mercato 🤖
**Input:** nicchie target, giorno corrente.
**Fonti:** Etsy search/autocomplete, bestseller, eRank/Marmalead, Pinterest Trends, Google
Trends, TikTok Creative Center, competitor, recensioni clienti.
**Output 📦:** N "schede opportunità" (schema `ProductOpportunity`) con: nome, nicchia,
cliente ideale, problema, domanda stimata (+fonte), concorrenza, saturazione, margine,
difficoltà, potenziale vendite, keyword, motivo, rischi, priorità 1-10.
**Regola d'oro:** ogni stima → fonte + data + `IPOTESI_DA_VALIDARE` o `VERIFICATO`.

## FASE 2 — Validazione 🤖
Esegue `tools/scoring.py`. Criteri pesati: domanda, concorrenza, evergreen, facilità,
margine, differenziazione, SEO, Pinterest, ads, velocità pubblicazione.
**Output 📦:** punteggio /10. **Solo ≥ 8/10 prosegue.** Sotto soglia → archiviato con motivo.

### 🧑 GATE 1 — Approvazione idea
L'agente ti presenta le opportunità ≥ 8/10. Tu approvi quali creare. *(Reversibile, ma è il
momento giusto per decidere dove investire tempo.)*

## FASE 3 — Creazione prodotto 🤖
Per ogni idea approvata: struttura completa, contenuto testuale, file digitale finale,
copertina, varianti, bonus, istruzioni cliente, naming file ordinato.
Formati: PDF, template Canva, Google Sheets, Notion template, PNG/JPG, ZIP.
**Output 📦:** prodotto "premium, utile, vendibile" + checklist QA.

## FASE 4 — Mockup e immagini 🤖
Genera o prepara prompt per: hero, lifestyle, detail, benefit, what's-included,
thumbnail mobile, pin Pinterest, ads creative. Requisiti: fotorealistico, pulito, leggibile
da mobile, focus prodotto, stile premium, non tagliato.
**Output 📦:** set immagini + prompt riproducibili.

## FASE 5 — SEO Etsy 🤖
Titolo ≤140 caratteri, 13 tag, descrizione SEO, bullet benefici, materiali, categoria,
keyword primarie/secondarie, prezzo consigliato, sconto iniziale, bundle, upsell/cross-sell.
**Output 📦:** pacchetto listing completo (vedi `templates/etsy-listing.md`).

### 🧑 GATE 2 — Approvazione listing
L'agente mostra: titolo finale, prezzo, descrizione, tag, file, immagini, categoria,
riepilogo. *Niente pubblicazione automatica.*

## FASE 6 — Pubblicazione 🧑
L'agente prepara tutto e attende il tuo **OK esplicito**. La pubblicazione su Etsy avviene
solo dopo approvazione umana (manuale o, in futuro, via Etsy API con conferma).

## FASE 7 — Monitoraggio performance 🤖 (loop giornaliero)
Legge: visualizzazioni, click, CTR, salvataggi, carrelli, vendite, conversion rate,
keyword che portano traffico, prodotti con basse performance.
**Output 📦:** report giornaliero + lista azioni di ottimizzazione (titolo, immagini, tag,
prezzo, bundle, promo, pin, ads). Le modifiche prezzo/promo passano da 🧑 GATE.

## FASE 8 — Ads e traffico 🤖
Idee Etsy Ads, pin Pinterest, caption TikTok, script video brevi, hook virali, angoli,
target, budget di test consigliato, creatività, piano organico+paid.
**Output 📦:** piano traffico. **Lo spend richiede 🧑 approvazione budget.**

---

## Riepilogo punti di approvazione umana
| Gate | Quando | Perché |
|------|--------|--------|
| 🧑 GATE 1 | dopo scoring | decidere dove investire tempo |
| 🧑 GATE 2 | dopo SEO | revisione listing finale |
| 🧑 PUBBLICA | FASE 6 | azione verso l'esterno |
| 🧑 BUDGET | FASE 8 / ads | spesa di denaro |
| 🧑 PREZZO/DELETE | FASE 7 e ovunque | modifica/eliminazione irreversibile |

Ogni consegna segue il [formato output standard](output-template.md).
