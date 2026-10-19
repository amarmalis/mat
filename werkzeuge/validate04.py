"""Prüfung für das Material-Schema 0.5 (Python-Fassung).

0.5 gegenüber 0.4: Enden enthalten keinen Suchauftrag mehr; das Template
bildet ihn aus den drei Merkmalen des Weges.

Spiegelt die Prüfregeln 1-18 aus „Datenmodell_Programm_Lerngruppe_Material“
(docs/Datenmodell_Programm_Lerngruppe_Material.md). Die JavaScript-Fassung
in index.html muss dieselben Ergebnisse liefern.

Aufruf aus dem Hauptordner des Repos:
  python3 werkzeuge/validate04.py materialien/<ID>.json
Optional: --lerngruppe DATEI (Standard: lerngruppen/<meta.lerngruppe>.json)
          --pictos DATEI     (Standard: assets/pictos/liste.json)

Rückgabe: Liste von (status, text) mit status in {"ok", "warn", "bad"}.
"""
import re

KNOTEN_IDS = ["S", "A", "B", "AA", "AB", "BA", "BB"]
ENDEN_IDS = ["AAA", "AAB", "ABA", "ABB", "BAA", "BAB", "BBA", "BBB"]
STUFEN = ["stufe1", "stufe2", "stufe3"]
LIM_TEXT = {"stufe1": 80, "stufe2": 150, "stufe3": 250}
LIM_AUFTRAG = {"stufe1": 80, "stufe2": 120, "stufe3": 160}
LIM_LABEL = 40
LIM_FUND = 25
LIM_WORT = 15
LIM_SUCHWORT = 30
LIM_TEAM = 30
WORTBILDER_MAX = 20


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def expected_variants(lg):
    """Ableitungsregel 1."""
    v = set(lg.get("lesestufen") or [])
    f = lg.get("foerder") or {}
    if (f.get("lernen") or 0) > 0 or (f.get("sprache") or 0) > 0:
        v.add("stufe1")
    if lg.get("kaum_deutsch") is True or any(j in (1, 2) for j in (lg.get("jahrgaenge") or [])):
        v.add("bild")
    return v


def wortbilder_required(lg):
    """Ableitungsregel 2."""
    f = lg.get("foerder") or {}
    return (f.get("lernen") or 0) > 0 or (f.get("sprache") or 0) > 0


def cut(a):
    return ", ".join(a[:6]) + (" …" if len(a) > 6 else "")


def check_entry(e, where, liste, bad, warn):
    """Regeln 10-12 für einen Bild- oder Wortbild-Eintrag."""
    if not isinstance(e, dict):
        bad.append(where + " (kein Objekt)")
        return
    w = e.get("wort")
    if not isinstance(w, str) or not w or len(w) > LIM_WORT or re.search(r"\s", w):
        bad.append(where + " (wort)")
    p = e.get("picto", "fehlt")
    if p is None:
        s = e.get("suchwort")
        if isinstance(s, str) and s.strip() and len(s) <= LIM_SUCHWORT:
            warn.append(where + " (" + s + ")")
        else:
            bad.append(where + " (picto null ohne suchwort)")
    elif is_int(p):
        if liste is not None and p not in liste:
            bad.append(where + " (ID " + str(p) + " nicht in Liste)")
    else:
        bad.append(where + " (picto)")


def validate(d, lg=None, liste=None, lg_id=None):
    res = []
    add = lambda s, t: res.append((s, t))
    meta = d.get("meta") or {}
    r = d.get("rahmen") or {}
    g = d.get("generiert") or {}
    gs = g.get("geschichte") or {}
    k = gs.get("knoten") or {}
    e = gs.get("enden") or {}

    # Regel 1
    sv = meta.get("schema_version")
    add("ok" if sv == "0.5" else "bad", "Schema-Version 0.5" + ("" if sv == "0.5" else " (gefunden: " + str(sv) + ")"))
    # Regel 2
    if lg is not None:
        ok = meta.get("lerngruppe") == lg_id
        add("ok" if ok else "warn", "Verweis auf Lerngruppe " + str(lg_id) + ("" if ok else " (im Material: " + str(meta.get("lerngruppe")) + ")"))
    else:
        add("warn", "Lerngruppe nicht geladen: Prüfung ohne Abgleich mit der Lerngruppe")
    # Regel 3
    ok = bool(r.get("klasse") and r.get("bibliothek") and r.get("programmtitel"))
    bilder = r.get("bilder")
    if bilder is not None:
        ok = ok and isinstance(bilder, list) and all(isinstance(b, dict) and b.get("datei") and b.get("beschreibung") for b in bilder)
    add("ok" if ok else "bad", "Rahmendaten vollständig, jedes Bild mit Datei und Beschreibung")
    # Regel 4
    bt = (g.get("brief") or {}).get("text")
    ok = isinstance(bt, str) and 0 < len(bt) <= 500
    add("ok" if ok else "bad", "Brief vorhanden, max. 500 Zeichen" + (" (" + str(len(bt)) + ")" if isinstance(bt, str) else ""))
    # Regel 5
    bb = g.get("bibliotheksblick")
    ok = isinstance(bb, list) and len(bb) == 1 and all(isinstance(x, dict) and is_int(x.get("bild")) and isinstance(bilder, list) and 0 <= x["bild"] < len(bilder) for x in bb)
    add("ok" if ok else "bad", "Blick in die Bibliothek: genau 1 Bild")
    # Regel 6
    mk = [i for i in KNOTEN_IDS if not isinstance(k.get(i), dict)]
    me = [i for i in ENDEN_IDS if not isinstance(e.get(i), dict)]
    bo = [i for i in KNOTEN_IDS if isinstance(k.get(i), dict) and not (isinstance(k[i].get("optionen"), list) and len(k[i]["optionen"]) == 2)]
    msg = []
    if mk: msg.append("fehlende Knoten: " + cut(mk))
    if me: msg.append("fehlende Enden: " + cut(me))
    if bo: msg.append("nicht genau 2 Optionen: " + cut(bo))
    add("bad" if msg else "ok", "7 Knoten, 8 Enden, je 2 Optionen" + (" (" + "; ".join(msg) + ")" if msg else ""))

    # Variantenfelder sammeln: (Ort, Objekt, Art) mit Art in text/label/auftrag
    felder = []
    for i in KNOTEN_IDS:
        n = k.get(i)
        if not isinstance(n, dict):
            continue
        felder.append((i, n.get("text"), "text"))
        for j, o in enumerate(n.get("optionen") or []):
            if isinstance(o, dict):
                felder.append((i + "/Option" + str(j + 1), o.get("label"), "label"))
    for i in ENDEN_IDS:
        n = e.get(i)
        if not isinstance(n, dict):
            continue
        felder.append((i, n.get("text"), "text"))
    mit_auftrag = [i for i in ENDEN_IDS if isinstance(e.get(i), dict) and "suchauftrag" in e[i]]
    add("bad" if mit_auftrag else "ok", "Suchaufträge erzeugt das Template (nicht im Material)" + (" – entfernen bei: " + cut(mit_auftrag) if mit_auftrag else ""))

    # Regel 7
    if lg is not None:
        soll = expected_variants(lg)
        basis = "Lerngruppe"
    else:
        s0 = (k.get("S") or {}).get("text")
        soll = set(s0.keys()) if isinstance(s0, dict) else set()
        basis = "Knoten S"
    falsch = []
    for wo, obj, art in felder:
        erwartet = soll - {"bild"} if art == "auftrag" else soll
        ist = set(obj.keys()) if isinstance(obj, dict) else set()
        if ist != erwartet:
            falsch.append(wo)
    vtext = ", ".join(sorted(soll)) or "keine"
    add("bad" if (falsch or not soll) else "ok", "Varianten wie " + basis + " (" + vtext + ")" + (" – abweichend: " + cut(falsch) if falsch else ""))

    # Regel 8
    lang = []
    for wo, obj, art in felder:
        if not isinstance(obj, dict):
            continue
        for s in STUFEN:
            if s not in obj:
                continue
            t = obj[s]
            lim = LIM_LABEL if art == "label" else (LIM_AUFTRAG[s] if art == "auftrag" else LIM_TEXT[s])
            if not isinstance(t, str) or not t:
                lang.append(wo + "/" + s + " (leer)")
            elif len(t) > lim:
                lang.append(wo + "/" + s + " (" + str(len(t)) + ")")
    for i in KNOTEN_IDS:
        n = k.get(i)
        if not isinstance(n, dict):
            continue
        for j, o in enumerate(n.get("optionen") or []):
            f = o.get("fund") if isinstance(o, dict) else None
            if not isinstance(f, dict) or not isinstance(f.get("name"), str) or not f["name"]:
                lang.append(i + "/Option" + str(j + 1) + "/Fund (fehlt)")
            elif len(f["name"]) > LIM_FUND:
                lang.append(i + "/Option" + str(j + 1) + "/Fund (" + str(len(f["name"])) + ")")
    add("bad" if lang else "ok", "Längengrenzen eingehalten" + (" – " + cut(lang) if lang else ""))

    # Regeln 9-12
    folge_bad, eintrag_bad, eintrag_warn = [], [], []
    for wo, obj, art in felder:
        if not isinstance(obj, dict) or "bild" not in obj or art == "auftrag":
            continue
        b = obj["bild"]
        lo, hi = (1, 1) if art == "label" else (1, 4)
        if not isinstance(b, list) or not (lo <= len(b) <= hi):
            folge_bad.append(wo)
            continue
        for x, ent in enumerate(b):
            check_entry(ent, wo + "/bild" + str(x + 1), liste, eintrag_bad, eintrag_warn)
    add("bad" if folge_bad else "ok", "Bildfolgen: 1–4 Einträge, bei Optionen genau 1" + (" – falsch: " + cut(folge_bad) if folge_bad else ""))

    # Regel 13
    wb = g.get("wortbilder")
    wb_bad, wb_warn = [], []
    pflicht = lg is not None and wortbilder_required(lg)
    if wb is None:
        if pflicht:
            add("bad", "Wortbilder fehlen (Pflicht wegen Förderbedarf Lernen oder Sprache)")
    elif not isinstance(wb, list) or not (1 <= len(wb) <= WORTBILDER_MAX):
        add("bad", "Wortbilder: 1–20 Einträge")
    else:
        for x, ent in enumerate(wb):
            check_entry(ent, "Wortbild" + str(x + 1), liste, wb_bad, wb_warn)
        add("bad" if wb_bad else "ok", "Wortbilder gültig (" + str(len(wb)) + ")" + (" – falsch: " + cut(wb_bad) if wb_bad else ""))
        # Regel 14
        s1 = [n.get("text", {}).get("stufe1", "") for n in list(k.values()) + list(e.values()) if isinstance(n, dict) and isinstance(n.get("text"), dict)]
        s1 = [t for t in s1 if isinstance(t, str)]
        fehlt = []
        for ent in wb:
            w = ent.get("wort") if isinstance(ent, dict) else None
            if isinstance(w, str) and w and not any(re.search(r"(?<!\w)" + re.escape(w) + r"(?!\w)", t, re.IGNORECASE) for t in s1):
                fehlt.append(w)
        add("warn" if fehlt else "ok", "Jedes Wortbild kommt in einem Blatt-Text vor" + (" – nicht gefunden: " + cut(fehlt) if fehlt else ""))

    # Regeln 10-12 zusammengefasst (Bildfolgen und Wortbilder)
    alle_bad = eintrag_bad + wb_bad
    alle_warn = eintrag_warn + wb_warn
    add("bad" if alle_bad else "ok", "Bild-Einträge: ein Wort (max. 15 Zeichen), Piktogramm aus der Liste" + (" – falsch: " + cut(alle_bad) if alle_bad else ""))
    if liste is None:
        add("warn", "Piktogramm-Liste nicht geladen: IDs nicht abgeglichen")
    add("warn" if alle_warn else "ok", "Alle Piktogramme vorhanden" + (" – nachtragen: " + cut(alle_warn) if alle_warn else ""))

    # Regel 15
    tn = g.get("teamnamen")
    ok_namen = isinstance(tn, list) and all(isinstance(n, str) and 0 < len(n) <= LIM_TEAM for n in tn)
    if lg is not None and is_int(lg.get("tablets")):
        soll_n = max(2, lg["tablets"])
        ok = ok_namen and len(tn) == soll_n
        add("ok" if ok else "bad", "Teamnamen: " + str(soll_n) + " (= Tablets, mind. 2), je max. 30 Zeichen" + ("" if ok else " (gefunden: " + (str(len(tn)) if isinstance(tn, list) else "keine") + ")"))
        # Regel 16
        nv = len(expected_variants(lg))
        add("ok" if lg["tablets"] >= nv else "warn", "Tablets (" + str(lg["tablets"]) + ") reichen für alle Varianten (" + str(nv) + ")")
    else:
        ok = ok_namen and len(tn) >= 2
        add("ok" if ok else "bad", "Teamnamen: mind. 2, je max. 30 Zeichen")

    # Regel 17
    at = g.get("absenden_text")
    ok = isinstance(at, str) and 0 < len(at) <= 200 and isinstance(g.get("luecken"), list)
    add("ok" if ok else "bad", "Absendetext (max. 200 Zeichen) und Lückenliste vorhanden")
    return res


if __name__ == "__main__":
    import json, os, sys

    def arg(name):
        return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None

    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print("Aufruf: python3 werkzeuge/validate04.py materialien/<ID>.json [--lerngruppe DATEI] [--pictos DATEI]")
        sys.exit(2)
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    lg_id = (d.get("meta") or {}).get("lerngruppe") if isinstance(d, dict) else None
    lg_pfad = arg("--lerngruppe") or (os.path.join("lerngruppen", str(lg_id) + ".json") if lg_id else None)
    lg = None
    if lg_pfad and os.path.exists(lg_pfad):
        lg = json.load(open(lg_pfad, encoding="utf-8"))
        lg_id = os.path.splitext(os.path.basename(lg_pfad))[0]
    pic_pfad = arg("--pictos") or os.path.join("assets", "pictos", "liste.json")
    liste = None
    if os.path.exists(pic_pfad):
        liste = [p["id"] for p in json.load(open(pic_pfad, encoding="utf-8")).get("pictos", [])]
    res = validate(d, lg, liste, lg_id)
    for s, t in res:
        print({"ok": "✓", "warn": "!", "bad": "✗"}[s], t)
    sys.exit(1 if any(s == "bad" for s, _ in res) else 0)
