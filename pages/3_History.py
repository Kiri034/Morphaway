import streamlit as st
import os
import json
import pandas as pd

st.title("🔍 History")

history_directory = "history_exports"

# Liste aller gespeicherten Auswertungen
files = [f for f in os.listdir(history_directory) if f.endswith(".json")]

if files:
    selected_file = st.selectbox("Wähle eine gespeicherte Auswertung", sorted(files, reverse=True))

    if selected_file:
        file_path = os.path.join(history_directory, selected_file)
        with open(file_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)

        st.subheader(f"Präparat: {loaded_data['praep_name']}")
        st.caption(f"Zeitpunkt: {loaded_data['timestamp']}")

        df_loaded = pd.DataFrame(loaded_data["data"])
        st.dataframe(df_loaded)

        # Optional: Kreisdiagramm wieder anzeigen
        import plotly.express as px
        filtered_df = df_loaded[df_loaded["Anzahl"] > 0]
        if not filtered_df.empty:
            fig = px.pie(filtered_df, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen")
            st.plotly_chart(fig)
else:
    st.info("Es sind noch keine gespeicherten Auswertungen vorhanden.")
