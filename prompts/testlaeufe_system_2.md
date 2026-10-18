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

## Befunde

1. Die formale Prüfung ist bestanden, obwohl die Kernlogik (Weg → Buchmerkmale) in 6 von 8 Enden falsch ist. Die Prüfregeln 1–17 erfassen die Logik der Geschichte nicht.
2. Das Modell leitet die Merkmale je Weg nicht zuverlässig selbst ab; es wiederholt Muster (Texte und Aufträge werden kopiert statt dem Weg angepasst).
3. Die Lesestufen werden bei kurzen Texten (Optionen, Suchaufträge) nicht unterschieden.

## Versionen

| Version | Datum | Änderung |
| --- | --- | --- |
| v0.1 | 17.10.2026 | erste Fassung (Material-Schema 0.4, Suchaufträge vom Modell) |
| v0.2 | 18.10.2026 | Folge aus Lauf 1: verbindlicher Plan aller 15 Felder mit bisheriger Wahl und anstehender Entscheidung; Suchaufträge entfallen (Material-Schema 0.5, das Template bildet sie aus den Merkmalen des Weges); Optionen als Handlungen ohne Merkmalswort; Lesestufen auch bei Optionen verschieden; Fundstücke als 14 verschiedene Gegenstände; Brief „bald“, nicht „heute“; Absendetext in Fridos Ich-Form; kein Ersatz-Piktogramm mit anderer Bedeutung; Wortbilder in gleicher Wortform im Blatt-Text. |
