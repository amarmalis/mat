# Eingabe für Stufe 1 (Vorlage)

Diese Nachricht schickst du nach dem System Prompt 1 in denselben Chat. Kopiere nur den Teil im Codeblock und ersetze die Teile in spitzen Klammern (die Klammern fallen weg). Jede Quelle steht zwischen ihren Markierungen, damit das Modell sie auseinanderhalten kann.

```
PROGRAMM-ID: <z. B. straubing-bibliotheksdetektive>

DOKUMENTE: <Dateinamen, durch Komma getrennt, oder: keine>
WEBSEITEN: <Adressen, durch Komma getrennt, oder: keine>

=== QUELLE 1: <Dateiname oder Adresse> ===
<Text der Quelle, kopiert>
=== ENDE QUELLE 1 ===

=== QUELLE 2: <Dateiname oder Adresse> ===
<Text der Quelle, kopiert>
=== ENDE QUELLE 2 ===

Erstelle das Programmprofil nach den Regeln.
```

Hinweise:
- Für jeden Lauf einen neuen Chat öffnen, damit keine früheren Antworten mitwirken.
- Den Text jeder Quelle kopieren. Angehängte PDF-Dateien und bloße Adressen werden je nach Chat-Umgebung nicht gelesen (Academic Cloud, Test vom 16.10.2026: nicht gelesen).
- Unter DOKUMENTE und WEBSEITEN nur Quellen nennen, deren Text unten eingefügt ist.
- Danach prüfen mit `werkzeuge/programm04.py`: `python3 programm04.py ausgabe.json --vorbefuellt --quelle quelltext.txt`. Die Prüfung findet Formfehler und Belege, die nicht wörtlich im Quelltext stehen; ob ein Beleg die Angabe inhaltlich trägt, bleibt redaktionelle Prüfung.
