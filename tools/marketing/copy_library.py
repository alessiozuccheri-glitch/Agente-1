"""
Libreria di copy per il motore marketing.

Contiene gli ELEMENTI riutilizzabili (angoli, hook, template, hashtag) che il
generatore combina per produrre il calendario editoriale. I testi sono in
italiano e pensati per prodotti digitali Etsy. Si personalizzano per prodotto
tramite i campi del file JSON (vedi product.budget-tracker.json).

Niente dati inventati: questi sono ASSET CREATIVI (copy), non metriche di mercato.
"""
from __future__ import annotations

# Angoli di marketing: ogni angolo è un "perché comprare" diverso dello stesso prodotto.
# {benefit}, {prodotto}, {nicchia} vengono riempiti dal JSON prodotto.
ANGOLI = [
    "controllo",      # smettere di non sapere dove finiscono i soldi
    "ansia_soldi",    # dal panico alla serenità finanziaria
    "automazione",    # si compila da solo, niente app a pagamento
    "obiettivi",      # raggiungere un obiettivo di risparmio concreto
    "in_italiano",    # finalmente uno strumento nella tua lingua
    "tempo",          # 5 minuti al mese, non un secondo di più
    "famiglia",       # gestire il budget di coppia/famiglia
    "proposito",      # il proposito che mantieni davvero
]

# Hook brevi per Reels/TikTok (primi 3 secondi). {benefit_breve} dal JSON.
HOOK_VIDEO = [
    "Ho smesso di stressarmi per i soldi con un solo foglio.",
    "Il motivo per cui non riesci a risparmiare non è lo stipendio.",
    "Da caos a controllo totale in 5 minuti al mese.",
    "Nessuno te lo dice, ma ti basta UN file per gestire i soldi.",
    "Ho provato 4 app di budget. Questo foglio le batte tutte.",
    "Se a fine mese non sai dove sono finiti i soldi, guarda qui.",
    "Il trucco delle persone che risparmiano davvero (e non è guadagnare di più).",
    "POV: apri il tuo budget e sai esattamente quanto puoi spendere oggi.",
]

# Struttura script video 15-30s: lista di (etichetta_sezione, testo)
SCRIPT_SEZIONI = [
    ("HOOK (0-3s)", "{hook}"),
    ("PROBLEMA (3-8s)", "Arrivi a fine mese e i soldi sono spariti, senza sapere dove."),
    ("SOLUZIONE (8-18s)", "Con {prodotto} registri entrate e spese e il foglio calcola da "
                          "solo quanto puoi risparmiare. Categorie, grafici, obiettivi: "
                          "tutto automatico."),
    ("PROVA (18-25s)", "Guarda: inserisco una spesa e la dashboard si aggiorna all'istante."),
    ("CTA (25-30s)", "Lo trovi nel mio shop Etsy, link in bio. {benefit_breve}."),
]

# Template titoli pin Pinterest (vincono i titoli "risultato + come"). {benefit}/{nicchia}.
PIN_TITLE = [
    "Come tenere i soldi sotto controllo (senza app)",
    "Il budget planner che si compila da solo",
    "Risparmia di più ogni mese con 1 foglio Excel",
    "Smetti di chiederti dove finiscono i soldi",
    "Budget mensile facile: il metodo in 5 minuti",
    "Organizza le tue finanze in italiano, finalmente",
    "Il foglio Excel che ti fa risparmiare davvero",
    "Pianifica spese e risparmi come un pro",
]

# Template descrizioni pin (SEO Pinterest). {keyword1},{keyword2},{prodotto},{link}.
PIN_DESC = [
    "Prendi il controllo del tuo {keyword1} con {prodotto}: dashboard automatica, budget vs "
    "speso e obiettivi di risparmio. Excel e Google Sheets, in italiano. 👉 {link} "
    "#{kw1_tag} #budgetplanner #risparmio",
    "Stanco di non sapere dove vanno i soldi? Questo {keyword2} calcola tutto da solo. "
    "Download digitale, personalizzabile. 👉 {link} #finanzepersonali #budget #excel",
    "Il metodo semplice per gestire {keyword1} e risparmiare ogni mese senza app a pagamento. "
    "👉 {link} #risparmiosoldi #budgetmensile #planner",
]

# Caption Instagram/TikTok. {hook},{benefit},{link}.
CAPTION = [
    "{hook}\n\n{benefit} Salva questo post e provalo questo mese. 💸\nLink in bio 👉 {link}",
    "{hook}\n\nNiente app, niente abbonamenti: solo un foglio che lavora per te.\n"
    "Lo trovi su Etsy, link in bio. {benefit}",
    "{hook}\n\nCommenta \"BUDGET\" e ti mando il link. {benefit}",
]

# Set di hashtag per canale (Pinterest ne usa pochi, IG/TikTok di più).
HASHTAG = {
    "pinterest": "#budgetplanner #risparmio #finanzepersonali",
    "instagram": "#budgetplanner #risparmio #finanzepersonali #budgetmensile #excel "
                 "#gestionespese #risparmiosoldi #etsyitalia #pianificazione #soldi",
    "tiktok": "#budget #risparmio #finanzepersonali #soldi #foryou #excel #budgetingtips",
}

# Idee per email settimanale (oggetto + angolo).
EMAIL = [
    ("Dove sono finiti i soldi questo mese?", "controllo"),
    ("Il trucco da 5 minuti per risparmiare di più", "automazione"),
    ("3 errori che ti impediscono di mettere da parte soldi", "obiettivi"),
    ("Il tuo budget, finalmente in italiano", "in_italiano"),
]
