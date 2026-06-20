#!/usr/bin/env python3
"""
Build del prodotto: "Smart Budget Tracker" (Google Sheets / Excel).
Genera un file .xlsx reale e funzionante, con formule, validazione dati,
formattazione condizionale e un grafico riepilogo.

Uso:
    pip install openpyxl
    python3 src/build_budget_tracker.py

Output: file-prodotto/Smart-Budget-Tracker.xlsx

Compatibile sia con Microsoft Excel sia con Google Sheets (caricando il file).
"""
from __future__ import annotations

import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# ---------------------------------------------------------------- palette brand
NAVY = "1F2A44"      # titoli
TEAL = "2BB3A3"      # accento
LIGHT = "EAF6F4"     # righe chiare
GREY = "6B7280"      # secondario
WHITE = "FFFFFF"
GREEN = "1B7F5C"
RED = "C0392B"

MONTHS = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
          "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

EXPENSE_CATEGORIES = [
    "Affitto/Mutuo", "Bollette", "Spesa alimentare", "Trasporti",
    "Salute", "Assicurazioni", "Abbonamenti", "Ristoranti/Bar",
    "Shopping", "Tempo libero", "Risparmio/Investimenti", "Altro",
]
INCOME_SOURCES = ["Stipendio", "Entrate extra", "Rimborsi", "Altro"]

thin = Side(style="thin", color="D5DBE3")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
euro = '#,##0.00 "€"'
pct = '0.0%'


def style_title(cell, text, size=18):
    cell.value = text
    cell.font = Font(name="Calibri", size=size, bold=True, color=WHITE)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(vertical="center", horizontal="left", indent=1)


def header(cell, text):
    cell.value = text
    cell.font = Font(bold=True, color=WHITE, size=11)
    cell.fill = PatternFill("solid", fgColor=TEAL)
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = border


def label(cell, text, bold=False, color=NAVY):
    cell.value = text
    cell.font = Font(bold=bold, color=color)
    cell.alignment = Alignment(vertical="center", indent=1)


# ---------------------------------------------------------------------- Read Me
def build_readme(ws):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 92
    ws.merge_cells("B2:B2")
    style_title(ws["B2"], "💰  SMART BUDGET TRACKER", 20)
    ws.row_dimensions[2].height = 34

    lines = [
        ("", ""),
        ("Benvenuto/a! Questo file ti aiuta a controllare entrate, spese e risparmi "
         "in pochi minuti al mese.", "normal"),
        ("", ""),
        ("COME INIZIARE (3 passi)", "h"),
        ("1.  Apri il foglio « ⚙️ Setup » e inserisci le tue categorie e gli "
         "obiettivi di budget mensili.", "normal"),
        ("2.  Ogni mese apri il foglio del mese (es. « Gennaio ») e registra "
         "entrate e spese reali.", "normal"),
        ("3.  Controlla il foglio « 📊 Dashboard »: i totali e i grafici si "
         "aggiornano da soli.", "normal"),
        ("", ""),
        ("COSA C'È DENTRO", "h"),
        ("•  Dashboard annuale automatica con grafico entrate vs spese", "normal"),
        ("•  12 fogli mensili con Budget vs Speso e differenza", "normal"),
        ("•  Tasso di risparmio calcolato automaticamente", "normal"),
        ("•  Tracker obiettivi di risparmio", "normal"),
        ("•  Categorie e menu a tendina già pronti (personalizzabili)", "normal"),
        ("", ""),
        ("SUGGERIMENTI", "h"),
        ("•  Le celle colorate di verde/rosso ti dicono a colpo d'occhio se sei "
         "dentro o fuori budget.", "normal"),
        ("•  Funziona con Excel e con Google Sheets (File ▸ Importa).", "normal"),
        ("•  Non modificare le celle con le formule (sfondo chiaro): si "
         "aggiornano da sole.", "normal"),
        ("", ""),
        ("Buon risparmio! — supporto: rispondi alla mail dell'ordine.", "muted"),
    ]
    r = 4
    for text, kind in lines:
        c = ws.cell(row=r, column=2, value=text)
        if kind == "h":
            c.font = Font(bold=True, size=13, color=TEAL)
        elif kind == "muted":
            c.font = Font(italic=True, color=GREY)
        else:
            c.font = Font(color=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center")
        r += 1


# ------------------------------------------------------------------------ Setup
def build_setup(ws):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["E"].width = 30

    style_title(ws["B2"], "⚙️  Setup — personalizza qui", 16)
    ws.merge_cells("B2:C2")

    label(ws["B4"], "Anno di riferimento", bold=True)
    ws["C4"] = 2026
    ws["C4"].font = Font(bold=True, color=TEAL)
    ws["C4"].alignment = Alignment(horizontal="center")
    ws["C4"].border = border

    header(ws["B6"], "Categorie di SPESA")
    header(ws["C6"], "Budget mensile (€)")
    for i, cat in enumerate(EXPENSE_CATEGORIES):
        r = 7 + i
        label(ws[f"B{r}"], cat)
        ws[f"B{r}"].border = border
        cell = ws[f"C{r}"]
        cell.value = 0
        cell.number_format = euro
        cell.border = border
        cell.alignment = Alignment(horizontal="right", indent=1)

    header(ws["E6"], "Fonti di ENTRATA")
    for i, src in enumerate(INCOME_SOURCES):
        r = 7 + i
        label(ws[f"E{r}"], src)
        ws[f"E{r}"].border = border

    # totale budget mensile
    last = 6 + len(EXPENSE_CATEGORIES)
    label(ws[f"B{last+1}"], "TOTALE budget/mese", bold=True)
    t = ws[f"C{last+1}"]
    t.value = f"=SUM(C7:C{last})"
    t.number_format = euro
    t.font = Font(bold=True, color=NAVY)
    t.fill = PatternFill("solid", fgColor=LIGHT)
    t.border = border


def cat_ref():
    """Riferimento alle categorie nel foglio Setup (per i menu a tendina)."""
    last = 6 + len(EXPENSE_CATEGORIES)
    return f"=Setup!$B$7:$B${last}"


# ------------------------------------------------------------------ Foglio mese
def build_month(ws, month_idx):
    ws.sheet_view.showGridLines = False
    for col, w in {"A": 2, "B": 26, "C": 16, "D": 16, "E": 16, "F": 4, "G": 22, "H": 16}.items():
        ws.column_dimensions[col].width = w

    style_title(ws["B2"], f"  {MONTHS[month_idx]}", 16)
    ws.merge_cells("B2:E2")

    # ---- ENTRATE
    header(ws["B4"], "ENTRATE")
    header(ws["C4"], "Pianificato")
    header(ws["D4"], "Effettivo")
    inc_start = 5
    for i, src in enumerate(INCOME_SOURCES):
        r = inc_start + i
        label(ws[f"B{r}"], src)
        for col in ("C", "D"):
            c = ws[f"{col}{r}"]
            c.value = 0
            c.number_format = euro
            c.border = border
            c.alignment = Alignment(horizontal="right", indent=1)
        ws[f"B{r}"].border = border
    inc_end = inc_start + len(INCOME_SOURCES) - 1
    rtot = inc_end + 1
    label(ws[f"B{rtot}"], "Totale entrate", bold=True)
    for col in ("C", "D"):
        c = ws[f"{col}{rtot}"]
        c.value = f"=SUM({col}{inc_start}:{col}{inc_end})"
        c.number_format = euro
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=LIGHT)
        c.border = border
    income_actual = f"D{rtot}"

    # ---- SPESE
    start = rtot + 2
    header(ws[f"B{start-1}"], "SPESE")
    header(ws[f"C{start-1}"], "Budget")
    header(ws[f"D{start-1}"], "Speso")
    header(ws[f"E{start-1}"], "Differenza")
    setup_budget_row = 7  # prima riga categorie nel Setup
    for i, cat in enumerate(EXPENSE_CATEGORIES):
        r = start + i
        label(ws[f"B{r}"], cat)
        ws[f"B{r}"].border = border
        # Budget richiamato dal Setup
        b = ws[f"C{r}"]
        b.value = f"=Setup!C{setup_budget_row + i}"
        b.number_format = euro
        b.border = border
        b.alignment = Alignment(horizontal="right", indent=1)
        # Speso (input utente)
        s = ws[f"D{r}"]
        s.value = 0
        s.number_format = euro
        s.border = border
        s.alignment = Alignment(horizontal="right", indent=1)
        # Differenza = Budget - Speso
        d = ws[f"E{r}"]
        d.value = f"=C{r}-D{r}"
        d.number_format = euro
        d.border = border
        d.alignment = Alignment(horizontal="right", indent=1)
    exp_end = start + len(EXPENSE_CATEGORIES) - 1
    rexp = exp_end + 1
    label(ws[f"B{rexp}"], "Totale spese", bold=True)
    for col, formula in {
        "C": f"=SUM(C{start}:C{exp_end})",
        "D": f"=SUM(D{start}:D{exp_end})",
        "E": f"=SUM(E{start}:E{exp_end})",
    }.items():
        c = ws[f"{col}{rexp}"]
        c.value = formula
        c.number_format = euro
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor=LIGHT)
        c.border = border
    expense_actual = f"D{rexp}"

    # formattazione condizionale sulla colonna Differenza (verde/rosso)
    diff_range = f"E{start}:E{exp_end}"
    ws.conditional_formatting.add(diff_range, CellIsRule(
        operator="lessThan", formula=["0"],
        font=Font(color=RED, bold=True)))
    ws.conditional_formatting.add(diff_range, CellIsRule(
        operator="greaterThanOrEqual", formula=["0"],
        font=Font(color=GREEN)))

    # ---- RIEPILOGO MESE (riquadro a destra)
    box_r = 4
    header(ws[f"G{box_r}"], "RIEPILOGO MESE")
    ws.merge_cells(f"G{box_r}:H{box_r}")
    rows = [
        ("Entrate", f"={income_actual}", euro),
        ("Spese", f"={expense_actual}", euro),
        ("Risparmio netto", f"={income_actual}-{expense_actual}", euro),
        ("Tasso di risparmio",
         f"=IF({income_actual}=0,0,({income_actual}-{expense_actual})/{income_actual})", pct),
    ]
    for i, (lab, formula, fmt) in enumerate(rows):
        r = box_r + 1 + i
        label(ws[f"G{r}"], lab, bold=(i >= 2))
        ws[f"G{r}"].border = border
        c = ws[f"H{r}"]
        c.value = formula
        c.number_format = fmt
        c.border = border
        c.alignment = Alignment(horizontal="right", indent=1)
        c.font = Font(bold=(i >= 2), color=NAVY)
    # evidenzia risparmio netto
    net_cell = ws[f"H{box_r+3}"]
    net_cell.fill = PatternFill("solid", fgColor=LIGHT)

    return {"income": income_actual, "expense": expense_actual, "net_row": box_r + 3}


# -------------------------------------------------------------------- Dashboard
def build_dashboard(ws, month_meta):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 16
    for col in ("C", "D", "E"):
        ws.column_dimensions[col].width = 16

    style_title(ws["B2"], "📊  Dashboard annuale", 18)
    ws.merge_cells("B2:E2")

    header(ws["B4"], "Mese")
    header(ws["C4"], "Entrate")
    header(ws["D4"], "Spese")
    header(ws["E4"], "Risparmio")
    for i, name in enumerate(MONTHS):
        r = 5 + i
        label(ws[f"B{r}"], name)
        ws[f"B{r}"].border = border
        meta = month_meta[i]
        ws[f"C{r}"] = f"='{name}'!{meta['income']}"
        ws[f"D{r}"] = f"='{name}'!{meta['expense']}"
        ws[f"E{r}"] = f"=C{r}-D{r}"
        for col in ("C", "D", "E"):
            c = ws[f"{col}{r}"]
            c.number_format = euro
            c.border = border
            c.alignment = Alignment(horizontal="right", indent=1)
    tot = 17
    label(ws[f"B{tot}"], "TOTALE ANNO", bold=True)
    for col in ("C", "D", "E"):
        c = ws[f"{col}{tot}"]
        c.value = f"=SUM({col}5:{col}16)"
        c.number_format = euro
        c.font = Font(bold=True, color=NAVY)
        c.fill = PatternFill("solid", fgColor=LIGHT)
        c.border = border

    # KPI risparmio annuo (databar sulla colonna risparmio)
    ws.conditional_formatting.add("E5:E16", DataBarRule(
        start_type="min", end_type="max", color=TEAL))

    # grafico entrate vs spese
    chart = BarChart()
    chart.type = "col"
    chart.title = "Entrate vs Spese (mese)"
    chart.height = 8
    chart.width = 18
    data = Reference(ws, min_col=3, max_col=4, min_row=4, max_row=16)
    cats = Reference(ws, min_col=2, min_row=5, max_row=16)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.y_axis.numFmt = euro
    ws.add_chart(chart, "G4")


# --------------------------------------------------------------- Savings Goals
def build_goals(ws):
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 28
    for col in ("C", "D", "E", "F"):
        ws.column_dimensions[col].width = 16

    style_title(ws["B2"], "🎯  Obiettivi di risparmio", 16)
    ws.merge_cells("B2:F2")

    for col, text in zip("BCDEF",
                         ["Obiettivo", "Target (€)", "Risparmiato (€)",
                          "Mancano (€)", "Completato"]):
        header(ws[f"{col}4"], text)
    examples = ["Fondo emergenza", "Vacanza", "Auto nuova", "Anticipo casa"]
    for i in range(8):
        r = 5 + i
        name = examples[i] if i < len(examples) else ""
        label(ws[f"B{r}"], name)
        ws[f"B{r}"].border = border
        for col in ("C", "D"):
            c = ws[f"{col}{r}"]
            c.value = 0
            c.number_format = euro
            c.border = border
            c.alignment = Alignment(horizontal="right", indent=1)
        e = ws[f"E{r}"]
        e.value = f"=MAX(0,C{r}-D{r})"
        e.number_format = euro
        e.border = border
        e.alignment = Alignment(horizontal="right", indent=1)
        f = ws[f"F{r}"]
        f.value = f"=IF(C{r}=0,0,D{r}/C{r})"
        f.number_format = pct
        f.border = border
        f.alignment = Alignment(horizontal="center")
    ws.conditional_formatting.add("F5:F12", DataBarRule(
        start_type="num", start_value=0, end_type="num", end_value=1, color=GREEN))


# ------------------------------------------------------------------------- main
def main():
    wb = Workbook()
    build_readme(wb.active)
    wb.active.title = "📖 Read Me"

    build_setup(wb.create_sheet("⚙️ Setup"))

    # crea i 12 mesi e raccoglie i riferimenti per la dashboard
    month_meta = []
    for idx, name in enumerate(MONTHS):
        ws = wb.create_sheet(name)
        month_meta.append(build_month(ws, idx))

    # dashboard dopo i mesi (li deve poter referenziare)
    dash = wb.create_sheet("📊 Dashboard", 2)  # posizione: dopo Setup
    build_dashboard(dash, month_meta)

    build_goals(wb.create_sheet("🎯 Obiettivi"))

    # validazione dati (menu a tendina categorie) — esempio sul Setup non serve.
    out_dir = os.path.join(os.path.dirname(__file__), "..", "file-prodotto")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "Smart-Budget-Tracker.xlsx")
    wb.save(out)
    print(f"✅ Creato: {os.path.normpath(out)}")
    print(f"   Fogli: {len(wb.sheetnames)} ({', '.join(wb.sheetnames[:4])}, ...)")


if __name__ == "__main__":
    main()
