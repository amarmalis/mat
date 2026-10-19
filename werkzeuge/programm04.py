"""Programmprofil (Schema 0.4): Prüfung.

Felder und Regeln: docs/Datenmodell_Programm_Lerngruppe_Material.md,
Abschnitt Programmprofil-Datei.

Das Programmprofil bildet das Bibliotheksformular ab (Stand 17.10.2026).
Stufe 1 (LLM-Aufruf 1, system_1 v0.3) füllt es aus den Quellen vor; nicht
gefundene Angaben stehen als null. Vor Stufe 2 prüft die Bibliothek und
ergänzt; erst dann dürfen Pflichtfelder nicht mehr null sein.

Voraussetzungen:
- Das Programm findet in der Bibliothek statt (findet_in_bibliothek_statt,
  Formularfeld 0.1, Bestätigung).
- Die Klasse hat Stöberzeit (gesetzt, nicht abgefragt). Deshalb ist "stöbern" keine wählbare Tätigkeit
  (Formularoption am 17.10.2026 gestrichen).

Aufruf aus dem Hauptordner des Repos:
  python3 werkzeuge/programm04.py programme/<programm-id>.json [--vorbefuellt] [--quelle QUELLTEXT.txt]
  --vorbefuellt: Stand nach Stufe 1; leere Pflichtfelder sind dann Warnungen.
  --quelle:      Text der Quellen; jeder Beleg muss darin wörtlich stehen.
"""
import json, re, sys

TAETIGKEITEN = {
    "zuhoeren": "zuhören (Vorlesen, Erzählen)",
    "selbst_lesen": "selbst lesen",
    "katalog": "den Bibliothekskatalog benutzen",
    "erkunden": "Bibliothek erkunden",
    "gestalten": "etwas gestalten",
}
AUSLEIHE = {
    "klassenausweis": "ja, über einen Klassenausweis",
    "eigener_ausweis": "ja, mit eigenem Ausweis",
    "nein": "nein",
}
# Feld -> (Formularfeld, Pflicht, von Stufe 1 vorbefüllbar)
FELDER = {
    "quellen":                    ("1.1/1.2", False, False),
    "findet_in_bibliothek_statt": ("0.1", True, True),
    "bibliothek":                 ("2.1", True, True),
    "titel":                      ("2.2", True, True),
    "worum_geht_es":              ("2.3", True, True),
    "buch_oder_thema":            ("2.4", False, True),
    "taetigkeiten":               ("3.1", True, True),
    "taetigkeiten_weiteres":      ("3.1", False, True),
    "orte":                       ("3.2", True, True),
    "ausleihe":                   ("4.1", True, True),
    "mitbringen":                 ("4.2", False, True),
    "foto":                       ("5.1-5.4", True, False),
}
BELEG_MAX = 150


def leer(v):
    return v is None or (isinstance(v, str) and not v.strip()) or (isinstance(v, list) and not v)


def norm(s):
    """Für den Wortlautvergleich: Leerraum vereinheitlichen, typografische Zeichen angleichen."""
    s = s.replace("„", '"').replace("“", '"').replace("”", '"').replace("’", "'")
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    return re.sub(r"\s+", " ", s).strip()


def ausschnitt(beleg):
    """'QUELLE 1: Text' oder 'Name: "Text"' -> Text ohne Quellenangabe und äußere Anführungszeichen."""
    teil = beleg.split(": ", 1)[1] if ": " in beleg else beleg
    teil = teil.strip()
    if len(teil) >= 2 and teil[0] in "\"„“'" and teil[-1] in "\"“”'":
        teil = teil[1:-1]
    return teil.strip()


def validate_programm(p, vorbefuellt=False, quelltext=None):
    """Rückgabe: Liste (status, text), status in ok/warn/bad."""
    res = []
    add = lambda s, t: res.append((s, t))
    add("ok" if p.get("schema_version") == "0.4" else "bad", "Schema-Version 0.4")
    pid = p.get("programm")
    ok = isinstance(pid, str) and re.fullmatch(r"[a-z0-9-]{1,60}", pid or "") is not None
    add("ok" if ok else "bad", "Programm-ID: Kleinbuchstaben, Ziffern, Bindestrich (max. 60)")
    # Hinweis (Stufe 1: Quelltext fehlt)
    h = p.get("hinweis")
    if isinstance(h, str) and h.startswith("Quelltext fehlt"):
        add("bad", "Stufe 1 ohne Quelltext – " + h)
    # Voraussetzung Ort
    ort = p.get("findet_in_bibliothek_statt")
    if ort is False:
        add("bad", "Programm findet nicht in der Bibliothek statt – ausgeschlossen")
    elif ort is not None and ort is not True:
        add("bad", "findet_in_bibliothek_statt: true, false oder null")
    # Pflichtfelder
    fehlend = [f + " (" + FELDER[f][0] + ")" for f, (_, pflicht, _vorb) in FELDER.items()
               if pflicht and leer(p.get(f))]
    if vorbefuellt:
        add("warn" if fehlend else "ok", "Pflichtangaben vorhanden" + (" – von der Bibliothek zu ergänzen: " + ", ".join(fehlend) if fehlend else ""))
    else:
        add("bad" if fehlend else "ok", "Pflichtangaben vorhanden" + (" – fehlt: " + ", ".join(fehlend) if fehlend else ""))
    # Quellen
    q = p.get("quellen")
    if q is not None:
        ok = isinstance(q, dict) and isinstance(q.get("dokumente", []), list) and isinstance(q.get("webseiten", []), list) \
             and all(isinstance(u, str) and re.match(r"https?://\S+$", u) for u in q.get("webseiten", []))
        add("ok" if ok else "bad", "Quellen: Dokumente als Liste, Webseiten als http(s)-Adressen")
    # Texte
    for f in ("bibliothek", "titel"):
        v = p.get(f)
        if v is not None and not (isinstance(v, str) and len(v) <= 120):
            add("bad", f + ": Text, max. 120 Zeichen")
    v = p.get("worum_geht_es")
    if v is not None:
        add("ok" if isinstance(v, str) and len(v) <= 600 else "bad", "Worum geht es: max. 600 Zeichen")
    # Tätigkeiten
    t = p.get("taetigkeiten")
    if t is not None:
        ok = isinstance(t, list) and len(t) >= 1 and all(x in TAETIGKEITEN for x in t) and len(set(t)) == len(t)
        add("ok" if ok else "bad", "Tätigkeiten aus der Auswahlliste, ohne Doppelungen")
    # Orte
    o = p.get("orte")
    if o is not None:
        ok = isinstance(o, list) and len(o) >= 1 and all(isinstance(x, str) and 0 < len(x) <= 40 for x in o)
        add("ok" if ok else "bad", "Orte: mind. 1, je max. 40 Zeichen")
    # Ausleihe
    a = p.get("ausleihe")
    if a is not None:
        add("ok" if a in AUSLEIHE else "bad", "Ausleihe: klassenausweis, eigener_ausweis oder nein")
    # Foto
    fo = p.get("foto")
    if fo is not None:
        ok = isinstance(fo, dict) and isinstance(fo.get("datei"), str) and fo["datei"] \
             and isinstance(fo.get("beschreibung"), str) and 0 < len(fo["beschreibung"]) <= 120
        add("ok" if ok else "bad", "Foto: Datei und Beschreibung (max. 120 Zeichen)")
        ok = isinstance(fo, dict) and fo.get("veroeffentlichen_erlaubt") is True and fo.get("keine_personen") is True
        add("ok" if ok else "bad", "Foto: beide Bestätigungen erteilt")
    # Belege (nur nach Stufe 1 vorhanden; Hilfe für die Prüfung gegen die Quellen)
    b = p.get("belege")
    if b is not None:
        if not isinstance(b, dict):
            add("bad", "Belege: Objekt Feld → Fundstelle")
        else:
            # Ein Beleg ist ein Text oder (bei mehreren Fundstellen) eine Liste von Texten
            liste = {k: ([x] if isinstance(x, str) else x) for k, x in b.items()}
            form = [k for k, x in liste.items() if not (isinstance(x, list) and x and all(isinstance(y, str) and y.strip() for y in x))]
            fremd = [k for k in b if k not in FELDER or not FELDER[k][2]]
            ohne = [f for f, (_, _, vorb) in FELDER.items() if vorb and not leer(p.get(f)) and leer(b.get(f))]
            gut = {k: x for k, x in liste.items() if k not in form}
            lang = [k for k, x in gut.items() if any(len(ausschnitt(y)) > BELEG_MAX for y in x)]
            add("bad" if form else "ok", "Belege als Text oder Liste von Texten" + (" – falsch: " + ", ".join(form) if form else ""))
            add("bad" if fremd else "ok", "Belege nur für vorbefüllbare Felder" + (" – unbekannt: " + ", ".join(fremd) if fremd else ""))
            add("warn" if ohne else "ok", "Jede vorbefüllte Angabe belegt" + (" – ohne Beleg: " + ", ".join(ohne) if ohne else ""))
            add("warn" if lang else "ok", "Belege je max. %d Zeichen" % BELEG_MAX + (" – zu lang: " + ", ".join(lang) if lang else ""))
            if quelltext is not None:
                qt = norm(quelltext)
                falsch = [k for k, x in gut.items() if any(norm(ausschnitt(y)) not in qt for y in x)]
                add("bad" if falsch else "ok", "Belege wörtlich im Quelltext" + (" – nicht gefunden: " + ", ".join(falsch) if falsch else ""))
    return res



if __name__ == "__main__":
    p = json.load(open(sys.argv[1], encoding="utf-8"))
    qt = None
    if "--quelle" in sys.argv:
        qt = open(sys.argv[sys.argv.index("--quelle") + 1], encoding="utf-8").read()
    res = validate_programm(p, "--vorbefuellt" in sys.argv, qt)
    for s, t in res:
        print({"ok": "✓", "warn": "!", "bad": "✗"}[s], t)
    sys.exit(1 if any(s == "bad" for s, _ in res) else 0)
