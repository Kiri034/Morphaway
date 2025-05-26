# filepath: utils/style.py
import streamlit as st

def set_background_color(color="#FFD6DA", sidebar_color="#FFE4EC"):
    import streamlit as st
    # Set the background color for the main app area
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