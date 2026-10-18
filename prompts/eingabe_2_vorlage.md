# Eingabe für Stufe 2 (Vorlage)

Diese Nachricht folgt im selben Chat auf den System Prompt 2 (oder steht direkt darunter in der ersten Nachricht). Kopiere nur den Teil im Codeblock und ersetze die Teile in spitzen Klammern (die Klammern fallen weg).

```
MODELL: <Name und Version des Modells, z. B. Qwen3 30B A3B Instruct 2507>
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
- Danach prüfen: Ausgabe in der Lehrkraftansicht unter „Inhalte laden“ einfügen. Die Lerngruppe wird über `meta.lerngruppe` nachgeladen; dafür muss `lerngruppen/<ID>.json` schon im Repo liegen.
- Ist die Prüfung ohne Fehler und die redaktionelle Durchsicht abgeschlossen: als `materialien/<ID>.json` ins Repo laden.
