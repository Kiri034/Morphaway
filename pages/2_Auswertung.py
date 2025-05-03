import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import io

# Titel der Seite
praep_name = st.session_state.get("praep_name", "Präparat")
st.title(f"Auswertung für {praep_name}")

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
        fig.write_image(img_bytes, format="png")
        img_bytes.seek(0)
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
        img_bytes = None

    # PDF erstellen
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Titel
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Auswertung für {praep_name}", ln=True, align="C")
    pdf.ln(10)

    # Tabelle in die PDF einfügen
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Tabelle der Ergebnisse:", ln=True)
    pdf.ln(5)
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Zelle']}: {row['Anzahl']} Klicks ({row['Relativer Anteil (%)']}%)", ln=True)

    # Diagramm in die PDF einfügen
    if img_bytes:
        pdf.ln(10)
        pdf.cell(200, 10, txt="Kreisdiagramm der Ergebnisse:", ln=True)
        pdf.ln(5)
        pdf.image(img_bytes, x=10, y=pdf.get_y(), w=180)

    # PDF als Download anbieten
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    st.download_button(
        label="📄 PDF herunterladen",
        data=pdf_output,
        file_name=f"Auswertung_{praep_name}.pdf",
        mime="application/pdf",
    )
else:
    st.warning("Keine Daten verfügbar. Bitte kehre zurück und zähle Zellen in Morphaway.")