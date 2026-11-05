# GitHub für KMU und Solo-Selbständige

> **Git und GitHub als versionsicheres Arbeits-, Wissens- und Redaktionssystem für kleine und mittlere Unternehmen (KMU), Solopreneure und Nicht-Programmierer.**

---

## 🎯 Über dieses Repository

GitHub wird häufig als reine Entwicklungsplattform für Programmierer wahrgenommen. Dieses Projekt zeigt, wie Solo-Selbständige, Freiberufler, Berater und KMU Git und GitHub gezielt für die tägliche Wissensarbeit einsetzen können:

* **Schluss mit dem Dateichaos:** Nie wieder Dateinamen wie `Konzept_final_v2_wirklich.docx`. Eine Datei besitzt eine lückenlose, nachvollziehbare Versionshistorie.
* **Redaktions- und Autorensystem:** Strukturierte Erstellung von Buchmanuskripten, Whitepapern, Playbooks und Dokumentationen mit Markdown.
* **Nachvollziehbarkeit & Zeitstempel:** Transparente Protokolle für Textstände, Meilensteine und Freigaben.
* **Wissens- und Vorlagensammlung:** Zentrale Pflege wiederverwendbarer Prozesse, Audits, Checklisten und Prompt-Bibliotheken.
* **Einfache Projektsteuerung & Automatisierung:** Aufgabenverwaltung via Issues und Boards sowie Veröffentlichung (z. B. via GitHub Pages) oder automatisierte Workflows (GitHub Actions).

---

## 📁 Repository-Struktur

```text
├── code/       # Hilfsskripte (Python) für Automatisierung und Setup
├── pdf/        # Präsentationen und Leitfäden als PDF
└── txt/        # Ausarbeitungen, Artikel-Entwürfe und Textrecherchen (Markdown)
```

### 1. `code/` – Werkzeuge & Automatisierung

Praktische Python-Skripte (erfordert Python 3.8+ ohne externe Abhängigkeiten):

* **`setup_buchprojekt.py`**:
  Initialisiert per Knopfdruck eine vollständige Redaktionsstruktur für Buch- oder Dokumentationsprojekte (inkl. Ordner für `manuskript/`, `recherche/`, `produktion/`, Vorlagen für Inhaltsverzeichnis, Kapitel, Quellen- und Zitate-Tracking sowie Lektorats-Checklisten).
  ```bash
  python3 code/setup_buchprojekt.py [ZIELPFAD]
  ```

* **`add_frontmatter.py`**:
  Analysiert Markdown-Dateien und ergänzt sie automatisiert um einen standardisierten YAML-Kopfteil (Front Matter mit `id`, `title`, `date`, `model`, `language`, `status`, `author`, `classification`).
  ```bash
  # Trockenlauf (zeigt geplante Änderungen an):
  python3 code/add_frontmatter.py ./txt

  # Änderungen anwenden:
  python3 code/add_frontmatter.py ./txt --apply

  # Validierung (prüft auf Duplikate, ungültige IDs oder fehlende Pflichtfelder):
  python3 code/add_frontmatter.py ./txt --check
  ```

### 2. `pdf/` – Leitfäden & Präsentationen

Enthält visuelle Foliensätze und Leitfäden zum Thema:
* `GitHub_für_KMU_und_Solo-Selbständige.pdf`
* `GitHub_für_Solopreneure.pdf`

### 3. `txt/` – Texte, Recherchen & Entwürfe

Textbeiträge und strukturierte Notizen im Markdown-Format (mit standardisiertem YAML-Header):
* Anwendungsfelder und Strategien für Solopreneure & KMU
* Vergleich und Funktionsweise von Git ohne Programmierbezug
* Leitfäden zur Strukturierung von Beratungsprojekten und Redaktionsprozessen
* Beiträge mit Unterstützung verschiedener Sprachmodelle (z. B. Claude, Perplexity, GPT, NotebookLM) erarbeitet und dokumentiert

---

## 🚀 Schnelleinstieg

### Voraussetzungen
* [Git](https://git-scm.com/) (lokal installiert)
* [Python 3.8+](https://www.python.org/) (Standardbibliothek genügt)
* Optional: Ein kostenloser Account auf [GitHub](https://github.com/) sowie ein Git-GUI wie [GitHub Desktop](https://desktop.github.com/) oder [VS Code](https://code.visualstudio.com/)

### Skripte ausführen

1. **Repository klonen:**
   ```bash
   git clone https://github.com/calyaconsult/github-fuer-kmu.git
   cd github-fuer-kmu
   ```

2. **Texte prüfen:**
   ```bash
   python3 code/add_frontmatter.py txt --check
   ```

3. **Neues Buch-/Schreibprojekt anlegen:**
   ```bash
   python3 code/setup_buchprojekt.py ~/mein-neues-buch
   ```

---

## 📄 Lizenz & Kontakt

Erstellt von **Michael Glünz / Calya Consult** ([calyaconsult.com](https://calyaconsult.com)).
Fragen, Anregungen oder Feedback können gerne über [GitHub Issues](https://github.com/calyaconsult/github-fuer-kmu/issues) eingereicht werden.
