import streamlit as st
import pandas as pd
import plotly.express as px

# Titel der Seite
praep_name = st.session_state.get("praep_name", "Präparat")
st.title(f"Auswertung für {praep_name}")

# Überprüfen, ob Zählerdaten aus 1_Morphaway.py vorhanden sind
if any(f"button_{i}_count" in st.session_state for i in range(1, 19)):
    # Liste der Zellen und Beschriftungen
    images = [
        {"label": "Lymphozyt"},
        {"label": "Monozyt"},
        {"label": "Eosinophil"},
        {"label": "Basophil"},
        {"label": "Segmentkernige Granulozyten"},
        {"label": "Stabkernige Granulozyten"},
        {"label": "Erythroblast"},
        {"label": "Blasten"},
        {"label": "Promyelozyt"},
        {"label": "Myelozyt"},
        {"label": "Metamyelozyt"},
        {"label": "reactive Lymphozyt"},
        {"label": "Abnormale Lymphozyten"},
        {"label": "Large granular lymphocyte"},
        {"label": "NRBC"},
        {"label": "Mastzelle"},
        {"label": "Plasmazelle"},
        {"label": "smudged cells"},
    ]

    # Daten für die Tabelle und das Diagramm vorbereiten
    data = []
    total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 19))
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        relative_count = (count / total_count * 100) if total_count > 0 else 0
        data.append({"Zelle": cell["label"], "Anzahl": count, "Relativer Anteil (%)": round(relative_count, 2)})

    # Daten in einen DataFrame umwandeln
    df = pd.DataFrame(data)

    # Tabelle anzeigen
    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df)

    # Kreisdiagramm erstellen (nur Zellen mit Anzahl > 0)
    filtered_df = df[df["Anzahl"] > 0]  # Filtere Zellen mit Anzahl > 0
    if not filtered_df.empty:
        st.subheader("Kreisdiagramm der Ergebnisse")
        fig = px.pie(filtered_df, names="Zelle", values="Anzahl", title="Verteilung der Zelltypen")
        st.plotly_chart(fig)
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
else:
    st.warning("Keine Daten verfügbar. Bitte kehre zurück und zähle Zellen in Morphaway.")