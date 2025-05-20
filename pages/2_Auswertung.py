# ====== Start Login Block ======
#from utils.login_manager import LoginManager
#LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

# ------------------------------------------------------------
# Hier beginnt die eigentliche App
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import os
import json
from datetime import datetime

praep_name = st.session_state.get("praep_name", "Unbekanntes Präparat")
st.title(f"Auswertung für {praep_name}")

# Maximalzahl aus Auswahl holen (z.B. "50 Zellen", "100 Zellen", ...)
max_cells = 100  # Fallback
if "selected_option" in st.session_state and st.session_state["selected_option"]:
    max_cells = int(str(st.session_state["selected_option"]).split()[0])

# Verzeichnis für gespeicherte Auswertungen
history_directory = "history_exports"
if not os.path.exists(history_directory):
    os.makedirs(history_directory)

if any(f"button_{i}_count" in st.session_state for i in range(1, 15)):
    images = [
        {"label": "Lymphozyt"},
        {"label": "reaktiver Lymphozyt"},
        {"label": "Monozyt"},
        {"label": "Eosinophile Gc*"},
        {"label": "Basophile Gc*"},
        {"label": "Segmentkernige Gc*"},
        {"label": "Stabkernige Gc*"},
        {"label": "Blasten"},
        {"label": "Promyelozyt"},
        {"label": "Myelozyt"},
        {"label": "Metamyelozyt"},
        {"label": "Plasmazelle"},
        {"label": "Erythroblast"},
        {"label": "smudged cells"},
    ]

    # Daten für die Tabelle und das Diagramm vorbereiten
    data = []
    total_count = sum(st.session_state.get(f"button_{i}_count", 0) for i in range(1, 15))
    for idx, cell in enumerate(images, start=1):
        count = st.session_state.get(f"button_{idx}_count", 0)
        # Prozentwert bezogen auf die Maximalzahl!
        relative_count = (count / max_cells * 100) if max_cells > 0 else 0
        data.append({"Zelle": cell["label"], "Anzahl": count, f"Anteil an {max_cells}": round(relative_count, 2)})

    df = pd.DataFrame(data)

    # Ergebnisse speichern
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{praep_name}_{timestamp}.json"
    filepath = os.path.join(history_directory, filename)
    export_data = {
        "praep_name": praep_name,
        "timestamp": timestamp,
        "data": df.to_dict(orient="records")
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    # Tabelle anzeigen
    st.subheader("Tabelle der Ergebnisse")
    st.dataframe(df)

    # Kreisdiagramm erstellen (nur Zellen mit Anzahl > 0)
    filtered_df = df[df["Anzahl"] > 0]
    diagram_path = None
    if not filtered_df.empty:
        st.subheader(f"Kreisdiagramm der Ergebnisse (bezogen auf {max_cells} Zellen)")
        fig = px.pie(
            filtered_df,
            names="Zelle",
            values=f"Anteil an {max_cells}",
            title=f"Verteilung der Zelltypen (in % von {max_cells})"
        )
        st.plotly_chart(fig)

        # Diagramm als Bild speichern
        diagram_path = "diagram.png"
        try:
            fig.write_image(diagram_path)
        except Exception as e:
            st.error(f"Fehler beim Speichern des Diagramms als Bild: {e}")
            diagram_path = None
    else:
        st.warning("Keine Daten für das Kreisdiagramm verfügbar. Alle Zellen haben 0 Klicks.")
        diagram_path = None
else:
    st.warning("Keine Zählerdaten vorhanden. Bitte kehren Sie zurück und geben Sie Ihre Werte ein.")
    df = pd.DataFrame()
    diagram_path = None

# PDF-Erstellung
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", style="B", size=16)
pdf.cell(200, 10, txt="Auswertung der Ergebnisse", ln=True, align="C")
pdf.ln(10)

# Tabelle in die PDF einfügen
pdf.set_font("Arial", size=12)
if not df.empty:
    pdf.cell(0, 5, txt=f"Tabelle der Ergebnisse (bezogen auf {max_cells} Zellen):", ln=True)
    pdf.ln(5)
    for index, row in df.iterrows():
        pdf.cell(0, 5, txt=f"{row['Zelle']}: {row['Anzahl']} Klicks ({row[f'Anteil an {max_cells}']}%)", ln=True)
else:
    pdf.cell(0, 5, txt="Keine Daten verfügbar.", ln=True)

# Kreisdiagramm ins PDF einfügen, falls vorhanden
if diagram_path and os.path.exists(diagram_path):
    pdf.ln(10)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, txt="Kreisdiagramm:", ln=True)
    pdf.ln(5)
    pdf.image(diagram_path, x=40, w=120)

# PDF in eine Datei speichern
pdf_file_path = f"{praep_name}_Auswertung.pdf"
pdf.output(pdf_file_path)

# PDF-Download-Button
if os.path.exists(pdf_file_path):
    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button(
            label="📄 PDF herunterladen",
            data=pdf_file,
            file_name=f"{praep_name}_Auswertung.pdf",
            mime="application/pdf",
        )
else:
    st.error("Die PDF-Datei konnte nicht erstellt werden.")

# Button für History anzeigen
if st.button("History"):
    st.switch_page("pages/3_History.py")