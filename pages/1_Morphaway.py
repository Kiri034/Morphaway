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

    # Zeige den Total Counter oben an
    st.markdown(
        f"<h2 style='text-align: center; color: white; padding: 10px;'>Total Klicks: {total_count}</h2>",
        unsafe_allow_html=True
    )

    # Überprüfen, ob die gewünschte Anzahl an Klicks erreicht wurde
    if (st.session_state["selected_option"] == "50 Zellen differenzieren" and total_count >= 50) or \
       (st.session_state["selected_option"] == "100 Zellen differenzieren" and total_count >= 100) or \
       (st.session_state["selected_option"] == "200 Zellen differenzieren" and total_count >= 200):
        # Blockiere die gesamte Benutzeroberfläche und zeige eine Vollbild-Meldung mit Button
        st.markdown(
            """
            <style>
            .fullscreen-message {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                font-size: 2rem;
                z-index: 9999;
            }
            .button-container {
                margin-top: 20px;
            }
            </style>
            <div class="fullscreen-message">
                🎉 Du hast die gewünschte Anzahl an Zellen erreicht! 🎉
                <div class="button-container">
            """,
            unsafe_allow_html=True
        )

        # Streamlit-Button für die Navigation
        if st.button("Auswertung starten"):
            st.session_state["current_page"] = "Auswertung"

        st.markdown("</div></div>", unsafe_allow_html=True)