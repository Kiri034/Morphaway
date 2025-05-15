import streamlit as st
import pandas as pd
import datetime  # Nicht vergessen!

# DataManager bleibt wie gehabt...
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

# Titel
st.title("Cell Counter")

# Reset-Funktion
def reset_all():
    for i in range(1, 19):
        st.session_state[f"button_{i}_count"] = 0
    st.session_state["total_count"] = 0
    st.session_state["praep_name"] = ""
    st.session_state["selected_option"] = None
    st.session_state["last_clicked_button"] = None

# Initialisierung
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(columns=["selected_option", "praep_name", "total_count"])

if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

if "last_clicked_button" not in st.session_state:
    st.session_state["last_clicked_button"] = None

if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:", key="praep_name_input")
    if praep_name:
        st.session_state["praep_name"] = praep_name
else:
    st.markdown(f"### Präparat: *{st.session_state['praep_name']}*")

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

    for i in range(1, 19):
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Rückgängig-Button
    if st.button("🔙 Rückgängig", key="undo_button"):
        last = st.session_state.get("last_clicked_button")
        if last and st.session_state.get(last, 0) > 0:
            st.session_state[last] -= 1
        else:
            st.warning("Kein letzter Klick zum Rückgängig machen vorhanden.")
        st.session_state["last_clicked_button"] = None

    # Buttons anzeigen
    images = [ ... ]  # Dein Bild-Array wie bisher
    cols = st.columns(4)

    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            btn_key = f"button_{idx + 1}"
            count_key = f"{btn_key}_count"
            if st.button("", key=btn_key):
                st.session_state[count_key] += 1
                st.session_state["last_clicked_button"] = count_key  # ← Wichtig!
            st.image(image["path"], use_container_width=True)
            st.write(f"{image['label']} - {st.session_state[count_key]}", use_container_width=True)

    # Dynamische Total-Count-Anzeige nach dem Klick
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 19))
    st.markdown(f"### Gesamtzahl: *{total_count}*")

    if st.button("Refresh", key="refresh_button"):
        reset_all()

    if st.button("Jetzt Auswerten", key="auswertung_button"):
        try:
            DataManager().append_record(
                session_state_key='data_df',
                record_dict={
                    'selected_option': st.session_state["selected_option"],
                    'praep_name': st.session_state["praep_name"],
                    'total_count': total_count,
                    'timestamp': datetime.datetime.now()
                }
            )
            st.switch_page("pages/2_Auswertung.py")
        except Exception as e:
            st.error(f"Fehler beim Speichern der Daten: {e}")
