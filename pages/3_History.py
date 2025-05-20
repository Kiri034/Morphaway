# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py') 
# ====== End Login Block ======

# ------------------------------------------------------------
# Here starts the actual app, which was developed previously
import streamlit as st
import os
import json
import pandas as pd
import datetime  # Für den Timestamp

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

# Erstelle eine Liste von Präparatnamen + Zeitstempel zusammen mit den zugehörigen Dateinamen
file_info = []
for file in files:
    file_path = os.path.join(history_directory, file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    praep_name = loaded_data.get('praep_name', 'Unbekannt')
    timestamp = loaded_data.get('timestamp', '')
    display_name = f"{praep_name} ({timestamp})" if timestamp else praep_name
    file_info.append((display_name, file))

if file_info:
    # Alle Einträge anzeigen, auch mit gleichem Präparatnamen
    selected_display_name = st.selectbox(
        "Wähle eine gespeicherte Auswertung",
        [item[0] for item in file_info]
    )
    # Hole den Dateinamen zur Auswahl
    selected_file = next(file for display, file in file_info if display == selected_display_name)

    if selected_file:
        file_path = os.path.join(history_directory, selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        st.subheader(f"Präparat: {loaded_data.get('praep_name', 'Unbekannt')}")
        st.caption(f"Zeitpunkt: {loaded_data.get('timestamp', '')}")

        df_loaded = pd.DataFrame(loaded_data["data"])
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
else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")