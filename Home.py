import streamlit as st


st.title("Home")
st.write("Willkommen bei Morphaway! Morphaway ist eine einfache und übersichtliche Variante, um ein Blutbild auszuzählen. ")
st.write("Durch eine individuelle Auswahl der Differenzier-Möglichkeiten ist unsere App sehr nutzerfreundlich aufgebaut und kann so in verschiedene Situationen angewendet werden. Egal, ob du dein:e Dozent:in mit einer schnellen 50er-Leukozytendifferenzierung beeindrucken möchtest, 100 Leukozyten für eine genauere Bestimmung brauchst oder ganze 200 Leukozyten zur Labordiagnostik differenzieren möchtest - Morphaway bietet dir die Unterstützung.")
st.write('Die Werte der ausgezählten Zellen findest du prozentual sowie grafisch dargestellt unter "History". Durch dein Nutzerlogin kannst du sie jederzeit als PDF-Datei herunterladen.')
st.write("Drücke auf den unteren Knopf, um mit der Differenzierung zu starten oder nutze die Seitenleiste für andere Funktionen!")

# Button zur Navigation zu Morphaway.py
st.link_button("Jetzt differenzieren", "https://morphaway.streamlit.app/~/+/Morphaway")
