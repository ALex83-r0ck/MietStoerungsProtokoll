# core/services/statistics_service.py

"""
Service für alle Berechnungen / Analysen.
GUI ruft nur diese Funktionen, keine DB-Zugriffe hier.
"""


def get_top_verursacher(df):
    """Berechnung des Häufigsten Verursachers"""
    if df.empty:
        return None
    return df["verursacher"].mode()[0]


def get_average_auswirkung(df):
    """Berechnung der durchschnittlichen Auswirkungen"""
    if df.empty:
        return 0
    return df["auswirkung"].astype(float).mean()


def get_average_duration(df):
    """Berechnung der durchschnittlichen Dauer der Störungen"""
    if df.empty:
        return 0
    return df["dauer"].mean()
