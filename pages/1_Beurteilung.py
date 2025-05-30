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
st.markdown("Beurteile das Blutbild und fahre fort, sobald du mit deiner Beurteilung fertig bist.")

# Erythrozyten Bilder und Beschriftungen
erythro = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/anisozytose.png", "caption": "Anisozytose"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/mikro.png", "caption": "Mikrozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/makro.png", "caption": "Makrozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hypo.png", "caption": "Hypochromasie"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hyper.png", "caption": "Hyperchromasie"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/polychromasie.png", "caption": "Polychromasie"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/poik.png", "caption": "Poikilozytose"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/akantozyt.png", "caption": "Akantozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/basotuepfelung.png", "caption": "Basophile Tüpfelung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/echino.png", "caption": "Echinocyte"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/fragm.png", "caption": "Fragment"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/howelljolly.png", "caption": "Howell-Jolly-Körperchen"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/teardrop.png", "caption": "Teardrop"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/target.png", "caption": "Target"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/stoma.png", "caption": "Stoma"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/sphaerozyt.png", "caption": "Sphaerozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/sichelzelle.png", "caption": "Sichelzelle"},
    
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/pappenheimer.png", "caption": "Pappenheimer Körperchen"}
]


# Neutrophilen Bilder und Beschriftungen
neutro = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/basoschlieren.png", "caption": "Basophile Tüpfelung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hypergranula.png", "caption": "Hypergranulation"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hyperseg.png", "caption": "Hypersegmentierung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hypogranula.png", "caption": "Hypogranulation"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hyposeg.png", "caption": "Hyposegmentierung"}
]


# Lymphozyten Bilder und Beschriftungen
lympho = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/auerstaebchen.png", "caption": "Auerstäbchen"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/lgl.png", "caption": "LGL"}
]


# Thrombocyten Bilder und Beschriftungen
thrombo = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/tcaggregat.png", "caption": "Thrombozytenaggregat"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/riesentc.png", "caption": "Riesenthrombozyt"}
]


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

    
