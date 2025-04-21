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
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite auswählen", ["Home", "Cell Counter", "History"])

# Inhalte basierend auf der Auswahl anzeigen
if page == "Home":
    home_page()
elif page == "Cell Counter":
    cell_counter_page()
elif page == "History":
    history_page()

    # Navigation mit Buttons im Hauptbereich
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"  # Standardseite

# Buttons für die Navigation
st.write("### Navigation")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Home"):
        st.session_state.current_page = "Home"
with col2:
    if st.button("Cell Counter"):
        st.session_state.current_page = "Cell Counter"
with col3:
    if st.button("History"):
        st.session_state.current_page = "History"

# Inhalte basierend auf der aktuellen Seite anzeigen
if st.session_state.current_page == "Home":
    home_page()
elif st.session_state.current_page == "Cell Counter":
    cell_counter_page()
elif st.session_state.current_page == "History":
    history_page()