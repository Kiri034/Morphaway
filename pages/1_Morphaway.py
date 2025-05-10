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

# Initialisiere Session State
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:", key="praep_name_input")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    st.markdown(f"### Präparat: **{st.session_state['praep_name']}**")

if not st.session_state["praep_name"]:
    st.warning("Bitte gib einen Namen für das Präparat ein, bevor du fortfährst.")
else:
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None

    if st.session_state["selected_option"] is None:
        st.session_state["selected_option"] = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"],
            key="function_select"
        )

    # Maximale Anzahl an Zellen basierend auf Auswahl
    if st.session_state["selected_option"] == "50 Zellen differenzieren":
        max_count = 50
    elif st.session_state["selected_option"] == "100 Zellen differenzieren":
        max_count = 100
    else:
        max_count = 200

    # Initialisiere Zähler für jeden Button
    for i in range(1, 19):
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Gesamtzähler berechnen
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))
    st.session_state["total_count"] = total_count  # falls für später nötig

    # Anzeige des Zählers
    st.metric("Gesamtanzahl Klicks", total_count)

    # Hinweis, wenn Ziel erreicht wurde 
    if total_count >= max_count:
        st.info(f"Du hast die gewünschte Anzahl von {max_count} Zellen erreicht. Du kannst jetzt die Auswertung starten.")
        if st.button("Jetzt Auswerten", key="auswertung_button"):
            st.switch_page("pages/2_Auswertung.py")

    # Bild-/Button-Liste
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

    # Layout in 4 Spalten
    cols = st.columns(4)

    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            if st.button("", key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1
            st.image(image["path"], use_column_width=True)
            st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}")

    # Refresh-Button
    if st.button("Refresh", key="refresh_button"):
        reset_all()