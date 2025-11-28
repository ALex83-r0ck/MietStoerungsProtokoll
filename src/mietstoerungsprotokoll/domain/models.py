from __future__ import annotations

from datetime import datetime
from enum import StrEnum, auto
from typing import Optional

from sqlmodel import SQLModel, Field


# ----------------------------------------------------------------------
# 1. Störungstypen – leicht erweiterbar
# ----------------------------------------------------------------------
class Stoerungstyp(StrEnum):
    """Alle Arten von Mietstörungen – einfach neue hinzufügen."""
    LAERM = auto()          # Nachtruhe, Partys, Baulärm etc.
    SCHIMMEL = auto()       # Schimmelbefall
    HEIZUNG = auto()        # Heizungsausfall, zu kalt, defekt
    WASSERSCHADEN = auto()  # Rohrbruch, Undichtigkeit, Überschwemmung
    NACHBARN = auto()       # sonstige Nachbarschaftsstreitigkeiten
    GEMEINSCHAFT = auto()   # Treppenhaus, Fahrstuhl, Müllraum, Hof etc.
    SONSTIGES = auto()      # Fallback für alles andere


# ----------------------------------------------------------------------
# 2. Störungseintrag – das Herzstück
# ----------------------------------------------------------------------
class Stoerungseintrag(SQLModel, table=True):
    """Ein einzelner Eintrag im Protokoll → wird 1:1 in SQLite gespeichert."""
    id: Optional[int] = Field(default=None, primary_key=True)

    # Zeitstempel
    datum: datetime = Field(default_factory=datetime.utcnow, index=True)
    beginn: Optional[datetime] = Field(default=None)   # nur relevant bei dauerhaften Störungen
    ende: Optional[datetime] = Field(default=None)

    # Inhalt
    typ: Stoerungstyp = Field(index=True)
    beschreibung: str = Field(min_length=1, max_length=2000)

    auswirkung: Optional[int] = Field(
        default=None,
        ge=1,
        le=5,  # zurück auf 5er-Skala – 10er macht selten Sinn bei subjektiver Belastung
        description="Subjektive Belastung: 1 = kaum störend, 5 = unerträglich"
    )

    # Beweise
    foto_pfad: Optional[str] = Field(default=None, max_length=500)
    video_pfad: Optional[str] = Field(default=None, max_length=500)  # für später

    # Meta
    erstellt_von: str = Field(default="Mieter", max_length=100)
    zeuge: Optional[str] = Field(default=None, max_length=100)        # klein geschrieben (Python-Konvention)

    # ------------------------------------------------------------------
    # Smarte Dauer-Berechnung
    # ------------------------------------------------------------------
    def dauer_in_minuten(self) -> Optional[int]:
        """
        Liefert die Dauer in Minuten NUR, wenn beginn und ende gesetzt sind
        und ende nach beginn liegt. Sonst → None (völlig korrekt für Schimmel etc.).
        """
        if self.beginn and self.ende and self.ende > self.beginn:
            return int((self.ende - self.beginn).total_seconds() // 60)
        return None

    # ------------------------------------------------------------------
    # Hilfsmethode für die GUI
    # ------------------------------------------------------------------
    def ist_dauer_sinnvoll(self) -> bool:
        """
        Soll die GUI überhaupt Beginn-/Ende-Felder anzeigen?
        Aktuell nur bei Lärm und sonst. Nachbarschaftsstreit sinnvoll.
        Kann später einfach erweitert werden.
        """
        return self.typ in {Stoerungstyp.LAERM, Stoerungstyp.NACHBARN}
        # Alternative: später z. B. auch HEIZUNG hinzufügen, wenn stundenweise Ausfall