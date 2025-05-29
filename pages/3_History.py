# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py') 
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from utils.data_manager import DataManager
from utils.style import set_background_color
from datetime import datetime

# Hintergrundfarbe & Bild nur rechts
set_background_color("#fbeaff", "#fae2ff", "https://raw.githubusercontent.com/Kiri034/Morphaway/refs/heads/main/Bilder/ec_background_purple_20.png")

# Logo anzeigen
st.image("https://raw.githubusercontent.com/Kiri034/Morphaway/bd399c4a2b974d03fc9117a45bd700e447c0a61b/Bilder/Logo.png", width=320)

st.title("🔍 History")

user = st.session_state.get("user")
df = st.session_state.get("data_df", pd.DataFrame())

st.write("Aktueller User:", user)
st.write("DataFrame:", df)

if user and not df.empty:
    df_user = df[df["user"] == user]
    if not df_user.empty:
        st.subheader("Tabelle der gespeicherten Auswertungen")
        st.dataframe(df_user[["praep_name", "timestamp", "total_count", "erythroblast_count"]], use_container_width=True)
        
        # Auswahl einer Auswertung per Präparatname
        praep_names = df_user["praep_name"].unique()
        selected_praep = st.selectbox("Wähle ein Präparat für Details & PDF:", praep_names)

        # Zeige Details zur gewählten Auswertung
        selected_row = df_user[df_user["praep_name"] == selected_praep].iloc[-1]  # letzte Auswertung mit diesem Namen
        st.markdown(f"**Präparat:** {selected_row['praep_name']}  \n**Zeitpunkt:** {selected_row['timestamp']}  \n**Gesamtzahl:** {selected_row['total_count']}  \n**Erythroblasten:** {selected_row['erythroblast_count']}")

        # Kreisdiagramm (Dummy-Daten, falls keine Einzelzell-Daten gespeichert)
        # Hier kannst du ggf. die Einzelzell-Daten aus einer Spalte laden, falls vorhanden
        pie_data = pd.DataFrame({
            "Zelle": ["Lymphozyt", "Monozyt", "Eosinophile", "Basophile"],
            "Anzahl": [selected_row.get("lymphozyt_count", 0), selected_row.get("mono_count", 0), selected_row.get("eos_count", 0), selected_row.get("baso_count", 0)]
        })
        pie_data = pie_data[pie_data["Anzahl"] > 0]
        if not pie_data.empty:
            st.subheader("Kreisdiagramm der Zellverteilung")
            fig = px.pie(pie_data, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen", color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig)
        else:
            st.info("Keine Zellverteilung für dieses Präparat gespeichert.")

        # PDF-Download
        if st.button("PDF herunterladen"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 15)
            pdf.cell(0, 12, f"Auswertung - Präparat: {selected_row['praep_name']}", ln=True, align="C")
            pdf.ln(8)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Zeitpunkt: {selected_row['timestamp']}", ln=True)
            pdf.cell(0, 10, f"Gesamtzahl: {selected_row['total_count']}", ln=True)
            pdf.cell(0, 10, f"Erythroblasten: {selected_row['erythroblast_count']}", ln=True)
            pdf.ln(8)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Zellverteilung:", ln=True)
            pdf.set_font("Arial", "", 12)
            for _, row in pie_data.iterrows():
                pdf.cell(0, 10, f"{row['Zelle']}: {row['Anzahl']}", ln=True)
            pdf_output = pdf.output(dest='S').encode('latin1')
            st.download_button("PDF herunterladen", data=pdf_output, file_name=f"{selected_row['praep_name']}_Auswertung.pdf", mime="application/pdf")

        # Präparat löschen
        if st.button("Präparat löschen"):
            df_user = df_user[df_user["praep_name"] != selected_praep]
            st.session_state["data_df"] = df[df["user"] != user]  # aus globalem DataFrame entfernen
            st.success("Präparat gelöscht. Seite neu laden, um die Änderung zu sehen.")

    else:
        st.info("Keine gespeicherten Auswertungen für diesen Benutzer.")
else:
    st.info("Keine gespeicherten Auswertungen vorhanden.")