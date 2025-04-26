import streamlit as st

# Titel der Seite
praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")