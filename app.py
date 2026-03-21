# app.py
import streamlit as st
from calculator import compute_benefits, quota_copertura_from_kwp
from pdf_report import build_pdf

st.set_page_config(
    page_title="Configuratore CER — Next S.r.l.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS — Allineato al portale Next
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Reset base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* Background */
.stApp {
    background-color: #f8f7fb;
}

/* Header area */
header[data-testid="stHeader"] {
    background-color: #f8f7fb;
}

/* Hide default hamburger and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2d2843;
}
[data-testid="stSidebar"] * {
    color: #c4b5fd !important;
}

/* Main title style */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #1e1b2e !important;
    letter-spacing: -0.3px;
}

h2, .stSubheader {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #1e1b2e !important;
}

h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #6b5f99 !important;
}

/* Body text */
p, span, label, .stMarkdown {
    font-size: 13px !important;
    color: #1e1b2e !important;
}

/* Input labels */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #6b5f99 !important;
    text-transform: none;
}

/* Input fields */
.stTextInput input, .stNumberInput input {
    background-color: #faf9fd !important;
    border: 1px solid #e8e5f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    color: #1e1b2e !important;
    padding: 8px 12px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 1px #7c3aed !important;
}

/* Buttons */
.stButton > button {
    background-color: #7c3aed !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 24px !important;
    transition: background-color 0.15s;
}
.stButton > button:hover {
    background-color: #6d28d9 !important;
}

/* Download button */
.stDownloadButton > button {
    background-color: #7c3aed !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    color: #7c3aed !important;
}
[data-testid="stMetricLabel"] {
    font-size: 12px !important;
    color: #6b5f99 !important;
    font-weight: 500 !important;
}

/* Success/Info/Warning boxes */
.stAlert {
    border-radius: 8px !important;
    font-size: 13px !important;
}
[data-testid="stAlert"] {
    border-radius: 8px !important;
}

/* Success box */
.element-container .stSuccess {
    background-color: rgba(22, 163, 74, 0.06) !important;
    border: 1px solid rgba(22, 163, 74, 0.15) !important;
    color: #166534 !important;
}

/* Info box */
.element-container .stInfo {
    background-color: rgba(124, 58, 237, 0.06) !important;
    border: 1px solid rgba(124, 58, 237, 0.15) !important;
    color: #5b21b6 !important;
}

/* Divider */
hr {
    border-color: #e8e5f0 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0px;
    border-bottom: 1px solid #e8e5f0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #9b8fc7 !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #7c3aed !important;
    border-bottom-color: #7c3aed !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6b5f99 !important;
    background-color: #faf9fd !important;
    border: 1px solid #e8e5f0 !important;
    border-radius: 8px !important;
}

/* Card-like containers */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #e8e5f0 !important;
    border-radius: 10px !important;
    background-color: #ffffff !important;
    padding: 20px !important;
}

/* Column gaps */
.row-widget.stHorizontalBlock {
    gap: 16px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div style="margin-bottom:24px">
    <h1 style="font-size:22px;font-weight:600;margin:0 0 4px;color:#1e1b2e">Analisi Rendita Energetica Attiva</h1>
    <p style="font-size:13px;color:#9b8fc7;margin:0">Configuratore commerciale Next S.r.l. — Simulazione vantaggi economici</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# DATI CLIENTE — TAB LAYOUT
# =========================================================

tab1, tab2, tab3 = st.tabs(["Dati cliente", "Parametri economici", "Risultati"])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        cliente = st.text_input("Nome cliente", value="Cliente Demo")
        consumo = st.number_input(
            "Consumo annuo (kWh)",
            min_value=500, max_value=50000, value=5400, step=1
        )

    with col2:
        base_kwp = st.number_input("Potenza impianto base (kWp)", value=6.56, step=0.01)
        bonus_kwp = st.number_input("Potenza impianto upgrade (kWp)", value=9.02, step=0.01)

    with col3:
        costo = st.number_input("Costo impianto (€)", value=13560.0, step=50.0)
        autoc_base_perc = st.number_input("Autoconsumo base %", value=0.80, step=0.01)

    autoc_bonus_perc = quota_copertura_from_kwp(bonus_kwp)
    st.markdown(
        f'<p style="font-size:12px;color:#16a34a;margin-top:8px">'
        f'Copertura calcolata automaticamente: <strong>{autoc_bonus_perc * 100:.1f}%</strong></p>',
        unsafe_allow_html=True
    )

with tab2:
    col4, col5, col6 = st.columns(3)

    with col4:
        prezzo_energia = st.number_input("Prezzo energia evitata €/kWh", value=0.30, step=0.01)
        incremento = st.number_input(
            "Incremento annuo costo energia (%)",
            min_value=0.0, max_value=15.0, value=3.0, step=0.5
        ) / 100

    with col5:
        rid = st.number_input("RID €/kWh", value=0.137, step=0.001)
        cer = st.number_input("CER €/kWh", value=0.06, step=0.005)

    with col6:
        quota = st.number_input("Quota energia condivisa (%)", value=50, step=5) / 100
        resa = st.number_input("Resa zona (kWh/kWp)", value=1200, step=50)

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

with tab3:

    # --- Energia ---
    st.markdown('<p style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#9b8fc7;margin-bottom:12px">Energia</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Produzione impianto", f"{res['produzione_bonus']:,.0f} kWh")
    c2.metric("Energia coperta", f"{res['autoconsumo_bonus']:,.0f} kWh")
    c3.metric("Immessa in rete", f"{res['energia_immessa']:,.0f} kWh")
    c4.metric("Extra vs base", f"{res['delta_autoconsumo']:,.0f} kWh")

    st.divider()

    # --- Benefici annui ---
    st.markdown('<p style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#9b8fc7;margin-bottom:12px">Benefici economici annui</p>', unsafe_allow_html=True)

    c5, c6, c7 = st.columns(3)
    c5.metric("Extra autoconsumo", f"€ {res['vantaggio_extra_autoconsumo']:,.2f}")
    c6.metric("RID annuo", f"€ {res['rid_annuo']:,.2f}")
    c7.metric("CER incentivo", f"€ {res['cer_prudente']:,.2f}")

    c8, c9, c10 = st.columns(3)
    c8.metric("Totale benefici annui", f"€ {res['totale_benefici_annui']:,.2f}")
    c9.metric("Detrazione fiscale annua", f"€ {res['detrazione_annua']:,.2f}")
    c10.metric("Rendita Energetica Attiva", f"€ {res['beneficio_annuale_totale']:,.2f}")

    st.divider()

    # --- Risparmio bolletta ---
    st.markdown('<p style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#9b8fc7;margin-bottom:12px">Risparmio in bolletta</p>', unsafe_allow_html=True)

    c11, c12 = st.columns(2)
    c11.metric("Risparmio bolletta annuo", f"€ {res['risparmio_bolletta']:,.2f}")
    c12.metric("Risparmio complessivo annuo", f"€ {res['risparmio_complessivo_annuo']:,.2f}")

    st.divider()

    # --- Orizzonte temporale ---
    st.markdown('<p style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#9b8fc7;margin-bottom:12px">Rendita nel tempo</p>', unsafe_allow_html=True)

    c13, c14 = st.columns(2)
    c13.metric("Rendita 10 anni", f"€ {res['beneficio_10_anni']:,.2f}")
    c14.metric("Rendita 20 anni", f"€ {res['beneficio_20_anni']:,.2f}")

    c15, c16 = st.columns(2)
    c15.metric("Risparmio complessivo 10 anni", f"€ {res['risparmio_complessivo_10']:,.2f}")
    c16.metric("Risparmio complessivo 20 anni", f"€ {res['risparmio_complessivo_20']:,.2f}")

    st.divider()

    # --- PDF ---
    st.markdown('<p style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#9b8fc7;margin-bottom:12px">Report PDF</p>', unsafe_allow_html=True)

    if st.button("Genera Report PDF"):
        pdf_path = build_pdf(
            cliente, res, costo, consumo, base_kwp, bonus_kwp,
            resa, prezzo_energia, rid, cer, quota,
            autoc_base_perc, autoc_bonus_perc, incremento,
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Scarica Report PDF",
                data=f,
                file_name=pdf_path,
                mime="application/pdf"
            )
        st.success("PDF generato correttamente.")
