# Agente-1

AI Agent operativo per ricerca di mercato, creazione di prodotti digitali, SEO Etsy e
automazione e-commerce. Analizza trend, individua opportunità ad alto potenziale, genera
contenuti, mockup e strategie di vendita. **Opera sempre con supervisione umana** sui
passaggi critici (pubblicazione, pagamenti, eliminazioni, modifiche definitive).

> ⚠️ **Principio guida n°1: non inventare mai dati.** Ogni stima di domanda, concorrenza o
> trend deve essere accompagnata dalla fonte e dal metodo con cui verificarla. I numeri non
> validati sono sempre etichettati come `IPOTESI DA VALIDARE`.

---

## Indice della documentazione

| # | Documento | Contenuto |
|---|-----------|-----------|
| 1 | [Architettura tecnica](docs/01-architettura-tecnica.md) | Come è fatto l'agente, livelli, flusso dati |
| 2 | [Strumenti consigliati](docs/02-strumenti-consigliati.md) | Stack no-code/low-code + API + costi |
| 3 | [Workflow completo](docs/03-workflow-completo.md) | Le 8 fasi end-to-end con i punti di approvazione |
| 4 | [Moduli dell'agente](docs/04-moduli-agente.md) | I sotto-agenti e le loro responsabilità |
| 5 | [Automazioni necessarie](docs/05-automazioni.md) | Cron, trigger, scheduling |
| 6 | [Permessi e sicurezza](docs/06-permessi-sicurezza.md) | Cosa può/non può fare, guardrail |
| 7 | [Piano operativo 7 giorni](docs/07-piano-7-giorni.md) | Cosa fa l'agente giorno per giorno |
| 8 | [Prima lista 10 prodotti](docs/08-prima-lista-10-prodotti.md) | Idee da validare con metodo |
| — | [Template output standard](docs/output-template.md) | Il formato fisso di ogni consegna |

- **Prompt pronti all'uso** → cartella [`prompts/`](prompts/)
- **Template compilabili** → cartella [`templates/`](templates/)
- **Motore di scoring (eseguibile)** → cartella [`tools/`](tools/)

---

## Quick start

```bash
# 1. Calcola il punteggio di validazione di un prodotto (FASE 2)
python3 tools/scoring.py tools/product_data.example.json

# 2. Solo i prodotti con punteggio >= 8/10 vengono creati.
```

## Il tuo ruolo (umano)

Approvi prodotti, pubblicazioni, budget e supervisioni le decisioni importanti.
L'agente fa ricerca, strategia, creazione, ottimizzazione e preparazione.

## Stato del progetto

Questo repository contiene **il progetto e gli asset operativi** dell'agente
(documentazione, prompt, template, motore di scoring). L'integrazione live con le API
esterne (Etsy, Pinterest, ecc.) va attivata seguendo
[docs/02-strumenti-consigliati.md](docs/02-strumenti-consigliati.md).
