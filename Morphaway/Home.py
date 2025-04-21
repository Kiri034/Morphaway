import streamlit as st
import Home
import Cell-counter

# Query-Parameter auslesen
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

# Navigation basierend auf der Seite
if page == "home":
    Home
elif page == "cell-counter":
    Cell-counter