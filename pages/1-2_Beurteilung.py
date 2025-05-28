# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import datetime
from utils.data_manager import DataManager
from utils.style import set_background_color

# Set background and sidebar image
set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")

st.title("🔬 Beurteilung der Zellen")

# Beispiel-Fotopfad-Liste (ersetze durch deine eigenen Bildpfade)
images_beurteilung = [
    {"path": "images/photo1.jpg", "caption": "Foto 1"},
    {"path": "images/photo2.jpg", "caption": "Foto 2"},
    {"path": "images/photo3.jpg", "caption": "Foto 3"},
]

for idx, images_beurteilung in enumerate(images_beurteilung):
    st.image(images_beurteilung["path"], caption=images_beurteilung["caption"], use_container_width=True)
    rating = st.slider(
        f"Bewertung für {images_beurteilung['caption']}:",
        min_value=0,
        max_value=3,
        value=0,
        step=1,
        key=f"rating_{idx}"
    )
    st.write(f"Deine Bewertung: {rating}")
    st.markdown("---")
