import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
import datetime
import numpy as np

# Configurazione pagina
st.set_page_config(page_title="Cryotech bolla di lavoro", layout="centered")

# Stile personalizzato
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

# Header con logo e nome
col1, col2 = st.columns([0.15, 0.85])
with col1:
    logo = Image.open("logo_cryotech.png")
    st.image(logo, use_column_width=True)
with col2:
    st.markdown("""<div class='cryotech-header'><h1>Cryotech Solutions Srls</h1></div>""", unsafe_allow_html=True)

# Sezione dati principali
numero_intervento = st.text_input("Numero Intervento")
data_intervento = st.date_input("Data Intervento")
cliente = st.text_input("Nome Cliente")
note = st.text_area("Note Aggiuntive")

materiale_list = st.session_state.get("materiale_list", [""])
updated_list = []
for idx, item in enumerate(materiale_list):
    updated_list.append(st.text_input(f"Materiale {idx+1}", item, key=f"mat_{idx}"))
if st.button("Aggiungi Materiale"):
    updated_list.append("")
st.session_state["materiale_list"] = updated_list

# Sezione Operatori, Ore, KM e Calcolo Totale automatico
st.markdown("<div class='section'><h3>Operatori e Tempi</h3>", unsafe_allow_html=True)
operatori_list = st.session_state.get("operatori_list", [])
updated_operatori = []
tot_ore = 0
tot_km = 0
for idx, operatore in enumerate(operatori_list):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nome = st.text_input(f"Operatore {idx+1}", operatore.get("nome", ""), key=f"nome_op_{idx}")
    with col2:
        ore = st.number_input(f"Ore Lavoro {idx+1}", min_value=0.0, step=0.5, key=f"ore_{idx}")
    with col3:
        km = st.number_input(f"KM {idx+1}", min_value=0, step=1, key=f"km_{idx}")
    with col4:
        tempo = round(ore * 60)  # tempo in minuti calcolato automaticamente
        st.text(f"Totale min: {tempo}")
    tot_ore += ore
    tot_km += km
    updated_operatori.append({"nome": nome, "ore": ore, "km": km, "tempo": tempo})
if st.button("Aggiungi Operatore"):
    updated_operatori.append({"nome": "", "ore": 0.0, "km": 0, "tempo": 0})
st.session_state["operatori_list"] = updated_operatori
st.markdown(f"**Totale Ore: {tot_ore} - Totale KM: {tot_km}**")
st.markdown("</div>", unsafe_allow_html=True)

# Sezione Firma
st.markdown("<div class='section'><h3>Firma</h3>", unsafe_allow_html=True)
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

# Funzione PDF completa con tutti i dati
def genera_pdf(numero_intervento, data_intervento, cliente, note, materiali, operatori, tot_ore, tot_km, firma_img):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    try:
        pdf.image("logo_cryotech.png", x=10, y=8, w=33)
    except:
        pass

    pdf.cell(200, 10, txt="Cryotech Solutions Srls", ln=True, align="C")
    pdf.ln(20)

    pdf.cell(200, 10, txt=f"Numero Intervento: {numero_intervento}", ln=True)
    pdf.cell(200, 10, txt=f"Data: {data_intervento}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Materiale Utilizzato:", ln=True)
    for m in materiali:
        pdf.cell(200, 10, txt=f"- {m}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Operatori:", ln=True)
    for op in operatori:
        pdf.multi_cell(0, 10, txt=f"{op['nome']} - Ore: {op['ore']} - KM: {op['km']} - Tempo Totale (minuti): {op['tempo']}")
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Totale Ore: {tot_ore}", ln=True)
    pdf.cell(200, 10, txt=f"Totale KM: {tot_km}", ln=True)
    pdf.ln(10)

    pdf.multi_cell(0, 10, txt=f"Note: {note}")
    pdf.ln(10)

    if firma_img is not None:
        firma_path = "firma.png"
        firma_img.save(firma_path)
        pdf.image(firma_path, x=10, y=pdf.get_y(), w=60)

    output_path = "bolla_lavoro.pdf"
    pdf.output(output_path)
    return output_path

# Bottone Genera PDF completo
if st.button("Genera PDF"):
    materiali_finali = [m for m in st.session_state.get("materiale_list", []) if m.strip() != ""]
    operatori_finali = st.session_state.get("operatori_list", [])
    firma_img = canvas_result.image_data if canvas_result.image_data is not None else None
    if firma_img is not None:
        img = Image.fromarray((firma_img[:, :, :3] * 255).astype(np.uint8))
    else:
        img = None
    path = genera_pdf(numero_intervento, data_intervento, cliente, note, materiali_finali, operatori_finali, tot_ore, tot_km, img)
    with open(path, "rb") as file:
        st.download_button("Scarica PDF", file, file_name="bolla_lavoro.pdf")
