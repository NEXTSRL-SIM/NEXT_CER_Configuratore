from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

import datetime
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------------
# GRAFICI
# ---------------------------------------------------------
def make_payback_chart(costo, beneficio_annuo):
    anni = list(range(0, 21))
    valori = [beneficio_annuo * a for a in anni]

    plt.figure()
    plt.plot(anni, valori)
    plt.axhline(costo)

    plt.title("Rientro dell'investimento (Payback)")
    plt.xlabel("Anni")
    plt.ylabel("Beneficio cumulato (€)")

    path = "payback.png"
    plt.savefig(path)
    plt.close()
    return path


def make_benefits_chart(b10, b20):
    plt.figure()
    plt.bar(["10 anni", "20 anni"], [b10, b20])
    plt.title("Beneficio Totale nel Tempo")
    plt.ylabel("Euro (€)")

    path = "benefici.png"
    plt.savefig(path)
    plt.close()
    return path


# ---------------------------------------------------------
# BUILD PDF
# ---------------------------------------------------------
def build_pdf(cliente, res, costo_impianto):

    filename = f"Report_{cliente}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['BodyText'],
        leading=16
    )

    story = []
    oggi = datetime.date.today().strftime("%d/%m/%Y")

    # =====================================================
    # PAGINA 1 — TESTO COMPLETO
    # =====================================================

    story.append(Paragraph("Sistema di Rendita Energetica Attiva Next", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Iniziativa riservata al Veneto e al Friuli Venezia Giulia, valida fino al 30 marzo 2026 e limitata ai primi 20 impianti.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles["Normal"]))
    story.append(Paragraph(f"<b>Data simulazione:</b> {oggi}", styles["Normal"]))
    story.append(Spacer(1, 20))

    # --- TESTO COMPLETO COME VERSIONE APPROVATA ---

    paragrafi = [
        "Questa iniziativa nasce da un’idea molto semplice.",
        "Quando si realizza un impianto fotovoltaico residenziale, normalmente si sceglie una potenza “sufficiente”.",
        "Noi abbiamo scelto un approccio diverso.",
        "Attraverso questa promozione abbiamo deciso di proporre un sistema completo – comprensivo di accumulo da 16 kWh – e di sfruttare al massimo la superficie disponibile del tetto, senza aumentare il prezzo rispetto alla configurazione base.",
        "<b>Vediamo come funziona.</b>",
        "Abbiamo suddiviso gli impianti monofase fino a 10 kW in due categorie:",
        "• la prima va da 3,28 kW fino a 5,74 kW",
        "• la seconda va da 6,56 kW fino a 9,84 kW",
        "All’interno di ciascuna categoria esiste una potenza base, che è la più bassa della fascia (3,28 e 6,56 kWp).",
        "Il prezzo viene determinato su quella potenza minima, ma installiamo tutta la potenza che il tetto può ospitare rimanendo all’interno della stessa categoria, senza aumentare il prezzo rispetto alla configurazione iniziale.",
        "In altre parole, paghi l’impianto base della fascia, ma ottieni tutta la potenza tecnicamente installabile nella stessa categoria.",
        "Ogni sistema è completo di accumulo da 16 kWh, incluso nel progetto.",
        "Ad esempio, nella prima fascia, il sistema completo (impianto + accumulo da 16 kWh) da 3,28 kWp ha un prezzo di 11.900 euro.",
        "Se il tetto consente una potenza superiore rispetto ai 3,28 kW iniziali, questa viene installata senza maggiorazioni di prezzo (fino a 5,74 kWp)."
    ]

    for p in paragrafi:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 10))

    # Immagine
    if os.path.exists("TESSERE.jpg"):
        img = Image("TESSERE.jpg")
        img._restrictSize(4.5 * inch, 3.2 * inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 15))

    finali = [
        "Questo è possibile perché oggi gli inverter monofase gestiscono range di ingresso molto ampi e la struttura tecnica dell’impianto non richiede variazioni proporzionali all’aumento dei moduli.",
        "In altre parole, il costo non cresce in modo lineare rispetto alla potenza installata.",
        "<b>Cosa significa, concretamente?</b>",
        "Significa produrre più energia durante l’anno.",
        "Significa aumentare l’autoconsumo reale grazie alla batteria da 16 kWh.",
        "Significa avere una quantità maggiore di energia che può essere immessa in rete.",
        "L’energia non autoconsumata viene valorizzata attraverso il Ritiro Dedicato.",
        "Se condivisa tramite la Comunità Energetica, riceve un incentivo aggiuntivo sull’energia immessa.",
        "A questo si aggiunge la detrazione fiscale del 50% in dieci anni.",
        "Il risultato è un sistema che agisce su più livelli contemporaneamente.",
        "Questa è la logica del Sistema di Rendita Energetica Attiva Next: non limitarsi a compensare la bolletta, ma creare una dinamica economica più ampia, capace di generare valore nel tempo."
    ]

    for p in finali:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 2 — TABELLE + ANALISI 10/20 ANNI
    # =====================================================

    story.append(Paragraph(
        "Dettaglio benefici economici annui derivanti dalla Rendita Energetica Attiva",
        styles["Heading1"]
    ))
    story.append(Spacer(1, 15))

    # Tabelle annuali (come prima)
    # --- omesso qui per lunghezza spiegazione ---
    # (rimangono identiche alla versione precedente con azzurro e verde)

    # -----------------------------------------------------
    # ANALISI DECENNALE E VENTENNALE
    # -----------------------------------------------------

    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "Dettaglio benefici economici su base decennale e ventennale",
        styles["Heading1"]
    ))
    story.append(Spacer(1, 15))

    beneficio_10 = res['beneficio_annuale_totale'] * 10
    beneficio_20 = res['beneficio_20_anni']

    vantaggio_10 = res['risparmio_complessivo_annuo'] * 10
    vantaggio_20 = res['risparmio_complessivo_10'] * 2

    percentuale_beneficio = (beneficio_10 / costo_impianto) * 100
    roi_10 = ((vantaggio_10 - costo_impianto) / costo_impianto) * 100

    data_dec = [
        ["Voce", "10 anni", "20 anni"],
        ["Rendita Energetica Attiva",
         f"{beneficio_10:,.2f}",
         f"{beneficio_20:,.2f}"],
        ["Vantaggio Complessivo Totale",
         f"{vantaggio_10:,.2f}",
         f"{vantaggio_20:,.2f}"]
    ]

    table_dec = Table(data_dec, colWidths=[230, 110, 110])
    table_dec.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (1, 1), (1, -1), colors.lawngreen),
        ("BACKGROUND", (0, 2), (-1, 2), colors.lightgreen),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
    ]))

    story.append(table_dec)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        f"<b>In 10 anni la Rendita Energetica Attiva genera € {beneficio_10:,.2f}</b>, "
        f"pari al <b>{percentuale_beneficio:.1f}%</b> del capitale investito.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"In 10 anni il vantaggio complessivo totale è di € {vantaggio_10:,.2f} "
        f"a fronte di un investimento di € {costo_impianto:,.2f}.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"<b>Resa sul capitale investito in 10 anni: {roi_10:.1f}%</b>",
        body_style
    ))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 3 — GRAFICI
    # =====================================================

    story.append(Paragraph("Proiezione nel Tempo e Rientro dell’Investimento", styles["Heading1"]))
    story.append(Spacer(1, 15))

    chart1 = make_payback_chart(costo_impianto, res["risparmio_complessivo_annuo"])
    chart2 = make_benefits_chart(res["beneficio_10_anni"], res["beneficio_20_anni"])

    story.append(Image(chart1, width=400, height=250))
    story.append(Spacer(1, 20))
    story.append(Image(chart2, width=350, height=250))

    doc.build(story)
    return filename
