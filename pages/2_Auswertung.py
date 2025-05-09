import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io
import os
from pathlib import Path
import json
from datetime import datetime

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")

# Verzeichnis für gespeicherte Auswertungen
history_directory = Path("history_exports")

# Erstelle das Verzeichnis, falls es nicht existiert
history_directory.mkdir(parents=True, exist_ok=True)

# Überprüfen, ob Zählerdaten aus 1_Morphaway.py vorhanden sind
if any(f"button_{i}_count" in st.session_state for i in range(1, 19)):
    # Liste der Zellen und Beschriftungen
    images = [
        {"label": "Lymphozyt"},
        {"label": "Monozyt"},
        {"label": "Eosinophil"},
        {"label": "Basophil"},
        {"label": "Segmentkernige Granulozyten"},
        {"label": "Stabkernige Granulozyten"},
        {"label": "Erythroblast"},
        {"label": "Blasten"},
        {"label": "Promyelozyt"},
        {"label": "Myelozyt"},
        {"label": "Metamyelozyt"},
        {"label": "reactive Lymphozyt"},
        {"label": "Abnormale Lymphozyten"},
        {"label": "Large granular lymphocyte"},
        {"label": "NRBC"},
        {"label": "Mastzelle"},
        {"label": "Plasmazelle"},
        {"label": "smudged cells"},
    ]

    # Daten für die Tabelle und das Diagramm vorbereiten
    data = []
    total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 19))
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        relative_count = (count / total_count * 100) if total_count > 0 else 0
        data.append({"Zelle": cell["label"], "Anzahl": count, "Relativer Anteil (%)": round(relative_count, 2)})

    # Daten in einen DataFrame umwandeln
    df = pd.DataFrame(data)

# Ergebnisse speichern
if 'df' in locals() and not df.empty:
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
    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(filtered_df, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen")
        st.plotly_chart(fig)

        # Diagramm als Bild in Bytes speichern
        img_bytes = io.BytesIO()
        try:
            fig.write_image(img_bytes, format="png")  # Erfordert kaleido
            img_bytes.seek(0)  # Setzt den Pointer zurück
        except Exception as e:
            st.error(f"Fehler beim Erstellen des Diagramms als Bild: {e}")
            img_bytes = io.BytesIO()  # Initialize img_bytes to avoid undefined variable error
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
        img_bytes = io.BytesIO()  # Initialize img_bytes to avoid undefined variable error
else:
    st.warning("Keine Zählerdaten vorhanden. Bitte kehren Sie zurück und geben Sie Ihre Werte ein.")

# PDF-Erstellung
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Titel
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="Auswertung der Ergebnisse", ln=True, align="C")
pdf.ln(10)

# Tabelle in die PDF einfügen
if 'df' in locals() and not df.empty:
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 5, txt="Tabelle der Ergebnisse:", ln=True)
    pdf.ln(5)
    for index, row in df.iterrows():
        pdf.cell(0, 5, txt=f"{row['Zelle']}: {row['Anzahl']} Klicks ({row['Relativer Anteil (%)']}%)", ln=True)
else:
    pdf.cell(0, 5, txt="Keine Daten verfügbar.", ln=True)

# Diagramm in die PDF einfügen
if img_bytes:
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, txt="Kreisdiagramm der Ergebnisse:", ln=True)
    pdf.ln(5)

    # Temporäre Datei erstellen
    with open("diagram.png", "wb") as f:
        f.write(img_bytes.getvalue())

    try:
        pdf.image("diagram.png", x=10, y=pdf.get_y(), w=180)
    except Exception as e:
        st.error(f"Fehler beim Einfügen des Diagramms in die PDF: {e}")

# PDF in eine Datei speichern
pdf_file_path = "auswertung.pdf"
pdf.output(pdf_file_path)

# PDF-Download-Button
if os.path.exists(pdf_file_path):
    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_file,
            file_name="auswertung.pdf",
            mime="application/pdf",
        )
else:
    st.error("Die PDF-Datei konnte nicht erstellt werden.")

# Button für History anzeigen
if st.button("History"):
    st.switch_page("pages/3_History.py")
