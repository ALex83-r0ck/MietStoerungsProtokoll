# core/services/protokol_service.py
"""
Service für alle DB-Operationen.
Speichern von Lärmdaten und Maßnahmen.
"""

import logging

from infrastructure.database.database_setup import insert_laermdaten, insert_massnahmen


def save_event(
    datum: str, beginn: str, ende: str, grund: str, verursacher: str, auswirkung: int
) -> None:
    """
    Speichert ein Lärmprotokoll-Ereignis.
    Trennung von GUI: GUI ruft nur diese Funktion auf.
    """
    try:
        insert_laermdaten(datum, beginn, ende, grund, verursacher, auswirkung)
        logging.info(
            f"Lärmdaten gespeichert: {datum}, {beginn}-{ende}, {grund}, {verursacher}, {auswirkung}"
        )
    except Exception as e:
        logging.error(f"Speichern fehlgeschlagen: {e}")
        raise


def save_action(zeitraum: str, beschreibung: str, ergebnis: str) -> None:
    # TODO: validierung der Eingabe muss verbessert werden.
    """
    Speichert die Maßnahme.
    Validierung erfolgt hier: (aktuell nur) keine leeren Felder erlaubt.
    """
    if not all([zeitraum, beschreibung, ergebnis]):
        raise ValueError("Bitte fülle alle Felder aus.")
    try:
        insert_massnahmen(zeitraum, beschreibung, ergebnis)
        logging.info(f"Maßnahme gespeichert: {zeitraum}, {beschreibung}, {ergebnis}")
    except Exception as e:
        logging.error(f"Speichern fehlgeschlagen: {e}")
        raise
