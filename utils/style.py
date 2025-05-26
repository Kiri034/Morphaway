# filepath: utils/style.py
import streamlit as st

def set_background_color(color="#FFD6DA"):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )