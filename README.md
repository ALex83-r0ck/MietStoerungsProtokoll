# 📝 Lärmprotokoll-App

Diese **Lärmprotokoll-App** ermöglicht es, Lärmstörungen detailliert zu protokolieren und hilft somit beim Nachweis in rechtlichen Auseinandersetzungen oder bei Gesprächen mit Vermietern. Sie bietet eine einfache Benutzeroberfläche zur Eingabe und Anzeige von Störungen/Diagrammen und speichert alle Daten in einer SQLite-Datenbank. Auch ist eine automatische Protokoll (PDF) erstellung Implementiert.

## Projektbeschreibung: Lärmprotokoll-App
### Hintergrund:
In vielen **Mietverhältnissen** kann es zu wiederholtem Lärm und Störungen kommen, die sowohl das Wohlbefinden als auch die Lebensqualität beeinträchtigen. Oftmals bleibt die Kommunikation mit den Nachbarn oder der Hausverwaltung erfolglos. In solchen Fällen ist es wichtig, eine detaillierte und strukturierte Aufzeichnung der Lärmstörungen zu führen, um bei Bedarf auf konkrete Beweise zurückgreifen zu können.
### Ziel:
Diese App wird entwickelt, um ein benutzerfreundliches und effizientes Lärmprotokoll zu führen. Sie ermöglicht es, Lärmstörungen systematisch zu dokumentieren, die wichtigsten Daten wie Datum, Uhrzeit und Art der Störung festzuhalten und auf einfache Weise zu verwalten. Die gesammelten Informationen können später übersichtlich exportiert und als Nachweis genutzt werden.
### Funktionen:
- **Strukturierte Eingabe**: Der Benutzer kann wichtige Informationen wie Datum, Uhrzeit und Art des Lärms in übersichtlichen Feldern eingeben.
  
- **Interaktive Benutzeroberfläche**: Das Design der App ermöglicht eine einfache Bedienung durch die Nutzung von verschiebbaren Karten, die unterschiedliche Abschnitte des Protokolls enthalten.

- **PDF-Export**: Einmal erfasste Protokolle können als PDF-Datei erstellt werden, um sie zu speichern oder an relevante Stellen weiterzuleiten.

- **Flexibles Layout**: Der Benutzer kann die Ansicht nach seinen Bedürfnissen anpassen, sodass er das Protokoll effizient führen kann.
### Zielgruppe:
Diese App richtet sich an **Mieter**, die regelmäßig Lärmstörungen erleben und eine strukturierte Möglichkeit suchen, diese zu dokumentieren. Sie ist ebenfalls nützlich für Personen, die **rechtliche Schritte gegen ihre Nachbarn oder Vermieter einleiten möchten und auf eine solide Dokumentation angewiesen sind**.
### Zukunftsperspektiven:
Die App ist derzeit als Desktop-Version in Entwicklung. In der Zukunft ist geplant, auch eine mobile Version zu entwickeln, die eine noch flexiblere Nutzung ermöglicht. Das Projekt soll ständig erweitert und verbessert werden, um weitere Funktionen hinzuzufügen und die Benutzerfreundlichkeit zu optimieren.
### Warum GitHub? Und warum das als erstes großes Projekt?
Ich teile dieses Projekt auf GitHub, um es mit anderen zu teilen, die möglicherweise ähnliche Herausforderungen haben und diese Lösung ebenfalls nutzen oder weiterentwickeln möchten. GitHub bietet eine großartige Möglichkeit für Feedback, Zusammenarbeit und Weiterentwicklung der App. Es ist auch eine Plattform, die eine kontinuierliche Verbesserung des Codes und die Dokumentation des Entwicklungsprozesses ermöglicht.
Zudem bin gerade selber in so einer Situation deswegen der Entschluss hierzu.

## 🚀 Features

- 📅 **Verschiebbare Cards und Diagrame** 
- 📅 **Erfassung von Lärmdaten** (Datum, Beginn, Ende, Dauer)
- 📊 **Analyse und Ausgabe mit Digrammen**
- 💾 **Speicherung der Daten** in einer SQLite-Datenbank
- 🔄 **Automatische Berechnung der Störungsdauer**
- ⚙️ **Einfache Benutzeroberfläche** mit Kivy & Kivymd
- 🛠️ **Möglichkeit, die Datenbank zu manipulieren** Einträge löschen, abändern, durchsuchen
- 🖥️ **Benutzerfreundlichkeit**

## 📋 Installation

## 1. Repository klonen

Code kopieren:

```bash
git clone git@github.com:ALex83-r0ck/Protolkoli.git
```

## 2. Virtuelle Umgebung einrichten

Erstelle und aktiviere eine virtuelle Umgebung:

```bash
git clone https://github.com/ALex83-r0ck/Protolkoli.git
cd Protolkoli
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python protokoll.py
```

## 👨‍💻 Nutzung

Nach dem Start der App kannst du:

Lärmdaten mit den folgenden Informationen erfassen:

- Datum der Störung
- Beginn und Ende der Störung
- Störungsgrund
- Verursacher (z.B. Nachbar)
- Auswirkungen der Störung (Bewertung von 1 bis 5)

Die Daten werden in einer SQLite-Datenbank gespeichert und sind leicht abrufbar.

## 🛠️ Technologien

***Kivy/Kivymd***: Für die Erstellung der grafischen Benutzeroberfläche

***SQLite***: Datenbank zur Speicherung der Störungen

***Python***: Hauptsprache des Projekts

***Pandas***: Zum analysieren der Daten

***Matplotlib***: Zum erstellen der Charts

## 🤝 Beitrag

Beiträge sind willkommen! Wenn du neue Features oder Verbesserungen hast, fork das Repository und schick einen Pull-Request.
Achte darauf, die bestehenden Code-Konventionen zu befolgen und Tests für neue Features zu schreiben.

## Schritte zum Beitrag

- Forke das Repository
- Erstelle einen Branch (git checkout -b feature-xyz)
- Implementiere die Änderungen
- Teste deine Änderungen
- Schicke einen Pull-Request an den main-Branch

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Details findest du in der LICENSE-Datei.

## 🖼️ Screenshots

Hier ist ein Beispiel, wie die Benutzeroberfläche aussieht:

![NewLayout](https://github.com/user-attachments/assets/ff4416e3-a960-4c64-a0e3-e8ecb8b38a53)
![Unbenannt1](https://github.com/user-attachments/assets/fd72d292-4241-41b5-9580-51c048590a4e)

## 📝 To-Do's

- [ ] Layout verbessern
