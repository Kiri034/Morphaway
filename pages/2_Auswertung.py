import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io
import json
import os
import tempfile

# Abrufen des Präparatnamens aus st.session_state
praep_name = st.session_state.get("praep_name", "Präparat")

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"
if not os.path.exists(history_directory):
    os.makedirs(history_directory)

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
        fig.write_image(img_bytes, format="png")  # Erfordert kaleido
        img_bytes.seek(0)
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
        img_bytes = None


# Überprüfen, ob 'data_df' in st.session_state existiert
if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
    data_df = st.session_state['data_df']
    
# PDF-Erstellung
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Titel
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="Zellzählungsergebnisse", ln=True, align="C")
pdf.ln(10)

# Tabelle in die PDF einfügen
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Tabelle der Ergebnisse:", ln=True)
pdf.ln(5)
if 'df' in locals() or 'df' in globals():
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Zelle']}: {row['Anzahl']} Klicks ({row['Relativer Anteil (%)']}%)", ln=True)
else:
    st.warning("Die Tabelle der Ergebnisse (df) ist nicht verfügbar.")

if img_bytes:
    # Diagramm in die PDF einfügen
    pdf.ln(10)
    pdf.cell(200, 10, txt="Kreisdiagramm der Ergebnisse:", ln=True)
    pdf.ln(5)

    # Temporäre Datei erstellen
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(img_bytes.getvalue())  # Schreibe das Bild in die temporäre Datei
        temp_file_path = temp_file.name  # Speichere den Pfad der temporären Datei

    # Füge das Bild aus der temporären Datei in die PDF ein
    pdf.image(temp_file_path, x=10, y=pdf.get_y(), w=180)

    # Lösche die temporäre Datei nach der Verwendung
    os.remove(temp_file_path)
    
# Diagramm in die PDF einfügen
if img_bytes:
    pdf.ln(10)
    pdf.cell(200, 10, txt="Kreisdiagramm der Ergebnisse:", ln=True)
    pdf.ln(5)

if not filtered_df.empty:
    img_bytes = io.BytesIO()
    fig.write_image(img_bytes, format="png")  # Erfordert kaleido
    img_bytes.seek(0)
else:
    st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
    img_bytes = None
    
    # Temporäre Datei erstellen
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(img_bytes.getvalue())  # Schreibe das Bild in die temporäre Datei
        temp_file_path = temp_file.name  # Speichere den Pfad der temporären Datei

    # Füge das Bild aus der temporären Datei in die PDF ein
    pdf.image(temp_file_path, x=10, y=pdf.get_y(), w=180)

    # Lösche die temporäre Datei nach der Verwendung
    os.remove(temp_file_path)

# PDF direkt in eine Datei schreiben
output_file_path = "zellzaehlung_ergebnisse.pdf"  # Pfad zur Ausgabedatei
pdf.output(output_file_path)  # Schreibe die PDF in die Datei

# Download-Button für die gespeicherte Datei
with open(output_file_path, "rb") as pdf_file:
    st.download_button(
        label="📄 PDF herunterladen",
        data=pdf_file,
        file_name="zellzaehlung_ergebnisse.pdf",
        mime="application/pdf",
    )