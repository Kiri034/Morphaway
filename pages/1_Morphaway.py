import streamlit as st

# Titel der Seite
st.title("Cell Counter")

# Überprüfen, ob ein Präparatname bereits gespeichert ist
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

# Eingabefeld für Präparatname
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    st.markdown(f"### Präparat: **{st.session_state['praep_name']}**")

# Nur fortfahren, wenn Name eingegeben wurde
if not st.session_state["praep_name"]:
    st.warning("Bitte gib einen Namen für das Präparat ein, bevor du fortfährst.")
else:
    # Ziel-Auswahl initialisieren
    if "selected_option" not in st.session_state:
        st.session_state["selected_option"] = None

    # Auswahl nur einmal anzeigen
    if st.session_state["selected_option"] is None:
        st.session_state["selected_option"] = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"]
        )

    # Initialisiere Button-Zähler für 18 Buttons
    for i in range(1, 19):
        key = f"button_{i}_count"
        if key not in st.session_state:
            st.session_state[key] = 0

    # Gesamtzähler berechnen
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))
    zielwert = int(st.session_state["selected_option"].split()[0])

    # Gesamtzähler anzeigen
    st.markdown(
        f"<h2 style='text-align: center; color: white; padding: 10px;'>Total Klicks: {total_count}</h2>",
        unsafe_allow_html=True
    )

    # ✅ Wenn Ziel erreicht: Overlay + echter Button zur Auswertung
    if total_count >= zielwert:
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

        # Sichtbarer und klickbarer Button
        st.markdown('<div class="button-layer">', unsafe_allow_html=True)
        if st.button("➡️ Zur Auswertung", key="go_to_eval"):
            st.switch_page("2_Auswertung.py")
        st.markdown('</div>', unsafe_allow_html=True)

        # App stoppen, um restlichen Inhalt auszublenden
        st.stop()

    # Bilddaten
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
        {"path": "https://via.placeholder.com/150?text=Button+12", "label": "Reactive Lymphozyt"},
        {"path": "https://via.placeholder.com/150?text=Button+13", "label": "Abnormale Lymphozyten"},
        {"path": "https://via.placeholder.com/150?text=Button+14", "label": "Large granular lymphocyte"},
        {"path": "https://via.placeholder.com/150?text=Button+15", "label": "NRBC"},
        {"path": "https://via.placeholder.com/150?text=Button+16", "label": "Mastzelle"},
        {"path": "https://via.placeholder.com/150?text=Button+17", "label": "Plasmazelle"},
        {"path": "https://via.placeholder.com/150?text=Button+18", "label": "Smudged cells"},
    ]

    # Buttons und Bilder anzeigen
    cols = st.columns(4)
    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            if st.button("", key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1
            st.image(image["path"], use_column_width=True)
            st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}")
