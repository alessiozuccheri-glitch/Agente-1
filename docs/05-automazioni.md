# 5 — Automazioni necessarie

L'agente lavora "in continuo" tramite job schedulati. Sotto: i trigger, la frequenza e il
comportamento. Implementabili in **Make/n8n** (no-code) o cron+script (low-code).

## Job schedulati

| ID | Job | Frequenza | Cosa fa | Gate umano |
|----|-----|-----------|---------|------------|
| J1 | **Daily Research** | ogni giorno 08:00 | M1 cerca opportunità, salva schede in DB | no |
| J2 | **Auto-Validation** | dopo J1 | M2 calcola scoring, marca ≥8/10 | no |
| J3 | **Approval Digest** | ogni giorno 09:00 | riepilogo idee ≥8/10 da approvare → te | 🧑 GATE 1 |
| J4 | **Build Queue** | on-demand (post-approvazione) | M3+M4+M5 creano prodotto/mockup/SEO | no |
| J5 | **Listing Review** | a build completata | mostra listing finale per OK | 🧑 GATE 2 |
| J6 | **Daily Metrics** | ogni giorno 07:30 | M6 legge stats Etsy, calcola CTR/CR | no |
| J7 | **Optimization Report** | ogni giorno 09:00 | M6 propone azioni; prezzo/promo → gate | 🧑 (se prezzo) |
| J8 | **Weekly Growth** | lunedì 10:00 | M7 pianifica pin/ads/contenuti settimana | 🧑 (se budget) |
| J9 | **Pinterest Pin Push** | 3x/settimana | pubblica pin programmati | no* |
| J10 | **Health Check** | ogni giorno 23:00 | verifica job falliti, alert | no |

\* solo contenuti organici già approvati nel piano settimanale.

## Pattern di automazione

### A. Pipeline ricerca → validazione (J1→J2)
```
Trigger orario
  → M1.cerca(nicchie)               # eRank, autocomplete, trend
  → per ogni opportunità: salva in DB con stato "ricerca"
  → M2.score(opportunità)           # scoring.py
  → se score >= 8: stato "validato"; else "archiviato" + motivo
```

### B. Digest approvazioni (J3) — *anti-frammentazione*
Invece di pingarti a ogni idea, l'agente accumula e ti manda **un solo messaggio** al giorno:
```
"3 idee ≥8/10 pronte. Approva quali creare:
 [1] Planner finanziario (8.6) — crea? S/N
 [2] Bundle CV ATS (8.2)       — crea? S/N
 [3] Template Notion freelance (8.0) — crea? S/N"
```

### C. Build queue (J4)
Parte **solo** sulle idee che hai approvato. Esegue M3→M4→M5 in sequenza, poi J5.

### D. Loop monitoraggio (J6→J7)
```
Trigger orario
  → M6.leggi_metriche()             # Etsy stats/API
  → calcola CTR, conversion, salvataggi
  → individua underperformer (sotto benchmark)
  → genera azioni; modifiche prezzo/promo accodate al gate umano
```

## Idempotenza e resilienza
- Chiave univoca per opportunità (`id`) → niente duplicati se un job rigira.
- Retry con backoff su errori di rete (2s, 4s, 8s, 16s).
- J10 (health check) notifica i job falliti invece di fallire in silenzio.

## Scheduling consigliato (fuso Europe/Rome)
- Mattina presto: metriche (J6) e ricerca (J1) → così il digest delle 09:00 ha tutto pronto.
- Un **unico digest 09:00** raggruppa: idee da approvare + azioni di ottimizzazione → riduce
  il carico mentale e rispetta il principio "approvazioni concentrate, non sparse".

## Esempio cron (low-code)
```cron
30 7 * * *  metrics_daily.py     # J6
0  8 * * *  research_daily.py     # J1 → J2
0  9 * * *  digest.py             # J3 + J7 (un solo messaggio)
0 10 * * 1  growth_weekly.py      # J8
0 23 * * *  health_check.py       # J10
```
