# ====== Start Login Block ======
#from utils.login_manager import LoginManager
#LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

# ------------------------------------------------------------
# Hier beginnt die eigentliche App
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

pdf_output_path = None  # <- Initialisierung

# Überprüfen, ob Zählerdaten aus 1_Morphaway.py vorhanden sind
if any(f"button_{i}_count" in st.session_state for i in range(1, 14)):
    # Liste der Zellen und Beschriftungen
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
    total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 14))
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        relative_count = (count / total_count * 100) if total_count > 0 else 0
        data.append({"Zelle": cell["label"], "Anzahl": count, "Relativer Anteil (%)": round(relative_count, 2)})

    # Daten in einen DataFrame umwandeln
    df = pd.DataFrame(data)

    # Ergebnisse speichern
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

    # Kreisdiagramm erstellen (nur Zellen mit Anzahl > 0)
    filtered_df = df[df["Anzahl"] > 0]  # Filtere Zellen mit Anzahl > 0
    diagram_path = None
    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(filtered_df, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen")
        st.plotly_chart(fig)

        # Diagramm als Bild in eine temporäre Datei speichern
        diagram_path = "diagram.png"
        try:
            fig.write_image(diagram_path)  # Speichert das Diagramm als PNG-Datei
        except Exception as e:
            st.error(f"Fehler beim Speichern des Diagramms als Bild: {e}")
            diagram_path = None
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
        diagram_path = None
else:
    st.warning("Keine Zählerdaten vorhanden. Bitte kehren Sie zurück und geben Sie Ihre Werte ein.")
    df = pd.DataFrame()  # Leerer DataFrame, damit der PDF-Teil nicht crasht
    diagram_path = None

# --- PDF-Export ---   
if st.button("PDF Export"):
    if not df.empty:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Titel
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Auswertung für {praep_name}", ln=True, align="C")

        # Tabelle
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, "Zelle", 1)
        pdf.cell(60, 10, "Anzahl", 1)
        pdf.cell(70, 10, "Relativer Anteil (%)", 1)
        pdf.ln()

        pdf.set_font("Arial", '', 12)
        for index, row in df.iterrows():
            pdf.cell(60, 10, row["Zelle"], 1)
            pdf.cell(60, 10, str(row["Anzahl"]), 1)
            pdf.cell(70, 10, str(row["Relativer Anteil (%)"]), 1)
            pdf.ln()

        # Diagramm hinzufügen
        if diagram_path and os.path.exists(diagram_path):
            pdf.image(diagram_path, x=10, y=pdf.get_y(), w=180)

        # Speichern des PDFs
        pdf_output_path = os.path.join(history_directory, f"{praep_name}_{timestamp}.pdf")
        try:
            pdf.output(pdf_output_path)
            st.success(f"PDF erfolgreich erstellt: {pdf_output_path}")
        except Exception as e:
            st.error(f"Fehler beim Erstellen des PDFs: {e}")
    else:
        st.warning("Keine Daten verfügbar. PDF-Export nicht möglich.")

# --- Download-Link für PDF-Datei ---
if pdf_output_path and os.path.exists(pdf_output_path):
    with open(pdf_output_path, "rb") as f:
        st.download_button(
            label="Download PDF",
            data=f,
            file_name=f"{praep_name}_{timestamp}.pdf",
            mime="application/pdf"
        )