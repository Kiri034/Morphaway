import streamlit as st

st.title("Cell Counter")

# Auswahlmöglichkeit für die Funktionalität
option = st.selectbox(
    "Wähle eine Funktion:",
    ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren", "Zellbeurteilung"]
)

# Inhalte basierend auf der Auswahl anzeigen
if option == "50 Zellen differenzieren":
    st.write("Du hast ausgewählt: 50 Zellen differenzieren.")
    st.write("Hier kannst du die Funktionalität für das Differenzieren von 50 Zellen hinzufügen.")
elif option == "100 Zellen differenzieren":
    st.write("Du hast ausgewählt: 100 Zellen differenzieren.")
    st.write("Hier kannst du die Funktionalität für das Differenzieren von 100 Zellen hinzufügen.")
elif option == "200 Zellen differenzieren":
    st.write("Du hast ausgewählt: 200 Zellen differenzieren.")
    st.write("Hier kannst du die Funktionalität für das Differenzieren von 200 Zellen hinzufügen.")
elif option == "Zellbeurteilung":
    st.write("Du hast ausgewählt: Zellbeurteilung.")
    st.write("Hier kannst du die Funktionalität für die Zellbeurteilung hinzufügen.")