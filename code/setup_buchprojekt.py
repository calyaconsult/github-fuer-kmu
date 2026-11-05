#!/usr/bin/env python3
"""
Setup-Skript für ein GitHub-Buchprojekt-Repository
Erstellt automatisch die Ordnerstruktur und Standard-Markdown-Vorlagen.
"""

import os
import sys
import subprocess

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"  [✓] Erstellt: {path}")

def main():
    base_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"🚀 Richte Buchprojekt-Struktur ein in: {base_dir}\n")

    # 1. README.md
    readme_content = """# Buchprojekt: [Buchtitel einfügen]

## Über dieses Repository
Dieses Repository dient als zentrales, versionsicheres Redaktionssystem für das Buchprojekt.

### 📁 Struktur
* `manuskript/` – Buchkapitel im Markdown-Format
* `recherche/` – Quellen, Zitate, Interviewnotizen und Nachweise
* `produktion/` – Lektorats-, Druck- und Veröffentlichungs-Checklisten

### ⚙️ Workflow & Konventionen
* Jedes Kapitel liegt als eigene Markdown-Datei vor.
* Offene Fragen, Recherche-Lücken und Lektoratspunkte werden über **GitHub Issues** nachverfolgt.
* Vor großen Überarbeitungen wird ein Commit mit aussagekräftiger Nachricht erstellt.
"""
    create_file(os.path.join(base_dir, "README.md"), readme_content)

    # 2. Manuskript-Vorlagen
    titel_content = """# Inhaltsverzeichnis & Buchübersicht

**Arbeitstitel:** [Dein Buchtitel]
**Untertitel:** [Dein Untertitel]
**Autor:in:** [Dein Name]
**Stand:** [Datum]

---

## Kapitelübersicht
- [ ] **Kapitel 1:** [Titel 1] (`manuskript/01_kapitel_1.md`)
- [ ] **Kapitel 2:** [Titel 2] (`manuskript/02_kapitel_2.md`)
- [ ] **Anhang:** [Titel Anhang] (`manuskript/99_anhang.md`)
"""
    create_file(os.path.join(base_dir, "manuskript", "00_titel_inhaltsverzeichnis.md"), titel_content)

    kapitel1_content = """# Kapitel 1: [Kapiteltitel]

> **Kernbotschaft des Kapitels:** [1-2 Sätze zur Hauptaussage]

---

## 1.1 Einleitung
[Hier mit dem Schreiben beginnen...]

## 1.2 Hauptteil
[Weitere Abschnitte...]

---
*Notizen für Überarbeitung:*
- [ ] Quellen für Zitat X prüfen
- [ ] Abbildung/Grafik einfügen
"""
    create_file(os.path.join(base_dir, "manuskript", "01_kapitel_1.md"), kapitel1_content)

    anhang_content = """# Anhang & Register

## Glossar
| Begriff | Erklärung |
| :--- | :--- |
| **Beispielbegriff** | Erklärung des Begriffs |

## Literaturverzeichnis & Weblinks
* Quellenübersicht siehe `recherche/quellen_und_zitate.md`
"""
    create_file(os.path.join(base_dir, "manuskript", "99_anhang.md"), anhang_content)

    # 3. Recherche-Vorlagen
    quellen_content = """# Quellen- und Zitatesammlung

| ID | Quelle / Autor | Zitat / Kernaussage | Verwendung im Buch | Status |
| :--- | :--- | :--- | :--- | :--- |
| Q01 | Max Mustermann (2025) | "Kernaussage hier..." | Kapitel 1, Abs. 2 | [ ] Geprüft |
"""
    create_file(os.path.join(base_dir, "recherche", "quellen_und_zitate.md"), quellen_content)

    zitat_content = """# Zitatprüfungen & Rechtliches

## Rechte-Clearing & Genehmigungen
- [ ] Zitat 1 (Name Rechteinhaber): Freigabe angefragt / erteilt am [Datum]
- [ ] Bild/Grafik 1: Lizenz geklärt (z. B. CC-BY / Kauf-Lizenz)
"""
    create_file(os.path.join(base_dir, "recherche", "zitatpruefungen.md"), zitat_content)

    os.makedirs(os.path.join(base_dir, "recherche", "interviewnotizen"), exist_ok=True)
    create_file(os.path.join(base_dir, "recherche", "interviewnotizen", ".gitkeep"), "# Ordner für Interview-Notizen")

    # 4. Produktion & Lektorat
    lektorat_content = """# Lektorats-Checkliste

## 1. Inhaltlicher Durchgang (Makro-Lektorat)
- [ ] Roter Faden in allen Kapiteln nachvollziehbar
- [ ] Logische Kapitelreihenfolge und verständliche Übergänge
- [ ] Vollständigkeit der Argumente und Beispiele

## 2. Sprachlicher Durchgang (Mikro-Lektorat)
- [ ] Einheitliche Begriffe und Tonalität
- [ ] Schachtelsätze vereinfacht
- [ ] Rechtschreibung, Grammatik und Zeichensetzung korrigiert

## 3. Formale Prüfung
- [ ] Alle Überschriften korrekt hierarchisch formatiert (`#`, `##`, `###`)
- [ ] Verweise und Fußnoten geprüft
"""
    create_file(os.path.join(base_dir, "produktion", "lektorats_checkliste.md"), lektorat_content)

    druck_content = """# Druck- & Formatierungs-Checkliste

- [ ] Buchsatz & Seitenumbruch kontrolliert
- [ ] Cover-Abmessungen & Rückenstärke von Druckerei bestätigt
- [ ] ISBN und Impressum auf Innenseite vorhanden
- [ ] Testdruck bestellen und Korrektur lesen
"""
    create_file(os.path.join(base_dir, "produktion", "druck_checkliste.md"), druck_content)

    plan_content = """# Veröffentlichungsplan & Meilensteine

| Meilenstein | Zieldatum | Status |
| :--- | :--- | :--- |
| Rohfassung abgeschlossen | YYYY-MM-DD | [ ] Ausstehend |
| Lektorat beendet | YYYY-MM-DD | [ ] Ausstehend |
| Korrektorat & Buchsatz | YYYY-MM-DD | [ ] Ausstehend |
| Druckfreigabe / E-Book Export | YYYY-MM-DD | [ ] Ausstehend |
| Veröffentlichungstermin | YYYY-MM-DD | [ ] Ausstehend |
"""
    create_file(os.path.join(base_dir, "produktion", "veroeffentlichungs_plan.md"), plan_content)

    # Git Init (Optional)
    print("\n💡 Tipp: Führe im Zielordner 'git init' aus, um das Git-Repository zu starten.")
    print("✅ Setup erfolgreich abgeschlossen!")

if __name__ == "__main__":
    main()
