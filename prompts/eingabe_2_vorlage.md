# Eingabe für Stufe 2 (Vorlage)

Gilt ab System Prompt 2 v0.9 (`prompts/system_2_v0.9.md`).

Diese Nachricht folgt im selben Chat auf den System Prompt 2 (oder steht direkt darunter in der ersten Nachricht). Kopiere nur den Teil im Codeblock und ersetze die Teile in spitzen Klammern (die Klammern fallen weg).

```
MODELL: <Name und Version des Modells, genau wie im Auswahlmenü, z. B. Claude Sonnet 5.5 oder Qwen3 30B A3B Instruct 2507>
DATUM: <JJJJ-MM-TT>
LERNGRUPPEN-ID: <z. B. 4713>

=== PROGRAMMPROFIL ===
<Inhalt von programme/<programm>.json>
=== ENDE PROGRAMMPROFIL ===

=== LERNGRUPPE ===
<Inhalt von lerngruppen/<ID>.json>
=== ENDE LERNGRUPPE ===

=== PIKTOGRAMME ===
<Inhalt von assets/pictos/liste.json>
=== ENDE PIKTOGRAMME ===

Erstelle das Material nach den Regeln.
```

Hinweise:
- Für jeden Lauf einen neuen Chat öffnen.
- Das Programmprofil muss von der Bibliothek geprüft sein (keine `belege`, keine `null` in Pflichtfeldern).
- Neu ab v0.9 im Programmprofil: `foto.nachweis` (Bildnachweis, wird unverändert in `rahmen.bilder` übernommen) und `lesetipps_vor_ort` (true/false; bei true und gewählter ⭐⭐⭐-Stufe erscheint die Zusatzfrage „Das lese ich gern“).
- Danach prüfen: Ausgabe als JSON speichern und `python3 werkzeuge/validate08.py <Datei>` ausführen, oder in der Lehrkraftansicht unter „Für die Entwicklung“ → „Inhalte laden“ einfügen.
- Kennwerte der Lesestufen: `python3 werkzeuge/stufen.py <Datei>`. In den Testläufen wird nicht nachgefordert (Entscheidung 13.11.2026). Nur als Ausblick: Meldet die Prüfung Regel 18 oder 19, erzeugt `stufen.py` einen Überarbeitungsauftrag (Einsetzen der Antwort mit `--einsetzen`).
- Die Lerngruppe wird über `meta.lerngruppe` nachgeladen; dafür muss `lerngruppen/<ID>.json` schon im Repo liegen.
- Ist die Prüfung ohne Fehler und die redaktionelle Durchsicht abgeschlossen: als `materialien/<ID>.json` ins Repo laden.
