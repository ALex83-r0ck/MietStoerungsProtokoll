import os
import sqlite3

DB_FILE = "database/protokoll.db"


def copy_data() -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO laermdaten (datum, beginn, ende, grund, verursacher, auswirkung)
        SELECT datum, startzeit, endzeit, dauer, grund, nachbar, auswirkung 
        FROM laermdaten_old
    """
    )
    conn.commit()
    cursor.execute("DROP TABLE laermdaten_old")
    conn.close()
    print("Migration abgeschlossen!")


def create_database() -> None:
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Migration prüfen
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='laermdaten_old'")
    if c.fetchone():
        print("Migration wird durchgeführt...")
        copy_data()

    # Tabellen
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS laermdaten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            beginn TEXT NOT NULL,
            ende TEXT NOT NULL,
            dauer REAL,
            grund TEXT NOT NULL,
            verursacher TEXT NOT NULL,
            auswirkung INTEGER NOT NULL CHECK(auswirkung BETWEEN 1 AND 5),
            UNIQUE(datum, beginn, verursacher)
        )
    """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS massnahmen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            massnahme TEXT NOT NULL,
            ergebnis TEXT
        )
    """
    )

    # Trigger
    c.execute(
        """
        CREATE TRIGGER IF NOT EXISTS calc_dauer AFTER INSERT ON laermdaten
        BEGIN
            UPDATE laermdaten 
            SET dauer = (julianday('2000-01-01 ' || NEW.ende) - julianday('2000-01-01 ' || NEW.beginn)) * 1440
            WHERE id = NEW.id;
        END
    """
    )

    conn.commit()
    conn.close()
    print("Datenbank bereit!")


def insert_laermdaten(
    datum: str, beginn: str, ende: str, grund: str, verursacher: str, auswirkung: int
) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO laermdaten (datum, beginn, ende, grund, verursacher, auswirkung) VALUES (?, ?, ?, ?, ?, ?)",
        (datum, beginn, ende, grund, verursacher, auswirkung),
    )
    conn.commit()
    conn.close()


def insert_massnahmen(datum: str, massnahme: str, ergebnis: str) -> None:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "INSERT INTO massnahmen (datum, massnahme, ergebnis) VALUES (?, ?, ?)",
        (datum, massnahme, ergebnis),
    )
    conn.commit()
    conn.close()


def get_all_laermdaten():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM laermdaten ORDER BY datum, beginn")
    data = c.fetchall()
    conn.close()
    return data


def get_all_massnahmen():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM massnahmen ORDER BY datum")
    data = c.fetchall()
    conn.close()
    return data
