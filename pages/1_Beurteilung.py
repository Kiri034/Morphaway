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
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ellipto.png", "caption": "Elliptozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/akantozyt.png", "caption": "Akantozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/stoma.png", "caption": "Stoma"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/sphaerozyt.png", "caption": "Sphaerozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/echino.png", "caption": "Echinocyte"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/target.png", "caption": "Target"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/teardrop.png", "caption": "Teardrop"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/sichelzelle.png", "caption": "Sichelzelle"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/fragm.png", "caption": "Fragment"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/basotuepfelung.png", "caption": "Basophile Tüpfelung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/howelljolly.png", "caption": "Howell-Jolly"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/pappenheimer.png", "caption": "Pappenheimer"}
]


# Neutrophilen Bilder und Beschriftungen
neutro = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hypergranula.png", "caption": "vergrößerte Granula"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/basoschlieren.png", "caption": "basophile Schlieren"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hypogranula.png", "caption": "Hypogranulation"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hyperseg.png", "caption": "Hypersegmentierung"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/hyposeg.png", "caption": "Hyposegmentierung"}
]


# Lymphozyten Bilder und Beschriftungen
lympho = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/lgl.png", "caption": "LGL"}
]


# Thrombocyten Bilder und Beschriftungen
thrombo = [
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/riesentc.png", "caption": "Riesenthrombozyt"},
    {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/tcaggregat.png", "caption": "Thrombozytenaggregat"},
]


# Erythrozyten Beurteilung
st.subheader("Erythrozyten Beurteilung")
cols_ery = st.columns(5)
for idx, eryth in enumerate(erythro):
    col = cols_ery[idx % 5]
    with col:
        st.image(eryth["path"], caption=eryth["caption"], use_container_width=True)
        rating = st.slider(
            f"Bewerte die Zelle: {eryth['caption']}",
            label_visibility="collapsed",
            min_value=0,
            max_value=3,
            value=0,
            step=1,
            key=f"rating_ery_{idx}"
        )
        if "ratings_ery" not in st.session_state:
            st.session_state["ratings_ery"] = {}
        st.session_state["ratings_ery"][eryth["caption"]] = rating
erythro_text = st.text_area("Kommentar zu den Erythrozyten", key="erythro_text")

# Neutrophile Granulozyten Beurteilung
st.subheader("Neutrophile Granulozyten Beurteilung")
cols_neutro = st.columns(5)
for idx, neut in enumerate(neutro):
    col = cols_neutro[idx % 5]
    with col:
        st.image(neut["path"], caption=neut["caption"], use_container_width=True)
        rating = st.slider(
            f"Bewerte die Zelle: {neut['caption']}",
            label_visibility="collapsed",
            min_value=0,
            max_value=3,
            value=0,
            step=1,
            key=f"rating_neutro_{idx}"
        )
        if "ratings_neutro" not in st.session_state:
            st.session_state["ratings_neutro"] = {}
        st.session_state["ratings_neutro"][neut["caption"]] = rating
neutro_text = st.text_area("Kommentar zu den Neutrophilen Granulozyten", key="neutro_text")

# Lymphozyten Beurteilung
st.subheader("Lymphozyten Beurteilung")
cols_lympho = st.columns(5)
for idx, lymph in enumerate(lympho):
    col = cols_lympho[idx % 5]
    with col:
        st.image(lymph["path"], caption=lymph["caption"], use_container_width=True)
        rating = st.slider(
            f"Bewerte die Zelle: {lymph['caption']}",
            label_visibility="collapsed",
            min_value=0,
            max_value=3,
            value=0,
            step=1,
            key=f"rating_lympho_{idx}"
        )
        if "ratings_lympho" not in st.session_state:
            st.session_state["ratings_lympho"] = {}
        st.session_state["ratings_lympho"][lymph["caption"]] = rating
lympho_text = st.text_area("Kommentar zu den Lymphozyten", key="lympho_text")

# Thrombozyten Beurteilung
st.subheader("Thrombozyten Beurteilung")
cols_thrombo = st.columns(5)
for idx, throm in enumerate(thrombo):
    col = cols_thrombo[idx % 5]
    with col:
        st.image(throm["path"], caption=throm["caption"], use_container_width=True)
        rating = st.slider(
            f"Bewerte die Zelle: {throm['caption']}",
            label_visibility="collapsed",
            min_value=0,
            max_value=3,
            value=0,
            step=1,
            key=f"rating_thrombo_{idx}"
        )
        if "ratings_thrombo" not in st.session_state:
            st.session_state["ratings_thrombo"] = {}
        st.session_state["ratings_thrombo"][throm["caption"]] = rating
thrombo_text = st.text_area("Kommentar zu den Thrombozyten", key="thrombo_text")

# Button zum Speichern der Beurteilung
