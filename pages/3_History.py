import streamlit as st
import os
import json

# Titel der Seite
st.title("History")

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"

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

                # PDF-Download-Button (falls PDF existiert)
                pdf_file = os.path.join("pdf_exports", f"{history_data['praep_name']}.pdf")
                if os.path.exists(pdf_file):
                    with open(pdf_file, "rb") as pdf:
                        st.download_button(
                            label="📄 PDF herunterladen",
                            data=pdf,
                            file_name=f"{history_data['praep_name']}.pdf",
                            mime="application/pdf",
                        )
                else:
                    st.warning("Keine PDF-Datei für diese Auswertung gefunden.")