import streamlit as st

from calculator import compute_benefits
from pdf_report import build_pdf


# -----------------------------
# CONFIG PAGINA
# -----------------------------
st.set_page_config(
    page_title="Firmasubito Upgrade NEXT + CER",
    layout="wide"
)

st.title("⚡ Firmasubito Upgrade NEXT + CER")
st.markdown(
    """
    Configuratore commerciale per simulare i vantaggi economici di:

    ✅ Upgrade NEXT  
    ✅ Comunità Energetica (CER)  
    ✅ RID (energia venduta)  
    ✅ Extra autoconsumo  
    ✅ Detrazione fiscale  
    ✅ Risparmio bolletta
    """
)

st.divider()


# -----------------------------
# INPUT CLIENTE
# -----------------------------
st.header("📌 Dati Cliente e Impianto")

col1, col2, col3 = st.columns(3)

with col1:
    cliente = st.text_input("Nome Cliente", value="Cliente Demo")

    consumo = st.number_input(
        "Consumo annuo (kWh)",
        min_value=1000,
        max_value=20000,
        value=5400,
        step=1
    )

with col2:
    base_kwp = st.number_input(
        "Potenza impianto base (kWp)",
        value=6.56,
        step=0.1
    )

    bonus_kwp = st.number_input(
        "Potenza impianto finale Upgrade NEXT (kWp)",
        value=9.02,
        step=0.1
    )

with col3:
    costo = st.number_input(
        "Costo impianto (€)",
        value=13560.0,
        step=100.0
    )

st.divider()


# -----------------------------
# PARAMETRI ECONOMICI
# -----------------------------
st.header("⚙️ Parametri Economici (modificabili solo dall'operatore)")

col4, col5, col6 = st.columns(3)

with col4:
    prezzo_energia = st.number_input(
        "Prezzo energia evitata €/kWh",
        value=0.30,
        step=0.01
    )

    rid = st.number_input(
        "RID €/kWh",
        value=0.137,
        step=0.001
    )

with col5:
    cer = st.number_input(
        "CER €/kWh",
        value=0.06,
        step=0.01
    )

    quota = st.number_input(
        "Quota energia condivisa (%)",
        value=50,
        step=5
    ) / 100

with col6:
    resa = st.number_input(
        "Resa zona (kWh/kWp)",
        value=1200,
        step=50
    )

    autoc_base_perc = st.number_input(
        "Autoconsumo base %",
        value=0.80,
        step=0.01
    )

    autoc_bonus_perc = st.number_input(
        "Autoconsumo bonus %",
        value=0.88,
        step=0.01
    )

st.divider()


# -----------------------------
# CALCOLO
# -----------------------------
st.header("📊 Risultati Simulazione")

res = compute_benefits(
    consumo,
    base_kwp,
    bonus_kwp,
    prezzo_energia,
    rid,
    cer,
    quota,
    costo,
    resa,
    autoc_base_perc,
    autoc_bonus_perc
)

# -----------------------------
# OUTPUT VISIVO
# -----------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("Energia (kWh)")

    st.write(f"**Produzione impianto Upgrade:** {res['produzione_bonus']:,.0f} kWh")
    st.write(f"**Autoconsumo bonus:** {res['autoconsumo_bonus']:,.0f} kWh")
    st.write(f"**Energia immessa in rete:** {res['energia_immessa']:,.0f} kWh")
    st.write(f"**Delta autoconsumo vs base:** {res['delta_autoconsumo']:,.0f} kWh")

with colB:
    st.subheader("Benefici economici (€ / anno)")

    st.write(f"**Extra autoconsumo:** € {res['vantaggio_extra_autoconsumo']:,.2f}")
    st.write(f"**RID energia venduta:** € {res['rid_annuo']:,.2f}")
    st.write(f"**CER prudente:** € {res['cer_prudente']:,.2f}")

    st.write("---")
    st.write(f"**Totale benefici annui Upgrade+CER:** € {res['totale_benefici_annui']:,.2f}")
    st.write(f"**Detrazione fiscale annua:** € {res['detrazione_annua']:,.2f}")

    st.success(f"✅ Beneficio annuale totale: € {res['beneficio_annuale_totale']:,.2f}")

st.divider()


# -----------------------------
# RISPARMIO BOLLETTA
# -----------------------------
st.header("💡 Risparmio Bolletta")

st.write(
    f"Risparmio annuo grazie all'autoconsumo diretto:\n\n"
    f"**€ {res['risparmio_bolletta']:,.2f} / anno**"
)

st.info(
    f"Risparmio complessivo annuo totale:\n\n"
    f"**€ {res['risparmio_complessivo_annuo']:,.2f} / anno**"
)

st.divider()


# -----------------------------
# ORIZZONTE TEMPORALE
# -----------------------------
st.header("⏳ Beneficio nel Tempo")

colX, colY, colZ = st.columns(3)

with colX:
    st.metric("Totale 10 anni", f"€ {res['beneficio_10_anni']:,.2f}")

with colY:
    st.metric("Totale 20 anni", f"€ {res['beneficio_20_anni']:,.2f}")

with colZ:
    st.metric("Risparmio complessivo 10 anni", f"€ {res['risparmio_complessivo_10']:,.2f}")

st.divider()


# -----------------------------
# PDF REPORT
# -----------------------------
st.header("📄 Report Cliente (PDF)")

if st.button("📌 Genera Report Firmasubito PDF"):
    pdf_path = build_pdf(cliente, res, costo)

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Scarica Report PDF",
            data=f,
            file_name=f"Report_Firmasubito_{cliente}.pdf",
            mime="application/pdf"
        )

    st.success("PDF generato correttamente!")
