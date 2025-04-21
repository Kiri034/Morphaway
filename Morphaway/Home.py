import streamlit as st

# Funktionen für die Seiten
def home_page():
    st.title("Hallo, Streamlit!")
    st.write("Dies ist eine einfache Streamlit-App.")

def cell_counter_page():
    st.title("Cell Counter")
    st.write("Hier kannst du Zellen zählen.")
    # Beispiel für eine einfache Zählerfunktion
    if "count" not in st.session_state:
        st.session_state.count = 0

    if st.button("Zelle hinzufügen"):
        st.session_state.count += 1

    st.write(f"Anzahl der gezählten Zellen: {st.session_state.count}")

def history_page():
    st.title("History")
    st.write("Hier kannst du die Historie einsehen.")
    st.write("Funktionalität wird noch hinzugefügt.")

# Sidebar-Navigation
st.sidebar.title("Morphaway")
page = st.sidebar.radio("Seite auswählen", ["Home", "Cell Counter", "History"])

# Inhalte basierend auf der Auswahl anzeigen
if page == "Home":
    home_page()
elif page == "Cell Counter":
    cell_counter_page()
elif page == "History":
    history_page()


