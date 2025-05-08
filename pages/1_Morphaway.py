import streamlit as st

# Titel der Seite
st.title("Cell Counter")

# Überprüfen, ob ein Präparatname bereits in st.session_state gespeichert ist
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

# Zeige das Eingabefeld nur, wenn der Präparatname noch nicht eingegeben wurde
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    # Zeige den gespeicherten Präparatnamen an
    st.markdown(f"### Präparat: **{st.session_state['praep_name']}**")

# Überprüfen, ob ein Präparatname eingegeben wurde
if not st.session_state["praep_name"]:
    st.warning("Bitte gib einen Namen für das Präparat ein, bevor du fortfährst.")
else:
    # Initialisiere "selected_option", falls es nicht existiert
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None

    # Zeige die Auswahloptionen nur, wenn noch keine Option ausgewählt wurde
    if st.session_state["selected_option"] is None:
        st.session_state["selected_option"] = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"]
        )

    # Initialisiere Zähler für jeden Button im Session State
    for i in range(1, 19):  # 18 Bilder
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Berechne den Total Counter
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

    # Zeige den Total Counter oben an (größer dargestellt und in Weiß)
    st.markdown(
        f"<h2 style='text-align: center; color: white; padding: 10px;'>Total Klicks: {total_count}</h2>",
        unsafe_allow_html=True
    )

    # Überprüfen, ob die gewünschte Anzahl an Klicks erreicht wurde
    if (st.session_state["selected_option"] == "50 Zellen differenzieren" and total_count >= 50) or \
       (st.session_state["selected_option"] == "100 Zellen differenzieren" and total_count >= 100) or \
       (st.session_state["selected_option"] == "200 Zellen differenzieren" and total_count >= 200):
        zielwert = int(st.session_state["selected_option"].split()[0])
total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

if total_count >= zielwert:
    # Overlay mit getrenntem Button-Container
    st.markdown(
        """
        <style>
        .fullscreen-message {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            z-index: 9998;
            pointer-events: none;
        }

        .button-layer {
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            pointer-events: auto;
        }

        .real-button {
            font-size: 1.5rem;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        .real-button:hover {
            background-color: #0056b3;
        }
        </style>

        <div class="fullscreen-message">
            🎉 Du hast die gewünschte Anzahl an Zellen erreicht! 🎉
            <br><br>
            <span style="font-size:1rem;">Klicke auf den Button unten, um zur Auswertung zu wechseln.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Jetzt platzieren wir den Streamlit-Button sichtbar und klickbar in einer "freien" Schicht
    st.markdown('<div class="button-layer">', unsafe_allow_html=True)
    if st.button("➡️ Zur Auswertung", key="go_to_eval"):
        st.switch_page("2_Auswertung.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Stop, um restlichen Inhalt zu unterdrücken
    st.stop()
# Blockiere die gesamte Benutzeroberfläche und zeige eine Vollbild-Meldung mit Button

        # Zielwert extrahieren
zielwert = int(st.session_state["selected_option"].split()[0])

# Wenn die gewünschte Anzahl an Klicks erreicht wurde
if total_count >= zielwert:
    # Overlay anzeigen
    st.markdown(
        """
        <style>
        .fullscreen-message {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.85);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 2rem;
            z-index: 9999;
        }
        </style>
        <div class="fullscreen-message">
            🎉 Du hast die gewünschte Anzahl an Zellen erreicht! 🎉
            <br><br>
            <span style="font-size:1rem;">Klicke unten auf den Button, um zur Auswertung zu wechseln.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Abstand für sichtbaren Button
    st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    # Echter Button für Navigation
    if st.button("➡️ Zur Auswertung"):
        st.switch_page("2_Auswertung.py")
    
    # Stoppe die App, um keine weiteren UI-Elemente mehr zu zeigen
    st.stop()


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