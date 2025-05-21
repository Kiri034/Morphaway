# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py')  # Weiterleitung zur Login-Seite
# ====== End Login Block ======
import streamlit as st
import os
import json
import pandas as pd
from utils.data_manager import DataManager


st.title("🔍 History")
# ------------------------------
# Überprüfe, ob der Benutzer eingeloggt ist
if "user" not in st.session_state:
    # Der Login-Manager hat den Benutzernamen gesetzt, wenn der Benutzer angemeldet ist.
    if st.session_state.get("user"):
        # Benutzername wurde beim Login gesetzt, z.B. 'user123'
        pass
    else:
        # Benutzer nicht angemeldet
        st.warning("Du musst dich anmelden, um fortzufahren.")
        st.stop()  # Stoppe die Ausführung, falls der Benutzer nicht angemeldet ist

# ------------------------------
# Benutzerspezifisches Verzeichnis erstellen
user = st.session_state["user"]
history_directory = os.path.join("history_exports", user)

# Stelle sicher, dass das Verzeichnis existiert
if not os.path.exists(history_directory):
    os.makedirs(history_directory)

# Liste der gespeicherten Auswertungen für den aktuellen Benutzer
files = [f for f in os.listdir(history_directory) if f.endswith(".json")]

# Erstelle eine Liste von Präparatnamen zusammen mit den zugehörigen Dateinamen
file_info = []
for file in files:
    file_path = os.path.join(history_directory, file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    praep_name = loaded_data.get('praep_name', 'Unbekannt')
    file_info.append((praep_name, file))

# Falls gespeicherte Auswertungen vorhanden sind, zeige sie an
if file_info:
    selected_praep_name = st.selectbox(
        "Wähle eine gespeicherte Auswertung",
        [item[0] for item in file_info]
    )
    selected_file = next(file for name, file in file_info if name == selected_praep_name)

    if selected_file:
        file_path = os.path.join(history_directory, selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        st.subheader(f"Präparat: {loaded_data.get('praep_name', 'Unbekannt')}")

        # Umwandeln der Daten in ein DataFrame für die Tabelle
        df_loaded = pd.DataFrame(loaded_data["data"])
        
        # Falls beim Speichern ein Index mitgespeichert wurde, setze ihn wieder
        if "index" in df_loaded.columns:
            df_loaded = df_loaded.set_index("index")

        # Gesamtzahl extrahieren und anzeigen
        total_count = None
        if "Total" in df_loaded.index or "Gesamt" in df_loaded.index:
            idx = "Total" if "Total" in df_loaded.index else "Gesamt"
            try:
                total_count = int(float(df_loaded.loc[idx, "Anzahl"]))
            except Exception:
                total_count = df_loaded.loc[idx, "Anzahl"]
        elif "Zelle" in df_loaded.columns and any(df_loaded["Zelle"].isin(["Total", "Gesamt"])):
            row = df_loaded[df_loaded["Zelle"].isin(["Total", "Gesamt"])].iloc[0]
            try:
                total_count = int(float(row["Anzahl"]))
            except Exception:
                total_count = row["Anzahl"]
        
        if total_count not in (None, "", " "):
            st.markdown(f"**Differenzierte Zellen gesamt:** {total_count}")
        
        # Zeige die Tabelle an
        st.subheader("Tabelle der Ergebnisse")
        st.dataframe(df_loaded)

        # Kreisdiagramm erstellen
        st.subheader("Kreisdiagramm der Ergebnisse")
        filtered_df = df_loaded[(df_loaded["Anzahl"] > 0) & (df_loaded["Zelle"] != "Erythroblast")]
        if not filtered_df.empty:
            fig = px.pie(
                filtered_df,
                names="Zelle",
                values="Anzahl",
                title="Verteilung der Zelltypen",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig)

        # Löschfunktion
        if st.button("❌ Auswertung löschen"):
            os.remove(file_path)
            st.success("Auswertung wurde gelöscht.")
            st.experimental_rerun()

        # PDF-Exportfunktion
        if st.button("📄 Exportiere als PDF"):
            # PDF erstellen
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt=f"Auswertung für {loaded_data['praep_name']}", ln=True, align="C")
            pdf.ln(10)
            
            # Tabelle zum PDF hinzufügen
            pdf.set_font("Arial", "B", 12)
            pdf.cell(40, 10, "Zelle", 1, 0, "C")
            pdf.cell(40, 10, "Anzahl", 1, 0, "C")
            pdf.cell(40, 10, "Relativer Anteil (%)", 1, 1, "C")
            pdf.set_font("Arial", "", 12)

            for index, row in df_loaded.iterrows():
                pdf.cell(40, 10, str(row['Zelle']), 1, 0, "C")
                pdf.cell(40, 10, str(row['Anzahl']), 1, 0, "C")
                pdf.cell(40, 10, str(row['Relativer Anteil (%)']), 1, 1, "C")

            # Kreisdiagramm als Bild hinzufügen
            img_path = "temp_chart.png"
            if not filtered_df.empty:
                fig.write_image(img_path)
                pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(200, 10, "Kreisdiagramm:", ln=True)
                pdf.image(img_path, x=30, w=150)
                os.remove(img_path)

            # PDF herunterladen
            pdf_output = pdf.output(dest="S").encode("latin1")
            st.download_button(
                label="📄 PDF herunterladen",
                data=pdf_output,
                file_name=f"{loaded_data['praep_name']}_Auswertung.pdf",
                mime="application/pdf"
            )

else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")
