import streamlit as st


st.title("Home")
st.write("Willkommen bei Morphaway! Morphaway ist eine einfache und übersichtliche Variante, um ein Blutbild auszuzählen. ")
st.write("Durch eine individuelle Auswahl der Differenzier-Möglichkeiten ist unsere App sehr nutzerfreundlich aufgebaut und kann so in verschiedene Situationen angewendet werden. Ob du nur 50 Leukozyten differenzieren kannst, um deinem Dozenten schnell die prozentualen Zahlen nennen zu können, 100 für eine schnelle aber genauere Differenzierung oder aber eine vollständige Leukozytendifferenzierung mit 200 Zellen - mit Morphaway ist alles möglich.")
st.write("Während deiner Differenzierung kannst du deine gefundenen Zellen zählen und anschliessend werden deine Werte prozentual kalkuliert und grafisch dargestellt. Diese Daten sind nun auch zum PDF-Download verfügbar und können durch das eigene Nutzerlogin im Menü «History» auch später erneut abgerufen werden.")
st.write("Um direkt mit Deiner Differenzierung loszulegen, drücke auf den unteren Knopf. Für andere Funktionen kannst Du die Sidebar benutzen.")

# Query-Parameter auslesen
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]

if page == "home":
    st.title("Home")
    st.write("Willkommen bei Morphaway! Morphaway ist eine einfache und übersichtliche Variante, um ein Blutbild auszuzählen. ")
    st.write("Durch eine individuelle Auswahl der Differenzier-Möglichkeiten ist unsere App sehr nutzerfreundlich aufgebaut und kann so in verschiedene Situationen angewendet werden. Ob du nur 50 Leukozyten differenzieren kannst, um deinem Dozenten schnell die prozentualen Zahlen nennen zu können, 100 für eine schnelle aber genauere Differenzierung oder aber eine vollständige Leukozytendifferenzierung mit 200 Zellen - mit Morphaway ist alles möglich.")
    st.write("Während deiner Differenzierung kannst du deine gefundenen Zellen zählen und anschliessend werden deine Werte prozentual kalkuliert und grafisch dargestellt. Diese Daten sind nun auch zum PDF-Download verfügbar und können durch das eigene Nutzerlogin im Menü «History» auch später erneut abgerufen werden.")
    st.write("Um direkt mit Deiner Differenzierung loszulegen, drücke auf den unteren Knopf. Für andere Funktionen kannst Du die Sidebar benutzen.")

    # Button zur Navigation zu Morphaway
    if st.button("Zum Morphaway"):
        st.experimental_set_query_params(page="Morphaway")
        st.experimental_rerun()

elif page == "Morphaway":
    st.title("Morphaway")
    st.write("Willkommen bei Morphaway! Hier kannst du deine Differenzierung starten.")

