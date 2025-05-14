import streamlit as st

# Titel der Seite
st.title("Cell Counter")

# Funktion zum Zurücksetzen des Total Count und der Session-Variablen
def reset_all():
    for i in range(1, 19):  # 18 Buttons
        st.session_state[f"button_{i}_count"] = 0
    st.session_state["total_count"] = 0
    st.session_state["praep_name"] = ""
    st.session_state["selected_option"] = None

# Initialisiere Session State Variablen
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None
for i in range(1, 19):
    if f"button_{i}_count" not in st.session_state:
        st.session_state[f"button_{i}_count"] = 0

# 1. Präparat Name eingeben
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:", key="praep_name_input")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    st.markdown(f"### Präparat: **{st.session_state['praep_name']}**")

    # 2. Funktion wählen
    if st.session_state["selected_option"] is None:
        st.session_state["selected_option"] = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"],
            key="function_select"
        )

    if st.session_state["selected_option"]:
        # Definiere die maximale Anzahl an Zellen
        max_cells = int(st.session_state["selected_option"].split()[0])  # Assumes "50 Zellen", "100 Zellen", "200 Zellen"

        # 3. Counter mit Bildern
        images = [
            {"path": "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/Lymphozyten.jpg", "label": "Lymphozyt"},
            {"path": "https://cdn.cellwiki.net/db/cells/page-32/gallery-63/002.jpg", "label": "Monozyt"},
            {"path": "https://via.placeholder.com/150?text=Button+3", "label": "Eosinophil"},
            {"path": "https://via.placeholder.com/150?text=Button+4", "label": "Basophil"},
            {"path": "https://via.placeholder.com/150?text=Button+5", "label": "Segmentkernige Granulozyten"},
            {"path": "https://via.placeholder.com/150?text=Button+6", "label": "Stabkernige Granulozyten"},
            {"path": "https://via.placeholder.com/150?text=Button+7", "label": "Erythroblast"},
            {"path": "https://via.placeholder.com/150?text=Button+8", "label": "Blasten"},
            {"path": "https://via.placeholder.com/150?text=Button+9", "label": "Promyelozyt"},
            {"path": "https://via.placeholder.com/150?text=Button+10", "label": "Myelozyt"},
            {"path": "https://via.placeholder.com/150?text=Button+11", "label": "Metamyelozyt"},
            {"path": "https://via.placeholder.com/150?text=Button+12", "label": "reactive Lymphozyt"},
            {"path": "https://via.placeholder.com/150?text=Button+13", "label": "Abnormale Lymphozyten"},
            {"path": "https://via.placeholder.com/150?text=Button+14", "label": "Large granular lymphocyte"},
            {"path": "https://via.placeholder.com/150?text=Button+15", "label": "NRBC"},
            {"path": "https://via.placeholder.com/150?text=Button+16", "label": "Mastzelle"},
            {"path": "https://via.placeholder.com/150?text=Button+17", "label": "Plasmazelle"},
            {"path": "https://via.placeholder.com/150?text=Button+18", "label": "smudged cells"},
        ]

        # Berechne den Total Counter
        total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

        # Anzeige des Gesamtzählers
        st.markdown(f"### Gesamtzahl: **{total_count}**")

        cols = st.columns(4)  # 4 Spalten pro Reihe
        for idx, image in enumerate(images):
            col = cols[idx % 4]
            with col:
                if st.button("", key=f"button_{idx + 1}"):
                    st.session_state[f"button_{idx + 1}_count"] += 1
                st.image(image["path"], use_container_width=True)
                st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}")

        # 4. Refresh Button und "Jetzt Auswerten" Button
        if st.button("Refresh", key="refresh_button"):
            reset_all()

        if total_count >= max_cells:
            st.warning(f"Die maximale Anzahl von {max_cells} Zellen wurde erreicht!")

        if st.button("Jetzt Auswerten", key="auswertung_button"):
            st.switch_page("pages/2_Auswertung.py")

        # Daten speichern
        from utils.data_manager import DataManager
        DataManager().append_record(session_state_key='data_df', record_dict=total_count)