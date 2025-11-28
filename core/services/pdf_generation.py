from datetime import date

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import simpleSplit
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from core.services.data_processing import get_all_data, get_all_massnahmen


def generiere_protokoll(self, *args):
    # Daten laden
    data = get_all_data()  # Holt die Rohdaten aus der Datenbank

    filename = f"Lärmprotokoll_vom_{date.today().strftime('%d-%m-%Y')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    # Styles und Logo
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    body_style = styles["BodyText"]

    logo_path = "utils/image/Designer.png"
    try:
        logo = Image(logo_path, width=100, height=100)
        elements.append(logo)
    except FileNotFoundError:
        print(f"Logo nicht gefunden: {logo_path}")

    # Titel und Datum hinzufügen
    title = Paragraph("Lärmprotokoll", title_style)
    date_paragraph = Paragraph(
        f"<b>Erstellt am:</b> {date.today().strftime('%d.%m.%Y')}", body_style
    )
    elements.append(title)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))

    # Beschreibung des Protokolls
    description = Paragraph(
        "Dieses Protokoll dokumentiert Lärmbelastungen im angegebenen Zeitraum. "
        "Diese Daten bilden die Störungen in einer Skala von (3-5) ab. Die Dauer ist in Minuten(min).",
        body_style,
    )
    elements.append(description)
    elements.append(Spacer(1, 20))

    # Tabellendaten vorbereiten (Spaltenüberschriften und Daten)
    if not data.empty:
        # Entfernen der ID-Spalte
        data = data.drop(columns=["id"], errors="ignore")

        # Datum im richtigen Format ändern
        data["datum"] = pd.to_datetime(data["datum"]).dt.strftime("%d.%m.%Y")

        # Uhrzeit im Format HH:MM ändern (z.B., 20:08 statt 20:08:00)
        data["beginn"] = pd.to_datetime(data["beginn"]).dt.strftime("%H:%M")
        data["ende"] = pd.to_datetime(data["ende"]).dt.strftime("%H:%M")

        # Umbenennung von 'grund' auf 'Art der Störung'
        data = data.rename(columns={"grund": "Art der Störung"})

        # Spaltenüberschrift in Großbuchstaben
        column_headers = [col.capitalize() for col in data.columns]
        table_data = [column_headers]

        # Datenzeilen hinzufügen
        for row in data.values.tolist():
            table_data.append(row)
    else:
        # Keine Daten verfügbar
        table_data = [["Keine Daten vorhanden"]]

    # Berechnung der Spaltenbreiten basierend auf der maximalen Textlänge
    col_widths = []
    for i in range(len(table_data[0])):
        max_len = max(
            [len(str(row[i])) for row in table_data]
        )  # Maximale Länge der Zellen in der Spalte
        col_widths.append(
            max_len * 6
        )  # Multiplizieren mit einem Faktor (z.B., 6) für bessere Sichtbarkeit

    # Tabelle formatieren
    table = Table(table_data, colWidths=col_widths, rowHeights=30, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),  # Überschriften grau hinterlegen
                ("WORDWRAP", (0, 0), (-1, -1), True),  # Umbruch des Textes
            ]
        )
    )

    # Funktion, um die Seitenzahl hinzuzufügen und die Tabelle richtig anzuordnen
    def on_page(canvas, doc):
        # Seitenzahl hinzufügen
        page_num = canvas.getPageNumber()
        text = f"Seite {page_num}"
        canvas.setFont("Helvetica", 10)
        canvas.drawString(530, 30, text)

    # Kopf- und Fußbereich
    elements.append(table)
    elements.append(PageBreak())  # Seitewechsel einfügen

    # Footer hinzufügen
    elements.append(Spacer(1, 40))
    footer = Paragraph(
        "Lärmprotokoll - Generated with Protokoli der Protokollapp - Version 1.0 (2024) - © Alexander Rothe",
        ParagraphStyle(name="Footer", alignment=1, fontSize=10),
    )
    elements.append(footer)

    # PDF erstellen
    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)


def generiere_massnahmen(self, *args):
    # Daten für Maßnahmen holen
    data = get_all_massnahmen()  # Holt die Daten der Maßnahmen

    # Umwandeln in DataFrame, um die Daten einfacher zu bearbeiten
    df = pd.DataFrame(data, columns=["Datum", "Maßnahme", "Ergebnis"])

    # Dokument Setup
    filename = (
        f"Massnahmen-Protokoll_vom_{date.today().strftime('%d-%m-%Y')}.pdf"  # Dynamischer Dateiname
    )
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    # Styles und Logo
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    body_style = styles["BodyText"]

    logo_path = "utils/image/Designer.png"
    try:
        logo = Image(logo_path, width=100, height=100)
        elements.append(logo)
    except FileNotFoundError:
        print(f"Logo nicht gefunden: {logo_path}")

    # Titel und Datum hinzufügen
    title = Paragraph("Maßnahmenprotokoll", title_style)
    date_paragraph = Paragraph(
        f"<b>Erstellt am:</b> {date.today().strftime('%d.%m.%Y')}", body_style
    )
    elements.append(title)
    elements.append(date_paragraph)
    elements.append(Spacer(1, 20))

    # Beschreibung des Protokolls
    description = Paragraph(
        "Dieses Protokoll dokumentiert die getroffenen Versuche zur selbständigen Lärm und Störungsbeseitigung.",
        body_style,
    )
    elements.append(description)
    elements.append(Spacer(1, 20))

    # Tabellendaten vorbereiten
    if not df.empty:
        # **Datum direkt als String belassen**:
        df["Datum"] = df["Datum"].astype(str)

        # Spaltenüberschriften
        column_headers = [col.capitalize() for col in df.columns]
        table_data = [column_headers]

        # Dynamische Zeilenumbrüche hinzufügen
        max_widths = [100, 200, 200]  # Maximale Spaltenbreiten in Pixel (Anpassung nach Bedarf)
        row_heights = []  # Liste für dynamische Zeilenhöhen
        for row in df.values.tolist():
            wrapped_row = []
            max_lines = 1  # Zählt die maximalen Zeilen einer Zelle in der Reihe
            for i, cell in enumerate(row):
                # Text auf die maximale Spaltenbreite umbrechen
                wrapped_text = "\n".join(simpleSplit(str(cell), "Helvetica", 10, max_widths[i]))
                wrapped_row.append(wrapped_text)
                # Anzahl der Zeilen berechnen und Höchstenwert speichern
                max_lines = max(max_lines, len(wrapped_text.split("\n")))
            table_data.append(wrapped_row)
            # Dynamische Höhe basierend auf der maximalen Anzahl von Zeilen
            row_heights.append(max_lines * 12)  # Multipliziert mit der Zeilenhöhe

    else:
        # Keine Daten verfügbar
        table_data = [["Keine Maßnahmen vorhanden"]]
        row_heights = [30]  # Standardhöhe für leere Tabelle

    # Dynamische Zeilenhöhen berechnen
    row_heights = []

    # Standardhöhe für die Kopfzeile hinzufügen
    row_heights.append(30)  # Höhe für die Kopfzeile

    col_widths = [100, 200, 200]  # Maximale Spaltenbreiten in Pixel (Anpassung nach Bedarf)
    # Berechnung der Höhen für Datenzeilen
    for row in table_data[1:]:  # Überspringe die Kopfzeile
        max_lines = 1  # Minimale Anzahl von Zeilen
        for i, cell in enumerate(row):
            # Text umbrechen, um die maximale Spaltenbreite zu berücksichtigen
            wrapped_text = "\n".join(simpleSplit(str(cell), "Helvetica", 10, col_widths[i]))
            max_lines = max(max_lines, len(wrapped_text.split("\n")))
        row_heights.append(max_lines * 12)  # Zeilenhöhe basierend auf der Anzahl der Zeilen

    # Tabelle erstellen
    table = Table(table_data, colWidths=col_widths, rowHeights=row_heights, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightskyblue),
                ("WORDWRAP", (0, 0), (-1, -1), True),  # Textumbruch aktivieren
            ]
        )
    )

    # Funktion, um die Seitenzahl hinzuzufügen
    def on_page(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Seite {page_num}"
        canvas.setFont("Helvetica", 10)
        canvas.drawString(530, 30, text)

    # Tabelle hinzufügen
    elements.append(table)

    # Footer hinzufügen
    footer = Paragraph(
        "Maßnahmenprotokoll - Generated with Protokoli der Protokollapp - Version 1.0 (2024) - © Alexander Rothe",
        ParagraphStyle(name="Footer", alignment=1, fontSize=10),
    )
    elements.append(Spacer(1, 20))
    elements.append(footer)

    # PDF erstellen
    try:
        doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
        print(f"PDF erfolgreich erstellt: {filename}")
    except Exception as e:
        print(f"Fehler beim Erstellen des PDFs: {e}")
