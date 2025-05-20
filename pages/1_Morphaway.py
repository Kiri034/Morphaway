import streamlit as st
import pandas as pd
import datetime  # Für den Timestamp

# Beispiel einer angepassten DataManager Klasse
class DataManager:
    def __init__(self):
        if "data_df" not in st.session_state:
            st.session_state["data_df"] = pd.DataFrame(
                columns=["selected_option", "praep_name", "total_count", "erythroblast_count", "timestamp"]
            )

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
    for i in range(1, 15):  # 14 Buttons
        st.session_state[f"button_{i}_count"] = 0
    st.session_state["total_count"] = 0  # Zurücksetzen des Gesamtzählers
    st.session_state["praep_name"] = ""  # Zurücksetzen des Präparatnamens
    st.session_state["selected_option"] = None  # Zurücksetzen der Auswahloption

# Initialisierung von 'data_df' falls nicht vorhanden (z.B. als leeres DataFrame)
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(
        columns=["selected_option", "praep_name", "total_count", "erythroblast_count", "timestamp"]
    )
# Überprüfen, ob ein Präparatname bereits in st.session_state gespeichert ist
if "praep_name" not in st.session_state:
    st.session_state["praep_name"] = ""

# Präparatname-Eingabe mit Bestätigungsbutton
if not st.session_state["praep_name"]:
    praep_name = st.text_input("Gib einen Namen für das Präparat ein:", key="praep_name_input")
    if st.button("Diffrenzieren", key="confirm_praep_name") and praep_name:
        st.session_state["praep_name"] = praep_name
# Counter-Logik
else:
    # Zeige den gespeicherten Präparatnamen an
    st.markdown(f"### Präparat: *{st.session_state['praep_name']}*")

    # Auswahloption NUR anzeigen, wenn noch keine Auswahl getroffen wurde
    if not st.session_state.get("selected_option"):
        selected = st.radio(
            "Wähle eine Funktion:",
            ["50 Zellen differenzieren", "100 Zellen differenzieren", "200 Zellen differenzieren"],
            key="function_select"
        )
        if selected:
            st.session_state["selected_option"] = selected

    # Initialisiere Zähler für jeden Button im Session State
    for i in range(1, 15):  # 14 Bilder
        if f"button_{i}_count" not in st.session_state:
            st.session_state[f"button_{i}_count"] = 0

    # Rückgängig Button
    if st.button("🔙 Rückgängig", key="undo_button"):
        for i in range(1, 15):
            if st.session_state[f"button_{i}_count"] > 0:
                st.session_state[f"button_{i}_count"] -= 1
                break  # Wir machen nur einen Rückgängig-Schritt

    # Liste der Bildnamen und Beschriftungen
    images = [
        {"path": "https://cdn.cellwiki.net/db/cells/page-28/gallery-55/003.jpg", "label": "Lymphozyt"},
        {"path": "https://cdn.cellwiki.net/db/aberrations/page-73/gallery-181/008.jpg", "label": "reaktiver Lymphozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-32/gallery-63/002.jpg", "label": "Monozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-21/gallery-30/011.jpg", "label": "Eosinophile Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-17/gallery-17/006.jpg", "label": "Basophile Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-26/gallery-45/003.jpg", "label": "Segmentkernige Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-25/gallery-44/003.jpg", "label": "Stabkernige Gc*"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-340/gallery-1537/004.jpg", "label": "Blasten"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-22/gallery-41/002.jpg", "label": "Promyelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-23/gallery-42/001.jpg", "label": "Myelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-24/gallery-43/002.jpg", "label": "Metamyelozyt"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-30/gallery-57/001.jpg", "label": "Plasmazelle"},
        {"path": "https://cdn.cellwiki.net/db/cells/page-36/gallery-75/004.jpg", "label": "Erythroblast"},
        {"path": "https://cdn.cellwiki.net/db/pathology/page-372/gallery-1739/030.jpg", "label": "smudged cells"},
    ]

    # Zuerst Buttons zählen, dann anzeigen!
    cols = st.columns(4)  # 4 Spalten pro Reihe
    for idx, image in enumerate(images):
        col = cols[idx % 4]
        with col:
            if st.button("", key=f"button_{idx + 1}"):
                st.session_state[f"button_{idx + 1}_count"] += 1

    # Nach allen Button-Events: Einzelwerte unter den Bildern anzeigen
cols = st.columns(4)  # 4 Spalten pro Reihe
for idx, image in enumerate(images):
    col = cols[idx % 4]
    with col:
        if st.button("", key=f"button_{idx + 1}"):
            st.session_state[f"button_{idx + 1}_count"] += 1
        st.image(image["path"], use_container_width=True)
        st.write(f"{image['label']} - {st.session_state[f'button_{idx + 1}_count']}", use_container_width=True)


    # Erythroblast separat zählen (Button 13)
    erythroblast_count = st.session_state["button_13_count"]
    # Gesamtzähler OHNE Erythroblast (alle außer Button 13)
    total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 15) if i != 13)

    # Anzeige des Gesamtzählers
    st.markdown(f"### Gesamtzahl: *{total_count}*")
    st.markdown(f"### Erythroblasten: *{erythroblast_count}*")

    # Maximale Zellzahl aus der Auswahl extrahieren
    max_cells = int(st.session_state["selected_option"].split()[0])

    # Warnmeldungen bei bestimmten Schwellenwerten
    if total_count == max_cells:
        st.warning(f"⚠️ Maximale Anzahl ausgezählter Zellen ({max_cells}) erreicht.")
    elif total_count > max_cells:
        st.error(f"❌ Grenze von {max_cells} Zellen überschritten! Bitte zurücksetzen.")

    # Reset-Button nach den Bild-Buttons
    if st.button("Refresh", key="refresh_button"):
        reset_all()

    # --- Save Cellcount data ---
    if st.button("Jetzt Auswerten", key="auswertung_button"):
        try:
            # Erythroblast separat zählen (Button 13)
            erythroblast_count = st.session_state["button_13_count"]
            # Gesamtzähler OHNE Erythroblast (nur Buttons 1-12 und 14)
            total_count = sum(st.session_state[f"button_{i}_count"] for i in range(1, 15) if i != 13)

            # Speichere die Daten, Erythroblast separat
            DataManager().append_record(
                session_state_key='data_df',
                record_dict={
                    'selected_option': st.session_state["selected_option"],
                    'praep_name': st.session_state["praep_name"],
                    'total_count': total_count,
                    'erythroblast_count': erythroblast_count,
                    'timestamp': datetime.datetime.now() 
                }
            )

            # Wechsel zur Auswertungsseite
            st.switch_page("pages/2_Auswertung.py")  # Achte darauf, dass der Seitenname stimmt
        except Exception as e:
            st.error(f"Fehler beim Speichern der Daten: {e}")