# app.py
import streamlit as st

from calculator import compute_benefits, quota_copertura_from_kwp
from pdf_report import build_pdf


st.set_page_config(
    page_title="Sistema di Rendita Energetica Attiva Next",
    layout="wide"
)

st.title("⚡ Analisi Rendita Energetica Attiva Next")
st.markdown(
    """
    Configuratore commerciale per simulare i vantaggi economici di:
    - Upgrade impianto NEXT
    - Comunità Energetica (CER) + RID
    - Extra autoconsumo
    - Incremento annuo costo energia
    - Detrazione fiscale (50% in 10 anni)
    - Risparmio in bolletta
    """
)

st.divider()

# =========================================================
# DATI CLIENTE
# =========================================================

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

# =========================================================
# PARAMETRI ECONOMICI
# =========================================================

st.header("⚙️ Parametri Economici")

col4, col5, col6 = st.columns(3)

with col4:
    prezzo_energia = st.number_input(
        "Prezzo energia evitata €/kWh",
        value=0.30,
        step=0.01
    )

    incremento = st.number_input(
        "Incremento annuo costo energia (%)",
        min_value=0.0,
        max_value=15.0,
        value=3.0,
        step=0.5
    ) / 100

    rid = st.number_input(
        "RID €/kWh",
        value=0.137,
        step=0.001
    )

with col5:
    cer = st.number_input(
        "CER €/kWh",
        value=0.06,
        step=0.005
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

    autoc_bonus_perc = quota_copertura_from_kwp(bonus_kwp)

    st.write(
        f"✅ Percentuale di copertura calcolata automaticamente: "
        f"**{autoc_bonus_perc * 100:.1f}%**"
    )

st.divider()

# =========================================================
# CALCOLO
# =========================================================

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
    incremento_prezzo_annuo=incremento,
)

# =========================================================
# RISULTATI
# =========================================================

st.header("📊 Risultati Simulazione")

colA, colB = st.columns(2)

with colA:
    st.subheader("Energia (kWh)")
    st.write(f"Produzione impianto upgrade: {res['produzione_bonus']:,.0f} kWh")
    st.write(f"Energia coperta upgrade: {res['autoconsumo_bonus']:,.0f} kWh")
    st.write(f"Energia immessa in rete: {res['energia_immessa']:,.0f} kWh")
    st.write(f"Energia aggiuntiva vs base: {res['delta_autoconsumo']:,.0f} kWh")

with colB:
    st.subheader("Benefici economici (€ / anno)")
    st.write(f"Maggior risparmio copertura aggiuntiva: € {res['vantaggio_extra_autoconsumo']:,.2f}")
    st.write(f"RID annuo: € {res['rid_annuo']:,.2f}")
    st.write(f"CER incentivo: € {res['cer_prudente']:,.2f}")
    st.write("---")
    st.write(f"Totale benefici annui: € {res['totale_benefici_annui']:,.2f}")
    st.write(f"Detrazione fiscale annua: € {res['detrazione_annua']:,.2f}")
    st.success(f"Beneficio annuale totale: € {res['beneficio_annuale_totale']:,.2f}")

st.divider()

# =========================================================
# RISPARMIO COMPLESSIVO
# =========================================================

st.header("💡 Risparmio in bolletta")
st.write(f"Risparmio bolletta annuo: € {res['risparmio_bolletta']:,.2f}")

st.info(
    f"Risparmio complessivo annuo: € {res['risparmio_complessivo_annuo']:,.2f}"
)

st.write(
    f"Risparmio complessivo 10 anni: € {res['risparmio_complessivo_10']:,.2f}"
)

st.write(
    f"Risparmio complessivo 20 anni: € {res['risparmio_complessivo_20']:,.2f}"
)

st.divider()

# =========================================================
# RENDITA NEL TEMPO
# =========================================================

st.header("⏳ Rendita Energetica Attiva nel Tempo")

colX, colY = st.columns(2)

with colX:
    st.metric("Rendita 10 anni", f"€ {res['beneficio_10_anni']:,.2f}")

with colY:
    st.metric("Rendita 20 anni", f"€ {res['beneficio_20_anni']:,.2f}")


st.divider()

# =========================================================
# PDF
# =========================================================

st.header("📄 Report Cliente (PDF)")

if st.button("📌 Genera Report PDF"):

    pdf_path = build_pdf(
        cliente,
        res,
        costo,
        consumo,
        base_kwp,
        bonus_kwp,
        resa,
        prezzo_energia,
        rid,
        cer,
        quota,
        autoc_base_perc,
        autoc_bonus_perc,
        incremento,
    )

    with open(pdf_path, "rb") as f:
        st.download_button(
            label="⬇️ Scarica Report PDF",
            data=f,
            file_name=pdf_path,
            mime="application/pdf"
        )

    st.success("PDF generato correttamente!")
