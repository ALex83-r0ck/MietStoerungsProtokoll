# MietStörungsProtokoll

**Zeitgestempeltes Protokoll für alle Arten von Mietstörungen**  
Lärm · Schimmel · Heizungsausfall · Nachbarschaftsstreit · defekte Gemeinschaftsanlagen · etc.

Desktop-App · Python + Kivy/KivyMD · 100 % offline-fähig · Open Source

## Warum dieses Projekt existiert

Ich bin selbst Mieter und steckte mitten in einem richtig nervigen Lärmstreit mit den Mietern über uns. Gleichzeitig gab es auch mit unserer Vermieterin immer wieder Situationen, bei denen man sich hinterher wünscht, **alles** lückenlos und zeitgestempelt dokumentiert zu haben.

Excel-Tabellen sind umständlich, handschriftliche Zettel mit meiner Sauklaue hätten vor Gericht sicher kein Gewicht – und fertige Vorlagen kosten Geld oder Nerven.

Deshalb habe ich dieses Tool gebaut.  
Ähnliches habe ich weder im App-Store noch als Open-Source-Projekt gefunden.

## Was die App leistet

Sie erstellt **zeitgestempelte, übersichtliche Protokolle – genau in der Form, wie Mietervereine und Gerichte sie als privates Beweismittel akzeptieren und empfehlen**.

## Features

| Status       | Funktion                                           |
|--------------|----------------------------------------------------|
| Done         | Zeitgestempelte Einträge mit freier Beschreibung   |
| Done         | Automatischer PDF-Export (klar strukturiert)        |
| Done         | Statistiken + Diagramme (Matplotlib)               |
| In Arbeit    | Erweiterung auf alle Störungsarten (Schimmel, Heizung, Nachbarn …) |
| In Arbeit    | Foto-Anhänge direkt im Eintrag                     |
| Geplant      | Fristenrechner & Erinnerungen                      |
| Geplant      | Vorlagen für Schreiben an Vermieter/Mieterverein   |

## Aktueller Stand – November 2025

Anfang war das ein klassisches „schnell mit KI zusammengeschustertes“ Hobby-Projekt (da auch schnell eine Lösung her musste).  
Seit November 2025 wird alles komplett neu und professionell aufgesetzt:

- Der ganze alte Code liegt offen im Ordner `/legacy` (Transparenz statt verstecken)
- Root ist sauber, moderne `pyproject.toml` + ruff + black + mypy (strict)
- Ziel: Clean-ish Architecture, ≥ 95 % Testabdeckung, SQLModel + Alembic
- Jeder Refactoring-Schritt ist im Commit-History nachvollziehbar

## Installation (noch Legacy-Version)

```bash
git clone https://github.com/ALex83-r0ck/MietStoerungsProtokoll.git
cd MietStoerungsProtokoll
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python legacy/app/main.py
```

Die neue saubere Version kommt Schritt für Schritt in den nächsten Wochen.

## Tech-Stack (Ziel)

Python 3.13 · Kivy/KivyMD · SQLModel + Alembic · Pydantic v2
pytest + Coverage ≥ 95 % · ruff, black, mypy (strict)

## Mitmachen?

Wer Lust hat – ob Debugging, neue Features, bessere Oberfläche oder einfach nur Feedback – ist herzlich willkommen.  

📧 **<rothe_alexander@t-online.de>**

Danke, für euer Interesse und das durchhalten.

Falls ihr selbst gerade Lärm, Schimmel oder ähnlichen Ärger habt – viel Kraft, und vielleicht hilft euch das Tool ein Stück weiter.
