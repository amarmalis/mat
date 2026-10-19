# Datenmodell\_Programm\_Lerngruppe\_Material

Oct 16, 2026 · @Anne

Das Datenmodell legt drei Datenstrukturen des Prototyps fest: das Programmprofil (Bibliotheksformular als JSON, Schema 0.4), das Lerngruppenprofil (Lehrkraft-Formular als JSON, Schema 0.4) und das Material (Ausgabe von LLM-Aufruf 2, Schema 0.5). Schema 0.4 richtete das Material an der Lerngruppe aus und erweiterte 0.3, ohne dessen Struktur zu brechen: Brief, Blick in die Bibliothek, Geschichte mit 7 Knoten und 8 Enden (drei Entscheidungen), Suchkarte und Lückenliste bleiben.

**Material-Schema 0.5 (18.10.2026):** Enden enthalten keinen `suchauftrag` mehr. Das Template bildet ihn aus den drei Merkmalen des Weges, z. B. Blatt: „Sucht ein spannendes Buch über ein Tier. Es hat viel Text.“ Steht ein Suchauftrag im Material, ist das ein Fehler. Grund: Lauf 1 von System Prompt 2, in dem nur 2 von 8 Suchaufträgen zu ihrem Weg passten. Programmprofil und Lerngruppe bleiben bei 0.4. Die Abschnitte unten geben den Stand 0.5 wieder.

**Neu in 0.4**

1. Texte enthalten nur die Lesestufen, die die Lehrkraft gewählt hat (`stufe1` Blatt, `stufe2` Baum, `stufe3` Wald).
2. Neue Variante `bild`: eine Folge aus 1–4 Piktogrammen mit je höchstens einem Wort, für Kinder, die noch nicht lesen oder kaum Deutsch verstehen.
3. `wortbilder`: Piktogramme zu Schlüsselwörtern der Blatt-Texte bei Förderbedarf Lernen oder Sprache.
4. Zahl der Teamnamen = Zahl der Tablets (mindestens 2).
5. Sprachfassungen als eigene Datei je Sprache.
6. Großdruck (Sehen) und „ankreuzen statt schreiben“ (Motorik) steuert das Template aus der Lerngruppen-Datei; das Modell erzeugt dafür nichts.
7. Die Prüfung kennt neben „erfüllt“ und „Fehler“ den Status „Warnung“.

## Dateien

Zu einem Material gehören bis zu fünf Dateien; Material und Lerngruppe teilen dieselbe ID, die Lerngruppe verweist über \`programm\` auf das Programmprofil.

| Datei | Inhalt | Entsteht durch |
| --- | --- | --- |
| programme/\<programm>.json | Programmprofil der Bibliothek, z. B. straubing-bibliotheksdetektive.json | Bibliotheksformular; Stufe 1 füllt vor, die Bibliothek prüft |
| `lerngruppen/<ID>.json` | Angaben der Lehrkraft | Lerngruppen-Formular (von Hand im Prototyp) |
| `materialien/<ID>.json` | Material auf Deutsch | LLM-Aufruf 2 (Stufe 2) |
| `materialien/<ID>.<sprache>.json` | Sprachfassung, z. B. `4713.uk.json` | Übersetzung (Konzept: DeepL-API; Prototyp: Chat) |
| `assets/pictos/liste.json` | erlaubte Piktogramme: ID und Wort | von Hand, je Programm ergänzt |

Das Template lädt `?id=4713` → Material und Lerngruppe. Vorgesehen, aber noch nicht umgesetzt: `?id=4713&lang=uk` → Sprachfassung und Lerngruppe. Die Piktogramm-Dateien sollen als `assets/pictos/<ID>.png` liegen; sie sind noch nicht hinterlegt.

## Lerngruppen-Datei

Die Datei bildet das Lerngruppen-Formular eins zu eins ab; das Modell (Sprachmodell, LLM-Aufruf 2) liest sie als Eingabe für die Generierung, das Template für die Darstellung.

| Feld | Typ | Formularfeld | Werte |
| --- | --- | --- | --- |
| `schema_version` | Text | – | `"0.4"` |
| `programm` | Text | 1.1 | Dateiname des Programmprofils ohne Endung |
| `klasse` | Text | 2.1 | z. B. `"3b"`, höchstens 30 Zeichen |
| `tablets` | Zahl | 2.2 | ganze Zahl ab 1 |
| `jahrgaenge` | Liste | 2.3 | mindestens ein Wert aus 1, 2, 3, 4 |
| lese`stufen` | Liste | 3.1 | mindestens ein Wert aus `stufe1`, `stufe2`, `stufe3` `stufe1` = Blatt, `stufe2` = Baum, `stufe3` = Wald |
| `kaum_deutsch` | ja/nein | 3.2 | `true` oder `false` |
| `sprachen` | Liste | 3.3/3.4 | Sprachcodes, leer bei „nein“: `ar` Arabisch, `bg` Bulgarisch, `en` Englisch, `es` Spanisch, `fa` Persisch, `it` Italienisch, `pl` Polnisch, `ro` Rumänisch, `ru` Russisch, `tr` Türkisch, `uk` Ukrainisch |
| `foerder` | Objekt | 4.1/4.2 | Anzahl je Bedarf, 0 = nicht angekreuzt: `sehen`, `lernen`, `sprache`, `motorik` |

**Ableitungsregeln** (gelten für Prompt, Template und Prüfung gleichermaßen)

1. Varianten im Material = lese`stufen`; dazu `stufe1`, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist; dazu `bild`, wenn `kaum_deutsch` = `true` ist oder `jahrgaenge` 1 oder 2 enthält.
2. `wortbilder` sind Pflicht, wenn `foerder.lernen` oder `foerder.sprache` größer 0 ist.
3. Zahl der Teamnamen = `tablets`, mindestens 2.
4. `foerder.sehen` größer 0 → Template bietet Großdruck mit hohem Kontrast an.
5. `foerder.motorik` größer 0 → Template bietet die Suchkarte zum Ankreuzen statt zum Schreiben an.
6. Je Eintrag in `sprachen` entsteht eine Sprachfassung.

**Beispiel** (`lerngruppen/4713.json`)

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

Aus diesem Beispiel folgen die Varianten `stufe1` (wegen Förderbedarf Lernen), `stufe2`, `stufe3` und `bild`, dazu Wortbilder, 8 Teamnamen und eine ukrainische Fassung.

## Programmprofil-Datei

Das Programmprofil bildet das Bibliotheksformular ab. Stufe 1 füllt es aus den Quellen vor; was dort nicht zu finden ist, steht als `null`. Vor Stufe 2 prüft und ergänzt die Bibliothek; danach darf kein Pflichtfeld mehr `null` sein.

| Feld | Formularfeld | Pflicht | Stufe 1 füllt vor | Werte |
| --- | --- | --- | --- | --- |
| `schema_version` | – | ja | – | `"0.4"` |
| `programm` | – | ja | – | ID = Dateiname; Kleinbuchstaben, Ziffern, Bindestrich, max. 60 |
| `quellen` | 1.1, 1.2 | nein | nein | `{"dokumente": [Dateinamen], "webseiten": [http(s)-Adressen]}` |
| `findet_in_bibliothek_statt` | Voraussetzung | ja | ja | true, false oder null; false = Programm ausgeschlossen (Grundvoraussetzung: Durchführung in der Bibliothek) |
| `bibliothek` | 2.1 | ja | ja | Text, max. 120 Zeichen |
| `titel` | 2.2 | ja | ja | Text, max. 120 Zeichen |
| `worum_geht_es` | 2.3 | ja | ja | Text, max. 600 Zeichen |
| `buch_oder_thema` | 2.4 | nein | ja | Text oder `null` |
| `taetigkeiten` | 3.1 | ja | ja | Liste, mind. 1: `zuhoeren`, `selbst_lesen`, `katalog`, `erkunden`, `gestalten` |
| `taetigkeiten_weiteres` | 3.1 „Weiteres“ | nein | ja | Text oder `null` |
| `orte` | 3.2 | ja | ja | Liste, mind. 1, je max. 40 Zeichen |
| `ausleihe` | 4.1 | ja | ja | `klassenausweis`, `eigener_ausweis`, `nein` |
| `mitbringen` | 4.2 | nein | ja | Text oder `null` |
| `foto` | 5.1–5.4 | ja | nein | `{"datei", "beschreibung" (max. 120 Zeichen), "veroeffentlichen_erlaubt": true, "keine_personen": true}` |
| `hinweis`, `herkunft` | – | nein | – | Vermerk und Protokoll: `vorbefuellt_von`, `geprueft_von`, `geprueft_am` |
| `belege` | – | nein | ja | Fundstelle je vorbefülltem Feld (Quelle + wörtlicher Ausschnitt, max. 150 Zeichen); Hilfe für die Prüfung gegen die Quellen, in Stufe 2 nicht verwendet |

**Übergang ins Material:** `rahmen.bibliothek` = `bibliothek`, `rahmen.programmtitel` = `titel`, `rahmen.bilder` = ein Eintrag aus `foto` (Datei, Beschreibung). Diese Werte setzt das System, nicht das Modell.

**Prüfung:** Werkzeug `programm04.py`. Nach Stufe 1 (Schalter `--vorbefuellt`) sind fehlende Pflichtangaben eine Warnung („von der Bibliothek zu ergänzen“), vor Stufe 2 ein Fehler. `findet_in_bibliothek_statt: false` ist immer ein Fehler (Programm ausgeschlossen), ebenso ein `hinweis` „Quelltext fehlt“. Belege dürfen nur für vorbefüllbare Felder stehen (sonst Fehler); fehlt einer vorbefüllten Angabe der Beleg oder ist ein Beleg länger als 150 Zeichen, warnt die Prüfung. Mit `--quelle QUELLTEXT.txt` prüft sie zusätzlich, ob jeder Beleg wörtlich im Quelltext steht (Leerraum und Anführungszeichen werden angeglichen); ein nicht gefundener Beleg ist ein Fehler. Ob ein Beleg die Angabe inhaltlich trägt, prüft das Werkzeug nicht; das bleibt redaktionelle Prüfung.

**Voraussetzungen (gesetzt, nicht abgefragt):** Das Programm findet in der Bibliothek statt, und die Klasse hat Stöberzeit. Deshalb ist „stöbern“ keine wählbare Tätigkeit (Formularoption am 17.10.2026 gestrichen); steht `stoebern` im Profil, ist das ein Fehler. Prüfprotokoll der Testläufe: `prompts/testlaeufe_system_1.md`.

**Beispiel** (`programme/straubing-bibliotheksdetektive.json`): Stand nach Stufe 1 (Lauf 4) und redaktioneller Korrektur; `orte`, `ausleihe` und `foto` sind für den Test gesetzte Annahmen (Foto: Platzhalterbild). Korrigiert gegenüber der Modellausgabe: `bibliothek`, `titel`, `buch_oder_thema`, `taetigkeiten` (ohne `zuhoeren` und `stoebern`), `taetigkeiten_weiteres`, `orte` (statt „Salzstadel“).

```json
{
  "schema_version": "0.4",
  "programm": "straubing-bibliotheksdetektive",
  "hinweis": "Stand nach Stufe 1 (system_1 v0.2, Lauf 4) und redaktioneller Korrektur. orte, ausleihe und foto sind für den Test gesetzte Annahmen, keine Angaben der Bibliothek; das Foto ist ein Platzhalterbild.",
  "quellen": {"dokumente": ["Bibliotheksdetektive.pdf"], "webseiten": []},
  "findet_in_bibliothek_statt": true,
  "bibliothek": "Stadtbibliothek Straubing",
  "titel": "Bibliotheksdetektive",
  "worum_geht_es": "Die Kinder werden zu Detektiven und spüren eine gestohlene Bücherkiste und den Dieb „Mr. X“ auf. Dafür lösen sie Text-Rätsel und Puzzles, finden sich in der Bibliothek zurecht und lernen, wie die Medien in den Regalen aufgestellt sind. Am Ende bekommen sie einen Detektiv-Ausweis.",
  "buch_oder_thema": "Krimi: Detektivgeschichte um eine gestohlene Bücherkiste",
  "taetigkeiten": ["erkunden"],
  "taetigkeiten_weiteres": "Text-Rätsel und Puzzles lösen; Kontakt mit Mr. X aufnehmen",
  "orte": ["Kinderbibliothek", "Bilderbuchecke", "Sachbuchregale", "Ausleihtheke"],
  "ausleihe": "klassenausweis",
  "mitbringen": null,
  "foto": {
    "datei": "bilder/bilderbuchecke.svg",
    "beschreibung": "Bilderbuchecke in der Kinderbibliothek",
    "veroeffentlichen_erlaubt": true,
    "keine_personen": true
  },
  "herkunft": {"vorbefuellt_von": "system_1 v0.2", "geprueft_von": "Testdaten (redaktionell ergänzt)", "geprueft_am": "2026-10-17"}
}
```

## Material-Datei

Das Material behält den Aufbau von 0.3 (`meta`, `rahmen`, `generiert`); geändert werden nur die Variantenfelder, dazu kommen `wortbilder` und ein Verweis auf die Lerngruppe.

**Variantenfelder**: Sie enthalten genau die Varianten, die aus der Lerngruppe folgen (Ableitungsregel 1), nicht mehr und nicht weniger.

| Feld | `stufe1`–`stufe3` | `bild` |
| --- | --- | --- |
| `geschichte.knoten.<ID>.text` | Text; höchstens 80 / 150 / 250 Zeichen | Bildfolge, 1–4 Einträge |
| `geschichte.knoten.<ID>.optionen[].label` | Text, höchstens 40 Zeichen | Bildfolge, genau 1 Eintrag |
| `geschichte.enden.<ID>.text` | Text; höchstens 80 / 150 / 250 Zeichen | Bildfolge, 1–4 Einträge |

**Bild-Eintrag**

| Feld | Pflicht | Regel |
| --- | --- | --- |
| `picto` | ja | ID aus `assets/pictos/liste.json` oder `null`, wenn der Begriff dort fehlt |
| `wort` | ja | genau ein Wort ohne Leerzeichen, höchstens 15 Zeichen; Deutsch |
| `suchwort` | nur bei `picto: null` | Begriff für die Nachsuche bei ARASAAC, höchstens 30 Zeichen |

**Wortbilder** (`generiert.wortbilder`, Pflicht nach Ableitungsregel 2): Liste mit 1–20 Einträgen `{"wort", "picto", "suchwort"}` nach denselben Regeln; jedes `wort` muss in mindestens einem `stufe1`-Text vorkommen. Das Template zeigt das Piktogramm neben diesem Wort.

**Teamnamen** (`generiert.teamnamen`): genau so viele wie Tablets, mindestens 2, je höchstens 30 Zeichen.

**Meta**: `schema_version` = `"0.5"`; `lerngruppe` = ID der Lerngruppen-Datei; dazu `erzeugt_von` (Modell und Plattform), `prompt_version`, `erzeugt_am` und `hinweis` (redaktionelle Vermerke).

**Unverändert gegenüber 0.3**: `rahmen` (Klasse, Bibliothek, Programmtitel, Bilder), `brief.text` (höchstens 500 Zeichen, wird vorgelesen, keine Bildfassung), `bibliotheksblick` (genau 1 Bild), `geschichte.kulisse`, Quellenangaben, `optionen[].symbol`, `optionen[].fund` (Name höchstens 25 Zeichen, Symbol), `absenden_text` (höchstens 200 Zeichen), `suchkarte.kartenkopf`, `luecken`.

**Auszug** (Knoten S und Ende AAA aus dem Material 4713 für die Lerngruppe 4713)

```json
"S": {
  "text": {
    "stufe1": "Die Bücherkiste ist weg! Frido hört es kichern. Und es raschelt.",
    "stufe2": "Frido steht in der Kinderbibliothek. Die Bücherkiste ist verschwunden! Hinter einem Regal kichert es. Aus der Ecke raschelt es leise.",
    "stufe3": "Frido steht in der Kinderbibliothek und traut seinen Augen kaum: Die Bücherkiste ist verschwunden! Plötzlich kichert es hinter einem Regal. Gleichzeitig raschelt es geheimnisvoll in der Ecke. Wohin gehen Frido und ihr zuerst?",
    "bild": [{"picto": 7055, "wort": "Biber"}, {"picto": 6946, "wort": "suchen"}, {"picto": 5935, "wort": "Kiste"}, {"picto": 3065, "wort": "Bibliothek"}]
  },
  "optionen": [
    {
      "label": {
        "stufe1": "Zum Kichern gehen",
        "stufe2": "Wir gehen dem Kichern nach.",
        "stufe3": "Wir folgen dem leisen Kichern.",
        "bild": [{"picto": 38792, "wort": "lachen"}]
      },
      "symbol": "😄",
      "fund": {"name": "Komischer Hut", "symbol": "🎩"}
    },
    {
      "label": {
        "stufe1": "Zum Rascheln gehen",
        "stufe2": "Wir gehen dem Rascheln nach.",
        "stufe3": "Wir schleichen dem Rascheln nach.",
        "bild": [{"picto": 2381, "wort": "zuhören"}]
      },
      "symbol": "🔦",
      "fund": {"name": "Lupe", "symbol": "🔍"}
    }
  ]
}

"AAA": {
  "text": {
    "stufe1": "Auf der Karte tanzt ein Tier. Frido lacht. Er hat eine Buch-Idee!",
    "stufe2": "Auf der bunten Karte tanzt ein Tier mit Hut. Frido muss laut lachen. Er hat eine Idee, welches Buch ihr suchen könnt.",
    "stufe3": "Auf der bunten Karte tanzt ein Tier mit einem viel zu großen Hut, und alle Bilder sehen zum Schreien komisch aus. Frido prustet vor Lachen. Dann hat er eine Idee, welches Buch ihr suchen könnt.",
    "bild": [{"picto": 7055, "wort": "Biber"}, {"picto": 3245, "wort": "froh"}, {"picto": 2450, "wort": "Buch"}, {"picto": 6946, "wort": "suchen"}]
  }
}
```

Das vollständige Beispiel liegt als `materialien/4713.json` (Schema 0.5) zusammen mit `lerngruppen/4713.json` im Repo. Erzeugt hat es Claude Sonnet 5.5 mit System Prompt 2 v0.2 (Lauf 3); die Piktogramme sind redaktionell nachgetragen. Den Suchauftrag zu AAA bildet das Template, z. B. Blatt: „Sucht ein lustiges Buch über ein Tier. Es hat viele Bilder.“

## Prüfregeln

Die Prüfung in der Lehrkraftansicht kennt drei Zustände: erfüllt, Warnung, Fehler. Freigabefähig ist ein Material erst ohne Fehler; Warnungen werden bearbeitet oder bewusst stehen gelassen. Dieselben Regeln prüft werkzeuge/validate04.py außerhalb des Browsers.

| Nr. | Regel | Bei Verstoß |
| --- | --- | --- |
| 1 | `meta.schema_version` ist `"0.5"` | Fehler |
| 2 | `meta.lerngruppe` stimmt mit der geladenen Lerngruppe überein | Warnung |
| 3 | Rahmendaten vollständig (Klasse, Bibliothek, Programmtitel); jedes Bild hat Datei und Beschreibung | Fehler |
| 4 | Brief vorhanden, höchstens 500 Zeichen | Fehler |
| 5 | Blick in die Bibliothek: genau 1 Bild | Fehler |
| 6 | Alle 7 Knoten und 8 Enden vorhanden; jeder Knoten hat genau 2 Optionen | Fehler |
| 7 | Jedes Variantenfeld enthält genau die Varianten aus Ableitungsregel 1 | Fehler |
| 8 | Längengrenzen der Texte, Optionen und Fundstücke eingehalten | Fehler |
| 9 | Bildfolgen: 1–4 Einträge, bei Optionen genau 1 | Fehler |
| 10 | Bild-Eintrag: `wort` ist ein Wort mit höchstens 15 Zeichen; `picto` steht in der Liste | Fehler |
| 11 | Bild-Eintrag mit `picto: null` und `suchwort` | Warnung (Piktogramm nachtragen) |
| 12 | Bild-Eintrag mit `picto: null` ohne `suchwort` | Fehler |
| 13 | `wortbilder` vorhanden, wenn Ableitungsregel 2 greift; 1–20 Einträge nach den Regeln 10–12 | Fehler |
| 14 | Jedes Wort aus `wortbilder` kommt in einem `stufe1`-Text vor | Warnung |
| 15 | Zahl der Teamnamen = Tablets (mindestens 2), je höchstens 30 Zeichen | Fehler |
| 16 | Tablets mindestens so viele wie Varianten | Warnung (organisatorisch) |
| 17 | Absendetext vorhanden, höchstens 200 Zeichen; Lückenliste vorhanden | Fehler |
| 18 | Kein Ende enthält einen suchauftrag (den bildet das Template) | Fehler |

**Ohne geladene Lerngruppe** (JSON nur eingefügt): Regel 7 prüft, dass alle Variantenfelder dieselben Varianten enthalten; die Regeln 2, 13, 15 (Anzahl) und 16 entfallen, die Ansicht weist darauf hin.

## Sprachfassung

Die Sprachfassung hat denselben Aufbau wie das deutsche Material; nur Texte für Kinder und Klasse werden übersetzt.

| Übersetzt | Unverändert |
| --- | --- |
| alle `stufe1`–`stufe3`-Texte und Optionen | `picto`, `suchwort`, Symbole, IDs |
| `wort` in Bild-Einträgen und Wortbildern | `rahmen` (Namen von Klasse, Bibliothek, Programm) |
| `brief.text`, `absenden_text`, Fundstück-Namen, Teamnamen, `suchkarte.kartenkopf` | Quellenangaben, `luecken`, `kulisse` |

`meta` erhält zusätzlich `sprache` (Code), `quelle` (`"4713.json"`) und `uebersetzt` (`"maschinell, nicht geprüft"`); die Lehrkraftansicht zeigt diesen Vermerk. Geprüft wird die Sprachfassung mit denselben Regeln; Längengrenzen gelten als Warnung, weil Übersetzungen länger ausfallen können.

## Offene Punkte

- Die Grenzwerte für Bildfolgen (1–4), `wort` (15 Zeichen), `suchwort` (30 Zeichen) und Wortbilder (20) sind Setzungen; nach dem ersten Test prüfen.
- In der Bildvariante bleiben Fundstück-Namen Text; angezeigt wird vor allem das Symbol.
- Das Template stellt Bildvariante, Wortbilder, Großdruck und Ankreuz-Suchkarte noch nicht dar; diese Spezifikation regelt zunächst Datei, Prüfung und Beispiel. Ebenfalls noch offen: Laden der Sprachfassung über \`?lang=\` und ihre Prüfung (Längengrenzen als Warnung).
- Figma: Der Ablauf des Prototyps (Phasen 1–3) liegt als FigJam-Diagramm vor (19.10.2026). Offen sind Phase 4 und der Ablauf der echten Anwendung (Plattform vergibt ID, Formulare, API).
- Echte Anwendung: Die Lehrkraft braucht vor dem Einsatz eine Ansicht zur redaktionellen Durchsicht aller Wege und Varianten, mit Fehlermeldung oder Korrektur.
- Sprachfassung: Texte, die das Template selbst bildet (u. a. die Suchaufträge), müssen mit übersetzt werden.
- Datenmodell, Prompts (system\_1.md, system\_2.md) und Prüfwerkzeuge (programm04.py, validate04.py, Prüfung in index.html) werden von Hand gleich gehalten; eine gemeinsame Schemadatei gibt es nicht. Jede Änderung an Feldern ist an allen Stellen nachzuziehen.

## Umsetzungsstand

Stand 19.10.2026: `index.html` (Template v4) setzt Material-Schema 0.5 um. Es bildet die Suchaufträge aus den Merkmalen des Weges und zeigt nach jeder Entscheidung erst den folgenden Text, dann das Fundstück. Die Prüfung des Materials liegt als JavaScript (`index.html`) und Python (`werkzeuge/validate04.py`) vor; beide liefern in 20 Testfällen identische Ergebnisse. Programmprofile prüft `werkzeuge/programm04.py`. Beispieldaten im Repo: `programme/straubing-bibliotheksdetektive.json`, `lerngruppen/4713.json`, `materialien/4713.json`.

Prüfergebnis für `materialien/4713.json`: 0 Fehler, 1 Warnung (Regel 11, für „Schriftrolle“ gibt es kein passendes Piktogramm).
