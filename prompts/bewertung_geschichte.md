# Bewertungsbogen Geschichte (Prompt-Iteration)

Lauf: ____ · Prompt: system_2 v____ · Modell: ____________ · Datum: ________ · Bewertet von: ________

## Vorgehen

- Jeden der 8 Wege einmal vollständig in der Tablet-Ansicht durchlesen (S → zweiter Knoten → dritter Knoten → Ende).
- Hauptsächlich in der Lesestufe **Baum** bewerten. Zusätzlich je Weg die **Blatt**-Fassung querlesen: Hängen die Sätze zusammen?
- Vorher das Feld `plan` im JSON lesen: Ziel, offene Frage, Begleitfiguren, Hinweise.

## Kriterien (je Weg 1 bis 3)

| Nr. | Kriterium | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| K1 | **Ziel erkennbar:** Man weiß, was Frido will und warum es für die Klasse wichtig ist. | nicht erkennbar | erkennbar, aber blass | klar und tragend |
| K2 | **Neugier:** Jeder Knoten endet so, dass man weiterlesen will. | nein | teilweise | durchgehend |
| K3 | **Entscheidungen mit Folgen:** Die Wahl verändert spürbar Ton, Begleitung und Hinweis. | beliebig | teilweise | deutlich |
| K4 | **Ton für Klasse 3/4:** Sprache und Humor bzw. Spannung sprechen Kinder an. | unpassend | mittel | passend |

**Gesamturteil (G):** Weckt der Weg den Wunsch weiterzulesen? ja / nein

## Bewertung

| Weg | K1 | K2 | K3 | K4 | G (ja/nein) | Blatt zusammenhängend? (ja/nein) | Auffällige Stellen (Feld, Zitat) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AAA (lustig, Tier, Bilder) | | | | | | | |
| AAB (lustig, Tier, Text) | | | | | | | |
| ABA (lustig, Kind, Bilder) | | | | | | | |
| ABB (lustig, Kind, Text) | | | | | | | |
| BAA (spannend, Tier, Bilder) | | | | | | | |
| BAB (spannend, Tier, Text) | | | | | | | |
| BBA (spannend, Kind, Bilder) | | | | | | | |
| BBB (spannend, Kind, Text) | | | | | | | |
| **Mittelwert / Anzahl ja** | | | | | | | |

## Entscheidungsregel (vorab festgelegt am 27.10.2026)

- Variante 2+1 (Prompt-Überarbeitung) gilt als **ausreichend**, wenn bei höchstens der Hälfte der Wege G = nein ist (also mindestens 4 von 8 Wegen G = ja).
- Ist G bei 5 oder mehr Wegen nein: Wechsel zu Variante 5+1 (Abfrage der Interessen und Geschichte getrennt, lineare Geschichte).
- Die Mittelwerte K1 bis K4 zeigen, woran es liegt, und steuern die nächste Prompt-Iteration (z. B. K1 < 2 → Grundanlage schärfen).

## Formale Prüfung (Lehrkraftansicht)

Fehler: ____ · Warnungen: ____ · Bemerkungen: ______________________________
