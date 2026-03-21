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
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background-color: #f8f7fb;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 28px !important;
    font-weight: 600 !important;
    color: #1e1b2e !important;
}
h2 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1e1b2e !important;
}

p, span, label, .stMarkdown, div {
    font-size: 15px !important;
    color: #1e1b2e !important;
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #6b5f99 !important;
}

.stTextInput input, .stNumberInput input {
    background-color: #ffffff !important;
    border: 1px solid #e8e5f0 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #1e1b2e !important;
    padding: 10px 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.12) !important;
}

.stButton > button {
    background-color: #7c3aed !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 10px 28px !important;
}
.stButton > button:hover {
    background-color: #6d28d9 !important;
    box-shadow: 0 4px 12px rgba(124,58,237,0.25) !important;
}

.stDownloadButton > button {
    background-color: #7c3aed !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #7c3aed !important;
}
[data-testid="stMetricLabel"] {
    font-size: 14px !important;
    color: #6b5f99 !important;
    font-weight: 500 !important;
}

.stAlert { border-radius: 10px !important; font-size: 15px !important; }

hr { border-color: #e8e5f0 !important; margin: 28px 0 !important; }

.section-hdr {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 36px 0 20px 0;
}
.section-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.section-title {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1e1b2e !important;
    margin: 0 !important;
}
.section-sub {
    font-size: 14px !important;
    color: #9b8fc7 !important;
    margin: 2px 0 0 0 !important;
}

.metric-card {
    background: #ffffff;
    border: 1px solid #e8e5f0;
    border-radius: 12px;
    padding: 22px;
    text-align: center;
}
.metric-card .mc-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 24px;
    font-weight: 600;
    color: #7c3aed;
    margin-bottom: 6px;
}
.metric-card .mc-label {
    font-size: 14px;
    color: #6b5f99;
    font-weight: 500;
}
.metric-card.green .mc-value { color: #16a34a; }
.metric-card.amber .mc-value { color: #d97706; }

.highlight-box {
    background: rgba(124,58,237,0.06);
    border: 1px solid rgba(124,58,237,0.12);
    border-radius: 12px;
    padding: 22px 28px;
    margin: 16px 0;
}
.highlight-box .hb-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 600;
    color: #7c3aed;
}
.highlight-box .hb-label {
    font-size: 15px;
    color: #6b5f99;
    margin-top: 6px;
}

.highlight-green {
    background: rgba(22,163,74,0.06);
    border: 1px solid rgba(22,163,74,0.12);
    border-radius: 12px;
    padding: 22px 28px;
    margin: 16px 0;
}
.highlight-green .hb-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 600;
    color: #16a34a;
}
.highlight-green .hb-label {
    font-size: 15px;
    color: #166534;
    margin-top: 6px;
}

.row-widget.stHorizontalBlock { gap: 16px; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================
def section(icon, color, title, subtitle=""):
    sub_html = f'<div class="section-sub">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
    <div class="section-hdr">
        <div class="section-icon" style="background:{color}20;color:{color}">{icon}</div>
        <div>
            <div class="section-title">{title}</div>
            {sub_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, style=""):
    st.markdown(f"""
    <div class="metric-card {style}">
        <div class="mc-value">{value}</div>
        <div class="mc-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div style="margin-bottom:8px">
    <h1 style="font-size:28px;font-weight:600;margin:0 0 6px;color:#1e1b2e">Configuratore CER</h1>
    <p style="font-size:15px;color:#9b8fc7;margin:0">Simulazione vantaggi economici — Next S.r.l.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# DATI CLIENTE E IMPIANTO
# =========================================================
section("👤", "#7c3aed", "Dati cliente e impianto", "Inserisci i dati del cliente e la configurazione dell'impianto")

col1, col2, col3 = st.columns(3)

with col1:
    cliente = st.text_input("Nome cliente", value="Cliente Demo")
    consumo = st.number_input("Consumo annuo (kWh)", min_value=500, max_value=50000, value=5400, step=1)

with col2:
    base_kwp = st.number_input("Potenza impianto base (kWp)", value=6.56, step=0.01)
    bonus_kwp = st.number_input("Potenza impianto upgrade (kWp)", value=9.02, step=0.01)

with col3:
    costo = st.number_input("Costo impianto (€)", value=13560.0, step=50.0)
    autoc_base_perc = st.number_input("Autoconsumo base %", value=0.80, step=0.01)

autoc_bonus_perc = quota_copertura_from_kwp(bonus_kwp)
st.markdown(f'<p style="font-size:14px;color:#16a34a;margin-top:4px">Copertura calcolata automaticamente: <strong>{autoc_bonus_perc * 100:.1f}%</strong></p>', unsafe_allow_html=True)

st.divider()

# =========================================================
# PARAMETRI ECONOMICI
# =========================================================
section("⚙️", "#d97706", "Parametri economici", "Configura i parametri della simulazione")

col4, col5, col6 = st.columns(3)

with col4:
    prezzo_energia = st.number_input("Prezzo energia evitata €/kWh", value=0.30, step=0.01)
    incremento = st.number_input("Incremento annuo costo energia (%)", min_value=0.0, max_value=15.0, value=3.0, step=0.5) / 100

with col5:
    rid = st.number_input("RID €/kWh", value=0.137, step=0.001)
    cer = st.number_input("CER €/kWh", value=0.06, step=0.005)

with col6:
    quota = st.number_input("Quota energia condivisa (%)", value=50, step=5) / 100
    resa = st.number_input("Resa zona (kWh/kWp)", value=1200, step=50)

st.divider()

# =========================================================
# CALCOLO
# =========================================================
res = compute_benefits(
    consumo_kwh=consumo, base_kwp=base_kwp, bonus_kwp=bonus_kwp,
    prezzo_energia=prezzo_energia, rid_eur_kwh=rid, cer_eur_kwh=cer,
    quota_condivisa=quota, costo_impianto=costo, resa_kwh_kwp=resa,
    autoc_base_perc=autoc_base_perc, autoc_bonus_perc=autoc_bonus_perc,
    incremento_prezzo_annuo=incremento,
)

# =========================================================
# RISULTATI — ENERGIA
# =========================================================
section("⚡", "#7c3aed", "Produzione e copertura", "Dati energetici dell'impianto")

c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("Produzione impianto", f"{res['produzione_bonus']:,.0f} kWh")
with c2: metric_card("Energia coperta", f"{res['autoconsumo_bonus']:,.0f} kWh")
with c3: metric_card("Immessa in rete", f"{res['energia_immessa']:,.0f} kWh")
with c4: metric_card("Extra vs base", f"{res['delta_autoconsumo']:,.0f} kWh", "amber")

st.divider()

# =========================================================
# BENEFICI ANNUI
# =========================================================
section("💰", "#16a34a", "Benefici economici annui", "Dettaglio dei vantaggi economici anno per anno")

c5, c6, c7 = st.columns(3)
with c5: metric_card("Extra autoconsumo", f"€ {res['vantaggio_extra_autoconsumo']:,.2f}")
with c6: metric_card("RID annuo", f"€ {res['rid_annuo']:,.2f}")
with c7: metric_card("CER incentivo", f"€ {res['cer_prudente']:,.2f}")

st.markdown("")

c8, c9 = st.columns(2)
with c8: metric_card("Totale benefici annui", f"€ {res['totale_benefici_annui']:,.2f}")
with c9: metric_card("Detrazione fiscale annua", f"€ {res['detrazione_annua']:,.2f}")

st.markdown(f"""
<div class="highlight-box">
    <div class="hb-value">€ {res['beneficio_annuale_totale']:,.2f}</div>
    <div class="hb-label">Rendita Energetica Attiva — beneficio totale annuo</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================================================
# RISPARMIO BOLLETTA
# =========================================================
section("📊", "#2563eb", "Risparmio in bolletta")

c11, c12 = st.columns(2)
with c11: metric_card("Risparmio bolletta annuo", f"€ {res['risparmio_bolletta']:,.2f}")
with c12: metric_card("Risparmio complessivo annuo", f"€ {res['risparmio_complessivo_annuo']:,.2f}", "green")

st.divider()

# =========================================================
# RENDITA NEL TEMPO
# =========================================================
section("📈", "#7c3aed", "Rendita nel tempo", "Proiezione a 10 e 20 anni")

c13, c14 = st.columns(2)
with c13:
    st.markdown(f"""
    <div class="highlight-box">
        <div class="hb-value">€ {res['beneficio_10_anni']:,.2f}</div>
        <div class="hb-label">Rendita Energetica Attiva — 10 anni</div>
    </div>
    """, unsafe_allow_html=True)
with c14:
    st.markdown(f"""
    <div class="highlight-box">
        <div class="hb-value">€ {res['beneficio_20_anni']:,.2f}</div>
        <div class="hb-label">Rendita Energetica Attiva — 20 anni</div>
    </div>
    """, unsafe_allow_html=True)

c15, c16 = st.columns(2)
with c15:
    st.markdown(f"""
    <div class="highlight-green">
        <div class="hb-value">€ {res['risparmio_complessivo_10']:,.2f}</div>
        <div class="hb-label">Risparmio complessivo — 10 anni</div>
    </div>
    """, unsafe_allow_html=True)
with c16:
    st.markdown(f"""
    <div class="highlight-green">
        <div class="hb-value">€ {res['risparmio_complessivo_20']:,.2f}</div>
        <div class="hb-label">Risparmio complessivo — 20 anni</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# PDF
# =========================================================
section("📄", "#6b5f99", "Report PDF", "Genera il report completo per il cliente")

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
