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

st.title("🔬 Morphaway")

# Funktion zum Zurücksetzen des Zählers
def reset_all():
    for i in range(1, 15):
        st.session_state[f"button_{i}_count"] = 0
    st.session_state["total_count"] = 0
    st.session_state["praep_name"] = ""
    st.session_state["selected_option"] = None

# Initialisiere DataFrame bei Bedarf
if "data_df" not in st.session_state or st.session_state["data_df"].empty:
    st.session_state["data_df"] = pd.DataFrame(
        columns=["selected_option", "praep_name", "total_count", "erythroblast_count", "timestamp"]
    )

# Schritt 1: Präparatname eingeben
if "praep_name" not in st.session_state or not st.session_state["praep_name"]:
    st.info("Der Präparatname darf nur einmal verwendet werden. Wenn du denselben Namen nochmal brauchst, hänge eine Nummer an, z.B. 'Blutbild 2'.")

    existing_names = set(st.session_state["data_df"]["praep_name"]) if "praep_name" in st.session_state["data_df"].columns else set()

    with st.form("praep_form"):
        praep_name_input = st.text_input("Gib einen Namen für das Präparat ein:")
        submitted = st.form_submit_button("Differenzieren")

        if submitted:
            if praep_name_input and praep_name_input not in existing_names:
                st.session_state["praep_name"] = praep_name_input
                st.rerun()
            else:
                st.warning("Es existiert bereits ein Präparat mit diesem Namen oder der Name ist ungültig.")
else:
    st.markdown(f"### Präparat: *{st.session_state['praep_name']}*")

    selected = st.radio(
        "Wähle eine Funktion:",
        ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"],
        key="function_select"
    )
    st.session_state["selected_option"] = selected

    # Initialisiere Button-Zähler falls noch nicht vorhanden
    for i in range(1, 15):
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Gesamtzähler direkt nach Auswahlmöglichkeit anzeigen
    erythroblast_count = st.session_state["button_13_count"]
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 15) if i != 13)


    st.markdown(f"### Gesamtzahl: *{total_count}*")

    # Button zum Zurücksetzen der Zähler
    if st.button("🔙", key="undo_button"):
        for i in range(14, 0, -1):
            if st.session_state[f"button_{i}_count"] > 0:
                st.session_state[f"button_{i}_count"] -= 1
                st.rerun()

    images = [
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/lymph_round.png", "label": "Lymphozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/reaktlymph.png", "label": "reaktiver Lymphozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/reaktlymph.png", "label": "Monozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/eos_round.png", "label": "Eosinophile Gc*"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/baso_round.png", "label": "Basophile Gc*"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/seg_round.png", "label": "Segmentkernige Gc*"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/band_round.png", "label": "Stabkernige Gc*"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/blast_round.png", "label": "Blasten"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/promyelo_round.png", "label": "Promyelozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/myelo_round.png", "label": "Myelozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/metamyelo_round.png", "label": "Metamyelozyt"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/plasma_round.png", "label": "Plasmazelle"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/smudged_round.png", "label": "smudged cells"},
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/erythro_round.png", "label": "Erythroblast"}
    ]

    cols = st.columns(3)

    for idx, image in enumerate(images):
        col = cols[idx % 3]
        with col:
            st.image(image["path"], use_container_width=True)
            btn_label = f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}"
            if st.button(btn_label, key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1
                st.rerun()

    max_cells = int(st.session_state["selected_option"].split()[0])

   # Sticky-Note für Zielwarnung
    st.markdown(
        """
        <style>
        .sticky-alert {
            position: fixed;
            top: 80px;
            right: 10px;
            width: 300px;
            z-index: 9999;
            background-color: #fff3cd;
            padding: 15px;
            border: 1px solid #ffeeba;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        </style>
        """, unsafe_allow_html=True
    )

    if total_count >= max_cells:
        st.markdown(
            f"""
            <div class="sticky-alert">
                ⚠️ <strong>Ziel erreicht!</strong> Sie haben die Zielzahl von {max_cells} Zellen erreicht oder überschritten.
            </div>
            """, unsafe_allow_html=True
        )

    if st.button("⟳", key="refresh_button"):
        reset_all()
        st.rerun()

    if st.button("Jetzt Auswerten", key="auswertung_button"):
        DataManager().append_record(
            session_state_key='data_df',
            record_dict={
                'selected_option': st.session_state["selected_option"],
                'praep_name': st.session_state["praep_name"],
                'total_count': total_count,
                'erythroblast_count': erythroblast_count,
                'timestamp': datetime.datetime.now()
            }
        )
        st.switch_page("pages/2_Auswertung.py")
