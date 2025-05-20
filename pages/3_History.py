# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py')
# ====== End Login Block ======

# ------------------------------------------------------------
import streamlit as st
import os
import json
import pandas as pd

st.title("🔍 History")

# Optional: Nutzername aus Session holen (falls vorhanden)
user = st.session_state.get("user")
if user:
    history_directory = os.path.join("history_exports", user)
else:
    history_directory = "history_exports"

if not os.path.exists(history_directory):
    os.makedirs(history_directory)

# Liste aller gespeicherten Auswertungen (Dateinamen)
files = [f for f in os.listdir(history_directory) if f.endswith(".json")]

# Erstelle eine Liste von Präparatnamen zusammen mit den zugehörigen Dateinamen
file_info = []
for file in files:
    file_path = os.path.join(history_directory, file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    praep_name = loaded_data.get('praep_name', 'Unbekannt')
    file_info.append((praep_name, file))

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

        df_loaded = pd.DataFrame(loaded_data["data"])
        # Falls beim Speichern ein Index mitgespeichert wurde, setze ihn wieder
        if "index" in df_loaded.columns:
            df_loaded = df_loaded.set_index("index")

        # Gesamtzahl extrahieren und anzeigen, robust für verschiedene Formate
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

        st.dataframe(df_loaded)

        # Kreisdiagramm mit festen Farben anzeigen
        import plotly.express as px
        filtered_df = df_loaded[df_loaded["Anzahl"] > 0]
        if not filtered_df.empty:
            fig = px.pie(
                filtered_df,
                names="Zelle",
                values="Anzahl",
                title="Verteilung der Zelltypen",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig)

        # Löschfunktion am Schluss (ohne Bestätigung)
        if st.button("❌ Auswertung löschen"):
            os.remove(file_path)
            st.success("Auswertung wurde gelöscht. Bitte Seite neu laden.")
            st.stop()
else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")