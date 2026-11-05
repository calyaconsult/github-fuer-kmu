#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_frontmatter.py - ergänzt Markdown-Dateien um einen YAML-Kopfteil (Front Matter).

Felder: id (6-stellig, hexadezimal), title, date, updated, model, language,
        status, author, classification

Ablauf:
  1. Alle *.md-Dateien unterhalb eines Ordners werden gesucht (.git wird übersprungen).
  2. Dateien, die schon einen Kopfteil haben, werden NICHT verändert.
     Ihre IDs werden aber eingelesen, damit keine Doppelten entstehen.
  3. Die ID wird aus den ersten 6 Zeichen der UUID im Dateinamen abgeleitet.
     Bei Kollision oder fehlender UUID wird eine ID aus dem Dateinamen-Hash
     gebildet (und bei Bedarf weiter gesucht).
  4. Ohne --apply wird nur angezeigt, was passieren würde (Trockenlauf).

Beispiele:
  python add_frontmatter.py ./txt                       # Trockenlauf
  python add_frontmatter.py ./txt --apply               # wirklich schreiben
  python add_frontmatter.py ./txt --apply --author "Max Muster"
  python add_frontmatter.py ./txt --check               # nur prüfen (Duplikate, fehlende Felder)

Nur Standardbibliothek, Python 3.8 oder neuer.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# Dateiname-Endung -> Modellbezeichnung. Nach Bedarf anpassen/ergänzen.
MODEL_BY_SUFFIX = {
    "claude": "Claude (Anthropic)",
    "chatgpt": "ChatGPT (OpenAI)",
    "gpt": "GPT (OpenAI)",
    "gemini": "Gemini (Google)",
    "mistral": "Mistral",
    "copilot": "Copilot (Microsoft)",
}
DEFAULT_MODEL = "unbekannt"

UUID_RE = re.compile(
    r"^([0-9a-f]{8})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{4})-([0-9a-f]{12})",
    re.I,
)
ID_RE = re.compile(r"^[0-9a-f]{6}$")
REQUIRED_KEYS = ["id", "date", "model"]
SKIP_DIRS = {".git", "node_modules", ".github", ".venv", "__pycache__"}
SKIP_FILES = {"readme.md", "license.md", "_template.md"}


def q(value):
    """Text als gültigen YAML-String (doppelte Anführungszeichen) ausgeben."""
    return json.dumps(str(value), ensure_ascii=False)


def read_text(path):
    """Datei lesen; liefert (Text, hatte_BOM, Zeilenende)."""
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.replace("\r\n", "\n"), bom, newline


def write_text(path, text, bom, newline):
    data = text.replace("\n", newline).encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    path.write_bytes(data)


def split_front_matter(text):
    """Liefert (kopfteil_text oder None, rest)."""
    m = re.match(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def get_key(block, key):
    m = re.search(r"^%s:[ \t]*(.*?)[ \t]*(?:#.*)?$" % re.escape(key), block, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def first_heading(body):
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def guess_language(body):
    """Sehr einfache Sprach-Erkennung über häufige Wörter."""
    words = re.findall(r"[a-zäöüéèàçîôùâêû]+", body.lower()[:5000])
    hints = {
        "de": {"der", "die", "das", "und", "nicht", "ist", "mit", "ein", "für"},
        "fr": {"le", "la", "les", "des", "et", "est", "une", "pour", "dans"},
        "it": {"il", "lo", "gli", "che", "per", "una", "con", "sono", "della"},
        "en": {"the", "and", "is", "of", "to", "with", "for", "that", "this"},
    }
    scores = {lang: sum(1 for w in words if w in hs) for lang, hs in hints.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "de"


def git_first_date(path):
    """Datum des ersten Commits der Datei (oder None)."""
    try:
        out = subprocess.run(
            ["git", "log", "--follow", "--diff-filter=A", "--format=%as", "--", path.name],
            cwd=path.parent, capture_output=True, text=True, timeout=15,
        ).stdout.strip().splitlines()
        return out[-1] if out else None
    except (OSError, subprocess.SubprocessError):
        return None


def pick_date(path, source):
    if source == "today":
        return dt.date.today().isoformat()
    if source == "git":
        d = git_first_date(path)
        if d:
            return d
    # mtime (auch Rückfall für git)
    return dt.datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()


def model_from_name(path, default):
    stem = path.stem.lower()
    for suffix, name in MODEL_BY_SUFFIX.items():
        if stem.endswith("-" + suffix) or stem.endswith("_" + suffix):
            return name
    return default


def make_id(path, used):
    """6-stellige Hex-ID. Bevorzugt: Anfang der UUID im Dateinamen."""
    candidates = []
    m = UUID_RE.match(path.stem)
    if m:
        full = "".join(m.groups()).lower()      # 32 Hex-Zeichen
        candidates += [full[i:i + 6] for i in range(0, 27, 6)]
    # Rückfall: Hash aus Dateiname, bei Bedarf mit Zähler
    n = 0
    while True:
        for c in candidates:
            if c not in used:
                return c
        candidates = [hashlib.sha1(f"{path.name}#{n}".encode()).hexdigest()[:6]]
        n += 1


def find_files(root):
    for p in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts[:-1]):
            continue
        if p.name.lower() in SKIP_FILES:
            continue
        yield p


def build_block(meta):
    lines = ["---"]
    lines.append(f"id: {q(meta['id'])}")
    lines.append(f"title: {q(meta['title'])}")
    lines.append(f"date: {meta['date']}")
    lines.append(f"updated: {meta['date']}")
    lines.append(f"model: {q(meta['model'])}")
    lines.append(f"language: {meta['language']}")
    lines.append(f"status: {meta['status']}")
    lines.append(f"author: {q(meta['author'])}")
    lines.append(f"classification: {meta['classification']}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def main():
    ap = argparse.ArgumentParser(description="YAML-Kopfteil in Markdown-Dateien einfügen.")
    ap.add_argument("ordner", help="Ordner mit den .md-Dateien (wird rekursiv durchsucht)")
    ap.add_argument("--apply", action="store_true", help="Änderungen wirklich schreiben")
    ap.add_argument("--check", action="store_true",
                    help="Nur prüfen: doppelte IDs, ungültige IDs, fehlende Pflichtfelder")
    ap.add_argument("--model", default=None,
                    help="Modell für alle Dateien (sonst aus Dateiname, sonst 'unbekannt')")
    ap.add_argument("--author", default="", help="Verantwortliche Person (Standard: leer)")
    ap.add_argument("--status", default="entwurf",
                    choices=["entwurf", "geprüft", "veröffentlicht", "veraltet"])
    ap.add_argument("--classification", default="öffentlich",
                    choices=["öffentlich", "intern", "vertraulich"])
    ap.add_argument("--date-source", default="git", choices=["git", "mtime", "today"],
                    help="Quelle für das Datum (Standard: erster Git-Commit, sonst Änderungsdatum)")
    args = ap.parse_args()

    root = Path(args.ordner)
    if not root.is_dir():
        sys.exit(f"Ordner nicht gefunden: {root}")

    files = list(find_files(root))
    if not files:
        sys.exit("Keine .md-Dateien gefunden.")

    # Schritt 1: vorhandene Kopfteile einlesen
    used = {}          # id -> Dateipfad
    todo = []
    problems = 0
    for p in files:
        text, _, _ = read_text(p)
        block, _ = split_front_matter(text)
        if block is None:
            todo.append(p)
            if args.check:
                print(f"[FEHLT]    {p}: kein Kopfteil")
                problems += 1
            continue
        fid = get_key(block, "id")
        if args.check:
            for k in REQUIRED_KEYS:
                if get_key(block, k) in (None, ""):
                    print(f"[FELD]     {p}: Pflichtfeld '{k}' fehlt")
                    problems += 1
        if fid:
            if not ID_RE.match(fid):
                print(f"[UNGÜLTIG] {p}: ID '{fid}' ist nicht 6-stellig hexadezimal")
                problems += 1
            if fid in used:
                print(f"[DOPPELT]  ID {fid}: {used[fid]} und {p}")
                problems += 1
            used[fid] = p

    if args.check:
        print(f"\n{len(files)} Dateien geprüft, {problems} Problem(e).")
        sys.exit(1 if problems else 0)

    # Schritt 2: fehlende Kopfteile ergänzen
    done = 0
    for p in todo:
        text, bom, newline = read_text(p)
        new_id = make_id(p, used)
        used[new_id] = p
        meta = {
            "id": new_id,
            "title": first_heading(text) or p.stem,
            "date": pick_date(p, args.date_source),
            "model": args.model or model_from_name(p, DEFAULT_MODEL),
            "language": guess_language(text),
            "status": args.status,
            "author": args.author,
            "classification": args.classification,
        }
        block = build_block(meta)
        print(f"{'[NEU]' if args.apply else '[TROCKEN]'} {p}  ->  id={new_id}, "
              f"date={meta['date']}, model={meta['model']}, lang={meta['language']}")
        if args.apply:
            write_text(p, block + text.lstrip("\n"), bom, newline)
        done += 1

    skipped = len(files) - len(todo)
    print(f"\n{done} Datei(en) {'geändert' if args.apply else 'würden geändert'}, "
          f"{skipped} übersprungen (Kopfteil vorhanden).")
    if not args.apply and done:
        print("Mit --apply wirklich schreiben. Tipp: vorher alles mit git committen.")


if __name__ == "__main__":
    main()

