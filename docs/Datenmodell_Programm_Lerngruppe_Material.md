# Datenmodell\_Programm\_Lerngruppe\_Material

Oct 30, 2026 · @Anne

Das Datenmodell legt drei Datenstrukturen des Prototyps fest: das Programmprofil (Bibliotheksformular als JSON, Schema 0.4), das Lerngruppenprofil (Lehrkraft-Formular als JSON, Schema 0.4) und das Material (Ausgabe von LLM-Aufruf 2, **Schema 0.8**). Grundlage ist das Konzept „Vorbereitungsmaterial (Variante 5+1)“ vom 30.10.2026 mit der Änderung vom 31.10.2026 (Sachtext statt Geschichte). Frühere Fassungen liegen als `docs/Datenmodell_Schema_0.5.md` (verzweigte Geschichte), `docs/Datenmodell_Schema_0.6.md` (lineare Geschichte mit 4 Abschnitten) und `docs/Datenmodell_Schema_0.7.md` (lineare Geschichte mit 3 Abschnitten) im Repo.

**Material-Schema 0.6 (30.10.2026):** Die verzweigte Geschichte (7 Knoten, 8 Enden, Optionen, Fundstücke) entfällt. Neu sind eine lineare Geschichte mit 4 Abschnitten, der Rahmen des Antwortbriefs und Übersetzungen der Geschichte in die Familiensprachen. Teamnamen und Absendetext entfallen. Grund: Läufe 4 und 5 von System Prompt 2 (Befunde 6 und 7 im Testprotokoll).

**Material-Schema 0.7 (30.10.2026):** 3 statt 4 Abschnitte (der Abschnitt „Hinweis“ mit Rätsel entfällt); `plan.hinweis` entfällt, `plan.motiv` ist Pflicht. Grund: Läufe 6 und 7 (Befunde 8 und 9 im Testprotokoll).

**Material-Schema 0.8 (31.10.2026):** Die Geschichte entfällt ganz; an ihre Stelle tritt ein Sachtext „Das erwartet euch“ mit einem oder zwei Abschnitten, in denselben Varianten (Lesestufen, Bildfassung) und mit Übersetzungen. `plan`, `geschichte` und `suchkarte` entfallen (der Titel der Karte, jetzt „Lesefutter-Karte der <Klasse>“, ist fest in der Website), neu ist `sachtext` mit `quellen` und `abschnitte`. Fridos Brief wird kürzer (höchstens 400 Zeichen), verrät den Ablauf des Besuchs nicht und enthält keine erfundene Handlung. Grund: Lauf 8 und die Durchsicht am 31.10.2026 (Befund 11 im Testprotokoll).

## Dateien

| Datei | Inhalt | Entsteht durch |
| --- | --- | --- |
| `programme/<programm>.json` | Programmprofil der Bibliothek | Bibliotheksformular; Stufe 1 füllt vor, die Bibliothek prüft |
| `lerngruppen/<ID>.json` | Angaben der Lehrkraft | Lerngruppen-Formular (von Hand im Prototyp) |
| `materialien/<ID>.json` | Material: Fridos Brief, Sachtext, Rahmen des Antwortbriefs, Übersetzungen des Sachtexts | LLM-Aufruf 2 (Stufe 2) |
| `assets/interview/de.json` | Wortlaut des Interviews (Fassungen „lang“ für ⭐⭐/⭐⭐⭐ und „kurz“ für ⭐), Themenlisten, Beschriftung der Suchkarte | von Hand, aus dem Dokument „Interview Suchkarte – Wortlaut“ |
| `assets/interview/<sprache>.json` | dieselbe Struktur in einer Familiensprache | einmal je Sprache übersetzt (KI-gestützt), unabhängig vom Material; noch keine vorhanden |
| `assets/pictos/liste.json` | erlaubte Piktogramme: ID und Wort | von Hand, je Programm ergänzt |

Neu gegenüber 0.5: Die Sprachfassung als eigene Materialdatei (`<ID>.<sprache>.json`) entfällt. Übersetzt wird nur noch der Sachtext (bis 0.7: die Geschichte), und zwar innerhalb der Materialdatei. Interviewfragen und Themen sind fest und werden deshalb nur einmal je Sprache übersetzt.

## Lerngruppen-Datei

Unverändert Schema 0.4. Die Felder bleiben, ihre Wirkung ändert sich.

| Feld | Typ | Formularfeld | Werte |
| --- | --- | --- | --- |
| `schema_version` | Text | – | `"0.4"` |
| `programm` | Text | 1.1 | Dateiname des Programmprofils ohne Endung |
| `klasse` | Text | 2.1 | z. B. `"3b"`, höchstens 30 Zeichen |
| `tablets` | Zahl | 2.2 | ganze Zahl ab 1; ein Tablet je Paar |
| `jahrgaenge` | Liste | 2.3 | mindestens ein Wert aus 1, 2, 3, 4 |
| `lesestufen` | Liste | 3.1 | mindestens ein Wert aus `stufe1` (⭐), `stufe2` (⭐⭐), `stufe3` (⭐⭐⭐); bisher Blatt, Baum, Wald |
| `kaum_deutsch` | ja/nein | 3.2 | `true` oder `false` |
| `sprachen` | Liste | 3.3/3.4 | Sprachcodes, leer bei „nein“: `ar`, `bg`, `en`, `es`, `fa`, `it`, `pl`, `ro`, `ru`, `tr`, `uk` |
| `foerder` | Objekt | 4.1/4.2 | Anzahl je Bedarf, 0 = nicht angekreuzt: `sehen`, `lernen`, `sprache`, `motorik` |

**Ableitungsregeln** (gelten für Prompt, Template und Prüfung gleichermaßen)

1. Varianten des Sachtexts = `lesestufen`; dazu `stufe1`, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist; dazu `bild`, wenn `kaum_deutsch` = `true` ist oder `jahrgaenge` 1 oder 2 enthält.
2. `wortbilder` sind Pflicht, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist.
3. Je Eintrag in `sprachen` enthält das Material eine Übersetzung des Sachtexts, und zwar der einfachsten vorhandenen Stufe (in der Regel `stufe1`).
4. `foerder.sehen` größer 0 → das Template bietet Großdruck mit hohem Kontrast an.
5. `foerder.motorik`: keine eigene Wirkung mehr; die Lesefutter-Karte (bis 31.10.2026: Suchkarte) besteht ohnehin nur aus Kreuzen.
6. Die Vorlesefunktion zeigt das Template nur in `stufe1` (⭐).

Entfallen gegenüber 0.5: Teamnamen (Regel 3 alt) und die Ankreuz-Suchkarte als Sonderfall (Regel 5 alt).

**Beispiel** (`lerngruppen/4713.json`, unverändert)

```json
{
  "schema_version": "0.4",
  "programm": "straubing-bibliotheksdetektive",
  "klasse": "3b",
  "tablets": 8,
  "jahrgaenge": [3],
  "lesestufen": ["stufe2", "stufe3"],
  "kaum_deutsch": true,
  "sprachen": ["uk"],
  "foerder": {"sehen": 1, "lernen": 2, "sprache": 0, "motorik": 0}
}
```

Daraus folgen die Varianten `stufe1` (wegen Förderbedarf Lernen), `stufe2`, `stufe3` und `bild`, dazu Wortbilder und eine ukrainische Übersetzung der `stufe1`-Fassung.

## Programmprofil-Datei

Unverändert Schema 0.4 (Felder, Pflichtangaben, Belege und Prüfung mit `programm04.py` wie in der Fassung 0.5 beschrieben). Für Variante 5+1 werden zwei Felder wichtiger:

| Feld | Bedeutung in 5+1 |
| --- | --- |
| `worum_geht_es`, `buch_oder_thema`, `taetigkeiten`, `orte` | Grundlage für Brief, Sachtext und Rahmen des Antwortbriefs |
| `ausleihe`, `mitbringen` | `ausleihe`: `klassenausweis` (über die Lehrkraft mit Schulausweis), `eigener_ausweis` (Kinder einzeln), `nein` oder `null` (keine Angabe). Ein Wert außer `null` setzt voraus, dass die Bibliothek ihn in Stufe 1 bestätigt hat; das Material verspricht eine Ausleihe nur bei `klassenausweis` oder `eigener_ausweis`. Voraussetzung des Konzepts ist eine Ausleihe; `nein` wird künftig als Warnung gemeldet, `null` meldet `programm04.py` als fehlende Pflichtangabe. Im Testprofil `straubing-bibliotheksdetektive` ist der Wert seit 30.10.2026 `null`, weil die Bibliothek ihn nicht bestätigt hat. |

Weiterhin gesetzt, nicht abgefragt: Das Programm findet in der Bibliothek statt, und die Klasse hat Zeit zum Suchen oder Stöbern. Die Mailadresse der Bibliothek kommt in der echten Anwendung aus BipaMap.NRW und steht nicht im Profil; im Prototyp zeigt die Website nur eine Vorschau der Mail.

## Material-Datei (Schema 0.8)

Aufbau wie bisher: `meta`, `rahmen` (setzt das System), `generiert` (erzeugt das Modell).

### Übersicht `generiert`

| Feld | Inhalt | Regel |
| --- | --- | --- |
| `brief` | Fridos Brief an die Klasse | `text` höchstens 400 Zeichen, drei Teile durch Zeilenumbruch getrennt: „Hallo <klasse>!“, Hauptteil, „euer Frido“; wird gemeinsam vorgelesen, keine Varianten; verrät den Ablauf des Besuchs nicht; `quellen` = genutzte Felder |
| `bibliotheksblick` | Foto der Bibliothek | genau `[{"bild": 0, "quellen": ["programmprofil.foto"]}]` |
| `sachtext` | „Das erwartet euch“: was beim Besuch passiert | `quellen` (genutzte Felder, mindestens eines), `abschnitte` (1 oder 2) |
| `uebersetzungen` | Sachtext in den Familiensprachen | je Sprachcode so viele Texte wie Abschnitte (Ableitungsregel 3); fehlt, wenn `sprachen` leer ist |
| `wortbilder` | Piktogramme zu Schlüsselwörtern | Pflicht nach Ableitungsregel 2 |
| `antwortbrief` | Rahmen des Antwortbriefs der Klasse | siehe unten |
| `luecken` | fehlende Angaben im Programmprofil | Liste kurzer Sätze, leer = `[]` |

### Sachtext

`sachtext.abschnitte` ist eine Liste mit einem oder zwei Einträgen: 1 „Was passiert beim Besuch?“, 2 (nur wenn das Profil genug hergibt) „Wo seid ihr, und was gibt es noch?“. Jeder Eintrag hat ein Variantenfeld `text`. Der Sachtext ist sachlich, spricht die Kinder mit „ihr“ an und hat keine erzählende Figur; jede Aussage stammt aus dem Programmprofil.

| Variante | Regel |
| --- | --- |
| `stufe1` (⭐) | höchstens 180 Zeichen |
| `stufe2` (⭐⭐) | höchstens 300 Zeichen |
| `stufe3` (⭐⭐⭐) | höchstens 450 Zeichen |
| `bild` | Bildfolge, 1–4 Einträge |

### Übersetzungen

`uebersetzungen` ist ein Objekt: Schlüssel = Sprachcode aus `sprachen`, Wert = `{"stufe": "<übersetzte Stufe>", "abschnitte": [je Abschnitt ein Text]}`. Übersetzt wird die einfachste vorhandene Stufe (Ableitungsregel 3). Längengrenzen gelten als Warnung, weil Übersetzungen länger ausfallen können. Die Website zeigt die Übersetzung über den Knopf „Auch auf … lesen“ unter dem deutschen Text; die Lehrkraftansicht vermerkt „maschinell übersetzt, nicht geprüft“.

### Antwortbrief

`antwortbrief` enthält feste Textteile; die Website setzt die Vermutungen und Fragen der Klasse als Listen dazwischen. Das Modell schreibt keine Vermutungen oder Fragen selbst.

| Feld | Inhalt | Länge |
| --- | --- | --- |
| `anrede` | z. B. „Liebe Stadtbibliothek Straubing,“ | höchstens 80 |
| `einleitung` | wer die Klasse ist und worauf sie sich freut, mit Bezug zum Programm | höchstens 300 |
| `vor_vermutungen` | Überleitung zur Liste der Vermutungen | höchstens 120 |
| `vor_fragen` | Überleitung zur Liste der Fragen | höchstens 120 |
| `schluss` | Abschluss mit Bezug zum Programm | höchstens 200 |
| `gruss` | z. B. „Bis bald, eure 3b“ | höchstens 60 |

In der Stunde zeigt die Website den zusammengesetzten Brief in einem bearbeitbaren Feld. Fehlt eine der beiden Listen, lässt sie die zugehörige Überleitung weg.

### Bild-Einträge und Wortbilder

Unverändert gegenüber 0.5: Bild-Eintrag `{"picto", "wort", "suchwort"}`; `picto` aus der Liste oder `null` mit `suchwort`; `wort` genau ein Wort, höchstens 15 Zeichen. `wortbilder`: 1–20 Einträge; jedes `wort` kommt in mindestens einem `stufe1`-Text des Sachtexts vor.

### Meta

`schema_version` = `"0.8"`, `lerngruppe`, `erzeugt_von`, `prompt_version` (`"system_2 v0.8"`), `erzeugt_am`, `hinweis`.

### Entfallen gegenüber früheren Fassungen

`geschichte.knoten`, `geschichte.enden`, Optionen, Fundstücke, Symbole der Optionen, `teamnamen`, `absenden_text`, Sprachfassung als eigene Datei (0.6); Abschnitt „Hinweis“ und `plan.hinweis` (0.7); `geschichte` und `plan` insgesamt (0.8). Der Rucksack als Sammelbehälter entfällt im Konzept; Frido überbringt nur den Antwortbrief.

### Beispiel (verkürzt)

```json
{
  "meta": {"schema_version": "0.8", "lerngruppe": "4713", "erzeugt_von": "<Modell>", "prompt_version": "system_2 v0.8", "erzeugt_am": "2026-10-31", "hinweis": null},
  "rahmen": {"_herkunft": "P", "klasse": "3b", "bibliothek": "Stadtbibliothek Straubing", "programmtitel": "Bibliotheksdetektive", "bilder": [{"datei": "bilder/bilderbuchecke.svg", "beschreibung": "Bilderbuchecke in der Kinderbibliothek"}]},
  "generiert": {
    "_herkunft": "G",
    "brief": {"text": "Hallo 3b!\n<…>\neuer Frido", "quellen": ["lerngruppe.klasse", "programmprofil.bibliothek", "programmprofil.titel"]},
    "bibliotheksblick": [{"bild": 0, "quellen": ["programmprofil.foto"]}],
    "sachtext": {
      "quellen": ["programmprofil.worum_geht_es", "programmprofil.orte"],
      "abschnitte": [
        {"text": {"stufe1": "<…>", "stufe2": "<…>", "stufe3": "<…>", "bild": [{"picto": 3065, "wort": "Bibliothek"}]}},
        {"text": {"…": "…"}}
      ]
    },
    "uebersetzungen": {"uk": {"stufe": "stufe1", "abschnitte": ["<…>", "<…>"]}},
    "wortbilder": [{"picto": 2450, "wort": "Buch"}],
    "antwortbrief": {"anrede": "Liebe Stadtbibliothek Straubing,", "einleitung": "<…>", "vor_vermutungen": "<…>", "vor_fragen": "<…>", "schluss": "<…>", "gruss": "Bis bald, eure 3b"},
    "luecken": []
  }
}
```

## Prüfregeln (Schema 0.8)

Drei Zustände wie bisher: erfüllt, Warnung, Fehler. Dieselben Regeln prüfen die Lehrkraftansicht (`index.html`) und `werkzeuge/validate08.py`; beide liefern für dasselbe Material dieselben Meldungen. Ältere Schemata prüfen `werkzeuge/validate07.py` (0.7) und `werkzeuge/validate04.py` (0.5).

| Nr. | Regel | Bei Verstoß |
| --- | --- | --- |
| 1 | `meta.schema_version` ist `"0.8"` | Fehler |
| 2 | `meta.lerngruppe` stimmt mit der geladenen Lerngruppe überein | Warnung |
| 3 | Rahmendaten vollständig; jedes Bild hat Datei und Beschreibung | Fehler |
| 4 | Brief vorhanden, höchstens 400 Zeichen | Fehler |
| 5 | Brief beginnt mit „Hallo <klasse>!“ und endet mit „euer Frido“ | Warnung |
| 6 | Blick in die Bibliothek: genau 1 Bild | Fehler |
| 7 | Sachtext mit 1 oder 2 Abschnitten und mindestens einer Quelle | Fehler |
| 8 | Jedes Variantenfeld enthält genau die Varianten aus Ableitungsregel 1 | Fehler |
| 9 | Längengrenzen der Abschnitte eingehalten | Fehler |
| 10 | Bildfolgen: 1–4 Einträge; Bild-Eintrag nach den Regeln aus 0.5 (Wort, Liste, `suchwort`) | Fehler bzw. Warnung bei `picto: null` mit `suchwort` |
| 11 | `wortbilder` vorhanden, wenn Ableitungsregel 2 greift; jedes Wort steht in einem `stufe1`-Text | Fehler bzw. Warnung |
| 12 | Je Sprachcode der Lerngruppe eine Übersetzung mit so vielen Texten wie Abschnitten; keine Übersetzung ohne Sprachcode | Fehler |
| 13 | Übersetzungen innerhalb der Längengrenzen der übersetzten Stufe | Warnung |
| 14 | `antwortbrief`: alle 6 Felder vorhanden, Längengrenzen eingehalten | Fehler |
| 15 | `luecken` vorhanden | Fehler |
| 16 | Keine Felder aus früheren Schemata (`geschichte`, `plan`, `teamnamen`, `absenden_text`) | Fehler |
| 17 | Tablets mindestens so viele wie Varianten | Warnung (organisatorisch) |

**Ohne geladene Lerngruppe** (JSON nur eingefügt): Regel 8 prüft, dass alle Variantenfelder dieselben Varianten enthalten; die Regeln 2, 11 (Pflicht), 12 (Abgleich mit der Lerngruppe) und 17 entfallen.

## Offene Punkte

- Längengrenzen der Abschnitte (180/300/450) und des Briefs (400) sind Setzungen; nach Lauf 9 prüfen.
- `assets/interview/<sprache>.json`: Aufbau wie `de.json` (Interviewtexte in drei Fassungen `stufe1` bis `stufe3`); Übersetzungen erst, wenn der Wortlaut fertig redigiert ist. Ohne Datei bietet das Tablet keine Sprachwahl im Interview an.
- Bildsymbole für die 16 Themen und die Rollen (🎤, 💬) sind noch festzulegen; sie gehören zur Website, nicht zum Material. In `de.json` stehen vorläufig Emoji als Platzhalter.
- Piktogramm-Dateien: Das Tablet zeigt ein Piktogramm nur, wenn `assets/pictos/<ID>.png` vorhanden ist, sonst nur das Wort. Die Lehrkraftansicht listet fehlende Dateien. Ausnahme: Das Piktogramm „Biber“ (7055) steht in der Bildfassung für Frido; die Website zeigt dafür die Frido-Figur (`assets/biber/biber-kopf.svg`) mit dem Wort „Frido“, eine Datei `7055.png` ist nicht nötig.
- Datenmodell, Prompts und Prüfwerkzeuge werden weiterhin von Hand gleich gehalten.

## Umsetzungsstand

Stand 31.10.2026: Prompt v0.8 und Schema 0.8 sind spezifiziert. `index.html` und `werkzeuge/validate08.py` werden auf Schema 0.8 umgestellt; `materialien/4713.json` wird durch das Ergebnis von Lauf 9 ersetzt. Das Material aus Lauf 8 (Schema 0.7) liegt in `materialien/archiv/`.

Korrekturen der Lehrkraft speichert die Lehrkraftansicht nur im Browser. Damit die Tablets sie zeigen, lädt die Lehrkraft die geprüfte Fassung herunter (`meta.hinweis` vermerkt Datum und geänderte Felder) und ersetzt damit `materialien/<ID>.json`. In der Anwendung übernähme das die Plattform: Sie speichert die freigegebene Fassung zentral und liefert sie an alle Geräte aus.
