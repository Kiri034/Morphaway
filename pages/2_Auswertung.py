import streamlit as st
import os
import json
from fpdf import FPDF

# Titel der Seite
st.title("History")

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"
pdf_directory = "pdf_exports"

# Überprüfen, ob das Verzeichnis existiert
if not os.path.exists(history_directory):
    st.warning("Es wurden noch keine Auswertungen gespeichert.")
else:
    # Liste der gespeicherten JSON-Dateien
    history_files = [f for f in os.listdir(history_directory) if f.endswith(".json")]

    if not history_files:
        st.warning("Es wurden noch keine Auswertungen gespeichert.")
    else:
        st.subheader("Gespeicherte Auswertungen")
        for file in history_files:
            file_path = os.path.join(history_directory, file)
            with open(file_path, "r", encoding="utf-8") as f:
                history_data = json.load(f)

            # Zeige die gespeicherten Daten an
            with st.expander(f"Auswertung: {history_data['praep_name']}"):
                st.write(f"**Präparatname:** {history_data['praep_name']}")
                st.write(f"**Total Klicks:** {history_data['total_count']}")
                st.write("**Ergebnisse:**")
                st.table(history_data["data"])

                # PDF-Erstellung
                pdf_file_path = os.path.join(pdf_directory, f"{history_data['praep_name']}.pdf")
                if not os.path.exists(pdf_directory):
                    os.makedirs(pdf_directory)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Titel
                pdf.set_font("Arial", style="B", size=16)
                pdf.cell(200, 10, txt=f"Auswertung: {history_data['praep_name']}", ln=True, align="C")
                pdf.ln(10)

                # Ergebnisse in die PDF einfügen
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Ergebnisse:", ln=True)
                pdf.ln(5)
                for row in history_data["data"]:
                    pdf.cell(200, 10, txt=f"{row['Zelle']}: {row['Anzahl']} Klicks ({row['Relativer Anteil (%)']}%)", ln=True)

                # PDF speichern
                pdf.output(pdf_file_path)

                # PDF-Download-Button
                with open(pdf_file_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 PDF herunterladen",
                        data=pdf_file,
                        file_name=f"{history_data['praep_name']}.pdf",
                        mime="application/pdf",
                    )