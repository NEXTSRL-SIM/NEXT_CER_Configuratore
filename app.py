# app.py
import streamlit as st

from calculator import compute_benefits, autoconsumo_bonus_from_kwp
from pdf_report import build_pdf


st.set_page_config(
    page_title="Firmasubito Upgrade NEXT + CER",
    layout="wide"
)

st.title("⚡ Firmasubito Upgrade NEXT + CER")
st.markdown(
    """
    Configuratore commerciale per simulare i vantaggi economici di:
    - Upgrade NEXT
    - Comunità Energetica (CER) + RID
    - Extra autoconsumo (incremento %)
    - Detrazione fiscale (50% in 10 anni)
    - Risparmio in bolletta (autoconsumo diretto)
    """
)

st.divider()

st.header("📌 Dati Cliente e Impianto")

col1, col2, col3 = st.columns(3)

with col1:
    cliente = st.text_input("Nome Cliente", value="Cliente Demo")
    consumo = st.number_input(
        "Consumo annuo (kWh)",
        min_value=500,
        max_value=50000,
        value=5400,
        step=1
    )

with col2:
    base_kwp = st.number_input("Potenza impianto base (kWp)", value=6.56, step=0.01)
    bonus_kwp = st.number_input("Potenza impianto finale Upgrade NEXT (kWp)", value=9.02, step=0.01)

with col3:
    costo = st.number_input("Costo impianto (€)", value=13560.0, step=50.0)

st.divider()

st.header("⚙️ Parametri Economici")

col4, col5, col6 = st.columns(3)

with col4:
    prezzo_energia = st.number_input("Prezzo energia evitata €/kWh", value=0.30, step=0.01)
    rid = st.number_input("RID €/kWh", value=0.137, step=0.001)

with col5:
    cer = st.number_input("CER €/kWh", value=0.06, step=0.005)
    quota = st.number_input("Quota energia condivisa (%)", value=50, step=5) / 100

with col6:
    resa = st.number_input("Resa zona (kWh/kWp)", value=1200, step=50)
    autoc_base_perc = st.number_input("Autoconsumo base %", value=0.80, step=0.01)

    autoc_bonus_perc = autoconsumo_bonus_from_kwp(bonus_kwp)
    st.write(f"✅ Autoconsumo bonus calcolato automaticamente: **{autoc_bonus_perc*100:.1f}%**")

st.divider()

res = compute_benefits(
    consumo_kwh=consumo,
    base_kwp=base_kwp,
    bonus_kwp=bonus_kwp,
    prezzo_energia=prezzo_energia,
    rid_eur_kwh=rid,
    cer_eur_kwh=cer,
    quota_condivisa=quota,
    costo_impianto=costo,
    resa_kwh_kwp=resa,
    autoc_base_perc=autoc_base_perc,
    autoc_bonus_perc=autoc_bonus_perc,
)

st.header("📊 Risultati Simulazione")

colA, colB = st.columns(2)

with colA:
    st.subheader("Energia (kWh)")
    st.write(f"**Produzione bonus (kWh):** {res['produzione_bonus']:,.0f}")
    st.write(f"**Autoconsumo bonus (kWh):** {res['autoconsumo_bonus']:,.0f}")
    st.write(f"**Energia immessa (kWh):** {res['energia_immessa']:,.0f}")
    st.write(f"**Delta autoconsumo vs base (kWh):** {res['delta_autoconsumo']:,.0f}")

with colB:
    st.subheader("Benefici economici (€ / anno)")
    st.write(f"**Vantaggio extra autoconsumo:** € {res['vantaggio_extra_autoconsumo']:,.2f}")
    st.write(f"**RID €/anno:** € {res['rid_annuo']:,.2f}")
    st.write(f"**CER prudente €/anno:** € {res['cer_prudente']:,.2f}")
    st.write("---")
    st.write(f"**Totale benefici annui (extra + RID + CER):** € {res['totale_benefici_annui']:,.2f}")
    st.write(f"**Detrazione fiscale annua:** € {res['detrazione_annua']:,.2f}")
    st.success(f"✅ Beneficio annuale totale (benefici + detrazione): € {res['beneficio_annuale_totale']:,.2f}")

st.divider()

st.header("💡 Risparmio in bolletta (autoconsumo diretto)")
st.caption("Nota: questo valore ESCLUDE l’extra autoconsumo, già conteggiato nella voce 'Vantaggio extra autoconsumo'.")
st.write(f"**RISPARMIO IN BOLLETTA ANNUO:** € {res['risparmio_bolletta']:,.2f}")

st.info(f"**RISPARMIO COMPLESSIVO ANNUALE (benefici + detrazione + risparmio bolletta):** € {res['risparmio_complessivo_annuo']:,.2f}")
st.write(f"**RISPARMIO COMPLESSIVO IN 10 ANNI (include risparmio bolletta):** € {res['risparmio_complessivo_10']:,.2f}")

st.divider()

st.header("⏳ Beneficio nel Tempo")

colX, colY = st.columns(2)
with colX:
    st.metric("Beneficio totale 10 anni", f"€ {res['beneficio_10_anni']:,.2f}")
with colY:
    st.metric("Beneficio totale 20 anni", f"€ {res['beneficio_20_anni']:,.2f}")

st.divider()

st.header("📄 Report Cliente (PDF)")

if st.button("📌 Genera Report Firmasubito PDF"):
    pdf_path = build_pdf(cliente, res, costo)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Scarica Report PDF",
            data=f,
            file_name=pdf_path,
            mime="application/pdf"
        )
    st.success("PDF generato correttamente!")
