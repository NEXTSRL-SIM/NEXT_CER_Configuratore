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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import datetime
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# FUNZIONE PER CREARE GRAFICO PAYBACK
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
# FUNZIONE PER CREARE GRAFICO BENEFICI 10–20 ANNI
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
# PDF COMMERCIALE PREMIUM
# ---------------------------------------------------------
def build_pdf(cliente, res, costo_impianto):

    filename = f"Report_Firmasubito_{cliente}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)

    styles = getSampleStyleSheet()
    story = []

    oggi = datetime.date.today().strftime("%d/%m/%Y")

    # =====================================================
    # PAGINA 1 — QUADRO COMMERCIALE
    # =====================================================

    story.append(Paragraph("Promozione Firmasubito con SISTEMA DI RENDITA ENERGETICA ATTIVA", styles["Title"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles["Normal"]))
    story.append(Paragraph(f"<b>Data simulazione:</b> {oggi}", styles["Normal"]))
    story.append(Spacer(1, 20))

    testo_intro = f"""
    Un upgrade immediato che moltiplica produzione, autoconsumo e ritorno economico grazie anche alla Comunità Energetica.
    Attraverso questi incentivi acceleri esponenzialmente il recupero del capitale investito. L'agevolazione è notevolmente superiore rispetto al costo dell'impianto.

    <br/><br/>
    Con la Promozione Firmasubito e grazie al sistema di rendimento attivo di Next srl, il cliente ottiene, in aggiunta alla detrazione fiscale del 50% in 10 anni, tre vantaggi simultanei:

    <br/><br/>
    <b>1. Upgrade NEXT</b>: l’impianto viene potenziato, aumentando l’autoconsumo reale, sopratutto nei mesi invernali, quando ogni kWh in più fa la differenza.<br/>
    <b>2. Energia immessa valorizzata</b>: l’energia non consumata viene venduta tramite RID a valori di mercato.<br/>
    <b>3. Incentivo Comunità Energetica (CER)</b>: premio aggiuntivo sull’energia condivisa. Aderendo alla CER, il cliente riceve un ulteriore incentivo economico sull’energia immessa e condivisa, amplificando ancora di più il ritorno annuale.

    <br/><br/>
    Il risultato è un flusso economico annuo positivo che accelera il rientro
    dell’investimento e trasforma il fotovoltaico in un asset che genera valore. A questo si aggiunge il taglio della spesa energetica.
    """

    story.append(Paragraph(testo_intro, styles["BodyText"]))
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"""
            <b>Costo impianto:</b> € {costo_impianto:,.2f}<br/>
            <b>Beneficio annuale totale stimato:</b> € {res['beneficio_annuale_totale']:,.2f}<br/>
            <b>Risparmio complessivo annuo (inclusa bolletta):</b> € {res['risparmio_complessivo_annuo']:,.2f}
            """,
            styles["BodyText"]
        )
    )

    story.append(PageBreak())

    # =====================================================
    # PAGINA 2 — DETTAGLIO NUMERICO + BREAKDOWN
    # =====================================================

    story.append(Paragraph("Dettaglio Benefici Economici Annui", styles["Heading1"]))
    story.append(Spacer(1, 15))

    data = [
        ["Voce", "Valore (€ / anno)"],
        ["Extra autoconsumo (Upgrade)", f"{res['vantaggio_extra_autoconsumo']:,.2f}"],
        ["RID energia immessa", f"{res['rid_annuo']:,.2f}"],
        ["CER prudente", f"{res['cer_prudente']:,.2f}"],
        ["Totale benefici Upgrade + CER", f"{res['totale_benefici_annui']:,.2f}"],
        ["Detrazione fiscale annua", f"{res['detrazione_annua']:,.2f}"],
        ["Beneficio annuale totale", f"{res['beneficio_annuale_totale']:,.2f}"],
        ["Risparmio bolletta annuo", f"{res['risparmio_bolletta']:,.2f}"],
        ["Risparmio complessivo annuo", f"{res['risparmio_complessivo_annuo']:,.2f}"],
    ]

    table = Table(data, colWidths=[280, 170])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightblue),
    ]))

    story.append(table)
    story.append(Spacer(1, 25))

    testo_pagina2 = """
    Come si vede, l’intervento genera valore su più livelli:

    • L’Upgrade NEXT aumenta l’autoconsumo e riduce la dipendenza dalla rete.<br/>
    • Il RID monetizza l’energia immessa.<br/>
    • La CER aggiunge un incentivo pluriennale sull’energia condivisa.<br/>
    • La detrazione fiscale accelera ulteriormente il rientro.

    <br/><br/>
    Il cliente non sta “spendendo”, ma sta convertendo una bolletta futura
    in un investimento produttivo.
    """

    story.append(Paragraph(testo_pagina2, styles["BodyText"]))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 3 — GRAFICI + PAYBACK + FUTURO
    # =====================================================

    story.append(Paragraph("Proiezione nel Tempo e Rientro dell’Investimento", styles["Heading1"]))
    story.append(Spacer(1, 15))

    # Grafici
    chart1 = make_payback_chart(costo_impianto, res["risparmio_complessivo_annuo"])
    chart2 = make_benefits_chart(res["beneficio_10_anni"], res["beneficio_20_anni"])

    story.append(Image(chart1, width=400, height=250))
    story.append(Spacer(1, 20))
    story.append(Image(chart2, width=350, height=250))

    story.append(Spacer(1, 25))

    testo_finale = f"""
    Con questi numeri, il cliente ottiene:

    <br/><br/>
    <b>• Beneficio totale in 10 anni:</b> € {res['beneficio_10_anni']:,.2f}<br/>
    <b>• Beneficio totale in 20 anni:</b> € {res['beneficio_20_anni']:,.2f}<br/>
    <b>• Risparmio complessivo in 10 anni:</b> € {res['risparmio_complessivo_10']:,.2f}

    <br/><br/>
    In altre parole: non realizzare questo intervento significa rinunciare
    a decine di migliaia di euro di valore futuro.

    <br/><br/>
    Firmasubito Upgrade NEXT + CER è la soluzione che trasforma l’energia
    in un vantaggio economico stabile, misurabile e duraturo.
    """

    story.append(Paragraph(testo_finale, styles["BodyText"]))
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<i>Report generato automaticamente – valori indicativi. NEXT S.r.l.</i>",
            styles["Normal"]
        )
    )

    # BUILD PDF
    doc.build(story)

    return filename
