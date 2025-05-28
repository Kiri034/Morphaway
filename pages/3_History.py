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

# Hintergrundfarbe & Bild nur rechts
set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")

# Logo anzeigen
st.image("https://raw.githubusercontent.com/Kiri034/Morphaway/bd399c4a2b974d03fc9117a45bd700e447c0a61b/Bilder/Logo.png", width=320)

st.title("🔍 History")

user = st.session_state.get("user")
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

    # Gesamtanzahl ermitteln und anzeigen
    total_count = None
    if "Total" in df_loaded.index or "Gesamt" in df_loaded.index:
        idx = "Total" if "Total" in df_loaded.index else "Gesamt"
        try:
            total_count = int(float(df_loaded.loc[idx, "Anzahl"]))
        except Exception:
            total_count = df_loaded.loc[idx, "Anzahl"]
    elif "Zelle" in df_loaded.columns and any(df_loaded["Zelle"].isin(["Total", "Gesamt"])):
        row = df_loaded[df_loaded["Zelle"].isin(["Total", "Gesamt"])].iloc[0]
        try:
            total_count = int(float(row["Anzahl"]))
        except Exception:
            total_count = row["Anzahl"]

    if total_count not in (None, "", " "):
        st.markdown(f"**Differenzierte Zellen gesamt:** {total_count}")

    # Tabelle anzeigen
    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df_loaded)

    # Kreisdiagramm (Zellen mit Anzahl > 0, ohne Erythroblast)
    filtered_df = df_loaded[(df_loaded["Anzahl"] > 0) & (df_loaded["Zelle"] != "Erythroblast")]

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
        st.experimental_rerun()

    # PDF Export Button
    if st.button("📄 Exportiere als PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Auswertung für {loaded_data['praep_name']}", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(40, 10, "Zelle", 1, 0, "C")
        pdf.cell(40, 10, "Anzahl", 1, 0, "C")
        pdf.cell(40, 10, "Relativer Anteil (%)", 1, 1, "C")

        pdf.set_font("Arial", "", 12)
        for _, row in df_loaded.iterrows():
            pdf.cell(40, 10, str(row["Zelle"]), 1, 0, "C")
            pdf.cell(40, 10, str(row["Anzahl"]), 1, 0, "C")
            pdf.cell(40, 10, str(row["Relativer Anteil (%)"]), 1, 1, "C")

        # Kreisdiagramm als Bild einfügen (temporär speichern)
        img_path = "temp_chart.png"
        if not filtered_df.empty:
            fig.write_image(img_path)
            pdf.ln(10)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Kreisdiagramm:", ln=True)
            pdf.image(img_path, x=30, w=150)
            os.remove(img_path)

        pdf_bytes = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"{loaded_data['praep_name']}_Auswertung.pdf",
            mime="application/pdf"
        )

else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")

    # Daten aus DataManager laden, falls vorhanden
    DataManager().load_user_data(
        user=user,
        data_directory='data',
        session_state_key='data_df',
        file_name='data.csv',
        initial_value=pd.DataFrame(),
        parse_dates=['timestamp']
    )
