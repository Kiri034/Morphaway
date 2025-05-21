# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py') 
# ====== End Login Block ======

# ------------------------------------------------------------
# Here starts the actual app, which was developed previously
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from datetime import datetime

from utils.data_manager import DataManager

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")

# Prüfen, ob überhaupt gezählt wurde
if any(f"button_{i}_count" in st.session_state for i in range(1, 15)):
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

    # Daten für die Tabelle und das Diagramm vorbereiten
    data = []
    total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 15))
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        relative_count = (count / total_count * 100) if total_count > 0 else 0
        data.append({"Zelle": cell["label"], "Anzahl": count, "Relativer Anteil (%)": round(relative_count, 2)})

    df = pd.DataFrame(data)

    # Tabelle anzeigen
    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df)

    # Kreisdiagramm erstellen (ohne Erythroblast und nur mit Anzahl > 0, falls sinnvoll)
    filtered_df = df[(df["Anzahl"] > 0) & (df["Zelle"] != "Erythroblast")]

    img_bytes = None
    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(
            filtered_df,
            names="Zelle",
            values="Anzahl",
            title="Verteilung der Zelltypen",
            color_discrete_sequence=px.colors.qualitative.Set3  # Farbiges Diagramm
        )
        st.plotly_chart(fig)
        try:
            img_bytes = fig.to_image(format="png")
        except Exception as e:
            st.error(f"Fehler beim Speichern des Diagramms als Bild: {e}")
            img_bytes = None
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks oder nur Erythroblasten.")
        img_bytes = None

    # PDF-Export
    if st.button("📄Export"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 15)
        pdf.cell(0, 12, f"Auswertung der Ergebnisse - Präparat: {praep_name}", ln=True, align="C")
        pdf.ln(8)

        # Tabelle (etwas breiter und höher)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(38, 9, "Zelle", 1, 0, "C")
        pdf.cell(22, 9, "Anzahl", 1, 0, "C")
        pdf.cell(36, 9, "Rel. Anteil (%)", 1, 1, "C")
        pdf.set_font("Arial", "", 10)
        if not df.empty:
            for index, row in df.iterrows():
                pdf.cell(38, 9, str(row['Zelle']), 1, 0, "C")
                pdf.cell(22, 9, str(row['Anzahl']), 1, 0, "C")
                pdf.cell(36, 9, str(row['Relativer Anteil (%)']), 1, 1, "C")
        else:
            pdf.cell(96, 9, "Keine Daten verfügbar.", 1, 1, "C")

        # Kreisdiagramm etwas größer, aber noch passend
        if img_bytes:
            img_path = "temp_chart.png"
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            pdf.ln(7)
            pdf.set_font("Arial", "B", 11)
            pdf.cell(0, 9, txt="Kreisdiagramm:", ln=True)
            pdf.ln(4)
            pdf.image(img_path, x=30, w=120)  # w=120 ist größer, passt aber noch auf A4 quer
            import os
            os.remove(img_path)

        # PDF als Bytes speichern und Download anbieten
        pdf_bytes = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"{praep_name}_Auswertung.pdf",
            mime="application/pdf"
        )

    # Speicherung in SwitchDrive (CSV) und Wechsel zur History-Seite
if st.button("Zur History"):
    DataManager().append_record(
        session_state_key='data_df',
        record_dict={
            "user" : st.session_state.get("user"),
            "praep_name": praep_name,
            "timestamp": datetime.now(),
            "total_count": total_count,
            "erythroblast_count": int(df[df["Zelle"] == "Erythroblast"]["Anzahl"].values[0]) if "Erythroblast" in df["Zelle"].values else 0,
            "zell_auswertung": df.to_json(orient="records")  # <-- komplette Tabelle als JSON-String speichern!
        }
    )
    st.success("Auswertung gespeichert!")
    st.switch_page("pages/3_History.py")

else:
    st.info("Noch keine Zellen gezählt. Es sind keine Auswertungen verfügbar.")