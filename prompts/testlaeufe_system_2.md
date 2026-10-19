# Testläufe System Prompt 2 (Stufe 2: Materialerzeugung)

## Bedingungen (alle Läufe)

| Merkmal | Wert |
| --- | --- |
| Plattform | Academic Cloud, Chat AI (GWDG) |
| Modell | Qwen3 30B A3B Instruct 2507 |
| System Prompt | nicht einstellbar; Inhalt von `system_2.md` am Anfang der Nachricht, Eingabe direkt darunter |
| Temperatur | nicht eingestellt (Standard der Plattform, Wert unbekannt) |
| Prüfung | Lehrkraftansicht (Prüfregeln 1–17) und Abgleich der Wege mit den Buchmerkmalen; redaktionelle Durchsicht |

## Läufe

| Nr. | Datum | Prompt | Programm / Lerngruppe | Ergebnis |
| --- | --- | --- | --- | --- |
| 1 | 18.10.2026 | v0.1 | Bibliotheksdetektive / 4713 | Ausgabe vollständig, kein Abbruch. Formale Prüfung: 0 Fehler, 1 Warnung (5 von 6 Wortbildern nicht in Blatt-Texten). Inhaltlich unbrauchbar: nur 2 von 8 Suchaufträgen passen zu den Merkmalen ihres Weges; Knotentexte nehmen spätere Entscheidungen vorweg oder widersprechen dem Weg; Optionen nennen das Merkmal wörtlich („Lustig: Kichern“); alle 14 Optionstexte in allen Stufen gleich; 6 verschiedene Fundstücke auf 14 Optionen; Piktogramm „Lehrerin“ für „Kind“; Brief behauptet „Heute geht es in die Bibliothek“; Absendetext gibt die Anweisung wieder („Frido verabschiedet sich …“); Detektiv-Motiv kaum aufgegriffen. |
| 2 | 18.10.2026 | v0.2 | Bibliotheksdetektive / 4713 | Ausgabe vollständig. Formale Prüfung: 0 Fehler, 1 Warnung (Wortbilder nicht in Blatt-Texten, darunter „Lehrerin“, „ja“). Verbessert: kein Widerspruch zwischen Weg und Endtext, Optionen als Handlungen, Fundstücke sind Gegenstände, Brief „bald“, Absendetext in Ich-Form, Orte aus dem Profil genutzt. Weiter fehlerhaft: Optionen von `B` identisch mit `A`, Optionen von `AA`, `AB`, `BA`, `BB` identisch (6 verschiedene Fundstücke auf 14 Optionen); alle 14 Optionstexte in allen Stufen gleich; alle 8 Endtexte Blatt = Baum; jeder Endtext nennt nur 2 der 3 Merkmale; Endtexte behaupten, das Buch sei schon gefunden; Knoten `AA` und `BB` nehmen Entscheidung 3 vorweg, `BA` ohne Tier-Bezug; Optionen beziehen sich auf nicht eingeführte Dinge (Schnurrbart, Schulranzen); Ersatz-Piktogramme mit anderer Bedeutung („Tür“ für Kästchen, „ja“ für Bilder anschauen); `erzeugt_am` 2026-10-17 statt Datum des Laufs. |
| 3 | 18.10.2026 | v0.2 | Bibliotheksdetektive / 4713 | **Modellvergleich: Claude Sonnet 5.5 (claude.ai, Denkaufwand „hoch“)**, gleicher Prompt, gleiche Eingabe. Formale Prüfung: 0 Fehler, 1 Warnung (17 Piktogramme fehlen in der Liste, korrekt als `null` mit Suchwort). Alle Regeln der Tabelle eingehalten: jeder Knoten passt zu bisheriger Wahl und Entscheidung, jedes Ende zu allen drei Merkmalen; 14 verschiedene Fundstücke, die in späteren Knoten wieder aufgegriffen werden (Hut, Lupe, Schlüssel); alle Optionen und Endtexte je Lesestufe verschieden; Längen knapp unter den Grenzen (79/148/225); Detektiv-Motiv durchgehend, Fall nicht aufgelöst; alle vier Orte aus dem Profil genutzt; Brief „bald“, Absendetext in Ich-Form. Kleinere Mängel: „Frido“ als Wortbild ohne Piktogramm, obwohl „Biber“ (7055) in der Liste steht; „zuhören“ für „Rascheln“ nur bedeutungsnah; `erzeugt_von` und `erzeugt_am` falsch, weil aus einer veralteten Eingabedatei übernommen. |

## Befunde

1. Die formale Prüfung ist bestanden, obwohl die Kernlogik (Weg → Buchmerkmale) in 6 von 8 Enden falsch ist. Die Prüfregeln 1–17 erfassen die Logik der Geschichte nicht.
2. Das Modell leitet die Merkmale je Weg nicht zuverlässig selbst ab; es wiederholt Muster (Texte und Aufträge werden kopiert statt dem Weg angepasst).
3. Die Lesestufen werden bei kurzen Texten (Optionen, Suchaufträge) nicht unterschieden.
4. Lauf 2 (v0.2): Die vorgegebene Tabelle beseitigt Widersprüche zwischen Weg und Ende, aber das Modell vervielfältigt Inhalte statt sie je Feld neu zu schreiben (gleiche Optionen in mehreren Knoten, gleiche Fassung in mehreren Stufen). Mehrere ausdrückliche Regeln werden nicht eingehalten (Lesestufen verschieden, 14 verschiedene Fundstücke, kein Ersatz-Piktogramm). Offen ist, ob das an der Größe des Modells oder am Prompt liegt.
5. Lauf 3 (Modellvergleich): Mit demselben Prompt erfüllt Claude Sonnet 5.5 die Regeln weitgehend. Die Fehler aus Lauf 1 und 2 liegen damit vor allem am Modell (Qwen3 30B A3B), nicht am Prompt. Für die Arbeit: Abwägung zwischen Leistungsfähigkeit (kommerzielles Modell) und Hosting in deutscher Hochschulinfrastruktur (Academic Cloud).

## Versionen

| Version | Datum | Änderung |
| --- | --- | --- |
| v0.1 | 17.10.2026 | erste Fassung (Material-Schema 0.4, Suchaufträge vom Modell) |
| v0.2 | 18.10.2026 | Folge aus Lauf 1: verbindlicher Plan aller 15 Felder mit bisheriger Wahl und anstehender Entscheidung; Suchaufträge entfallen (Material-Schema 0.5, das Template bildet sie aus den Merkmalen des Weges); Optionen als Handlungen ohne Merkmalswort; Lesestufen auch bei Optionen verschieden; Fundstücke als 14 verschiedene Gegenstände; Brief „bald“, nicht „heute“; Absendetext in Fridos Ich-Form; kein Ersatz-Piktogramm mit anderer Bedeutung; Wortbilder in gleicher Wortform im Blatt-Text. |
| v0.3 | 18.10.2026 | Folge aus dem Funktionstest der Seite mit Lauf 3: Zeitpunkt des Fundstücks festgelegt (es wird im Text des folgenden Abschnitts entdeckt); das Template zeigt seither erst diesen Text, dann das Fundstück. Lauf 3 entspricht dem bereits. |
