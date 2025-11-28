import sqlite3


def backup_and_update_database():
    # Connect to the SQLite database
    conn = sqlite3.connect("database/protokoll.db")
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE laermdaten RENAME TO laermdaten_old")

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS laermdaten (
                       id INTEGER PRIMARY KEY,
                       datum TEXT,
                       beginn TEXT,
                       ende TEXT,
                       dauer TEXT,
                       grund TEXT,
                       verursacher TEXT,
                       auswirkung INTEGER CHECK(auswirkung BETWEEN 1 AND 5),
                       UNIQUE(datum, beginn, verursacher))"""
    )

    # Kopiere alle Daten aus der alten Tabelle in die neue Tabelle
    cursor.execute(
        """
    INSERT INTO laermdaten (id, datum, beginn, ende, dauer, grund, verursacher, auswirkung)
    SELECT id, datum, beginn, ende, dauer, grund, verursacher, auswirkung FROM laermdaten_old
    """
    )

    # Lösche die alte Tabelle (optional)
    cursor.execute("DROP TABLE laermdaten_old")

    conn.commit()
    conn.close()


def copy_data():
    old_conn = sqlite3.connect("database/protokoll.db")
    old_cursor = old_conn.cursor()

    new_conn = sqlite3.connect("database/protokoll.db")
    new_cursor = new_conn.cursor()

    old_cursor.execute(
        "SELECT datum, startzeit, endzeit, dauer, grund, nachbar, auswirkung FROM laermdaten_old"
    )
    data = old_cursor.fetchall()

    for row in data:
        new_cursor.execute(
            """INSERT INTO laermdaten (datum, beginn, ende, dauer, grund, verursacher, auswirkung)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
            row,
        )

    new_conn.commit()

    old_conn.close()
    new_conn.close()

    print("Daten erfolgreich übertragen")


# Funktion ausführen
copy_data()
