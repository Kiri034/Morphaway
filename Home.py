import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

from utils.style import set_background_color

# Sidebar-Konfiguration
st.set_page_config(initial_sidebar_state="collapsed")

# Setze einen Hintergrund und ein Bild nur auf die rechte Seite
set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")  # Hauptbereich und Seitenleiste Hintergrundfarbe setzen

# ====== Start Init Block =======

# Initialisieren des DataManagers
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Morphy")  # switch drive 

# Initialisieren des LoginManagers
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# Laden der Daten vom persistenten Speicher
data_manager.load_user_data(
    session_state_key='data_df',
    file_name='data.csv',
    initial_value=pd.DataFrame(),
    parse_dates=['timestamp']
)

# ====== End Init Block ======


# Logo
st.image("https://raw.githubusercontent.com/Kiri034/Morphaway/bd399c4a2b974d03fc9117a45bd700e447c0a61b/Bilder/Logo.png", width=320)
 
 # Username in der Seitenleiste anzeigen
with st.sidebar:
    username = st.session_state.get("username")
    if username:
        st.markdown(f"**Eingeloggt als:** {username}")

# Nutzername aus der Session State abrufen
name = st.session_state.get("name")

if name:
    first_name = name.split()[0]
    st.write(f"Herzlich Willkommen {first_name} bei Morphaway!")
else:
    st.write("Herzlich Willkommen bei Morphaway!")
st.write("Morphaway ist eine einfache und übersichtliche Variante, um ein Blutbild auszuzählen.")
st.write("Durch eine individuelle Auswahl der Differenzierungsoptionen ist unsere App sehr nutzerfreundlich aufgebaut und kann so in verschiedene Situationen angewendet werden.")
st.write("Egal, ob du dein:e Dozent:in mit einer schnellen 50er-Leukozytendifferenzierung beeindrucken möchtest, 100 Leukozyten für eine genauere Bestimmung brauchst oder ganze 200 Leukozyten zur Labordiagnostik differenzieren möchtest - Morphaway bietet dir die Unterstützung.")
st.write("Die Werte der ausgezählten Zellen findest du prozentual sowie grafisch dargestellt unter \"History\". Durch dein Nutzerlogin kannst du sie jederzeit als PDF-Datei herunterladen.")
st.write("Drücke auf den unteren Knopf, um mit der Differenzierung zu starten oder öffne auf der linken oberen Seite die Menüleiste für andere Funktionen!")

# Button zur Navigation zu Morphaway.py
if st.button("Jetzt Differenzieren"):
    st.switch_page("pages/1_Morphaway.py")


