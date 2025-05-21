# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py')
# ====== End Login Block ======

# ------------------------------------------------------------
import streamlit as st
import os
import json
import pandas as pd
import plotly.express as px

from utils.data_manager import DataManager

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

    file_path = os.path.join(history_directory, selected_file)
    with open(file_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)

    st.subheader(f"Präparat: {loaded_data.get('praep_name', 'Unbekannt')}")

    df_loaded = pd.DataFrame(loaded_data["data"])
    if "index" in df_loaded.columns:
        df_loaded = df_loaded.set_index("index")

    # Gesamtzahl extrahieren
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

    # "Total" und "Gesamt" entfernen, aber Erythroblast bleibt
    df_display = df_loaded.copy()
    if "Zelle" in df_display.columns:
        df_display = df_display[~df_display["Zelle"].isin(["Total", "Gesamt"])]

    # Relativer Anteil (%)
    if "Zelle" in df_display.columns and "Anzahl" in df_display.columns:
        total_ohne_ery = df_display.loc[df_display["Zelle"] != "Erythroblast", "Anzahl"].sum()
        df_display["Relativer Anteil (%)"] = df_display.apply(
            lambda row: round(row["Anzahl"] / total_ohne_ery * 100, 2) if total_ohne_ery > 0 else 0,
            axis=1
        )

        st.dataframe(df_display)

        # Kreisdiagramm: ohne Erythroblast
        filtered_df = df_display[
            (df_display["Anzahl"] > 0) & (df_display["Zelle"] != "Erythroblast")
        ]

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
        st.rerun()

else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")

# Lade die CSV-Daten aus SwitchDrive (optional)
DataManager().load_user_data(
    user=user,
    data_directory='data',
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

# Optional anzeigen:
if 'data_df' in st.session_state:
    st.subheader("📄 Geladene CSV-Daten")
    st.dataframe(st.session_state['data_df'])
