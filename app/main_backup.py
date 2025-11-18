"""
Protolkoli – Gerichtsfestes Lärmprotokoll
Autor: Alexander Rothe
STATUS: CLEAN | MINIMAL | PERFEKT | GOTT-MODUS
"""

from typing import Optional
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from database.database_setup import *
from .widgets import MyDraggableCard
from services.adapters.data_processing import get_all_data, generate_plots  # ← NEU: generate_plots!
from services.adapters.pdf_generation import generiere_protokoll, generiere_massnahmen
from datetime import datetime
import re 
import os
import logging
logging.getLogger('matplotlib.font_manager').disabled = True
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.getLogger('kivy').setLevel(logging.WARNING)
os.environ['KIVY_NO_CONSOLELOG'] = '1'
import json

# === KONFIGURATION ===
with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

PLOT_FOLDER = CONFIG["paths"]["plots"]
DB_FILE = CONFIG["paths"]["database"]

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    filename=CONFIG["paths"]["logs"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

os.makedirs(PLOT_FOLDER, exist_ok=True)

class MyDraggableCard(MyDraggableCard):
    pass
    
class RootWidget(MDBoxLayout):
    plot_menu_button = ObjectProperty(None)
    chart_box = ObjectProperty(None)
    datum = ObjectProperty(None)
    beginn = ObjectProperty(None)
    ende = ObjectProperty(None)
    grund = ObjectProperty(None)
    verursacher = ObjectProperty(None)
    auswirkung = ObjectProperty(None)
    zeitraum = ObjectProperty(None)
    beschreibung = ObjectProperty(None)
    ergebnis = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_menu, 0)

    def initialize_menu(self, dt) -> None:
        self.create_plot_menu()

    def generiere_alle_protokolle(self) -> None:
        try:
            generiere_protokoll(self)
            generiere_massnahmen(self)
            self.show_message("Protokolle erfolgreich generiert!")
            logging.info("Protokolle generiert")
        except Exception as e:
            self.show_message(f"Fehler: {e}")
            logging.error(f"Protokoll-Generierung fehlgeschlagen: {e}")

    def save_data(self) -> None:
        if not self.validate_inputs():
            return
        try:
            insert_laermdaten(
                self.datum.text,
                self.beginn.text,
                self.ende.text,
                self.grund.text,
                self.verursacher.text,
                int(self.auswirkung.text)
            )
            self.show_message("Daten gespeichert!")
            logging.info("Lärmdaten gespeichert")
            self.update_plots()  # ← Hier werden jetzt die 5 neuen Plots generiert
        except Exception as e:
            self.show_message(f"Speichern fehlgeschlagen: {e}")
            logging.error(f"Speichern fehlgeschlagen: {e}")

    def speichere_massnahme(self, zeitraum: str, beschreibung: str, ergebnis: str) -> None:
        if not all([zeitraum, beschreibung, ergebnis]):
            self.show_message("Bitte alle Felder ausfüllen!")
            return
        try:
            insert_massnahmen(zeitraum, beschreibung, ergebnis)
            self.show_message("Maßnahme gespeichert!")
            logging.info("Maßnahme gespeichert")
        except Exception as e:
            self.show_message(f"Fehler: {e}")
            logging.error(f"Maßnahme speichern fehlgeschlagen: {e}")

    def validate_inputs(self) -> bool:
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", self.datum.text):
            self.show_message("Datum: DD-MM-YYYY")
            return False
        if not all(re.match(r"^\d{2}:\d{2}$", t.text) for t in [self.beginn, self.ende]):
            self.show_message("Zeit: HH:MM")
            return False
        if self.beginn.text >= self.ende.text:
            self.show_message("Beginn muss vor Ende sein!")
            return False
        if not all(getattr(self, f).text for f in ["grund", "verursacher", "auswirkung"]):
            self.show_message("Alle Felder ausfüllen!")
            return False
        try:
            a = int(self.auswirkung.text)
            if not 1 <= a <= 5:
                self.show_message("Auswirkung: 1–5")
                return False
        except ValueError:
            self.show_message("Auswirkung muss Zahl sein!")
            return False
        return True

    def show_message(self, text: str) -> None:
        MDSnackbar(text=text, duration=3).open()

    def create_plot_menu(self) -> None:
        items = []
        try:
            plot_files = [
                "01_trend_dauer.png",
                "02_histogramm_dauer.png",
                "03_top_stoerungen.png",
                "04_uhrzeiten.png",
                "05_prognose.png"
            ]
            for f in plot_files:
                path = os.path.join(PLOT_FOLDER, f)
                if os.path.exists(path):
                    items.append({
                        "viewclass": "OneLineListItem",
                        "text": f.split("_", 1)[1].replace(".png", "").replace("_", " ").title(),
                        "on_release": lambda x=f: self.show_plot(x)
                    })
        except Exception as e:
            logging.error(f"Plot-Menü Fehler: {e}")

        from kivymd.uix.menu import MDDropdownMenu
        self.menu = MDDropdownMenu(
            caller=self.ids.top_app_bar,
            items=items or [{"text": "Keine Plots verfügbar", "viewclass": "OneLineListItem"}],
            width_mult=4,
        )

    def show_plot(self, filename: str) -> None:
        path = os.path.join(PLOT_FOLDER, filename)
        if not os.path.exists(path):
            self.show_message("Plot nicht gefunden")
            return
        try:
            self.chart_box.clear_widgets()
            from kivymd.uix.fitimage import FitImage
            self.chart_box.add_widget(FitImage(source=path, allow_stretch=True))
            self.show_message(f"{filename} geladen")
            logging.info(f"Plot geöffnet: {filename}")
        except Exception as e:
            self.show_message(f"Anzeige fehlgeschlagen: {e}")
        finally:
            if hasattr(self, "menu"):
                self.menu.dismiss()

    def menu_open(self) -> None:
        if hasattr(self, "menu"):
            self.menu.open()

    def update_plots(self) -> None:
        """NEU: Einfach generate_plots() aufrufen – ALLES wird neu generiert"""
        try:
            generate_plots()  # ← Das ist alles. 5 Plots. Perfekt. Sauber.
            self.create_plot_menu()
            self.show_message("5 Analysen aktualisiert!")
            logging.info("5 wichtige Plots aktualisiert")
        except Exception as e:
            self.show_message(f"Plot-Update fehlgeschlagen: {e}")
            logging.error(f"Plot-Update Fehler: {e}")


class ProtokollApp(MDApp):
    root: Optional[RootWidget] = None

    def build(self):
        Builder.load_file("protokoll.kv")
        create_database()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return RootWidget()

    def on_start(self):
        Clock.schedule_once(self.set_default_values, 0)

    def set_default_values(self, dt) -> None:
        if not self.root:
            return
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M")
        for field in ["datum", "beginn", "ende"]:
            if hasattr(self.root, field):
                getattr(self.root, field).text = date_str if field == "datum" else time_str

    def erfasse_daten(self, *args):
        if self.root:
            self.root.save_data()

    def speichere_massnahme(self, zeitraum: str, beschreibung: str, ergebnis: str):
        if self.root:
            self.root.speichere_massnahme(zeitraum, beschreibung, ergebnis)

    def analyse_haeufigkeit(self):
        if not self.root: return
        try:
            df = get_all_data()
            if df.empty:
                self.root.show_message("Keine Daten")
                return
            top = df['verursacher'].mode()[0]
            self.root.ids.haeufigster_verursacher.text = f"Häufigster: {top}"
        except Exception as e:
            self.root.show_message(f"Analyse fehlgeschlagen: {e}")

    def analyse_auswirkung(self):
        if not self.root: return
        try:
            df = get_all_data()
            if df.empty: return
            avg = df['auswirkung'].astype(float).mean()
            self.root.ids.durchschnittliche_auswirkung.text = f"Ø Auswirkung: {avg:.2f}"
        except Exception as e:
            self.root.show_message(f"Fehler: {e}")

    def analyse_dauer(self):
        if not self.root: return
        try:
            df = get_all_data()
            if df.empty: return
            avg = df['dauer'].mean()
            self.root.ids.durchschnittliche_dauer.text = f"Ø Dauer: {avg:.1f} Min"
        except Exception as e:
            self.root.show_message(f"Fehler: {e}")


if __name__ == "__main__":
    try:
        ProtokollApp().run()
    except Exception as e:
        logging.critical(f"App-Absturz: {e}")
        raise