# 6 — Permessi e sicurezza

## Modello dei permessi

L'agente opera con **principio del privilegio minimo**: ha solo i permessi necessari e quelli
"pericolosi" passano sempre da te.

### ✅ Permessi concessi (autonomo)
- Leggere dati di mercato da fonti consentite (eRank, API ufficiali, UI trend).
- Scrivere/aggiornare il database interno (idee, pipeline, metriche).
- Generare contenuti, file prodotto, mockup, testi SEO (**bozze**, non pubblicate).
- Leggere le statistiche dello shop Etsy (visualizzazioni, click, vendite) via Etsy API.
- Programmare e pubblicare **contenuti organici già approvati** (es. pin Pinterest dal piano
  settimanale).
- Proporre ottimizzazioni e creatività.

### 🧑 Permessi che richiedono SEMPRE approvazione umana
| Azione | Perché | Gate |
|--------|--------|------|
| **Pubblicare un listing** su Etsy | azione verso l'esterno, irreversibile di fatto | GATE PUBBLICA |
| **Spendere denaro** (Etsy Ads, Pinterest Ads, tool a pagamento) | impatto economico | GATE BUDGET |
| **Modificare il prezzo** di un listing live | impatto su vendite/percezione | GATE PREZZO |
| **Eliminare/disattivare** un listing | irreversibile | GATE DELETE |
| **Modifica definitiva** dello shop (policy, sezioni, branding) | irreversibile | GATE SHOP |

### ❌ Azioni vietate (mai, nemmeno con approvazione automatica)
- Scraping vietato dai Terms of Service di Etsy, Pinterest, TikTok, Google.
- Copiare prodotti protetti da copyright.
- Usare marchi registrati senza verifica.
- Inventare dati di mercato o spacciare stime per fatti.
- Aggirare i rate limit / le protezioni delle piattaforme.

## Permessi tecnici da configurare (checklist)

- [ ] **Anthropic API key** → secret manager, scope: solo inferenza.
- [ ] **Etsy OAuth 2.0** → scope minimi: `listings_r`, `shops_r`, `transactions_r`. Aggiungere
      `listings_w` **solo** se decidi di automatizzare la pubblicazione con conferma; di
      default tenerlo **off**.
- [ ] **Pinterest API** → scope: `pins:write` solo per contenuti del piano approvato.
- [ ] **eRank/Marmalead** → sola lettura.
- [ ] **Database** (Airtable/Supabase/Notion) → read/write sulle tabelle del progetto.
- [ ] **Nessuna** credenziale di pagamento data all'agente in modo autonomo.

## Gestione segreti
- Mai committare chiavi nel repo. Usare `.env` (in `.gitignore`) o il vault
  dell'orchestratore.
- Rotazione chiavi ogni 90 giorni.
- Log di audit: ogni azione su gate umano registra **chi/quando/cosa** (tabella `approvals`).

## Conformità & etica
- **Scraping etico**: solo API ufficiali e lettura UI consentita; rispetto di `robots.txt` e
  ToS. Quando un dato non è ottenibile in modo conforme → si rinuncia al dato, non si forza.
- **Copyright/Trademark**: prima di ogni prodotto, M3 esegue un controllo nomi/asset; in caso
  di dubbio → flag a te, non si procede.
- **Dati personali**: l'agente non raccoglie PII dei clienti oltre a quanto Etsy fornisce
  legittimamente.

## Fail-safe
- **Default deny** sulle azioni pericolose: se manca un'approvazione, l'agente **si ferma e
  chiede**, non procede.
- **Dry-run** disponibile per ogni job: simula senza scrivere/pubblicare.
- **Kill switch**: una variabile `AGENT_PAUSED=true` mette in pausa tutti i job schedulati.
