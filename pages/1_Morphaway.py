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

    for i in range(1, 15):
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    if st.button("🔙", key="undo_button"):
        for i in range(14, 0, -1):
            if st.session_state[f"button_{i}_count"] > 0:
                st.session_state[f"button_{i}_count"] -= 1
                break

    images = [
        {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/Lymphozyt.png", "label": "Lymphozyt"},
        {"path": "https://cdn.cellwiki.net/db/aberrations/page-73/gallery-181/008.jpg", "label": "reaktiver Lymphozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-32/gallery-63/002.jpg", "label": "Monozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-21/gallery-30/011.jpg", "label": "Eosinophile Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-17/gallery-17/006.jpg", "label": "Basophile Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-26/gallery-45/003.jpg", "label": "Segmentkernige Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-25/gallery-44/003.jpg", "label": "Stabkernige Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-340/gallery-1537/004.jpg", "label": "Blasten"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-22/gallery-41/002.jpg", "label": "Promyelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-23/gallery-42/001.jpg", "label": "Myelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-24/gallery-43/002.jpg", "label": "Metamyelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-30/gallery-57/001.jpg", "label": "Plasmazelle"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-36/gallery-75/004.jpg", "label": "Erythroblast"},
        {"path": "https://cdn.cellwiki.net/db/pathology/page-372/gallery-1739/030.jpg", "label": "smudged cells"},
    ]

    cols = st.columns(4)
    clicked_button_index = None  # Merken, welcher gedrückt wurde

    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            st.image(image["path"], use_container_width=True)
            btn_label = f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}"
            if st.button(btn_label, key=f"button_{idx + 1}"):
                clicked_button_index = idx + 1

    if clicked_button_index:
        st.session_state[f"button_{clicked_button_index}_count"] += 1
        st.rerun()

    erythroblast_count = st.session_state["button_13_count"]
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 15) if i != 13)

    st.markdown(f"### Gesamtzahl: *{total_count}*")
    st.markdown(f"### Erythroblasten: *{erythroblast_count}*")

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

    # Sticky-Note für Gesamtzähler, angepasst an Hintergrund (leicht lila, kein Rahmen)
    st.markdown(
        """
        <style>
        .sticky-counter {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 9999;
            padding: 5px 12px;
            font-weight: bold;
            font-size: 18px;
            color: #6a4c93;  /* dunkles Lila */
            background-color: #fbeaff;  /* helles Lila, wie Hintergrund */
            border-radius: 8px;
            box-shadow: 0 0 6px rgba(106, 76, 147, 0.15);
        }
        </style>
        <div class="sticky-counter">
            Gesamtzähler: <span style="font-size:24px;">{total_count}</span>
        </div>
        """.format(total_count=total_count), unsafe_allow_html=True
    )

    if st.button("⟳", key="refresh_button"):
        reset_all()

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
        st.experimental_set_query_params()  # Falls du irgendwelche Query Params zurücksetzen willst
        st.experimental_rerun()  # Oder st.switch_page("pages/2_Auswertung.py") wenn du das nutzt
