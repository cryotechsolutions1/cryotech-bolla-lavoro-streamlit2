import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
import datetime
import numpy as np

st.set_page_config(page_title="Cryotech bolla di lavoro", layout="centered")

# Stile grafico
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.cryotech-header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px 0 20px 0;
    border-bottom: 2px solid #e0e0e0;
    margin-bottom: 25px;
}
.cryotech-header img {
    height: 60px;
}
.cryotech-header h1 {
    color: #0a58ca;
    font-size: 28px;
    margin: 0;
}
.section {
    background: #fff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 25px;
}
.stButton button {
    background-color: #0a58ca;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Header con logo
col1, col2 = st.columns([0.15, 0.85])
with col1:
    logo = Image.open("logo_cryotech.png")
    st.image(logo, use_container_width=True)
with col2:
    st.markdown("""<div class='cryotech-header'><h1>Cryotech Solutions Srls</h1></div>""", unsafe_allow_html=True)

# Numero e Data
numero_intervento = st.text_input("NUMERO INTERVENTO")
data_intervento = st.date_input("DATA")

# Dati Cliente
cliente = st.text_input("DATI CLIENTE")

# Lavorazioni Eseguite
st.markdown("<div class='section'><h3>LAVORAZIONI ESEGUITE</h3>", unsafe_allow_html=True)
lavorazioni = st.text_area("Descrizione Lavorazioni")
st.markdown("</div>", unsafe_allow_html=True)

# Manodopera Tecnico
st.markdown("<div class='section'><h3>Manodopera Tecnico</h3>", unsafe_allow_html=True)
operatori_list = st.session_state.get("operatori_list", [])
updated_operatori = []
for idx, op in enumerate(operatori_list):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        nome = st.text_input(f"Nome {idx+1}", op.get("nome", ""), key=f"nome_{idx}")
    with col2:
        ora_inizio = st.time_input(f"Ora Inizio {idx+1}", key=f"inizio_{idx}")
    with col3:
        ora_fine = st.time_input(f"Ora Fine {idx+1}", key=f"fine_{idx}")
    with col4:
        pausa = st.number_input(f"Pausa (min) {idx+1}", min_value=0, step=5, key=f"pausa_{idx}")
    with col5:
        totale = 0
        if ora_inizio and ora_fine:
            delta = datetime.datetime.combine(datetime.date.today(), ora_fine) - datetime.datetime.combine(datetime.date.today(), ora_inizio)
            totale = max(0, (delta.total_seconds() / 60) - pausa)
        st.text(f"Totale ore: {totale / 60:.2f}")
    updated_operatori.append({"nome": nome, "inizio": ora_inizio, "fine": ora_fine, "pausa": pausa, "totale": totale})
if st.button("Aggiungi Tecnico"):
    updated_operatori.append({"nome": "", "inizio": None, "fine": None, "pausa": 0, "totale": 0})
st.session_state["operatori_list"] = updated_operatori
st.markdown("</div>", unsafe_allow_html=True)

# Viaggio
st.markdown("<div class='section'><h3>Viaggio</h3>", unsafe_allow_html=True)
viaggi_list = st.session_state.get("viaggi_list", [])
updated_viaggi = []
for idx, viaggio in enumerate(viaggi_list):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        nome = st.text_input(f"Tecnico Viaggio {idx+1}", viaggio.get("nome", ""), key=f"viaggio_nome_{idx}")
    with col2:
        ore_andata = st.number_input(f"Ore Andata {idx+1}", min_value=0.0, step=0.5, key=f"ore_andata_{idx}")
    with col3:
        km_andata = st.number_input(f"KM Andata {idx+1}", min_value=0, step=1, key=f"km_andata_{idx}")
    with col4:
        ore_ritorno = st.number_input(f"Ore Ritorno {idx+1}", min_value=0.0, step=0.5, key=f"ore_ritorno_{idx}")
    with col5:
        km_ritorno = st.number_input(f"KM Ritorno {idx+1}", min_value=0, step=1, key=f"km_ritorno_{idx}")
    updated_viaggi.append({"nome": nome, "ore_andata": ore_andata, "km_andata": km_andata, "ore_ritorno": ore_ritorno, "km_ritorno": km_ritorno})
if st.button("Aggiungi Viaggio"):
    updated_viaggi.append({"nome": "", "ore_andata": 0.0, "km_andata": 0, "ore_ritorno": 0.0, "km_ritorno": 0})
st.session_state["viaggi_list"] = updated_viaggi
st.markdown("</div>", unsafe_allow_html=True)

# Materiale Utilizzato
st.markdown("<div class='section'><h3>Materiale Utilizzato</h3>", unsafe_allow_html=True)
materiale_list = st.session_state.get("materiale_list", [])
updated_list = []
for idx, item in enumerate(materiale_list):
    col1, col2 = st.columns(2)
    with col1:
        descrizione = st.text_input(f"Materiale {idx+1}", item.get("descrizione", ""), key=f"mat_desc_{idx}")
    with col2:
        quantita = st.number_input(f"Quantità {idx+1}", min_value=0, step=1, key=f"mat_quant_{idx}")
    updated_list.append({"descrizione": descrizione, "quantita": quantita})
if st.button("Aggiungi Materiale"):
    updated_list.append({"descrizione": "", "quantita": 0})
st.session_state["materiale_list"] = updated_list
st.markdown("</div>", unsafe_allow_html=True)

# Note
note = st.text_area("NOTE")

# Firma Tecnico / Cliente
st.markdown("<div class='section'><h3>Firma Tecnico / Cliente</h3>", unsafe_allow_html=True)
canvas_result = st_canvas(
    fill_color=None,
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    update_streamlit=True,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)
st.markdown("</div>", unsafe_allow_html=True)

# Funzione genera PDF
def genera_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    try:
        logo = Image.open("logo_cryotech.png")
        logo_path = "temp_logo.png"
        logo.save(logo_path)
        pdf.image(logo_path, x=10, y=8, w=33)
        pdf.set_font("Arial", style="B", size=14)
        pdf.set_xy(120, 8)
        pdf.set_font("Arial", style="B", size=10)
        pdf.multi_cell(80, 6, txt=f"NUMERO: {numero_intervento}\nDATA: {data_intervento.strftime('%d/%m/%Y')}\nCLIENTE: {cliente}", align="R")
    except:
        pass

    pdf.ln(5)
    pdf.rect(10, pdf.get_y(), 190, 20)
    pdf.cell(200, 10, txt="Lavorazioni Eseguite:", ln=True)
    pdf.multi_cell(0, 10, lavorazioni)
    pdf.ln(5)
    pdf.rect(10, pdf.get_y(), 190, 10)
    pdf.cell(200, 10, txt="Manodopera Tecnico:", ln=True)
    for op in updated_operatori:
        pdf.multi_cell(0, 10, txt=f"{op['nome']} - Inizio: {op['inizio']} - Fine: {op['fine']} - Pausa: {op['pausa']} min - Totale: {op['totale'] / 60:.2f} ore")
    pdf.ln(2)

    pdf.ln(5)
    pdf.rect(10, pdf.get_y(), 190, 10)
    pdf.cell(200, 10, txt="Viaggio:", ln=True)
    for viaggio in updated_viaggi:
        tot_viaggio_ore = viaggio['ore_andata'] + viaggio['ore_rit
