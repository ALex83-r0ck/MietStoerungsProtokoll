# -*- coding: utf-8 -*-
# app/main.py
# Author: Alexander Rothe

"""
Main GUI.
Alle Datenoperationen gehen über Services.
"""
from typing import Optional
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from core.services import protokol_service, statistics_service
from core.services.data_processing import generate_plots
from core.services.pdf_generation import generiere_protokoll, generiere_massnahmen
from infrastructure.database.database_setup import create_database, get_all_massnahmen, get_all_laermdaten
from app.widgets.draggable_card import MyDraggableCard 
from datetime import datetime
import json, os, logging, re

# === CONFIG ===
with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)
PLOT_FOLDER = CONFIG["paths"]["plots"]
os.makedirs(PLOT_FOLDER, exist_ok=True)

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    filename=CONFIG["paths"]["logs"],
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

os.environ['KIVY_NO_CONSOLELOG'] = '1'

class RootWidget(MDBoxLayout):
    """GUI-Logik"""
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

    def initialize_menu(self, dt):
        self.create_plot_menu()

    # =====================
    # === Events / GUI ===
    # =====================
    def save_data(self):
        """Save Lärmprotokoll über Service"""
        if not self.validate_inputs():
            return
        try:
            protokol_service.save_event(
                self.datum.text, self.beginn.text, self.ende.text,
                self.grund.text, self.verursacher.text, int(self.auswirkung.text)
            )
            self.show_message("Daten gespeichert!")
            self.update_plots()
        except Exception as e:
            self.show_message(f"Speichern fehlgeschlagen: {e}")

    def speichere_massnahme(self, zeitraum, beschreibung, ergebnis):
        """Save Maßnahme über Service"""
        try:
            protokol_service.save_action(zeitraum, beschreibung, ergebnis)
            self.show_message("Maßnahme gespeichert!")
        except ValueError as ve:
            self.show_message(str(ve))
        except Exception as e:
            self.show_message(f"Fehler: {e}")

    def validate_inputs(self):
        """GUI-Validierung, bevor Service aufgerufen wird"""
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", self.datum.text):
            self.show_message("Datum: DD-MM-YYYY")
            return False
        if not all(re.match(r"^\d{2}:\d{2}$", t.text) for t in [self.beginn, self.ende]):
            self.show_message("Zeit: HH:MM")
            return False
        if self.beginn.text >= self.ende.text:
            self.show_message("Beginn muss vor Ende sein!")
            return False
        if not all(getattr(self, f).text for f in ["grund","verursacher","auswirkung"]):
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

    def show_message(self, text):
        """Snackbar anzeigen"""
        MDSnackbar(text=text, duration=3).open()

    # =====================
    # === Statistik / Analyse ===
    # =====================
    def analyse_haeufigkeit(self):
        df = get_all_laermdaten()
        top = statistics_service.get_top_verursacher(df)
        if top:
            self.ids.haeufigster_verursacher.text = f"Häufigster: {top}"
        else:
            self.show_message("Keine Daten verfügbar!")

    def analyse_auswirkung(self):
        df = get_all_laermdaten()
        avg = statistics_service.get_average_auswirkung(df)
        self.ids.durchschnittliche_auswirkung.text = f"Ø Auswirkung: {avg:.2f}"

    def analyse_dauer(self):
        df = get_all_laermdaten()
        avg = statistics_service.get_average_duration(df)
        self.ids.durchschnittliche_dauer.text = f"Ø Dauer: {avg:.1f} Min"

    # =====================
    # === Plots / Menü ===
    # =====================
    def create_plot_menu(self):
        """Dropdown Menü der Plots erstellen"""
        from kivymd.uix.menu import MDDropdownMenu
        items = []
        plot_files = ["01_trend_dauer.png","02_histogramm_dauer.png","03_top_stoerungen.png","04_uhrzeiten.png","05_prognose.png"]
        for f in plot_files:
            path = os.path.join(PLOT_FOLDER, f)
            if os.path.exists(path):
                items.append({"viewclass":"OneLineListItem",
                              "text":f.split("_",1)[1].replace(".png","").replace("_"," ").title(),
                              "on_release": lambda x=f: self.show_plot(x)})
        self.menu = MDDropdownMenu(caller=self.ids.top_app_bar, items=items or [{"text":"Keine Plots verfügbar"}], width_mult=4)

    def show_plot(self, filename):
        path = os.path.join(PLOT_FOLDER, filename)
        if not os.path.exists(path):
            self.show_message("Plot nicht gefunden")
            return
        from kivymd.uix.fitimage import FitImage
        self.chart_box.clear_widgets()
        self.chart_box.add_widget(FitImage(source=path, allow_stretch=True))
        self.show_message(f"{filename} geladen")
        self.menu.dismiss()

    def menu_open(self):
        self.menu.open()

    def update_plots(self):
        """Alle Plots aktualisieren"""
        try:
            generate_plots()
            self.create_plot_menu()
            self.show_message("5 Analysen aktualisiert!")
            logging.info("Plots aktualisiert")
        except Exception as e:
            self.show_message(f"Plot-Update fehlgeschlagen: {e}")
            logging.error(f"Plot-Update Fehler: {e}")

# =====================
# === App-Klasse ===
# =====================
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

    def set_default_values(self, dt):
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M")
        for field in ["datum","beginn","ende"]:
            if hasattr(self.root, field):
                getattr(self.root, field).text = date_str if field=="datum" else time_str

if __name__ == "__main__":
    try:
        ProtokollApp().run()
    except Exception as e:
        logging.critical(f"App-Absturz: {e}")
        raise
