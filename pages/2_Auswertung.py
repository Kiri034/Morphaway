import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
from datetime import datetime
from io import BytesIO

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")

# Daten vorbereiten (wie gehabt)
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

data = []
total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 15))
for idx, cell in enumerate(images, start=1):
    count = st.session_state.get(f"button_{idx}_count", 0)
    relative_count = (count / total_count * 100) if total_count > 0 else 0
    data.append({"Zelle": cell["label"], "Anzahl": count, "Relativer Anteil (%)": round(relative_count, 2)})

df = pd.DataFrame(data)
st.subheader("Tabelle der Ergebnisse")
st.dataframe(df)

# Kreisdiagramm erstellen (nur Zellen mit Anzahl > 0)
filtered_df = df[df["Anzahl"] > 0]
diagram_path = None
if not filtered_df.empty:
    st.subheader("Kreisdiagramm der Ergebnisse")
    fig = px.pie(filtered_df, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen")
    st.plotly_chart(fig)
    diagram_path = "diagram.png"
    try:
        fig.write_image(diagram_path)
    except Exception as e:
        st.error(f"Fehler beim Speichern des Diagramms als Bild: {e}")
        diagram_path = None
else:
    st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
    diagram_path = None

# --- PDF-Button ---
if st.button("PDF herunterladen"):
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

    # Diagramm ins PDF einfügen
    if diagram_path and os.path.exists(diagram_path):
        pdf.ln(5)
        pdf.image(diagram_path, x=10, y=pdf.get_y(), w=180)

    # PDF als Download anbieten
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        label="Download PDF",
        data=pdf_buffer,
        file_name=f"{praep_name}_{timestamp}.pdf",
        mime="application/pdf"
    )