# Testläufe System Prompt 1 (Stufe 1: Vorbefüllung des Programmprofils)

## Bedingungen (alle Läufe)

| Merkmal | Wert |
| --- | --- |
| Plattform | Academic Cloud, Chat AI (GWDG) |
| Modell | Qwen3 30B A3B Instruct 2507 |
| System Prompt | nicht als System Prompt einstellbar; Inhalt von `system_1.md` am Anfang der ersten Nachricht |
| Temperatur | nicht eingestellt (Standard der Plattform, Wert unbekannt) |
| Prüfung | `werkzeuge/programm04.py --vorbefuellt --quelle` und redaktioneller Abgleich mit dem Quelltext |
| Quellen | Programmbeschreibungen der Stadtbibliothek Straubing (PDF, Canva, Stand 18.09.2024) |

## Läufe

| Nr. | Datum | Prompt | Programm | Eingabe | Ergebnis |
| --- | --- | --- | --- | --- | --- |
| 1 | 16.10.2026 | v0.1 | Auf den Spuren der Waldbewohner | PDF angehängt | PDF nicht gelesen. Titel, Inhalt, Orte, Ausleihe und 7 von 7 Belegen erfunden; Formatprüfung ohne Fehler. |
| 2 | 16.10.2026 | v0.1 | Auf den Spuren der Waldbewohner | nur URL | Inhaltlich wortgleich mit Lauf 1 (Ursache unklar: selber Chat oder niedrige Temperatur); kein Quelltext gelesen. |
| 3 | 16.10.2026 | v0.1 | Auf den Spuren der Waldbewohner | Text kopiert | Keine erfundenen Inhalte; 7 von 7 Belegen wörtlich. Fehler: unbelegte Schlüsse (`ausleihe` aus „Durchführbar in: Schule“, `orte` = „Bücherei“), `stoebern` und `erkunden` ohne Grundlage, `bibliothek` aus der Programm-ID, 2 Belege über 150 Zeichen. Quellenangaben weichen von der Eingabe ab (möglicherweise Reste früherer Läufe im selben Chat). |
| 4 | 17.10.2026 | v0.2 | Bibliotheksdetektive | Text kopiert, neuer Chat | Keine erfundenen Inhalte; Ort richtig (`true`); `ausleihe` bei „Ausleihmodalitäten kennen“ richtig `null`. Fehler: `stoebern` und `zuhoeren` ohne Grundlage, `orte` = Bibliotheksgebäude („Salzstadel“), thematische Rahmung („Krimi“) übersehen, Titel mit Zielgruppe, 1 Beleg umgestellt (nicht wörtlich), 1 Beleg über 150 Zeichen. |

## Befunde

1. Ohne lesbaren Quelltext erfindet das Modell eine plausible Ausgabe, statt `null` zu setzen; auch die Belege sind erfunden. Die Formatprüfung erkennt das nicht, die Prüfung auf wörtliche Belege schon (Lauf 1: 7 von 7).
2. Mit Quelltext treten keine erfundenen Inhalte mehr auf, wohl aber Zuordnungs- und Schlussfehler: Ein echtes Zitat wird als Beleg für eine Angabe genutzt, die es nicht trägt. Das erkennt nur die redaktionelle Prüfung.
3. Die Regel gegen Schlussfolgerungen (v0.2) wirkte bei `ausleihe`; die Regeln zu `orte` und `stoebern` hielt das Modell nicht ein.
4. `stoebern` wurde in 2 von 2 Läufen mit Quelltext ohne Grundlage gesetzt. Folge: Ab v0.3 setzt Stufe 1 `stoebern` nie; die Bibliothek kreuzt es selbst an.
5. Die Längengrenze für Belege (150 Zeichen) wurde in allen Läufen mit Quelltext überschritten; das ist folgenlos (Warnung) und wird nicht weiter angepasst.

## Versionen

| Version | Datum | Änderung |
| --- | --- | --- |
| v0.1 | 16.10.2026 | erste Fassung |
| v0.2 | 17.10.2026 | nur Quelltext zählt; keine Schlüsse; Regel bei fehlendem Quelltext; Feld `findet_in_bibliothek_statt`; `orte` ohne die Bibliothek selbst; `katalog` eng gefasst; Beleglänge betont |
| v0.3 | 17.10.2026 | `stoebern` wird von Stufe 1 nie gesetzt. Festgeschrieben: keine weitere Anpassung an einzelne Testquellen. |
