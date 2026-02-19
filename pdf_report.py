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

    testo_pagina1 = [
        "Questa iniziativa nasce da un’idea molto semplice.",
        "Quando si realizza un impianto fotovoltaico residenziale, normalmente si sceglie una potenza “sufficiente”.",
        "Noi abbiamo scelto un approccio diverso.",
        "Attraverso questa promozione abbiamo deciso di proporre un sistema completo – comprensivo di accumulo da 16 kWh – e di sfruttare al massimo la superficie disponibile del tetto, senza aumentare il prezzo rispetto alla configurazione base.",
        "<b>Vediamo come funziona.</b>",
        "Abbiamo suddiviso gli impianti monofase fino a 10 kW in due categorie:",
        "• la prima va da 3,28 kW fino a 5,74 kW",
        "• la seconda va da 6,56 kW fino a 9,84 kW",
        "All’interno di ciascuna categoria esiste una potenza base, che è la più bassa della fascia (3,28 e 6,56 kWp).",
        "Il prezzo viene determinato su quella potenza minima, ma installiamo tutta la potenza che il tetto può ospitare rimanendo all'interno della stessa categoria,<b>senza aumentare il prezzo rispetto alla configurazione iniziale<b>.",
        "In altre parole, paghi l’impianto base della fascia, ma ottieni tutta la potenza tecnicamente installabile nella stessa categoria.",
        "Ogni sistema è completo di accumulo da 16 kWh, incluso nel progetto.",
        "Se il tetto consente una potenza superiore rispetto ai 3,28 kW iniziali, questa viene installata senza maggiorazioni di prezzo fino a 5,74 kWp.",
        "</b>Cosa significa, concretamente?</b>",
        "Significa produrre più energia durante l’anno.",
        "Significa aumentare l’autoconsumo reale grazie alla batteria da 16 kWh, che consente di utilizzare anche la sera l’energia prodotta di giorno.",
        "Significa avere una quantità maggiore di energia che può essere immessa in rete.",
        "Ed è qui che l’impianto cambia natura. Fino a quel punto stiamo parlando di risparmio. Dal momento in cui l’energia prodotta supera quella consumata e viene immessa in rete, entriamo in una logica diversa.",
        "</b>1)	L’energia non autoconsumata viene valorizzata attraverso il Ritiro Dedicato.</b>",
        "</b> condivisa tramite la Comunità Energetica, riceve un incentivo aggiuntivo sull’energia immessa.</b>",
        "In termini pratici, l’energia prodotta in eccesso genera un ritorno economico. E più l’impianto produce, maggiore diventa questa componente. A questo si aggiunge la detrazione fiscale del 50% in dieci anni. Il risultato è un sistema che agisce su più livelli contemporaneamente: riduce la spesa energetica annua, aumenta l’autonomia dalla rete, valorizza l’energia immessa, beneficia della Comunità Energetica, recupera parte dell’investimento tramite detrazione. Non si tratta semplicemente di installare un impianto più grande. Si tratta di utilizzare in modo più intelligente la stessa struttura tecnica per trasformare il tetto in una piattaforma di produzione energetica evoluta. Questa è la logica del Sistema di Rendita Energetica Attiva Next: non limitarsi a compensare la bolletta, ma creare una dinamica economica più ampia, capace di generare valore nel tempo, una rendita energetica appunto."
    ]

    for p in testo_pagina1:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 10))

    if os.path.exists("TESSERE.jpg"):
        img = Image("TESSERE.jpg")
        img._restrictSize(4.5 * inch, 3.2 * inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 15))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 2 — BENEFICI ANNUALI
    # =====================================================

    story.append(Paragraph(
        "Dettaglio benefici economici annui derivanti dalla Rendita Energetica Attiva",
        styles["Heading1"]
    ))
    story.append(Spacer(1, 15))

    # Tabella 1
    data1 = [
        ["Voce", "Valore (€ / anno)"],
        ["Extra autoconsumo (Upgrade)", f"{res['vantaggio_extra_autoconsumo']:,.2f}"],
        ["RID energia immessa", f"{res['rid_annuo']:,.2f}"],
        ["CER prudente", f"{res['cer_prudente']:,.2f}"],
        ["Totale benefici Upgrade + CER", f"{res['totale_benefici_annui']:,.2f}"],
        ["Detrazione fiscale annua", f"{res['detrazione_annua']:,.2f}"],
        ["Beneficio annuale totale – Rendita Energetica Attiva",
         f"{res['beneficio_annuale_totale']:,.2f}"],
    ]

    table1 = Table(data1, colWidths=[280, 170])
    table1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightblue),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    story.append(table1)
    story.append(Spacer(1, 20))

    # Tabella 2
    data2 = [
        ["Voce", "Valore (€ / anno)"],
        ["Rendita Energetica Attiva", f"{res['beneficio_annuale_totale']:,.2f}"],
        ["Risparmio in bolletta", f"{res['risparmio_bolletta']:,.2f}"],
        ["Vantaggio complessivo totale annuo",
         f"{res['risparmio_complessivo_annuo']:,.2f}"],
    ]

    table2 = Table(data2, colWidths=[280, 170])
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 3), (-1, 3), colors.lightgreen),
        ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
    ]))

    story.append(table2)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "Il cliente non sta spendendo: sta convertendo una bolletta futura in un investimento produttivo.",
        body_style
    ))
    story.append(Spacer(1, 25))

    # =====================================================
    # SEZIONE 10 / 20 ANNI
    # =====================================================

    story.append(Paragraph(
        "Dettaglio benefici economici su base decennale e ventennale",
        styles["Heading1"]
    ))
    story.append(Spacer(1, 15))

    beneficio_10 = res['beneficio_10_anni']
    beneficio_20 = res['beneficio_20_anni']

    vantaggio_10 = res['risparmio_complessivo_10']
    vantaggio_20 = res['risparmio_complessivo_annuo'] * 20

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
