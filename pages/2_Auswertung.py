# ====== Start Login Block ======
# from utils.login_manager import LoginManager
# LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

# ------------------------------------------------------------
# Hier beginnt die eigentliche App, die zuvor entwickelt wurde
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import json
from datetime import datetime

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"
if not os.path.exists(history_directory):
    os.makedirs(history_directory)

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

    # Ergebnisse speichern (optional)
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

    # Tabelle anzeigen
    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df)

    # Kreisdiagramm erstellen (nur Zellen mit Anzahl > 0 und ohne Erythroblast)
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
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Auswertung der Ergebnisse – Präparat: {praep_name}", ln=True, align="C")
        pdf.ln(10)

        # Tabelle
        pdf.set_font("Arial", "B", 10)
        pdf.cell(32, 8, "Zelle", 1, 0, "C")
        pdf.cell(18, 8, "Anzahl", 1, 0, "C")
        pdf.cell(28, 8, "Rel. Anteil (%)", 1, 1, "C")
        pdf.set_font("Arial", "", 10)
        if not df.empty:
            for index, row in df.iterrows():
                pdf.cell(32, 8, str(row['Zelle']), 1, 0, "C")
                pdf.cell(18, 8, str(row['Anzahl']), 1, 0, "C")
                pdf.cell(28, 8, str(row['Relativer Anteil (%)']), 1, 1, "C")
        else:
            pdf.cell(78, 8, "Keine Daten verfügbar.", 1, 1, "C")

        # Kreisdiagramm kleiner einfügen
        if img_bytes:
            img_path = "temp_chart.png"
            with open(img_path, "wb") as f:
                f.write(img_bytes)
            pdf.ln(5)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 8, txt="Kreisdiagramm:", ln=True)
            pdf.ln(3)
            pdf.image(img_path, x=35, w=90)
            os.remove(img_path)

        # PDF als Bytes speichern und Download anbieten
        pdf_bytes = pdf.output(dest="S").encode("latin1")
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"{praep_name}_Auswertung.pdf",
            mime="application/pdf"
        )
else:
    st.info("Noch keine Zellen gezählt. Es sind keine Auswertungen verfügbar.")