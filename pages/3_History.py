# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Home.py')
# ====== End Login Block ======

# ------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("🔍 History")

# Pfad zur zentralen CSV-Datei im SwitchDrive (bitte anpassen!)
csv_path = r"X:\SwitchDrive\gemeinsamer_ordner\history.csv"  # <-- Passe diesen Pfad an!

zelltypen = [
    "Lymphozyt", "reaktiver Lymphozyt", "Monozyt", "Eosinophile Gc*", "Basophile Gc*",
    "Segmentkernige Gc*", "Stabkernige Gc*", "Blasten", "Promyelozyt", "Myelozyt",
    "Metamyelozyt", "Plasmazelle", "Erythroblast", "smudged cells"
]

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    if not df.empty:
        # Dropdown für Auswahl einer Auswertung
        auswahl = st.selectbox(
            "Auswertung auswählen:",
            df.apply(lambda row: f"{row['timestamp']} - {row['praep_name']}", axis=1)
        )
        idx = df.index[df.apply(lambda row: f"{row['timestamp']} - {row['praep_name']}", axis=1) == auswahl][0]
        auswertung = df.loc[idx]

        st.subheader(f"Präparat: {auswertung['praep_name']}")
        st.caption(f"Zeitpunkt: {auswertung['timestamp']}")

        # Tabelle der Zelltypen
        daten = []
        total = 0
        for zelle in zelltypen:
            anzahl = int(auswertung.get(zelle, 0))
            daten.append({"Zelle": zelle, "Anzahl": anzahl})
            total += anzahl
        for d in daten:
            d["Relativer Anteil (%)"] = round((d["Anzahl"] / total * 100) if total > 0 else 0, 2)
        df_zellen = pd.DataFrame(daten)
        st.dataframe(df_zellen)

        # Kreisdiagramm
        filtered_df = df_zellen[(df_zellen["Anzahl"] > 0) & (df_zellen["Zelle"] != "Erythroblast")]
        if not filtered_df.empty:
            fig = px.pie(
                filtered_df,
                names="Zelle",
                values="Anzahl",
                title="Verteilung der Zelltypen",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig)
        else:
            st.info("Keine Daten für das Kreisdiagramm verfügbar.")

        # Löschfunktion für einzelne Auswertung
        if st.button("❌ Auswertung löschen"):
            df = df.drop(idx)
            df.to_csv(csv_path, index=False)
            st.success("Auswertung wurde gelöscht. Bitte Seite neu laden.")
            st.stop()
    else:
        st.info("Noch keine Auswertungen vorhanden.")