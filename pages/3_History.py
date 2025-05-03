import streamlit as st
import os
import json

# Titel der Seite
st.title("History")

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"
pdf_directory = "pdf_exports"

# Debugging: Überprüfe, ob das Verzeichnis existiert
if not os.path.exists(history_directory):
    st.warning(f"Das Verzeichnis {history_directory} existiert nicht.")
else:
    st.write(f"Das Verzeichnis {history_directory} wurde gefunden.")

# Überprüfen, ob das Verzeichnis existiert
if not os.path.exists(history_directory):
    st.warning("Es wurden noch keine Auswertungen gespeichert.")
else:
    # Liste der gespeicherten JSON-Dateien
    history_files = [f for f in os.listdir(history_directory) if f.endswith(".json")]
    st.write("Gefundene JSON-Dateien:", history_files)

    if not history_files:
        st.warning("Es wurden noch keine Auswertungen gespeichert.")
    else:
        st.subheader("Gespeicherte Auswertungen")
        for file in history_files:
            file_path = os.path.join(history_directory, file)
            with open(file_path, "r", encoding="utf-8") as f:
                history_data = json.load(f)
            st.write(f"Inhalt der Datei {file}:", history_data)

            # Zeige die gespeicherten Daten an
            with st.expander(f"Auswertung: {history_data['praep_name']}"):
                st.write(f"**Präparatname:** {history_data['praep_name']}")
                st.write(f"**Total Klicks:** {history_data['total_count']}")
                st.write("**Ergebnisse:**")
                st.table(history_data["data"])

                # PDF-Download-Button (falls PDF existiert)
                pdf_file = os.path.join(pdf_directory, f"{history_data['praep_name']}.pdf")
                if os.path.exists(pdf_file):
                    with open(pdf_file, "rb") as pdf:
                        st.download_button(
                            label="📄 PDF herunterladen",
                            data=pdf,
                            file_name=f"{history_data['praep_name']}.pdf",
                            mime="application/pdf",
                        )
                else:
                    st.warning(f"Keine PDF-Datei für {history_data['praep_name']} gefunden.")