import streamlit as st

# Titel der Seite
st.title("Cell Counter")

# Eingabe für den Namen des Präparats
praep_name = st.text_input("Gib einen Namen für das Präparat ein:")

# Speichere den Präparatnamen in st.session_state
if praep_name:
    st.session_state["praep_name"] = praep_name

# Überprüfen, ob ein Präparatname eingegeben wurde
if not praep_name:
    st.warning("Bitte gib einen Namen für das Präparat ein, bevor du fortfährst.")
else:
    # Überprüfen, ob eine Option bereits ausgewählt wurde
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None

    # Zeige die Auswahloptionen nur, wenn noch keine Option ausgewählt wurde
    if st.session_state["selected_option"] is None:
        st.session_state["selected_option"] = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"]
        )
    else:
        # Präparatname und Auswahlmöglichkeiten verschwinden
        st.write(f"Du hast ausgewählt: {st.session_state['selected_option']}")

    # Initialisiere Zähler für jeden Button im Session State
    for i in range(1, 19):  # 18 Bilder
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Berechne den Total Counter
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

    # Zeige den Total Counter oben an (größer dargestellt)
    st.markdown(f"<h2 style='text-align: center; color: black;'>Total Klicks: {total_count}</h2>", unsafe_allow_html=True)

    # Liste der Bildnamen und Beschriftungen
    images = [
        {"path": "https://via.placeholder.com/150?text=Button+1", "label": "Lymphozyt"},
        {"path": "https://via.placeholder.com/150?text=Button+2", "label": "Monozyt"},
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

    # Anordnung der Buttons in mehreren Reihen
    cols = st.columns(4)  # 4 Spalten pro Reihe

    for idx, image in enumerate(images):
        col = cols[idx % 4]  # Wähle die Spalte basierend auf dem Index
        with col:
            # Klickbares Bild als Button
            if st.button("", key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1
            st.image(image["path"], use_column_width=True)
            # Beschriftung unter dem Bild
            st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}")