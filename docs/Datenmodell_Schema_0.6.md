# Datenmodell\_Programm\_Lerngruppe\_Material

Oct 30, 2026 · @Anne

Das Datenmodell legt drei Datenstrukturen des Prototyps fest: das Programmprofil (Bibliotheksformular als JSON, Schema 0.4), das Lerngruppenprofil (Lehrkraft-Formular als JSON, Schema 0.4) und das Material (Ausgabe von LLM-Aufruf 2, **Schema 0.6**). Grundlage ist das Konzept „Vorbereitungsmaterial (Variante 5+1)“ vom 30.10.2026. Die Fassung für Schema 0.5 (verzweigte Geschichte) liegt als `docs/Datenmodell_Schema_0.5.md` im Repo.

**Material-Schema 0.6 (30.10.2026):** Die verzweigte Geschichte (7 Knoten, 8 Enden, Optionen, Fundstücke) entfällt. Neu sind eine lineare Geschichte mit 4 Abschnitten, der Rahmen des Antwortbriefs und Übersetzungen der Geschichte in die Familiensprachen. Teamnamen und Absendetext entfallen. Grund: Läufe 4 und 5 von System Prompt 2 (Befunde 6 und 7 im Testprotokoll).

## Dateien

| Datei | Inhalt | Entsteht durch |
| --- | --- | --- |
| `programme/<programm>.json` | Programmprofil der Bibliothek | Bibliotheksformular; Stufe 1 füllt vor, die Bibliothek prüft |
| `lerngruppen/<ID>.json` | Angaben der Lehrkraft | Lerngruppen-Formular (von Hand im Prototyp) |
| `materialien/<ID>.json` | Material: Fridos Brief, Geschichte, Rahmen des Antwortbriefs, Übersetzungen der Geschichte | LLM-Aufruf 2 (Stufe 2) |
| `assets/interview/<sprache>.json` | Interviewfragen und Themen in einer Familiensprache | einmal je Sprache übersetzt (KI-gestützt), unabhängig vom Material |
| `assets/pictos/liste.json` | erlaubte Piktogramme: ID und Wort | von Hand, je Programm ergänzt |

Neu gegenüber 0.5: Die Sprachfassung als eigene Materialdatei (`<ID>.<sprache>.json`) entfällt. Übersetzt wird nur noch die Geschichte, und zwar innerhalb der Materialdatei. Interviewfragen und Themen sind fest und werden deshalb nur einmal je Sprache übersetzt.

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

1. Varianten der Geschichte = `lesestufen`; dazu `stufe1`, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist; dazu `bild`, wenn `kaum_deutsch` = `true` ist oder `jahrgaenge` 1 oder 2 enthält.
2. `wortbilder` sind Pflicht, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist.
3. Je Eintrag in `sprachen` enthält das Material eine Übersetzung der Geschichte, und zwar der einfachsten vorhandenen Stufe (in der Regel `stufe1`).
4. `foerder.sehen` größer 0 → das Template bietet Großdruck mit hohem Kontrast an.
5. `foerder.motorik`: keine eigene Wirkung mehr; die Suchkarte besteht ohnehin nur aus Kreuzen.
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
| `worum_geht_es`, `buch_oder_thema`, `orte` | Grundlage für Brief, Geschichte und Rahmen des Antwortbriefs; aus ihnen bestimmt das Modell die Kulisse und ob das Programm eine Auflösung beim Besuch bietet |
| `ausleihe` | `klassenausweis` (über die Lehrkraft mit Schulausweis), `eigener_ausweis` (Kinder einzeln) oder `nein`. Voraussetzung des Konzepts ist eine Ausleihe; `nein` wird künftig als Warnung gemeldet. |

Weiterhin gesetzt, nicht abgefragt: Das Programm findet in der Bibliothek statt, und die Klasse hat Zeit zum Suchen oder Stöbern. Die Mailadresse der Bibliothek kommt in der echten Anwendung aus BipaMap.NRW und steht nicht im Profil; im Prototyp zeigt die Website nur eine Vorschau der Mail.

## Material-Datei (Schema 0.6)

Aufbau wie bisher: `meta`, `rahmen` (setzt das System), `generiert` (erzeugt das Modell).

### Übersicht `generiert`

| Feld | Inhalt | Regel |
| --- | --- | --- |
| `plan` | Planung der Geschichte, wird nicht angezeigt | `motiv` (ab system_2 v0.6), `ort`, `ausgangslage`, `hinweis`, `offene_frage` (je höchstens 200 Zeichen), `aufloesung_beim_besuch` (true/false) |
| `brief` | Fridos Brief an die Klasse | `text` höchstens 600 Zeichen, wird gemeinsam vorgelesen, keine Varianten; `quellen` = genutzte Felder |
| `bibliotheksblick` | Foto der Bibliothek | genau `[{"bild": 0, "quellen": ["programmprofil.foto"]}]` |
| `geschichte` | lineare Geschichte | `kulisse`, `kulisse_quellen`, `abschnitte` (genau 4) |
| `uebersetzungen` | Geschichte in den Familiensprachen | je Sprachcode 4 Texte (Ableitungsregel 3); fehlt, wenn `sprachen` leer ist |
| `wortbilder` | Piktogramme zu Schlüsselwörtern | Pflicht nach Ableitungsregel 2 |
| `antwortbrief` | Rahmen des Antwortbriefs der Klasse | siehe unten |
| `suchkarte` | `kartenkopf` | Überschrift der Suchkarte mit Klassenname, höchstens 40 Zeichen |
| `luecken` | fehlende Angaben im Programmprofil | Liste kurzer Sätze, leer = `[]` |

### Geschichte

`geschichte.abschnitte` ist eine Liste mit genau 4 Einträgen in fester Reihenfolge: 1 Aufbruch, 2 Ankunft, 3 Hinweis, 4 offenes Ende. Jeder Eintrag hat ein Variantenfeld `text`.

| Variante | Regel |
| --- | --- |
| `stufe1` (⭐) | höchstens 180 Zeichen |
| `stufe2` (⭐⭐) | höchstens 300 Zeichen |
| `stufe3` (⭐⭐⭐) | höchstens 450 Zeichen |
| `bild` | Bildfolge, 1–4 Einträge |

Die Längen sind Setzungen (vier Abschnitte in etwa 10 Minuten Lesezeit); nach dem ersten Test prüfen. `kulisse` bleibt `programmwelt`, `thema` oder `allgemein` wie in 0.5.

### Übersetzungen

`uebersetzungen` ist ein Objekt: Schlüssel = Sprachcode aus `sprachen`, Wert = `{"stufe": "<übersetzte Stufe>", "abschnitte": [4 Texte]}`. Übersetzt wird die einfachste vorhandene Stufe (Ableitungsregel 3). Längengrenzen gelten als Warnung, weil Übersetzungen länger ausfallen können. Die Website zeigt die Übersetzung über den Knopf „Auch auf … lesen“ unter dem deutschen Text. Vermerk in `meta.hinweis` oder der Lehrkraftansicht: „maschinell übersetzt, nicht geprüft“.

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

Unverändert gegenüber 0.5: Bild-Eintrag `{"picto", "wort", "suchwort"}`; `picto` aus der Liste oder `null` mit `suchwort`; `wort` genau ein Wort, höchstens 15 Zeichen. `wortbilder`: 1–20 Einträge; jedes `wort` kommt in mindestens einem `stufe1`-Text der Geschichte vor.

### Meta

`schema_version` = `"0.6"`, `lerngruppe`, `erzeugt_von`, `prompt_version` (`"system_2 v0.5"`), `erzeugt_am`, `hinweis`.

### Entfallen gegenüber 0.5

`geschichte.knoten`, `geschichte.enden`, Optionen, Fundstücke, Symbole der Optionen, `teamnamen`, `absenden_text`, Sprachfassung als eigene Datei.

### Beispiel (verkürzt)

```json
{
  "meta": {"schema_version": "0.6", "lerngruppe": "4713", "erzeugt_von": "<Modell>", "prompt_version": "system_2 v0.5", "erzeugt_am": "2026-10-30", "hinweis": null},
  "rahmen": {"_herkunft": "P", "klasse": "3b", "bibliothek": "Stadtbibliothek Straubing", "programmtitel": "Bibliotheksdetektive", "bilder": [{"datei": "bilder/bilderbuchecke.svg", "beschreibung": "Bilderbuchecke in der Kinderbibliothek"}]},
  "generiert": {
    "_herkunft": "G",
    "plan": {"motiv": "<…>", "ort": "Ausleihtheke", "ausgangslage": "<…>", "hinweis": "<…>", "offene_frage": "<…>", "aufloesung_beim_besuch": true},
    "brief": {"text": "Hallo 3b! <…> euer Frido", "quellen": ["lerngruppe.klasse", "programmprofil.worum_geht_es"]},
    "bibliotheksblick": [{"bild": 0, "quellen": ["programmprofil.foto"]}],
    "geschichte": {
      "kulisse": "programmwelt",
      "kulisse_quellen": ["programmprofil.orte", "programmprofil.worum_geht_es"],
      "abschnitte": [
        {"text": {"stufe1": "<…>", "stufe2": "<…>", "stufe3": "<…>", "bild": [{"picto": 7055, "wort": "Biber"}]}},
        {"text": {"…": "…"}}, {"text": {"…": "…"}}, {"text": {"…": "…"}}
      ]
    },
    "uebersetzungen": {"uk": {"stufe": "stufe1", "abschnitte": ["<…>", "<…>", "<…>", "<…>"]}},
    "wortbilder": [{"picto": 2450, "wort": "Buch"}],
    "antwortbrief": {"anrede": "Liebe Stadtbibliothek Straubing,", "einleitung": "<…>", "vor_vermutungen": "<…>", "vor_fragen": "<…>", "schluss": "<…>", "gruss": "Bis bald, eure 3b"},
    "suchkarte": {"kartenkopf": "Detektiv-Suchkarte der 3b"},
    "luecken": []
  }
}
```

## Prüfregeln (Schema 0.6)

Drei Zustände wie bisher: erfüllt, Warnung, Fehler. Dieselben Regeln prüfen die Lehrkraftansicht (`index.html`) und `werkzeuge/validate04.py` (nach Anpassung).

| Nr. | Regel | Bei Verstoß |
| --- | --- | --- |
| 1 | `meta.schema_version` ist `"0.6"` | Fehler |
| 2 | `meta.lerngruppe` stimmt mit der geladenen Lerngruppe überein | Warnung |
| 3 | Rahmendaten vollständig; jedes Bild hat Datei und Beschreibung | Fehler |
| 4 | Brief vorhanden, höchstens 600 Zeichen | Fehler |
| 5 | Blick in die Bibliothek: genau 1 Bild | Fehler |
| 6 | `plan` vollständig, `aufloesung_beim_besuch` ist true oder false | Fehler |
| 7 | Genau 4 Abschnitte | Fehler |
| 8 | Jedes Variantenfeld enthält genau die Varianten aus Ableitungsregel 1 | Fehler |
| 9 | Längengrenzen der Abschnitte eingehalten | Fehler |
| 10 | Bildfolgen: 1–4 Einträge; Bild-Eintrag nach den Regeln aus 0.5 (Wort, Liste, `suchwort`) | Fehler bzw. Warnung bei `picto: null` mit `suchwort` |
| 11 | `wortbilder` vorhanden, wenn Ableitungsregel 2 greift; jedes Wort steht in einem `stufe1`-Text | Fehler bzw. Warnung |
| 12 | Je Sprachcode der Lerngruppe eine Übersetzung mit 4 Texten; keine Übersetzung ohne Sprachcode | Fehler |
| 13 | Übersetzungen innerhalb der Längengrenzen der übersetzten Stufe | Warnung |
| 14 | `antwortbrief`: alle 6 Felder vorhanden, Längengrenzen eingehalten | Fehler |
| 15 | `suchkarte.kartenkopf` höchstens 40 Zeichen; `luecken` vorhanden | Fehler |
| 16 | Keine Felder aus Schema 0.5 (`knoten`, `enden`, `teamnamen`, `absenden_text`) | Fehler |
| 17 | Tablets mindestens so viele wie Varianten | Warnung (organisatorisch) |

**Ohne geladene Lerngruppe** (JSON nur eingefügt): Regel 8 prüft, dass alle Variantenfelder dieselben Varianten enthalten; die Regeln 2, 11 (Pflicht), 12 und 17 entfallen.

## Offene Punkte

- Längengrenzen der Abschnitte (180/300/450) und des Briefs (600) sind Setzungen; nach dem ersten Test prüfen.
- `assets/interview/<sprache>.json`: Aufbau festlegen, sobald der Wortlaut des Interviews fertig ist.
- Bildsymbole für die 16 Themen und die Rollen (🎤, 💬) sind noch festzulegen; sie gehören zur Website, nicht zum Material.
- Datenmodell, Prompts und Prüfwerkzeuge werden weiterhin von Hand gleich gehalten.

## Umsetzungsstand

Stand 30.10.2026: Schema 0.6 ist spezifiziert, aber noch nicht umgesetzt. `index.html` und `validate04.py` prüfen und zeigen weiterhin Schema 0.5.
