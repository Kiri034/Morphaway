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
st.markdown("Beurteile das Blutbild und fahre fort, sobald du mit der Beurteilung fertig bist.")

# Erythrozyten Bilder und Beschriftungen
erythro = [ ... ]


# Neutrophilen Bilder und Beschriftungen
neutro = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/baso_tuepfelung.jpg", "caption": "Basophile Tüpfelung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/howell-jolly.jpg", "caption": "Howell-Jolly-Körperchen"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/polychromasie.jpg", "caption": "Polychromasie"}
]

# Lymphozyten Bilder und Beschriftungen
lympho = [ ]

# Thrombocyten Bilder und Beschriftungen
thrombo = [ ]


st.subheader("Neutrophile Granulozyten Beurteilung")

cols = st.columns(5)

for idx, neutro in enumerate(neutro):
    col = cols[idx % 5]
    with col:
        st.image(neutro["path"], caption=neutro["caption"], use_container_width=True)
        rating = st.slider(
        f"Bewerte die Zelle: {neutro['caption']}",
        label_visibility="collapsed",   # Versteckt die Beschriftung des Sliders
        min_value=0,
        max_value=3,
        value=0,
        step=1,
        key=f"rating_{idx}"
    )

    if "ratings" not in st.session_state:
        st.session_state["ratings"] = {}
    st.session_state["ratings"][neutro["caption"]] = rating

    
