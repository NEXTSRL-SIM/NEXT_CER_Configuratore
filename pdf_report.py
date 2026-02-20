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
import os
import datetime
import matplotlib.pyplot as plt

def make_payback_chart(costo, beneficio_primi_10, beneficio_dal_11):

    anni = list(range(0, 21))
    valori = []

    cumulato = 0

    for anno in anni:
        if anno == 0:
            valori.append(0)
            continue

        if anno <= 10:
            cumulato += beneficio_primi_10
        else:
            cumulato += beneficio_dal_11

        valori.append(cumulato)

    fig, ax = plt.subplots()

    # Linea rendimento cumulato (verde come prima)
    ax.plot(anni, valori, color="#4CAF50", linewidth=3)

    # Linea investimento (azzurro tratteggiato come prima)
    ax.axhline(costo, color="#5CB8E4", linestyle="--", linewidth=2)

    ax.set_title("Rientro dell'investimento (Payback reale)")
    ax.set_xlabel("Anni")
    ax.set_ylabel("Beneficio cumulato (€)")

    ax.grid(alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    path = os.path.join(base_dir, f"payback_{int(datetime.datetime.now().timestamp())}.png")

    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)

    return path


def make_benefits_chart(b10, b20):
    fig, ax = plt.subplots()

    # 10 anni verde pieno, 20 anni verde light
    ax.bar(["10 anni", "20 anni"], [b10, b20], color=["#4CAF50", "#A5D6A7"])

    ax.set_title("Beneficio Totale nel Tempo")
    ax.set_ylabel("Euro (€)")

    ax.grid(axis='y', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # DEBUG: timestamp dentro il grafico (poi lo togli)
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    ax.text(0.99, 0.01, stamp, transform=ax.transAxes, ha="right", va="bottom", fontsize=8, alpha=0.6)

    base_dir = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    path = os.path.join(base_dir, f"benefici_{int(datetime.datetime.now().timestamp())}.png")

    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return path


# ---------------------------------------------------------
# BUILD PDF
# ---------------------------------------------------------
def build_pdf(
    cliente,
    res,
    costo_impianto,
    consumo_kwh,
    base_kwp,
    bonus_kwp,
    resa_kwh_kwp,
    prezzo_energia,
    rid_eur_kwh,
    cer_eur_kwh,
    quota_condivisa,
    autoc_base_perc,
    autoc_bonus_perc,
):

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
        "<b>Iniziativa valida fino al 30 marzo 2026 e limitata ai primi 20 impianti.</b>",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles["Normal"]))
    story.append(Paragraph(f"<b>Data simulazione:</b> {oggi}", styles["Normal"]))
    story.append(Spacer(1, 20))

    testo_pagina1 = [
    "Questa iniziativa nasce da un’idea molto semplice. Quando si realizza un impianto fotovoltaico residenziale, normalmente si sceglie una potenza “sufficiente”.",
    "Noi abbiamo scelto un approccio diverso.",
    "Attraverso questa promozione abbiamo deciso di proporre un sistema completo – comprensivo di accumulo da 16 kWh – e di sfruttare al massimo la superficie disponibile del tetto, senza aumentare il prezzo rispetto alla configurazione base.",
    "<b>Vediamo come funziona.</b>",
    "Abbiamo suddiviso gli impianti monofase fino a 10 kW in due categorie:",
    "• la prima va da 3,28 kW fino a 5,74 kW",
    "• la seconda va da 6,56 kW fino a 9,84 kW",
    "All’interno di ciascuna categoria esiste una potenza base, che è la più bassa della fascia (3,28 e 6,56 kWp). Il prezzo viene determinato su quella potenza minima, ma installiamo tutta la potenza che il tetto può ospitare rimanendo all'interno della stessa categoria, <b>senza aumentare il prezzo rispetto alla configurazione iniziale</b>.",
    "In altre parole, paghi l’impianto base della fascia, ma ottieni tutta la potenza tecnicamente installabile nella stessa categoria. Ogni sistema è completo di accumulo da 16 kWh, incluso nel progetto.",
    "Se il tetto consente una potenza superiore rispetto ai 3,28 kW iniziali, questa viene installata senza maggiorazioni di prezzo fino a 5,74 kWp.",
    "<b>Cosa significa, concretamente?</b>",
    "Significa produrre più energia durante l’anno.",
    "Significa aumentare l’autoconsumo reale grazie alla batteria da 16 kWh, che consente di utilizzare anche la sera l’energia prodotta di giorno.",
    "Significa avere una quantità maggiore di energia che può essere immessa in rete.",
    "Ed è qui che l’impianto cambia natura. Fino a quel punto stiamo parlando di risparmio. Dal momento in cui l’energia prodotta supera quella consumata e viene immessa in rete, entriamo in una logica diversa.",
    "<b>1) L’energia non autoconsumata viene valorizzata attraverso il Ritiro Dedicato.</b>",
    "<b>2) Se condivisa tramite la Comunità Energetica, riceve un incentivo aggiuntivo sull’energia immessa.</b>",
    "In termini pratici, l’energia prodotta in eccesso genera un ritorno economico. E più l’impianto produce, maggiore diventa questa componente. A questo si aggiunge la detrazione fiscale del 50% in dieci anni. Il risultato è un sistema che agisce su più livelli contemporaneamente: riduce la spesa energetica annua, aumenta l’autonomia dalla rete, valorizza l’energia immessa, beneficia della Comunità Energetica, recupera parte dell’investimento tramite detrazione. Non si tratta semplicemente di installare un impianto più grande. Si tratta di utilizzare in modo più intelligente la stessa struttura tecnica per trasformare il tetto in una piattaforma di produzione energetica evoluta. Questa è la logica del Sistema di Rendita Energetica Attiva Next: non limitarsi a compensare la bolletta, ma creare una dinamica economica più ampia, capace di generare valore nel tempo, una rendita energetica appunto."
]


    for p in testo_pagina1:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 10))

     # Inserimento immagine nel punto corretto
        if "5,74 kWp" in p:
            if os.path.exists("TESSERE.jpg"):
                img = Image("TESSERE.jpg")
                img._restrictSize(5.2 * inch, 3.6 * inch)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 30))

    story.append(PageBreak())

    # =====================================================
    # SCHEDA TECNICA DI SIMULAZIONE
    # =====================================================

    story.append(Paragraph("Scheda tecnica della simulazione", styles["Heading1"]))
    story.append(Spacer(1, 30))

    story.append(Paragraph(f"<b>Cliente:</b> {cliente}", styles["Normal"]))
    story.append(Spacer(1, 30))

    story.append(Paragraph(
        "La presente simulazione è stata elaborata sulla base delle seguenti ipotesi tecniche ed economiche:",
        styles["Normal"]
    ))
    story.append(Spacer(1, 25))

    testo_simulazione = [
        f"Consumo annuo stimato: <b>{consumo_kwh:,.0f} kWh</b>",
        f"Impianto base considerato: <b>{base_kwp:.2f} kWp</b>",
        f"Impianto upgrade considerato: <b>{bonus_kwp:.2f} kWp</b>",
        f"Resa ipotizzata per area geografica: <b>{resa_kwh_kwp:,.0f} kWh/kWp</b>",
        f"Produzione teorica impianto upgrade: <b>{res['produzione_bonus_teorica']:,.0f} kWh</b>",
    ]

    if res["percentuale_clipping"] > 0:
        testo_simulazione.append(
            f"Ottimizzazione inverter (clipping stimato): <b>{res['percentuale_clipping']*100:.1f}%</b>"
        )

    testo_simulazione += [
    f"Produzione effettiva stimata: <b>{res['produzione_bonus']:,.0f} kWh</b>",
    "",
    "<b>Parametri economici adottati nella simulazione:</b>",
    f"Prezzo energia evitata: <b>{prezzo_energia:.3f} €/kWh</b>",
    f"Ritiro Dedicato (RID): <b>{rid_eur_kwh:.3f} €/kWh</b>",
    f"Incentivo Comunità Energetica (CER): <b>{cer_eur_kwh:.3f} €/kWh</b>",
    f"Quota energia condivisa stimata: <b>{quota_condivisa*100:.0f}%</b>",
    f"Costo impianto considerato: € <b>{costo_impianto:,.2f}</b>",
    "",
    "<b>Ipotesi di copertura dei consumi:</b>",
    f"Copertura con impianto base: <b>{autoc_base_perc*100:.1f}%</b>",
    f"Copertura con impianto upgrade: <b>{autoc_bonus_perc*100:.1f}%</b>",
    "",
    "Le percentuali di copertura rappresentano una stima prudenziale "
    "della quota di fabbisogno energetico annuo coperta dall’impianto "
    "fotovoltaico in presenza di accumulo da 16 kWh.",
    "",
    "",
    "",
    ""
]

    for riga in testo_simulazione:
        story.append(Paragraph(riga, styles["Normal"]))
        story.append(Spacer(1, 15))

    story.append(Spacer(1, 15))

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
        ["Totale benefici Upgrade + RID + CER", f"{res['totale_benefici_annui']:,.2f}"],
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
        "Grazie a questo sistema stai convertendo una bolletta futura in un investimento produttivo.",
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

    secondo_decennio = (res["beneficio_annuale_totale"] - res["detrazione_annua"]) * 10 \
                   + res["risparmio_bolletta"] * 10

    vantaggio_20 = vantaggio_10 + secondo_decennio

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
        f"<b>Resa sul capitale investito in 10 anni: {roi_10:.1f}%</b><br/>"
        f"<b>Resa annua sul capitale investito: {(roi_10 / 10):.1f}%</b>",
        body_style
    ))

    story.append(PageBreak())

    # =====================================================
    # PAGINA 3 — GRAFICI
    # =====================================================

    story.append(Paragraph("Proiezione nel Tempo e Rientro dell’Investimento", styles["Heading1"]))
    story.append(Spacer(1, 15))

    # =============================
    # Definizione benefici
    # =============================

    beneficio_primi_10 = res["risparmio_complessivo_annuo"]

    beneficio_dal_11 = (
        res["beneficio_annuale_totale"] - res["detrazione_annua"]
    ) + res["risparmio_bolletta"]

    # =============================
    # Calcolo payback dinamico
    # =============================

    cumulato = 0
    payback_anni = 0

    for anno in range(1, 31):
        if anno <= 10:
            beneficio_annuale = beneficio_primi_10
        else:
            beneficio_annuale = beneficio_dal_11

        if cumulato + beneficio_annuale >= costo_impianto:
            # quota residua da coprire
            residuo = costo_impianto - cumulato
            frazione_anno = residuo / beneficio_annuale
            payback_anni = (anno - 1) + frazione_anno
            break

        cumulato += beneficio_annuale

    # =============================
    # Testo descrittivo payback
    # =============================

    testo_payback = (
        "Il grafico seguente rappresenta l’andamento cumulato del beneficio economico "
        "generato dall’impianto nel tempo, confrontato con l’investimento iniziale sostenuto. "
        "La curva evidenzia il punto di rientro dell’investimento (payback), ossia "
        "il momento in cui i benefici economici cumulati eguagliano il capitale iniziale."
    )

    story.append(Paragraph(testo_payback, body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        f"<b>L’investimento si ripaga in circa {payback_anni:.1f} anni.</b>",
    body_style
    ))
    story.append(Spacer(1, 20))

    # =============================
    # Grafici
    # =============================

    chart1 = make_payback_chart(
        costo_impianto,
        beneficio_primi_10,
        beneficio_dal_11
    )

    chart2 = make_benefits_chart(
        res["beneficio_10_anni"],
        res["beneficio_20_anni"]
    )

    story.append(Image(chart1, width=400, height=250))
    story.append(Spacer(1, 20))
    story.append(Image(chart2, width=350, height=250))

    story.append(Spacer(1, 25))

    # =============================
    # Valutazione finale
    # =============================

    vantaggio_10 = res["risparmio_complessivo_10"]
    differenza_netto = vantaggio_10 - costo_impianto

    story.append(PageBreak())

    story.append(Paragraph("Valutazione Economico/Strategica Complessiva", styles["Heading1"]))
    story.append(Spacer(1, 15))

    testo_chiusura = [
        f"Il grafico e i dati che precedono mostrano chiaramente che, nel corso di 10 anni, "
        f"il Risparmio Complessivo Totale generato dal Sistema di Rendita Energetica Attiva "
        f"supera ampiamente il capitale iniziale investito.",

        "",
        f"In questo caso, è stato stimato un beneficio cumulato di € {vantaggio_10:,.2f} "
        f"a fronte di un investimento di € {costo_impianto:,.2f}.",

        f"<b>Non realizzare l’intervento significa rinunciare a un valore economico potenziale "
        f"netto di oltre € {differenza_netto:,.2f} in 10 anni.</b>",
        "",
        "In un contesto di mercati energetici volatili e strutturalmente in crescita, "
        "proteggersi dal rischio di aumento dei costi dell’energia elettrica rappresenta "
        "una leva di stabilità economica nel medio-lungo periodo.",
        "",
        "La presente simulazione non considera alcun incremento futuro dei prezzi dell’energia. "
        "Qualora tali aumenti dovessero verificarsi, il beneficio economico cumulato "
        "risulterebbe ulteriormente maggiore.",
        "",
        "In sintesi:",
        "• l’impianto non è soltanto uno strumento di riduzione della bolletta;",
        "• genera un flusso economico positivo nel tempo;",
        "• riduce l’esposizione al rischio energetico;",
        "• può essere supportato da soluzioni finanziarie dedicate.",

        "",
        "Scegliere di attivare il Sistema di Rendita Energetica Attiva Next significa "
        "trasformare una spesa energetica futura incerta in un flusso di valore definito "
        "e progressivamente crescente nel tempo.",

        "",
        "NEXT SRL - Report simulazione",
        "Valori indicativi",
        f"Data {oggi}"
    ]

    for p in testo_chiusura:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    return filename