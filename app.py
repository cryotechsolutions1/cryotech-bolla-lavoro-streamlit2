import streamlit as st
from fpdf import FPDF
import datetime
import os
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io

st.title("Cryotech Solutions Srls - Bolla di Lavoro")

numero = st.text_input("Numero")
data = st.date_input("Data", datetime.date.today())
cliente = st.text_input("Dati Cliente")

st.header("Operatori e Viaggi")

num_operatori = st.number_input("Quante persone hanno lavorato?", min_value=1, step=1, value=1)
operatori = []

for i in range(int(num_operatori)):
    st.subheader(f"Operatore {i+1}")
    nome = st.text_input(f"Nome e Cognome {i+1}", key=f"nome_{i}")
    ora_inizio = st.time_input(f"Ora Inizio {i+1}", key=f"start_{i}")
    ora_fine = st.time_input(f"Ora Fine {i+1}", key=f"end_{i}")
    pausa = st.number_input(f"Pausa [min] {i+1}", min_value=0, key=f"pausa_{i}")

    ore_lavorate = (datetime.datetime.combine(datetime.date.today(), ora_fine) - datetime.datetime.combine(datetime.date.today(), ora_inizio)).seconds / 3600
    ore_totali = max(0, ore_lavorate - (pausa / 60))

    st.text(f"Ore totali lavorate: {ore_totali:.2f}")

    st.text(f"Viaggio per {nome if nome else 'Operatore ' + str(i+1)}")
    ore_andata = st.number_input(f"Ore Viaggio Andata {i+1}", min_value=0.0, step=0.1, key=f"ore_andata_{i}")
    km_andata = st.number_input(f"Km Viaggio Andata {i+1}", min_value=0, key=f"km_andata_{i}")
    ore_ritorno = st.number_input(f"Ore Viaggio Ritorno {i+1}", min_value=0.0, step=0.1, key=f"ore_ritorno_{i}")
    km_ritorno = st.number_input(f"Km Viaggio Ritorno {i+1}", min_value=0, key=f"km_ritorno_{i}")

    km_totali = km_andata + km_ritorno
    ore_viaggio_totali = ore_andata + ore_ritorno

    st.text(f"Km totali: {km_totali} km, Ore viaggio totali: {ore_viaggio_totali:.2f} h")

    operatori.append({
        "nome": nome,
        "ora_inizio": ora_inizio,
        "ora_fine": ora_fine,
        "pausa": pausa,
        "ore_totali": ore_totali,
        "ore_andata": ore_andata,
        "km_andata": km_andata,
        "ore_ritorno": ore_ritorno,
        "km_ritorno": km_ritorno
    })

st.header("Materiale Utilizzato")

num_materiali = st.number_input("Quanti materiali vuoi inserire?", min_value=1, step=1, value=1)
materiali = []

for i in range(int(num_materiali)):
    materiale = st.text_input(f"Materiale {i+1}", key=f"materiale_{i}")
    quantita = st.text_input(f"Quantità {i+1}", key=f"quantita_{i}")
    materiali.append({"materiale": materiale, "quantita": quantita})

note = st.text_area("Note")

st.header("Firma Tecnico")
uploaded_firma_tecnico = st.file_uploader("Carica immagine firma tecnico", type=["png", "jpg"], key="upload_tecnico")
st.text("Oppure firma tracciata sotto:")
canvas_tecnico = st_canvas(height=150, width=300, drawing_mode="freedraw", stroke_width=2, key="canvas_firma_tecnico")

st.header("Firma Cliente")
uploaded_firma_cliente = st.file_uploader("Carica immagine firma cliente", type=["png", "jpg"], key="upload_cliente")
st.text("Oppure firma tracciata sotto:")
canvas_cliente = st_canvas(height=150, width=300, drawing_mode="freedraw", stroke_width=2, key="canvas_firma_cliente")

if st.button("Genera PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=10, y=8, w=40)

    pdf.ln(25)
    pdf.cell(200, 10, txt="Cryotech Solutions Srls - Bolla di Lavoro", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"NUMERO: {numero}   DATA: {data.strftime('%d/%m/%Y')}", ln=True)
    pdf.multi_cell(0, 10, txt=f"DATI CLIENTE: {cliente}")

    pdf.ln(5)
    pdf.cell(200, 10, txt="Operatori e Viaggi:", ln=True)
    for op in operatori:
        pdf.multi_cell(0, 10, txt=(
            f"{op['nome']} - Inizio: {op['ora_inizio']} - Fine: {op['ora_fine']} - Pausa: {op['pausa']} min - Ore Lavorate: {op['ore_totali']:.2f} h\n"
            f"Viaggio Andata: {op['ore_andata']} h / {op['km_andata']} km | Ritorno: {op['ore_ritorno']} h / {op['km_ritorno']} km"
        ))

    pdf.ln(5)
    pdf.cell(200, 10, txt="Materiali Utilizzati:", ln=True)
    for mat in materiali:
        pdf.cell(200, 10, txt=f"{mat['materiale']} - Quantità: {mat['quantita']}", ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"NOTE:\n{note}")

    pdf.ln(10)
    y_position = pdf.get_y()

    if uploaded_firma_tecnico:
        firma_tecnico_path = "firma_tecnico.png"
        Image.open(uploaded_firma_tecnico).save(firma_tecnico_path)
        pdf.image(firma_tecnico_path, x=10, y=y_position, w=40)
        os.remove(firma_tecnico_path)
    elif canvas_tecnico.image_data is not None:
        img = Image.fromarray((canvas_tecnico.image_data[:, :, :3] * 255).astype('uint8'))
        firma_tecnico_path = "firma_tecnico.png"
        img.save(firma_tecnico_path)
        pdf.image(firma_tecnico_path, x=10, y=y_position, w=40)
        os.remove(firma_tecnico_path)

    if uploaded_firma_cliente:
        firma_cliente_path = "firma_cliente.png"
        Image.open(uploaded_firma_cliente).save(firma_cliente_path)
        pdf.image(firma_cliente_path, x=70, y=y_position, w=40)
        os.remove(firma_cliente_path)
    elif canvas_cliente.image_data is not None:
        img = Image.fromarray((canvas_cliente.image_data[:, :, :3] * 255).astype('uint8'))
        firma_cliente_path = "firma_cliente.png"
        img.save(firma_cliente_path)
        pdf.image(firma_cliente_path, x=70, y=y_position, w=40)
        os.remove(firma_cliente_path)

    pdf_data = pdf.output(dest="S").encode("latin-1")

    st.success("PDF generato con successo!")
    st.download_button("Scarica PDF", data=pdf_data, file_name="bolla_di_lavoro.pdf", mime="application/pdf")
