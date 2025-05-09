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

# Initialisiere Session States
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = None
for i in range(1, 19):
    if f"button_{i}_count" not in st.session_state:
        st.session_state[f"button_{i}_count"] = 0

# Präparatname eingeben
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    st.markdown(f"### Präparat: **{st.session_state['praep_name']}**")

# Auswahloption
if st.session_state["praep_name"] and st.session_state["selected_option"] is None:
    st.session_state["selected_option"] = st.radio(
        "Wähle eine Funktion:",
        ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"]
    )

# Wenn kein Präparatname, Hinweis anzeigen
if not st.session_state["praep_name"]:
    st.warning("Bitte gib einen Namen für das Präparat ein, bevor du fortfährst.")
else:
    # Berechne Total Count
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

    # Zeige Total Count
    st.markdown(
        f"<h2 style='text-align: center; color: white; padding: 10px;'>Total Klicks: {total_count}</h2>",
        unsafe_allow_html=True
    )

    # Max Count festlegen
    selected = st.session_state["selected_option"]
    if selected == "50 Zellen differenzieren":
        max_count = 50
    elif selected == "100 Zellen differenzieren":
        max_count = 100
    elif selected == "200 Zellen differenzieren":
        max_count = 200
    else:
        max_count = 0

    # Hinweise zum Zählziel
    if total_count == max_count:
        st.warning(f"Du hast die gewünschte Anzahl von {max_count} Zellen erreicht. Du kannst jetzt die Auswertung starten.")
        if st.button("Jetzt Auswerten"):
            st.switch_page("pages/2_Auswertung.py")
    elif total_count > max_count:
        st.info(f"Achtung: Du hast das Limit von {max_count} Zellen überschritten. Weitere Klicks sind trotzdem möglich.")

    # Bilder mit Plus/Minus Buttons
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

    # Anordnung in 4 Spalten
    cols = st.columns(4)
    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            st.image(image["path"], use_column_width=True)
            st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}")

            # Plus- und Minus-Buttons
            plus, minus = st.columns(2)
            with plus:
                if st.button("+", key=f"plus_{idx + 1}"):
                    st.session_state[f"button_{idx + 1}_count"] += 1
            with minus:
                if st.button("-", key=f"minus_{idx + 1}"):
                    if st.session_state[f"button_{idx + 1}_count"] > 0:
                        st.session_state[f"button_{idx + 1}_count"] -= 1

    # Reset-Button
    st.markdown("---")
    if st.button("Refresh"):
        reset_all()
