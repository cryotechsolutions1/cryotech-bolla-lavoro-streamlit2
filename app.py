import streamlit as st
from fpdf import FPDF
import datetime
import os

st.title("Cryotech - Bolla di Lavoro")

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

    st.text(f"Viaggio per {nome if nome else 'Operatore ' + str(i+1)}")
    ore_andata = st.number_input(f"Ore Viaggio Andata {i+1}", min_value=0.0, step=0.1, key=f"ore_andata_{i}")
    km_andata = st.number_input(f"Km Viaggio Andata {i+1}", min_value=0, key=f"km_andata_{i}")
    ore_ritorno = st.number_input(f"Ore Viaggio Ritorno {i+1}", min_value=0.0, step=0.1, key=f"ore_ritorno_{i}")
    km_ritorno = st.number_input(f"Km Viaggio Ritorno {i+1}", min_value=0, key=f"km_ritorno_{i}")

    operatori.append({
        "nome": nome,
        "ora_inizio": ora_inizio,
        "ora_fine": ora_fine,
        "pausa": pausa,
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

    materiali.append({
        "materiale": materiale,
        "quantita": quantita
    })

note = st.text_area("Note")
firma_tecnico = st.text_input("Firma Tecnico")
firma_cliente = st.text_input("Firma e Timbro Cliente")

if st.button("Genera PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if os.path.exists("logo.png"):
        pdf.image("logo.png", x=10, y=8, w=30)

    pdf.ln(20)
    pdf.cell(200, 10, txt="Cryotech - Bolla di Lavoro", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"NUMERO: {numero}", ln=True)
    pdf.cell(200, 10, txt=f"DATA: {data.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, txt=f"DATI CLIENTE: {cliente}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, txt="Operatori e Viaggi:", ln=True)
    for op in operatori:
        pdf.multi_cell(0, 10, txt=(
            f"Nome: {op['nome']} - Inizio: {op['ora_inizio']} - Fine: {op['ora_fine']} - Pausa: {op['pausa']} min\n"
            f"Viaggio Andata: {op['ore_andata']} h - {op['km_andata']} km | Ritorno: {op['ore_ritorno']} h - {op['km_ritorno']} km"
        ))

    pdf.ln(10)
    pdf.cell(200, 10, txt="Materiali Utilizzati:", ln=True)
    for mat in materiali:
        pdf.multi_cell(0, 10, txt=f"Materiale: {mat['materiale']} - Quantità: {mat['quantita']}")

    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"NOTE:\n{note}")

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"FIRMA TECNICO: {firma_tecnico}", ln=True)
    pdf.cell(200, 10, txt=f"FIRMA E TIMBRO CLIENTE: {firma_cliente}", ln=True)

    # ✅ CORRETTO: Creazione PDF in formato stringa per Streamlit Cloud
    pdf_data = pdf.output(dest="S").encode("latin-1")

    st.success("PDF generato con successo!")

    st.download_button(
        label="Scarica PDF",
        data=pdf_data,
        file_name="bolla_di_lavoro.pdf",
        mime="application/pdf"
    )
