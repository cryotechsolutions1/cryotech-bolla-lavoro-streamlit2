import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF

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
    logo = Image.open("logo_cryotech.png")  # Assicurati che il logo sia nella stessa cartella
    st.image(logo, use_column_width=True)
with col2:
    st.markdown("""<div class='cryotech-header'><h1>Cryotech Solutions Srls</h1></div>""", unsafe_allow_html=True)

# Sezione Dati Cliente
with st.container():
    st.markdown("<div class='section'><h3>Dati Cliente</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome Cliente")
        indirizzo = st.text_input("Indirizzo")
    with col2:
        telefono = st.text_input("Telefono")
        email = st.text_input("Email")
    st.markdown("</div>", unsafe_allow_html=True)

# Sezione Materiale dinamica
with st.container():
    st.markdown("<div class='section'><h3>Materiale</h3>", unsafe_allow_html=True)
    materiale_list = st.session_state.get("materiale_list", [""])
    updated_list = []
    for idx, item in enumerate(materiale_list):
        updated_list.append(st.text_input(f"Materiale {idx+1}", item, key=f"mat_{idx}"))
    if st.button("Aggiungi Materiale"):
        updated_list.append("")
    st.session_state["materiale_list"] = updated_list
    st.markdown("</div>", unsafe_allow_html=True)

# Sezione Firma tracciabile
with st.container():
    st.markdown("<div class='section'><h3>Firma</h3>", unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",
        stroke_width=2,
        stroke_color="#000000",
        background_color="#FFFFFF",
        update_streamlit=True,
        height=150,
        drawing_mode="freedraw",
        key="canvas",
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Funzione per generare PDF
def genera_pdf(cliente, indirizzo, telefono, email, materiali, firma_img):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Cryotech Solutions Srls", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt="Bolla di lavoro", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Indirizzo: {indirizzo}", ln=True)
    pdf.cell(200, 10, txt=f"Telefono: {telefono}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Materiale:", ln=True)
    for m in materiali:
        pdf.cell(200, 10, txt=f"- {m}", ln=True)
    pdf.ln(10)
    if firma_img is not None:
        firma_path = "firma.png"
        firma_img.save(firma_path)
        pdf.image(firma_path, x=10, y=pdf.get_y(), w=60)
    output_path = "bolla_lavoro.pdf"
    pdf.output(output_path)
    return output_path

# Bottone Genera PDF
if st.button("Genera PDF"):
    materiali_finali = [m for m in st.session_state.get("materiale_list", []) if m.strip() != ""]
    firma_img = canvas_result.image_data if canvas_result.image_data is not None else None
    if firma_img is not None:
        from PIL import Image
        import numpy as np
        img = Image.fromarray((firma_img[:, :, :3] * 255).astype(np.uint8))
    else:
        img = None
    path = genera_pdf(cliente, indirizzo, telefono, email, materiali_finali, img)
    with open(path, "rb") as file:
        st.download_button("Scarica PDF", file, file_name="bolla_lavoro.pdf")
