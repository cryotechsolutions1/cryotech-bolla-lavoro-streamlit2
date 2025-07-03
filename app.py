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

# Tabella Operatori: Nome - Ora Inizio - Ora Fine - Pausa - Totale
st.markdown("<div class='section'><h3>Operatori e Tempi</h3>", unsafe_allow_html=True)
operatori_list = st.session_state.get("operatori_list", [])
updated_operatori = []
tot_ore_lavoro = 0
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
        st.text(f"Totale min: {totale}")
    tot_ore_lavoro += totale
    updated_operatori.append({"nome": nome, "inizio": ora_inizio, "fine": ora_fine, "pausa": pausa, "totale": totale})
if st.button("Aggiungi Operatore"):
    updated_operatori.append({"nome": "", "inizio": None, "fine": None, "pausa": 0, "totale": 0})
st.session_state["operatori_list"] = updated_operatori
st.markdown(f"**Totale Minuti Lavoro: {tot_ore_lavoro}**")
st.markdown("</div>", unsafe_allow_html=True)

# Viaggio Andata/Ritorno KM e Ore
st.markdown("<div class='section'><h3>Viaggi</h3>", unsafe_allow_html=True)
ore_andata = st.number_input("Ore Viaggio Andata", min_value=0.0, step=0.5)
km_andata = st.number_input("KM Viaggio Andata", min_value=0, step=1)
ore_ritorno = st.number_input("Ore Viaggio Ritorno", min_value=0.0, step=0.5)
km_ritorno = st.number_input("KM Viaggio Ritorno", min_value=0, step=1)
tot_viaggio_ore = ore_andata + ore_ritorno
tot_viaggio_km = km_andata + km_ritorno
st.text(f"Totale Ore Viaggio: {tot_viaggio_ore} | Totale KM Viaggio: {tot_viaggio_km}")
st.markdown("</div>", unsafe_allow_html=True)

# Materiale con Quantità
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

# Note Finali
note = st.text_area("NOTE")

# Firma Tecnico e Cliente
st.markdown("<div class='section'><h3>Firma Tecnico / Cliente</h3>", unsafe_allow_html=True)
canvas_result = st_canvas(
    fill_color="#FFFFFF",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    update_streamlit=True,
    height=150,
    drawing_mode="freedraw",
    key="canvas",
)
st.markdown("</div>", unsafe_allow_html=True)

# Funzione Genera PDF

def genera_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    try:
        pdf.image("logo_cryotech.png", x=10, y=8, w=33)
    except:
        pass
    pdf.cell(200, 10, txt="Cryotech Solutions Srls", ln=True, align="C")
    pdf.ln(15)
    pdf.cell(200, 10, txt=f"Numero: {numero_intervento}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {data_intervento}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Lavorazioni Eseguite:", ln=True)
    pdf.multi_cell(0, 10, lavorazioni)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Operatori:", ln=True)
    for op in updated_operatori:
        pdf.multi_cell(0, 10, txt=f"{op['nome']} - Inizio: {op['inizio']} - Fine: {op['fine']} - Pausa: {op['pausa']} min - Totale: {op['totale']} min")
    pdf.ln(2)
    pdf.cell(200, 10, txt=f"Totale Minuti Lavoro: {tot_ore_lavoro}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Viaggio Andata: {ore_andata} ore - {km_andata} km", ln=True)
    pdf.cell(200, 10, txt=f"Viaggio Ritorno: {ore_ritorno} ore - {km_ritorno} km", ln=True)
    pdf.cell(200, 10, txt=f"Totale Viaggio: {tot_viaggio_ore} ore - {tot_viaggio_km} km", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Materiale Utilizzato:", ln=True)
    for m in updated_list:
        pdf.cell(200, 10, txt=f"{m['descrizione']} - Quantità: {m['quantita']}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Note:", ln=True)
    pdf.multi_cell(0, 10, note)
    pdf.ln(10)
    if canvas_result.image_data is not None:
        firma_img = Image.fromarray((canvas_result.image_data[:, :, :3] * 255).astype(np.uint8))
        firma_img.save("firma.png")
        pdf.image("firma.png", x=10, y=pdf.get_y(), w=60)
    pdf.output("bolla_lavoro.pdf")

# Bottone Download PDF
if st.button("Genera PDF"):
    genera_pdf()
    with open("bolla_lavoro.pdf", "rb") as file:
        st.download_button("Scarica PDF", file, file_name="bolla_lavoro.pdf")
