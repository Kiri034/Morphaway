import streamlit as st
import pandas as pd  # Wir benötigen pandas, um mit DataFrames zu arbeiten

# Beispiel einer angepassten DataManager Klasse
class DataManager:
    def __init__(self):
        if "data_df" not in st.session_state:
            st.session_state["data_df"] = pd.DataFrame(columns=["selected_option", "praep_name", "total_count"])

    def append_record(self, session_state_key: str, record_dict: dict):
        df = st.session_state.get(session_state_key)
        if df is not None:
            new_entry = pd.DataFrame([record_dict])
            updated_df = pd.concat([df, new_entry], ignore_index=True)
            st.session_state[session_state_key] = updated_df
        else:
            raise ValueError(f"Kein DataFrame gefunden für den Schlüssel: {session_state_key}")


# Titel der Seite
st.title("Cell Counter")

# Funktion zum Zurücksetzen des Total Count und der Session-Variablen
def reset_all():
    for i in range(1, 19):  # 18 Buttons
        st.session_state[f"button_{i}_count"] = 0
    st.session_state["total_count"] = 0  # Zurücksetzen des Gesamtzählers
    st.session_state["praep_name"] = ""  # Zurücksetzen des Präparatnamens
    st.session_state["selected_option"] = None  # Zurücksetzen der Auswahloption

# Initialisierung von 'data_df' falls nicht vorhanden (z.B. als leeres DataFrame)
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=["selected_option", "praep_name", "total_count"])

# Überprüfen, ob ein Präparatname bereits in st.session_state gespeichert ist
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

# Zeige das Eingabefeld nur, wenn der Präparatname noch nicht eingegeben wurde
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:", key="praep_name_input")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    # Zeige den gespeicherten Präparatnamen an
    st.markdown(f"### Präparat: *{st.session_state['praep_name']}*")

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
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"],
            key="function_select"
        )

    # Initialisiere Zähler für jeden Button im Session State
    for i in range(1, 19):  # 18 Bilder
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Berechne den Total Counter
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))

    if st.button("🔙 Rückgängig", key="undo_button"):
        last = st.session_state.get("last_clicked_button")
        if last and st.session_state.get(last, 0) > 0:
            st.session_state[last] -= 1
        else:
            st.warning("Kein letzter Klick zum Rückgängig machen vorhanden.")
        st.session_state["last_clicked_button"] = None  # Setze den letzten Klick zurück
    # Speichere den letzten geklickten Button   

    # Anzeige des Gesamtzählers
    st.markdown(f"### Gesamtzahl: *{total_count}*")

    # Liste der Bildnamen und Beschriftungen
    images = [
        {"path": "https://via.placeholder.com/150?text=Button+1", "label": "Lymphozyt"},
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

    cols = st.columns(4)  # 4 Spalten pro Reihe

    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            if st.button("", key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1
            st.image(image["path"], use_container_width=True)
            st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}", use_container_width=True)

    # Reset-Button nach den Bild-Buttons
    if st.button("Refresh", key="refresh_button"):
        reset_all()

    # --- Save Cellcount data ---
    if st.button("Jetzt Auswerten", key="auswertung_button"):
        try:
            # Speichere die Daten
            DataManager().append_record(
                session_state_key='data_df',
                record_dict={
                    'selected_option': st.session_state["selected_option"],
                    'praep_name': st.session_state["praep_name"],
                    'total_count': total_count,
                    'timestamp': datetime.datetime.now() 
                }
            )

            # Wechsel zur Auswertungsseite
            st.switch_page("pages/2_Auswertung.py")  # Achte darauf, dass der Seitenname stimmt
        except Exception as e:
            st.error(f"Fehler beim Speichern der Daten: {e}")