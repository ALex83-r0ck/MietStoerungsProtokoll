# Protolkoli – Dein Lärmprotokoll. Gerichtsfest. Automatisch. Kostenlos.

> **„Ich habe 2 Jahre gelitten. Jetzt habe ich Beweise.“**  
> — Alexander Rothe, Entwickler & Betroffener

[![Stars](https://img.shields.io/github/stars/ALex83-r0ck/Protolkoli?style=social)](https://github.com/ALex83-r0ck/Protolkoli)
[![Downloads](https://img.shields.io/github/downloads/ALex83-r0ck/Protolkoli/total)](https://github.com/ALex83-r0ck/Protolkoli/releases)
[![License](https://img.shields.io/github/license/ALex83-r0ck/Protolkoli)](LICENSE)

<img src="https://github.com/user-attachments/assets/ff4416e3-a960-4c64-a0e3-e8ecb8b38a53" width="100%">

---

## Warum diese App existiert

Ich habe **2 Jahre unter Dauerlärm gelitten**.  
- Nachbarn über mir: Trampeln, Klavier, Geschrei  
- Vermieter: „Kann ich nichts machen“  
- Polizei: „Kein Notfall“  

Ich habe **alles dokumentiert**. Mit Stift. Auf Papier.  
→ **Verloren nach 2 Monaten**

**Protolkoli ist die App, die ich damals gebraucht hätte.**

---

## Features, die dich retten werden

| Feature                        | Status | Beweis |
|-------------------------------|--------|------|
| Lärm in 10 Sekunden erfassen   | Done   | Draggable Cards |
| Automatische Dauerberechnung   | Done   | SQLite Trigger |
| **Gerichtsfeste PDF-Protokolle** | Done   | `Lärmprotokoll_vom_07-11-2025.pdf` |
| **15 Analysen + Prognose**     | Done   | Heatmap, Trend, KI-Vorhersage |
| 100% Offline + lokal          | Done   | Kein Cloud-Zwang |
| Datenbank-Migration            | Done   | Alte Daten werden übernommen |

---

## Installation (2 Minuten)

```bash
git clone https://github.com/ALex83-r0ck/Protolkoli.git
cd Protolkoli
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python protokoll.py
```bash

In 30 Sekunden loslegen

App starten
Lärm eintragen (Datum, Zeit, „Trampeln“, „Nachbar oben“, 4)
Klick auf PDF → fertig!
An Vermieter schicken → Schweigen


Projektstruktur (Profi-Level)
textProtolkoli/
├── database/          → Migrationen, Trigger, Setup
├── utils/             → Plots, PDFs, Bilder
├── custom_widget/     → Draggable Cards
├── data/reports/      → Deine Beweise
├── plots/             → 15 Analysen
└── tests/             → Ja, ich habe Tests

Kommende Features (Hilf mit!)

 Android APK (Buildozer)
 Mikrofon-Integration (Decibel-Messung)
 Verschlüsselter Cloud-Sync
 Anwalt-Vorlage als Word
 Dark Mode


Mitmachen? Unbedingt!
bashgit checkout -b feature/dein-name
# z.B. "fix: dark mode"
git push origin feature/dein-name
Jeder PR wird persönlich gedankt – mit Name im CONTRIBUTORS.md!

Lizenz
MIT – Mach damit, was du willst.
Aber wenn du jemanden rettest, schick mir eine DM. Das ist alles, was ich will.

Protolkoli – Weil Lärm kein Schicksal ist.
Made with ❤️ and too much coffee
Alexander Rothe – angehender FIAE
GitHub: @ALex83-r0ck
E-Mail: alexander.rothe@t-online.de

„Das beste Projekt entsteht aus dem größten Schmerz.“