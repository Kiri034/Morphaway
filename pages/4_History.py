# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import json

from utils.data_manager import DataManager
from utils.style import set_background_color

with st.sidebar:
    username = st.session_state.get("username")
    if username:
        st.markdown(f"**Eingeloggt als:** {username}")

# Hintergrundfarbe & Bild nur rechts
set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")

# Logo anzeigen
st.image("https://raw.githubusercontent.com/Kiri034/Morphaway/bd399c4a2b974d03fc9117a45bd700e447c0a61b/Bilder/Logo.png", width=320)

st.title("🔍 History")

user = st.session_state.get("username")
if user:
    history_directory = os.path.join("history_exports", user)
else:
    history_directory = "history_exports"

if not os.path.exists(history_directory):
    os.makedirs(history_directory)

# Alle gespeicherten JSON-Dateien auslesen
files = [f for f in os.listdir(history_directory) if f.endswith(".json")]

file_info = []
for file in files:
    file_path = os.path.join(history_directory, file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    praep_name = loaded_data.get('praep_name', 'Unbekannt')
    timestamp = loaded_data.get('timestamp', '')
    file_info.append((f"{praep_name} ({timestamp})", file))


if file_info:
    selected_label = st.selectbox(
        "Wähle eine gespeicherte Auswertung",
        [item[0] for item in file_info]
    )
    selected_file = next(file for label, file in file_info if label == selected_label)

    file_path = os.path.join(history_directory, selected_file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    st.subheader(f"Präparat: {loaded_data.get('praep_name', 'Unbekannt')}")

    df_loaded = pd.DataFrame(loaded_data["data"])

    # Index ggf. setzen, falls mit Index gespeichert
    if "index" in df_loaded.columns:
        df_loaded = df_loaded.set_index("index")

    # Erythroblasten pro 100 Leukozyten berechnen
    if "Erythroblast" in df_loaded["Zelle"].values:
        erythro_row = df_loaded[df_loaded["Zelle"] == "Erythroblast"].iloc[0]
        erythro_count = erythro_row["Anzahl"]
        total_wo_ery = df_loaded[df_loaded["Zelle"] != "Erythroblast"]["Anzahl"].sum()
        eryblast_per_100 = round(erythro_count / total_wo_ery * 100, 2) if total_wo_ery > 0 else 0.0
    else:
        eryblast_per_100 = 0.0

    # Tabelle anzeigen (ohne Erythroblast)
    st.subheader("Tabelle der Ergebnisse")
    df_ohne_ery = df_loaded[df_loaded["Zelle"] != "Erythroblast"]
    st.dataframe(df_ohne_ery, hide_index=True, use_container_width=True)

    # Erythroblasten pro 100 Leukozyten anzeigen
    st.markdown(f"**Erythroblasten / 100 Leukozyten:** {eryblast_per_100}")

    # Kreisdiagramm (Zellen mit Anzahl > 0, ohne Erythroblast)
    filtered_df = df_ohne_ery[df_ohne_ery["Anzahl"] > 0]

    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(
            filtered_df,
            names="Zelle",
            values="Anzahl",
            title="Verteilung der Zelltypen",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig)
    else:
        st.warning("Keine geeigneten Daten für das Kreisdiagramm gefunden.")

    # Löschen Button
    if st.button("❌ Auswertung löschen"):
        os.remove(file_path)
        st.success("Auswertung wurde gelöscht.")
        st.rerun()

    # Beurteilungstexte laden (falls vorhanden)
    beurteilung = loaded_data.get("beurteilung", {})
    erythro_text = beurteilung.get("erythrozyten", "-")
    neutro_text = beurteilung.get("neutrophile", "-")
    lympho_text = beurteilung.get("lymphozyten", "-")
    thrombo_text = beurteilung.get("thrombozyten", "-")

    # Beurteilung anzeigen
    st.subheader("Beurteilung der Kategorien")
    st.markdown(f"**Erythrozyten:**<br>{erythro_text}", unsafe_allow_html=True)
    st.markdown(f"**Neutrophile Granulozyten:**<br>{neutro_text}", unsafe_allow_html=True)
    st.markdown(f"**Lymphozyten:**<br>{lympho_text}", unsafe_allow_html=True)
    st.markdown(f"**Thrombozyten:**<br>{thrombo_text}", unsafe_allow_html=True)

    # PDF Export Button
    if st.button("📄 Exportiere als PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 15)
        pdf.cell(0, 12, f"Auswertung für {loaded_data['praep_name']}", ln=True, align="C")
        pdf.ln(8)

        pdf.set_font("Arial", "B", 11)
        pdf.cell(38, 9, "Zelle", 1, 0, "C")
        pdf.cell(22, 9, "Anzahl", 1, 0, "C")
        pdf.cell(36, 9, "Relativer Anteil (%)", 1, 1, "C")

        pdf.set_font("Arial", "", 10)
        for _, row in df_ohne_ery.iterrows():
            pdf.cell(38, 9, str(row["Zelle"]), 1, 0, "C")
            pdf.cell(22, 9, str(row["Anzahl"]), 1, 0, "C")
            pdf.cell(36, 9, str(row["Relativer Anteil (%)"]), 1, 1, "C")

        pdf.ln(7)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 9, f"Erythroblasten / 100 Leukozyten: {eryblast_per_100}", ln=True)

        # Kreisdiagramm als Bild einfügen (temporär speichern)
        img_path = "temp_chart.png"
        if not filtered_df.empty:
            fig.write_image(img_path)
            pdf.ln(7)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 9, "Kreisdiagramm:", ln=True)
            pdf.image(img_path, x=30, w=120)
            os.remove(img_path)

        # Neue Seite für Beurteilung
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 12, "Beurteilung der Kategorien", ln=True, align="C")
        pdf.ln(6)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Erythrozyten:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, erythro_text if erythro_text else "-")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Neutrophile Granulozyten:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, neutro_text if neutro_text else "-")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Lymphozyten:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, lympho_text if lympho_text else "-")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Thrombozyten:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 8, thrombo_text if thrombo_text else "-")

        pdf_bytes = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"{loaded_data['praep_name']}_Auswertung.pdf",
            mime="application/pdf"
        )

else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")