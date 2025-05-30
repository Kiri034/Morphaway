# filepath: utils/style.py

def set_background_color(color="#fbeaff", sidebar_color="#fae2ff", image_path="https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png"):
    import streamlit as st
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            background-image: url('{image_path}');
            background-repeat: no-repeat;
            background-position: right;
            background-size: cover;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )