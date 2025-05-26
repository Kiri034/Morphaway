# filepath: utils/style.py
def set_background_color(color="#FFD6DA", sidebar_color="#FFE4EC", image_path="/static/erythro.png"):
    import streamlit as st
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
            background-image: url('{image_path}');
            background-repeat: repeat;
            background-size: 60px;  /* Bildgröße, z.B. 60px x 60px */
        }}
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )