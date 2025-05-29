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
from datetime import datetime

from utils.data_manager import DataManager
from utils.style import set_background_color

set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")

st.image("https://raw.githubusercontent.com/Kiri034/Morphaway/bd399c4a2b974d03fc9117a45bd700e447c0a61b/Bilder/Logo.png", width=320)

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"📄Auswertung für {praep_name}")

user = st.session_state.get("user")
if user:
    history_directory = os.path.join("history_exports", user)
else:
    history_directory = "history_exports"
if not os.path.exists(history_directory):
    os.makedirs(history_directory)

counted = any(st.session_state.get(f"button_{i}_count", 0) > 0 for i in range(1, 15))

if counted:
    images = [
        {"label": "Lymphozyt"},
        {"label": "reaktiver Lymphozyt"},
        {"label": "Monozyt"},
        {"label": "Eosinophile Gc*"},
        {"label": "Basophile Gc*"},
        {"label": "Segmentkernige Gc*"},
        {"label": "Stabkernige Gc*"},
        {"label": "Blasten"},
        {"label": "Promyelozyt"},
        {"label": "Myelozyt"},
        {"label": "Metamyelozyt"},
        {"label": "Plasmazelle"},
        {"label": "Erythroblast"},
        {"label": "smudged cells"},
    ]

    erythroblast_index = 13
    total_count = sum(
        st.session_state.get(f"button_{i}_count", 0)
        for i in range(1, 15) if i != erythroblast_index
    )

    data = []
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        relative = (count / total_count * 100) if total_count > 0 else 0
        data.append({
            "Zelle": cell["label"],
            "Anzahl": count,
            "Relativer Anteil (%)": round(relative, 2)
        })

    df = pd.DataFrame(data)

    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df)

    filtered_df = df[(df["Anzahl"] > 0) & (df["Zelle"] != "Erythroblast")]
    img_bytes = None
    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(filtered_df,
                     names="Zelle",
                     values="Anzahl",
                     title="Verteilung der Zelltypen",
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig)
        try:
            img_bytes = fig.to_image(format="png")
        except Exception as e:
            st.error(f"Fehler beim Erstellen des Diagrammbildes: {e}")
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 oder nur Erythroblasten.")

    if st.button("📄 Export"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 15)
        pdf.cell(0, 12, f"Auswertung - Präparat: {praep_name}", ln=True, align="C")
        pdf.ln(8)

        pdf.set_font("Arial", "B", 11)
        pdf.cell(38, 9, "Zelle", 1, 0, "C")
        pdf.cell(22, 9, "Anzahl", 1, 0, "C")
        pdf.cell(36, 9, "Rel. Anteil (%)", 1, 1, "C")
        pdf.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            pdf.cell(38, 9, str(row["Zelle"]), 1, 0, "C")
            pdf.cell(22, 9, str(row["Anzahl"]), 1, 0, "C")
            pdf.cell(36, 9, str(row["Relativer Anteil (%)"]), 1, 1, "C")

        if img_bytes:
            img_path = "temp_chart.png"
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            pdf.ln(7)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 9,txt="Kreisdiagramm:", ln=True)
            pdf.ln(4)
            pdf.image(img_path, x=30, w=120)
            os.remove(img_path)

        pdf_bytes = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"{praep_name}_Auswertung.pdf",
            mime="application/pdf"
        )

    if st.button("Zur History"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{praep_name}_{timestamp}.json"
        filepath = os.path.join(history_directory, filename)
        export_data = {
            "praep_name": praep_name,
            "timestamp": timestamp,
            "data": df.to_dict(orient="records")
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        st.success("Auswertung gespeichert!")
        st.switch_page("pages/3_History.py")
       

else:
    st.info("Noch keine Zellen gezählt. Es sind keine Auswertungen verfügbar.")
    df = pd.DataFrame()
    total_count = 0

if not df.empty:
    DataManager().append_record(
        session_state_key=f'data_df_{user}' if user else 'data_df',
        record_dict={
            "user": user,
            "praep_name": praep_name,
            "timestamp": datetime.now(),
            "total_count": total_count,
            "erythroblast_count": int(df[df["Zelle"] == "Erythroblast"]["Anzahl"].values[0]) if "Erythroblast" in df["Zelle"].values else 0,
        }
    )
