import streamlit as st

# Sidebar-Navigation
st.sidebar.title("Morphaway")
page = st.sidebar.radio("Seite auswählen", ["Home", "Cell Counter", "History"])

# Inhalte basierend auf der Auswahl anzeigen
if page == "Home":
    st.title("Home")
    st.write("Willkommen bei Morphaway! Morphaway ist eine App, die Dir hilft, Zellen zu zählen und ihre Morphologie zu analysieren.")
    st.write("Hier kannst Du die verschiedenen Funktionen der App erkunden.")
    st.write("Wähle eine der Optionen in der linken Seitenleiste aus, um fortzufahren.")
elif page == "Cell Counter":
    st.title("Cell Counter")
    st.write("Dies ist eine leere Seite für Cell Counter.")
elif page == "History":
    st.title("History")
    st.write("Dies ist eine leere Seite für History.")

