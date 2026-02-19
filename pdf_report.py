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
# GRAFICO PAYBACK
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

    chart_path = "payback.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path


# ---------------------------------------------------------
# GRAFICO BENEFICI
# ---------------------------------------------------------
def make_benefits_chart(b10, b20):
    plt.figure()
    plt.bar(["10 anni", "20 anni"], [b10, b20])

    plt.title("Beneficio Totale nel Tempo")
    plt.ylabel("Euro (€)")

    chart_path = "benefici.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path


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
    # PAGINA 1
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

    # Testo prima parte (spezzato)

    story.append(Paragraph("Questa iniziativa nasce da un’idea molto semplice.", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Quando si realizza un impianto fotovoltaico residenziale, normalmente si sceglie una potenza “sufficiente”.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Noi abbiamo scelto un approccio diverso.", body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Attraverso questa promozione abbiamo deciso di proporre un sistema completo – comprensivo di accumulo da 16 kWh – e di sfruttare al massimo la superficie disponibile del tetto, senza aumentare il prezzo rispetto alla configurazione base.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Vediamo come funziona.</b>", body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Abbiamo suddiviso gli impianti monofase fino a 10 kW in due categorie:",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("• la prima va da 3,28 kW fino a 5,74 kW", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("• la seconda va da 6,56 kW fino a 9,84 kW", body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "All’interno di ciascuna categoria esiste una potenza base, che è la più bassa della fascia (3,28 e 6,56 kWp).",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Il prezzo viene determinato su quella potenza minima, ma installiamo tutta la potenza che il tetto può ospitare rimanendo all’interno della stessa categoria, senza aumentare il prezzo rispetto alla configurazione iniziale.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "In altre parole, paghi l’impianto base della fascia, ma ottieni tutta la potenza tecnicamente installabile nella stessa categoria.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Ogni sistema è completo di accumulo da 16 kWh, incluso nel progetto.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Ad esempio, nella prima fascia, il sistema completo (impianto + accumulo da 16 kWh) da 3,28 kWp ha un prezzo di 11.900 euro.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Se il tetto consente una potenza superiore rispetto ai 3,28 kW iniziali, questa viene installata senza maggiorazioni di prezzo (fino a 5,74 kWp).",
        body_style
    ))
    story.append(Spacer(1, 20))

    # Immagine proporzionale sicura
    if os.path.exists("TESSERE.jpg"):
        img = Image("TESSERE.jpg")
        img._restrictSize(5 * inch, 4 * inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 20))

    # Parte finale prima pagina

    story.append(Paragraph(
        "Questo è possibile perché oggi gli inverter monofase gestiscono range di ingresso molto ampi e la struttura tecnica dell’impianto non richiede variazioni proporzionali all’aumento dei moduli.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "In altre parole, il costo non cresce in modo lineare rispetto alla potenza installata.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Cosa significa, concretamente?</b>", body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Significa produrre più energia durante l’anno.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Significa aumentare l’autoconsumo reale grazie alla batteria da 16 kWh.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Significa avere una quantità maggiore di energia che può essere immessa in rete.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "L’energia non autoconsumata viene valorizzata attraverso il Ritiro Dedicato.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "Se condivisa tramite la Comunità Energetica, riceve un incentivo aggiuntivo sull’energia immessa.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "A questo si aggiunge la detrazione fiscale del 50% in dieci anni.",
        body_style
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        "Questa è la logica del Sistema di Rendita Energetica Attiva Next: creare una dinamica economica più ampia, capace di generare valore nel tempo.",
        body_style
    ))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 2 — TABELLE
    # =====================================================

    story.append(Paragraph(
        "Dettaglio benefici economici annui derivanti dalla Rendita Energetica Attiva",
        styles["Heading1"]
    ))
    story.append(Spacer(1, 15))

    data1 = [
        ["Voce", "Valore (€ / anno)"],
        ["Extra autoconsumo (Upgrade)", f"{res['vantaggio_extra_autoconsumo']:,.2f}"],
        ["RID energia immessa", f"{res['rid_annuo']:,.2f}"],
        ["CER prudente", f"{res['cer_prudente']:,.2f}"],
        ["Totale benefici Upgrade + CER", f"{res['totale_benefici_annui']:,.2f}"],
        ["Detrazione fiscale annua", f"{res['detrazione_annua']:,.2f}"],
        ["Beneficio annuale totale – Rendita Energetica Attiva", f"{res['beneficio_annuale_totale']:,.2f}"],
    ]

    table1 = Table(data1, colWidths=[280, 170])
    table1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightblue),
    ]))

    story.append(table1)
    story.append(Spacer(1, 20))

    data2 = [
        ["Voce", "Valore (€ / anno)"],
        ["Rendita Energetica Attiva", f"{res['beneficio_annuale_totale']:,.2f}"],
        ["Risparmio in bolletta", f"{res['risparmio_bolletta']:,.2f}"],
        ["Vantaggio complessivo totale annuo", f"{res['risparmio_complessivo_annuo']:,.2f}"],
    ]

    table2 = Table(data2, colWidths=[280, 170])
    table2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    story.append(table2)

    doc.build(story)
    return filename

