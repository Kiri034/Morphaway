import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# Titel der Seite
st.title("Auswertung der Ergebnisse")

# Beispiel-Daten (falls keine Daten vorhanden sind)
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame({
        "Datum": ["2025-05-01", "2025-05-02"],
        "Wert": [10, 20],
        "Einheit": ["mg/dL", "mg/dL"]
    })

data_df = st.session_state['data_df']

# Tabelle anzeigen
st.subheader("Tabelle der Ergebnisse")
st.dataframe(data_df)

# Kreisdiagramm erstellen
st.subheader("Kreisdiagramm der Ergebnisse")
fig = px.pie(data_df, names="Datum", values="Wert", title="Verteilung der Werte")
st.plotly_chart(fig)

# PDF-Erstellung
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Titel in die PDF einfügen
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="Auswertung der Ergebnisse", ln=True, align="C")
pdf.ln(10)

# Tabelle in die PDF einfügen
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Tabelle der Ergebnisse:", ln=True)
pdf.ln(5)
for index, row in data_df.iterrows():
    pdf.cell(200, 10, txt=f"{row['Datum']}: {row['Wert']} ({row['Einheit']})", ln=True)

# Diagramm in die PDF einfügen
pdf.ln(10)
pdf.cell(200, 10, txt="Kreisdiagramm der Ergebnisse:", ln=True)
pdf.ln(5)

# Diagramm als Bild speichern und in die PDF einfügen
img_bytes = io.BytesIO()
fig.write_image(img_bytes, format="png")  # Erfordert kaleido
img_bytes.seek(0)

# Temporäre Datei für das Diagramm erstellen
import tempfile
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
    temp_file.write(img_bytes.getvalue())
    temp_file_path = temp_file.name

pdf.image(temp_file_path, x=10, y=pdf.get_y(), w=180)

# PDF als Download anbieten
pdf_output = io.BytesIO()
pdf.output(pdf_output)
pdf_output.seek(0)

st.download_button(
    label="📄 PDF der gesamten Seite herunterladen",
    data=pdf_output,
    file_name="auswertung_gesamte_seite.pdf",
    mime="application/pdf",
)