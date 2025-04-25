import streamlit as st

st.title("Cell Counter")

praep_name = st.text_input(" Gib einen Namen für das Präparat ein:")

# Auswahlmöglichkeit für die Funktionalität
option = st.radio(
    "Wähle eine Funktion:",
    ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"]
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

import streamlit as st

st.title("Leukozyten Differenzierung")

# Initialisiere Zähler für jeden Button im Session State
for i in range(1, 18):
    if f"button_{i}_count" not in st.session_state:
        st.session_state[f"button_{i}_count"] = 0

# Liste der Bildnamen und Beschriftungen
images = [
    {"path": "https://via.placeholder.com/150?text=Button+1", "label": "Lymphozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+2", "label": "Monozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+3", "label": "Eosinophil"},
    {"path": "https://via.placeholder.com/150?text=Button+4", "label": "Basophil"},
    {"path": "https://via.placeholder.com/150?text=Button+5", "label": "Segmentkernige Granulozyten"},
    {"path": "https://via.placeholder.com/150?text=Button+5", "label": "Stabkernige Granulozyten"},
    {"path": "https://via.placeholder.com/150?text=Button+6", "label": "Erythroblast"},
    {"path": "https://via.placeholder.com/150?text=Button+7", "label": "Blasten"},
    {"path": "https://via.placeholder.com/150?text=Button+8", "label": "Promyelozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+9", "label": "Myelozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+10", "label": "Metamyelozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+11", "label": "reactive Lymphozyt"},
    {"path": "https://via.placeholder.com/150?text=Button+12", "label": "Abnormale Lymphozyten"},
    {"path": "https://via.placeholder.com/150?text=Button+13", "label": "Large granular lymphocyte"},
    {"path": "https://via.placeholder.com/150?text=Button+14", "label": "NRBC"},
    {"path": "https://via.placeholder.com/150?text=Button+15", "label": "Mastzelle"},
    {"path": "https://via.placeholder.com/150?text=Button+16", "label": "Plasmazelle"},
    {"path": "https://via.placeholder.com/150?text=Button+17", "label": "smudged cells"},   
]

# Anordnung der Buttons in mehreren Reihen
cols = st.columns(4)  # 4 Spalten pro Reihe

for idx, image in enumerate(images):
    col = cols[idx % 4]  # Wähle die Spalte basierend auf dem Index
    with col:
        if st.button(image["label"]):
            st.session_state[f"button_{idx + 1}_count"] += 1
        st.image(image["path"], caption=image["label"], use_column_width=True)
        st.write(f"Geklickt: {st.session_state[f'button_{idx + 1}_count']} Mal")