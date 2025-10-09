from email.mime import image
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from utils.data_processing import analyse_dauer
from utils.pdf_generation import generiere_protokoll, generiere_massnahmen
from custom_widget import draggable_card
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.fitimage import FitImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivy_garden.graph import Graph, MeshLinePlot
from database.database_setup import create_database, insert_laermdaten, get_all_laermdaten, insert_massnahmen
from datetime import datetime
import re
import os

PLOTER_FOLDER = os.path.join(os.getcwd(), "plots")

class RootWidget(MDBoxLayout):
    plot_menu_button = ObjectProperty()
    chart_box = ObjectProperty()
    datum = ObjectProperty()
    beginn = ObjectProperty()
    ende = ObjectProperty()
    grund = ObjectProperty()
    verursacher = ObjectProperty()
    auswirkung = ObjectProperty()
    zeitraum = ObjectProperty()
    beschreibung = ObjectProperty()
    ergebnis = ObjectProperty()
    menu_open = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        app = MDApp.get_running_app()
        if app is not None:
            Clock.schedule_once(lambda dt: app.set_default_values(), 0)

    def generiere_protokoll(self):
        # Get the data from the input fields
        data = [
            [
                self.datum,
                self.beginn,
                self.ende,
                self.grund,
                self.verursacher,
                self.auswirkung
            ]
        ]

        # Call the function that generates the protocol PDF
        generiere_protokoll(data)
    
    def generiere_massnahmen(self):
        self.zeitraum = self.ids.massnahme_zeitraum.text.strip()
        self.beschreibung = self.ids.massnahme_beschreibung.text.strip()
        self.ergebnis = self.ids.massnahme_ergebnis.text.strip()


        # Daten für die PDF-Generierung vorbereiten
        data = [
            {
                self.zeitraum,
                self.beschreibung,
                self.ergebnis,
            }
        ]

        # PDF generieren
        generiere_massnahmen(data)

    def generiere_alle_protokolle(self):
        self.generiere_protokoll()  # Lärmprotokoll
        self.generiere_massnahmen()  # Maßnahmenprotokoll

    def save_data(self):
        """Speichert die Eingabedaten in der Datenbank."""
        try:
            datum = self.datum.text
            beginn = self.beginn.text
            ende = self.ende.text
            grund = self.grund.text
            verursacher = self.verursacher.text
            auswirkung = self.auswirkung.text

            # Validierung der Eingaben
            app = MDApp.get_running_app()
            if app is None or not app.validate_inputs(datum, beginn, ende, grund, verursacher, auswirkung):
                return

            # Daten in die Datenbank einfügen
            insert_laermdaten(datum, beginn, ende, grund, verursacher, auswirkung)
            app_instance = MDApp.get_running_app()
            if app_instance is not None:
                app_instance.show_message("Daten erfolgreich gespeichert!")
            else:
                print("Daten erfolgreich gespeichert!")
        except Exception as e:
            app_instance = MDApp.get_running_app()
            if app_instance is not None:
                app_instance.show_message(f"Fehler: {e}")
            else:
                print(f"Fehler: {e}")

    def load_data(self):
        """Lädt die gespeicherten Daten aus der Datenbank."""
        try:
            data = get_all_laermdaten()
            print("Gespeicherte Daten:")
            for entry in data:
                print(entry)
            app_instance = MDApp.get_running_app()
            if app_instance is not None:
                app_instance.show_message("Daten erfolgreich geladen!")
            else:
                print("Daten erfolgreich geladen!")
        except Exception as e:
            app_instance = MDApp.get_running_app()
            if app_instance is not None:
                app_instance.show_message(f"Fehler: {e}")
            else:
                print(f"Fehler: {e}")


class ProtokollApp(MDApp):
    def __init__(self, **kwargs):
        super(ProtokollApp, self).__init__(**kwargs)
        self.menu = None

    def build(self):
        #Builder.load_file("protokoll.kv")
        create_database()  # Datenbank erstellen
        self.root = RootWidget()
        self.create_plot_menu()
        return self.root

    def on_start(self):
        self.set_default_values()

    def set_default_values(self, *args):
        """Setzt Standardwerte für Datum und Zeit"""
        current_date = datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.now().strftime("%H:%M")

        for field, value in [("datum", current_date), ("beginn", current_time), ("ende", current_time)]:
            if self.root.ids.get(field):
                getattr(self.root, field).text = value

    def validate_inputs(self, datum, beginn, ende, grund, verursacher, auswirkung):
        datum_pattern = r"^\d{4}-\d{2}-\d{2}$"
        zeit_pattern = r"^\d{2}:\d{2}$"
        if not re.match(datum_pattern, datum):
            self.show_message("Datum im Format YYYY-MM-DD eingeben!")
            return False
        if not all(re.match(zeit_pattern, t) for t in [beginn, ende]):
            self.show_message("Zeit im Format HH:MM eingeben!")
            return False
        if beginn >= ende:
            self.show_message("Beginn muss vor Ende liegen!")
            return False
        if not all([grund, verursacher, auswirkung]):
            self.show_message("Bitte alle Felder ausfüllen!")
            return False
        return True

    def show_message(self, message):
        """Zeigt eine Nachricht in der App (z. B. als Snackbar)."""
        from kivymd.uix.snackbar import Snackbar
        Snackbar(text=message).open()

    def analyse_haeufigkeit(self):
        """Analyse des häufigsten Verursachers."""
        try:
            data = get_all_laermdaten()
            if data:
                verursacher = [row[4] for row in data]
                haeufigster = max(set(verursacher), key=verursacher.count)
                self.root.ids.haeufigster_verursacher.text = f"Häufigster Verursacher: {haeufigster}"
        except Exception as e:
            self.show_message(f"Fehler bei der Häufigkeitsanalyse: {e}")

    def analyse_auswirkung(self):
        """Durchschnittliche Auswirkung berechnen."""
        try:
            data = get_all_laermdaten()
            if data:
                auswirkungen = [int(row[5]) for row in data]
                durchschnitt = sum(auswirkungen) / len(auswirkungen)
                self.root.ids.durchschnittliche_auswirkung.text = f"Durchschnittliche Auswirkung: {durchschnitt:.2f}"
        except Exception as e:
            self.show_message(f"Fehler bei der Auswirkungsanalyse: {e}")

    def analyse_dauer(self):
        """Ruft die Methode zur Daueranalyse auf und zeigt das Ergebnis an."""
        data = get_all_laermdaten()
        durchschnitt = analyse_dauer(data)
        self.root.ids.durchschnittliche_dauer.text = f"Durchschnittliche Dauer: {durchschnitt}"

    def erfasse_daten(self, datum, beginn, ende, grund, verursacher, auswirkung):
        """Daten erfasen un in der Datenbank speichern"""
        # Validierung: Sind alle Felder ausgefüllt?
        if not datum or not beginn or not ende or not grund or not verursacher or not auswirkung:
            print("Bitte die Felder ausfüllen!")
            return
        
        # Daten in die DB speichern
        try:
            insert_laermdaten(datum, beginn, ende, grund, verursacher, auswirkung)
            print("Daten erfolgreich gespeichert!")
        except Exception as e:
            print(f"Fehler beim Speichern der Daten: {e}")

    def speichere_massnahme(self, zeitraum, beschreibung, ergebnis):
        """Massnahme-Daten speichern"""
        # Validierung: Sind alle Felder ausgefüllt?
        if not zeitraum or not beschreibung or not ergebnis:
            print("Bitte füllen Sie alle Felder aus.")
            return

        # Daten speichern (z.B. in einer Datenbank)
        try:
            insert_massnahmen(zeitraum, beschreibung, ergebnis)  # Funktion aus database_setup
            print("Massnahme erfolgreich gespeichert!")
        except Exception as e:
            print(f"Fehler beim Speichern der Massnahme: {e}")

    def create_plot_menu(self):
        """Erstellt ein Dropdown-Menü für generierte Plots."""
        plot_folder = "./plots"
        menu_items = []

        try:
            if os.path.exists(plot_folder):
                for plot_file in os.listdir(plot_folder):
                    if plot_file.endswith(".png"):
                        menu_items.append(
                            {
                                "viewclass": "OneLineListItem",
                                "text": plot_file,
                                "on_release": lambda x=plot_file: self.show_plot(x),
                            }
                        )
            else:
                self.show_message("Der Ordner 'plots' ist nicht vorhanden.")
        except Exception as e:
            self.show_message(f"Fehler beim Laden der Plots: {e}")

        # Menu erstellen auch wenn keine Items vorhanden sind
        self.menu = MDDropdownMenu(
            caller=self.root.ids.top_app_bar,
            items=menu_items or [{"text": "Keine Plots verfügbar", "viewclass": "OneLineListItem"}],
            width_mult=4,
        )


    def show_plot(self, plot_file):
        """Zeigt den ausgewählten Plot in der App an."""
        plot_path = os.path.join(PLOTER_FOLDER, plot_file)

        # Wenn der Plot existiert, anzeigen
        if os.path.exists(plot_path):
            self.root.ids.chart_box.clear_widgets()
            image = FitImage(source=plot_path)
            self.root.ids.chart_box.add_widget(image)
        else:
            self.show_message(f"Plot '{plot_file}' wurde nicht gefunden.")

        # Menü schließen
        if self.menu is not None:
            self.menu.dismiss()


    def menu_open(self):
        """Öffnet das DDM"""
        if self.menu:
            self.menu.open()
        else:
            self.show_message("Das Menü ist nicht initialisiert.")


if __name__ == '__main__':
    ProtokollApp().run()