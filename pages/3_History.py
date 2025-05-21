# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py')
# ====== End Login Block ======

# ------------------------------------------------------------
import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.title("🔍 History")

# Lade die CSV-Daten aus SwitchDrive
DataManager().load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

df = st.session_state.get("data_df", pd.DataFrame())

if not df.empty:
    # Optional: Nur eigene Daten anzeigen, falls du User-Spalte hast
    # user = st.session_state.get("user")
    # if "user" in df.columns and user:
    #     df = df[df["user"] == user]

    # Auswahlbox für Präparatnamen
    praep_names = df["praep_name"].unique()
    selected_praep = st.selectbox("Wähle ein Präparat", praep_names)

    df_selected = df[df["praep_name"] == selected_praep]

    st.subheader(f"Präparat: {selected_praep}")
    st.dataframe(df_selected)

    # Kreisdiagramm (ohne Erythroblast und nur mit Anzahl > 0, falls sinnvoll)
    import plotly.express as px
    if "Zelle" in df_selected.columns and "Anzahl" in df_selected.columns:
        filtered_df = df_selected[(df_selected["Anzahl"] > 0) & (df_selected["Zelle"] != "Erythroblast")]
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