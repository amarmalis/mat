# System Prompt 2 v0.9: Änderungen gegenüber v0.8 und Begründung

Stand 11.11.2026, noch nicht getestet. Der vollständige Prompt steht in `prompts/system_2_v0.9.md`; v0.8 bleibt eingefroren (`prompts/system_2.md`). Diese Datei dokumentiert die Änderungen und ihre Begründung.

Änderungen im Überblick: (A) messbare Lesestufen, (B) Leitlinie Lesemotivation L1–L4 samt leitlinienkonformem Beispiel, (C) Prüf- und Nachschärf-Schleife (Werkzeug, nicht Prompt), (E) neue Rahmenfelder `lesetipps` und `bilder[].nachweis`, (F) neues Beispiel für `vor_vermutungen`, Selbstprüfung um Fragen 10 und 11 ergänzt, (G) Lücken als verständliche Sätze an die Lehrkraft.

## A – Lesestufen messbar machen

### Anlass

Lauf 9 (v0.8): ⭐⭐ und ⭐⭐⭐ unterscheiden sich kaum. Gemessen mit `werkzeuge/stufen.py`: Wörter je Satz 8,6 gegenüber 10,1; ⭐⭐⭐ hat nach LIX sogar einen niedrigeren Wert als ⭐⭐ (32,7 gegenüber 35,2). Ursache: v0.8 beschreibt die Stufen nur mit Adjektiven („kurze Sätze“, „abwechslungsreichere Sätze“). Steuerung und Prüfung sollen künftig denselben Maßstab verwenden.

### Ersetzt den Abschnitt „Lesestufen“

| Stufe | Text je Abschnitt | Satzbau |
| --- | --- | --- |
| `stufe1` ⭐ | höchstens 180 Zeichen | nur Hauptsätze; höchstens 8 Wörter je Satz; häufige Wörter |
| `stufe2` ⭐⭐ | höchstens 300 Zeichen | kurze Sätze, im Schnitt etwas länger als ⭐; höchstens jeder dritte Satz mit Nebensatz |
| `stufe3` ⭐⭐⭐ | höchstens 450 Zeichen | im Schnitt mindestens 2 Wörter je Satz mehr als ⭐⭐; mindestens jeder dritte Satz mit Nebensatz (weil, dass, wenn, der/die/das …); abwechslungsreichere Wörter, aber Wortschatz der Grundschule |

Alle Fassungen eines Abschnitts enthalten dieselben Informationen, aber jede ist eigens für ihre Stufe formuliert. Kopiere keine Fassung in eine andere Stufe; `stufe3` ist nicht `stufe2` mit ein paar zusätzlichen Wörtern. Die ⭐-Fassung besteht aus ganzen Sätzen, nicht aus Stichworten. Prüfe vor der Ausgabe für jede Stufe, ob der Satzbau den Vorgaben entspricht.

## B – Leitlinie Lesemotivation

### Anlass

v0.8 nennt das Ziel („neugierig auf den Besuch und auf Bücher“), setzt Prinzipien der Lesemotivationsförderung aber nur implizit um („Neugierig machen durch die Sache“, Ansprache mit „ihr“). Die Lesemotivationsförderung liegt überwiegend in der Architektur des Materials (Wahl, Interesse, eigenes Buch, Briefpaar; fest in der Website). Der Prompt verankert die Prinzipien nur dort, wo das Modell Text schreibt, und zwar als konkrete, prüfbare Regeln – nicht als abstrakte Appelle, weil diese in den Läufen 4–9 schwach steuerten oder zum Erfinden verleiteten (Befunde 6, 7, 11; Lesestufen in Lauf 9). Befund Lauf 9: Keine Sachtext-Fassung spricht das Lesen an; nur ⭐⭐⭐ endet mit einer Frage.

### Neuer Abschnitt nach „Grundsätze“ (Sachtext), gilt auch für Brief und Antwortbrief-Rahmen, soweit angegeben

> ### Leitlinie Lesemotivation
>
> Das Material soll Lust auf den Besuch und aufs Lesen machen. Halte dafür in jeder Fassung des Sachtexts diese vier Regeln ein. Sie ändern nichts an den Grundregeln: Alles stammt aus dem Programmprofil.
>
> | Nr. | Regel | Gilt für | Warum |
> | --- | --- | --- | --- |
> | L1 | Mindestens ein Satz spricht das Lesen an oder Bücher, mit denen die Kinder beim Besuch etwas tun (aussuchen, entdecken, ausleihen). Nur, was das Profil hergibt, zum Beispiel `buch_oder_thema`, Regale in `orte`, `ausleihe`. | jede Sachtext-Fassung | Bezug zu Büchern, nicht nur zum Erlebnis |
> | L2 | Abschnitt 1 endet mit einer Frage zum Motiv des Programms, die erst der Besuch beantwortet. Die Frage verrät nichts und erfindet nichts. | jede Sachtext-Fassung | Neugier |
> | L3 | Einladend statt kontrollierend: „ihr könnt“, „ihr sucht euch aus“, nicht „ihr müsst“, „ihr sollt“, „verboten“. | Sachtext, Brief, Antwortbrief-Rahmen | Selbstbestimmung |
> | L4 | Keine Schul- oder Prüfungswörter (lernen, üben, Test, Note). Steht so etwas im Profil, umschreibe es („ihr findet heraus, wo welche Bücher stehen“). | Sachtext, Brief | Lesen als Freude, nicht als Pflicht |
>
> Höchstens eine Frage je Abschnitt gilt weiter; die Frage aus L2 zählt dazu.

### Prüfung

Regel 19 des Validators (`werkzeuge/stufen.py`, Funktion `leitlinie`; gleich in `index.html`) prüft L1–L4 mit Wortlisten. Verstöße im Sachtext gehen in denselben Überarbeitungsauftrag wie die Lesestufen (siehe C); Verstöße in Brief und Antwortbrief-Rahmen werden nur gemeldet.

## C – Prüf- und Nachschärf-Schleife (ohne Lehrkraft)

1. Das Material wird erzeugt und mit `werkzeuge/validate08.py` geprüft (Regel 18: Abstand der Lesestufen; Regel 19: Leitlinie Lesemotivation).
2. Verfehlt eine Stufe die Zielwerte oder die Leitlinie, erzeugt `werkzeuge/stufen.py` einen Überarbeitungsauftrag. Er nennt die gemessenen Werte, die Ziele und nur die betroffenen Fassungen.
3. Der Auftrag geht als nächste Nachricht in denselben Chat (Prototyp) bzw. als zweiter Aufruf an das Modell (spätere API-Fassung). Die Antwort enthält nur die neuen Fassungen als JSON.
4. `werkzeuge/stufen.py --einsetzen` setzt sie ein, prüft Zeichengrenzen und misst neu. Höchstens zwei Runden; danach gilt die beste Fassung.

Im Prototyp führt diese Schritte die Entwicklerin aus (Lehrkraftansicht, Bereich „Für die Entwicklung“, oder Kommandozeile). In einer API-Fassung liefen sie automatisch. Die Lehrkraft sieht davon nichts; sie erhält fertig differenziertes Material („niederschwellig, sofort einsetzbar“, RQ1).

## E – Neue Rahmenfelder

- `rahmen.bilder[].nachweis`: Bildnachweis aus `programmprofil.foto.nachweis`, unverändert übernommen (Lizenzpflicht CC BY: Urheber, Titel, Quelle, Lizenz). Die Webseite zeigt `nachweis.text` als Bildunterschrift und den vollständigen Nachweis in der Lehrkraftansicht.
- `rahmen.lesetipps`: `true` nur, wenn `programmprofil.lesetipps_vor_ort` `true` ist und die Lerngruppe ⭐⭐⭐ gewählt hat. Die Webseite zeigt dann für ⭐⭐⭐ die Zusatzfrage („Was liest du gern? …“) und die Zeile „Das lese ich gern“ auf der Lesefutter-Karte. Frage und Kartenzeile sind fest in der Webseite, nicht generiert.

## F – Beispiel und Selbstprüfung

- Das Kartenschatz-Beispiel erfüllt nun selbst die Leitlinie (L1, L2) und die Satzbau-Ziele (mit `werkzeuge/stufen.py` gemessen: ⭐ 6,0 Wörter je Satz, 0 % Nebensätze, LIX 22,7; ⭐⭐ 8,2 / 20 % / 30,2; ⭐⭐⭐ 16,2 / 50 % / 33,2). In v0.8 widersprach das Beispiel der neuen Leitlinie (⭐ und ⭐⭐ ohne Frage, kein Lesebezug); da Modelle Beispiele stark übernehmen, wäre die Regel sonst durch das Beispiel unterlaufen worden.
- Beispiel für `vor_vermutungen` geändert in „Wir haben schon überlegt, was uns erwarten könnte:“. Befund Lauf 9: Das Modell übernahm das v0.8-Beispiel wörtlich. Das neue Beispiel ist die von der Entwicklerin gewählte Formulierung; wird es wieder wörtlich übernommen, ist das erwünscht. Methodisch bedeutet das: Das Feld ist faktisch vorgegeben, nicht generiert (für die Arbeit zu benennen).
- Selbstprüfung: Frage 10 (Satzbau je Stufe), Frage 11 (L1–L4); Frage 9 um die Lücken ergänzt.

## G – Lücken an die Lehrkraft gerichtet

Befund Lauf 9: Die Einträge in `luecken` lauteten „Das Programmprofil enthält keine Angabe, …“. Sie erscheinen in der Lehrkraftansicht unter „Vor dem Besuch klären“; der Begriff „Programmprofil“ ist dort unverständlich. Grundregel 3 verlangt nun Sätze an die Lehrkraft, als offene Frage zum Besuch, ohne Fachbegriffe und Feldnamen (mit Falsch-/Richtig-Beispiel).

## D – Grenzen

- Die Zielwerte sind heuristisch gesetzt, nicht empirisch normiert.
- Bei rund 60 Wörtern je Stufe sind LIX und Satzlänge nur grobe Anhaltspunkte; geprüft werden deshalb vor allem Abstände zwischen den Stufen.
- Die Leitlinien-Prüfung arbeitet mit Wortlisten; sie erkennt Verstöße, aber nicht, ob ein Text tatsächlich motiviert. Das bleibt Sache der Durchsicht und der Evaluation.
- Die Nebensatzerkennung ist eine Regel-Heuristik (Konjunktion oder Relativpronomen nach Komma, Verb am Ende) und kann sich irren.
