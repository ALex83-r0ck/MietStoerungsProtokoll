"""
utils/data_processing.py
Protolkoli – 5 WICHTIGE PLOTS | PYLANCE: 0 FEHLER | FINAL VICTORY
"""

import os
import sqlite3
from typing import List, Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
from sklearn.linear_model import LinearRegression

# === CACHE ===
_cached_data: Optional[pd.DataFrame] = None


def get_all_data(force_reload: bool = False) -> pd.DataFrame:
    global _cached_data
    if not force_reload and _cached_data is not None:
        return _cached_data

    try:
        with sqlite3.connect("database/protokoll.db") as conn:
            df = pd.read_sql_query("SELECT * FROM laermdaten", conn)
    except Exception as e:
        print(f"DB Fehler: {e}")
        return pd.DataFrame()

    if df.empty:
        _cached_data = pd.DataFrame()
        return _cached_data

    df["datum"] = pd.to_datetime(df["datum"], format="%d-%m-%Y", dayfirst=True)
    df["beginn"] = pd.to_datetime(
        df["datum"].dt.strftime("%Y-%m-%d") + " " + df["beginn"].astype(str)
    )
    df["ende"] = pd.to_datetime(df["datum"].dt.strftime("%Y-%m-%d") + " " + df["ende"].astype(str))
    df["dauer"] = (df["ende"] - df["beginn"]).dt.total_seconds() / 60

    _cached_data = df.copy()
    return _cached_data


def _save_plot(name: str) -> None:
    os.makedirs("plots", exist_ok=True)
    plt.savefig(f"plots/{name}", dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()


# ====================== DIE 5 WICHTIGSTEN PLOTS ======================


def plot_trend_dauer(df: pd.DataFrame) -> None:
    if df.empty:
        return
    plt.figure(figsize=(11, 6))
    sns.lineplot(data=df, x="datum", y="dauer", marker="o", color="#1f77b4", linewidth=2.5)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.title("Trend: Störungsdauer über Zeit", fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Datum")
    plt.ylabel("Dauer (Minuten)")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    _save_plot("01_trend_dauer.png")


def plot_histogramm_dauer(df: pd.DataFrame) -> None:
    if df.empty or "dauer" not in df.columns:
        return
    dauer = df["dauer"].dropna()
    if dauer.empty:
        return

    plt.figure(figsize=(10, 6))

    ax = sns.histplot(
        data=pd.DataFrame({"dauer": dauer}),
        x="dauer",
        bins=20,
        kde=True,
        color="#1f77b4",
        edgecolor="black",
        alpha=0.85,
        line_kws={"linewidth": 3, "color": "#d62728"},
    )

    patches: List[Rectangle] = [p for p in ax.patches if isinstance(p, Rectangle)]

    if patches:
        heights = [p.get_height() for p in patches]
        max_idx = int(np.argmax(heights))
        max_patch = patches[max_idx]
        max_patch.set_facecolor("#d62728")
        max_patch.set_edgecolor("#8B0000")

        center = max_patch.get_x() + max_patch.get_width() / 2
        height = max_patch.get_height()

        plt.text(
            center,
            height + max(heights) * 0.03,
            f"Häufigste Dauer\n{int(center)} Min",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
            color="red",
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="red", boxstyle="round"),
        )

    plt.title("Verteilung der Störungsdauern", fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Dauer (Minuten)")
    plt.ylabel("Häufigkeit")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    _save_plot("02_histogramm_dauer.png")


def plot_top_stoerungen(df: pd.DataFrame) -> None:
    if df.empty or "grund" not in df.columns:
        return
    top10 = df["grund"].value_counts().head(10)
    if top10.empty:
        return

    plt.figure(figsize=(10, 7))
    sns.barplot(y=top10.index, x=top10.values, hue=top10.index, palette="viridis", legend=False)
    plt.title("Top 10 Störungsarten", fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Häufigkeit")
    plt.ylabel("Störungsgrund")
    plt.tight_layout()
    _save_plot("03_top_stoerungen.png")


def plot_uhrzeiten(df: pd.DataFrame) -> None:
    if df.empty or "beginn" not in df.columns:
        return
    stunden = df["beginn"].dt.hour.value_counts().sort_index()
    if stunden.empty:
        return

    plt.figure(figsize=(12, 6))

    x_values = stunden.index.tolist()
    y_values = stunden.values.astype(float).tolist()

    bars = plt.bar(x_values, y_values, color="#ff7f0e", edgecolor="black", alpha=0.9)

    # FIX: max_hour definiert, Typ int, Index sicher
    max_hour: int = int(stunden.idxmax())
    if 0 <= max_hour < len(bars.patches):
        bars.patches[max_hour].set_facecolor("#d62728")
        bars.patches[max_hour].set_edgecolor("#8B0000")

    plt.title("Störungen nach Uhrzeit", fontsize=16, pad=20, fontweight="bold")
    plt.xlabel("Uhrzeit")
    plt.ylabel("Anzahl Störungen")
    plt.xticks(range(24))
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    _save_plot("04_uhrzeiten.png")


def plot_prognose(df: pd.DataFrame, tage: int = 14) -> None:
    if df.empty or len(df) < 5:
        return
    df_temp = df.copy()
    df_temp["tag"] = df_temp["datum"].map(pd.Timestamp.toordinal)

    X = df_temp["tag"].to_numpy().reshape(-1, 1)
    y = df_temp["dauer"].to_numpy().reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    zukunft = np.arange(df_temp["tag"].max() + 1, df_temp["tag"].max() + tage + 1).reshape(-1, 1)
    vorhersage = model.predict(zukunft)

    zukunft_daten = [pd.Timestamp.fromordinal(int(d)) for d in zukunft.flatten()]

    plt.figure(figsize=(11, 6))
    sns.lineplot(
        data=df_temp.tail(30),
        x="datum",
        y="dauer",
        label="Vergangenheit",
        color="gray",
        linewidth=2,
    )
    sns.lineplot(
        x=zukunft_daten,
        y=vorhersage.flatten(),
        label=f"Prognose (+{tage} Tage)",
        color="#d62728",
        linewidth=3,
    )

    plt.title(
        f"Prognose: Störungsdauer nächste {tage} Tage", fontsize=16, pad=20, fontweight="bold"
    )
    plt.xlabel("Datum")
    plt.ylabel("Dauer (Minuten)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    _save_plot("05_prognose.png")


# ====================== GENERIEREN ======================
def generate_plots() -> None:
    df = get_all_data(force_reload=True)
    if df.empty:
        print("Keine Daten zum Plotten")
        return

    print("Generiere die 5 wichtigsten Plots...")
    plot_trend_dauer(df)
    plot_histogramm_dauer(df)
    plot_top_stoerungen(df)
    plot_uhrzeiten(df)
    plot_prognose(df)
    print("FERTIG: 5 Plots generiert – PYLANCE: 0 FEHLER – DU: GOTT")


# ====================== ZUSATZ FÜR PDF ======================
def get_all_massnahmen() -> pd.DataFrame:
    """Lädt alle Maßnahmen aus der DB – für PDF-Generierung"""
    try:
        with sqlite3.connect("database/protokoll.db") as conn:
            df = pd.read_sql_query("SELECT * FROM massnahmen", conn)
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        print(f"Maßnahmen laden fehlgeschlagen: {e}")
        return pd.DataFrame()


# Auto-Start
if __name__ != "__main__":
    try:
        df = get_all_data()
        if not df.empty and len(df) >= 5:
            generate_plots()
    except:
        pass

if __name__ == "__main__":
    generate_plots()
