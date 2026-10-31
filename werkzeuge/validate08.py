"""Prüfung für das Material-Schema 0.8 (Python-Fassung).

Spiegelt die Prüfregeln 1-17 aus „Datenmodell_Programm_Lerngruppe_Material“
(docs/Datenmodell_Programm_Lerngruppe_Material.md). Die JavaScript-Fassung
in index.html (Funktion validate) liefert dieselben Ergebnisse.
Für Material im Schema 0.7 gilt werkzeuge/validate07.py, für 0.5 werkzeuge/validate04.py.

Aufruf aus dem Hauptordner des Repos:
  python3 werkzeuge/validate08.py materialien/<ID>.json
Optional: --lerngruppe DATEI (Standard: lerngruppen/<meta.lerngruppe>.json)
          --pictos DATEI     (Standard: assets/pictos/liste.json)

Rückgabe: Liste von (status, text) mit status in {"ok", "warn", "bad"};
Exit-Code 1, wenn mindestens ein Fehler vorliegt.
"""
import re

STUFEN = ["stufe1", "stufe2", "stufe3"]
LIM_TEXT = {"stufe1": 180, "stufe2": 300, "stufe3": 450}
LIM_BRIEF = 400
LIM_WORT = 15
LIM_SUCHWORT = 30
WORTBILDER_MAX = 20
LIM_AB = {"anrede": 80, "einleitung": 300, "vor_vermutungen": 120, "vor_fragen": 120, "schluss": 200, "gruss": 60}
AB_FELDER = ["anrede", "einleitung", "vor_vermutungen", "vor_fragen", "schluss", "gruss"]


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_obj(v):
    return isinstance(v, dict)


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
    """Bild- oder Wortbild-Eintrag."""
    if not is_obj(e):
        bad.append(where + " (kein Objekt)")
        return
    w = e.get("wort")
    if not isinstance(w, str) or not w or len(w) > LIM_WORT or re.search(r"\s", w):
        bad.append(where + " (wort)")
    if "picto" not in e:
        bad.append(where + " (picto)")
        return
    p = e["picto"]
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


def validate(d, lg, liste, lg_id):
    res = []

    def add(s, t):
        res.append((s, t))

    meta = d.get("meta") if is_obj(d.get("meta")) else {}
    r = d.get("rahmen") if is_obj(d.get("rahmen")) else {}
    g = d.get("generiert") if is_obj(d.get("generiert")) else {}
    st = g.get("sachtext") if is_obj(g.get("sachtext")) else {}
    ab = st.get("abschnitte") if isinstance(st.get("abschnitte"), list) else []
    lg = lg if is_obj(lg) else None

    # Regel 1
    sv = meta.get("schema_version")
    add("ok" if sv == "0.8" else "bad", "Schema-Version 0.8" + ("" if sv == "0.8" else " (gefunden: " + ("keine" if sv is None else str(sv)) + ")"))
    # Regel 2
    if lg is not None:
        ok = meta.get("lerngruppe") == lg_id
        add("ok" if ok else "warn", "Verweis auf Lerngruppe " + str(lg_id) + ("" if ok else " (im Material: " + ("keiner" if meta.get("lerngruppe") is None else str(meta.get("lerngruppe"))) + ")"))
    else:
        add("warn", "Lerngruppe nicht geladen: Prüfung ohne Abgleich mit der Lerngruppe")
    # Regel 3
    ok = bool(r.get("klasse") and r.get("bibliothek") and r.get("programmtitel"))
    bilder = r.get("bilder")
    if bilder is not None:
        ok = ok and isinstance(bilder, list) and all(is_obj(b) and b.get("datei") and b.get("beschreibung") for b in bilder)
    add("ok" if ok else "bad", "Rahmendaten vollständig, jedes Bild mit Datei und Beschreibung")
    # Regel 4
    bt = g["brief"].get("text") if is_obj(g.get("brief")) else None
    ok = isinstance(bt, str) and 0 < len(bt) <= LIM_BRIEF
    add("ok" if ok else "bad", "Brief vorhanden, max. 400 Zeichen" + (" (" + str(len(bt)) + ")" if isinstance(bt, str) else ""))
    # Regel 5
    if isinstance(bt, str) and bt:
        anrede = "Hallo " + str(r.get("klasse") or "") + "!"
        ok = bt.strip().startswith(anrede) and bt.strip().endswith("euer Frido")
        add("ok" if ok else "warn", "Brief beginnt mit „" + anrede + "“ und endet mit „euer Frido“")
    # Regel 6
    bb = g.get("bibliotheksblick")
    ok = isinstance(bb, list) and len(bb) == 1 and all(
        is_obj(x) and is_int(x.get("bild")) and isinstance(bilder, list) and 0 <= x["bild"] < len(bilder) for x in bb)
    add("ok" if ok else "bad", "Blick in die Bibliothek: genau 1 Bild")
    # Regel 7
    q = st.get("quellen")
    q_ok = isinstance(q, list) and len(q) > 0 and all(isinstance(x, str) and x for x in q)
    ok = 1 <= len(ab) <= 2 and all(is_obj(a) and is_obj(a.get("text")) for a in ab) and q_ok
    add("ok" if ok else "bad", "Sachtext mit 1 oder 2 Abschnitten und Quellen" + ("" if ok else " (Abschnitte: " + str(len(ab)) + ", Quellen: " + ("ja" if q_ok else "keine") + ")"))
    # Regel 8
    if lg is not None:
        soll, basis = expected_variants(lg), "Lerngruppe"
    else:
        t0 = ab[0].get("text") if ab and is_obj(ab[0]) and is_obj(ab[0].get("text")) else None
        soll, basis = set(t0.keys()) if t0 else set(), "Abschnitt 1"
    falsch = []
    for i, a in enumerate(ab):
        ist = set(a["text"].keys()) if is_obj(a) and is_obj(a.get("text")) else set()
        if ist != soll:
            falsch.append("Abschnitt " + str(i + 1))
    vtext = ", ".join(sorted(soll)) or "keine"
    add("bad" if (falsch or not soll) else "ok", "Varianten wie " + basis + " (" + vtext + ")" + (" – abweichend: " + cut(falsch) if falsch else ""))
    # Regel 9
    lang = []
    for i, a in enumerate(ab):
        if not is_obj(a) or not is_obj(a.get("text")):
            continue
        for s in STUFEN:
            if s not in a["text"]:
                continue
            t = a["text"][s]
            if not isinstance(t, str) or not t:
                lang.append("Abschnitt " + str(i + 1) + "/" + s + " (leer)")
            elif len(t) > LIM_TEXT[s]:
                lang.append("Abschnitt " + str(i + 1) + "/" + s + " (" + str(len(t)) + ")")
    add("bad" if lang else "ok", "Längengrenzen der Abschnitte (180/300/450)" + (" – " + cut(lang) if lang else ""))
    # Regel 10
    folge_bad, eintrag_bad, eintrag_warn = [], [], []
    for i, a in enumerate(ab):
        if not is_obj(a) or not is_obj(a.get("text")) or "bild" not in a["text"]:
            continue
        b = a["text"]["bild"]
        if not isinstance(b, list) or not 1 <= len(b) <= 4:
            folge_bad.append("Abschnitt " + str(i + 1))
            continue
        for x, e in enumerate(b):
            check_entry(e, "Abschnitt " + str(i + 1) + "/Bild " + str(x + 1), liste, eintrag_bad, eintrag_warn)
    add("bad" if folge_bad else "ok", "Bildfolgen: 1–4 Einträge" + (" – falsch: " + cut(folge_bad) if folge_bad else ""))
    # Regel 11
    wb = g.get("wortbilder")
    wb_bad, wb_warn = [], []
    pflicht = lg is not None and wortbilder_required(lg)
    if wb is None:
        if pflicht:
            add("bad", "Wortbilder fehlen (Pflicht wegen Förderbedarf Lernen oder Sprache)")
    elif not isinstance(wb, list) or not 1 <= len(wb) <= WORTBILDER_MAX:
        add("bad", "Wortbilder: 1–20 Einträge")
    else:
        for x, e in enumerate(wb):
            check_entry(e, "Wortbild " + str(x + 1), liste, wb_bad, wb_warn)
        add("bad" if wb_bad else "ok", "Wortbilder gültig (" + str(len(wb)) + ")" + (" – falsch: " + cut(wb_bad) if wb_bad else ""))
        s1 = [a["text"]["stufe1"] for a in ab if is_obj(a) and is_obj(a.get("text")) and isinstance(a["text"].get("stufe1"), str)]
        fehlt = []
        for e in wb:
            w = e.get("wort") if is_obj(e) else None
            if isinstance(w, str) and w:
                rx = re.compile(r"(?<!\w)" + re.escape(w) + r"(?!\w)", re.IGNORECASE)
                if not any(rx.search(t) for t in s1):
                    fehlt.append(w)
        add("warn" if fehlt else "ok", "Jedes Wortbild kommt in einem ⭐-Text vor" + (" – nicht gefunden: " + cut(fehlt) if fehlt else ""))
    alle_bad, alle_warn = eintrag_bad + wb_bad, eintrag_warn + wb_warn
    add("bad" if alle_bad else "ok", "Bild-Einträge: ein Wort (max. 15 Zeichen), Piktogramm aus der Liste" + (" – falsch: " + cut(alle_bad) if alle_bad else ""))
    if liste is None:
        add("warn", "Piktogramm-Liste nicht geladen: IDs nicht abgeglichen")
    add("warn" if alle_warn else "ok", "Alle Piktogramme vorhanden" + (" – nachtragen: " + cut(alle_warn) if alle_warn else ""))
    # Regeln 12 und 13
    ue = g.get("uebersetzungen")
    ue_obj = ue if is_obj(ue) else {}
    ue_bad, ue_warn = [], []
    if ue is not None and not is_obj(ue):
        ue_bad.append("kein Objekt")
    soll_spr = lg.get("sprachen") if lg is not None and isinstance(lg.get("sprachen"), list) else None
    if soll_spr is not None:
        for c in soll_spr:
            if c not in ue_obj:
                ue_bad.append(c + " fehlt")
        for c in ue_obj:
            if c not in soll_spr:
                ue_bad.append(c + " ohne Sprachcode in der Lerngruppe")
    for c, u in ue_obj.items():
        texte = u.get("abschnitte") if is_obj(u) else None
        if not isinstance(texte, list) or len(texte) != len(ab) or not all(isinstance(t, str) and t for t in texte):
            ue_bad.append(c + " (" + str(len(ab)) + " Texte)")
            continue
        if u.get("stufe") not in LIM_TEXT:
            ue_bad.append(c + " (stufe)")
            continue
        for i, t in enumerate(texte):
            if len(t) > LIM_TEXT[u["stufe"]]:
                ue_warn.append(c + "/Abschnitt " + str(i + 1) + " (" + str(len(t)) + ")")
    if soll_spr is not None or ue_obj:
        add("bad" if ue_bad else "ok", "Übersetzungen: je Sprache der Lerngruppe ein Text je Abschnitt" + (" – " + cut(ue_bad) if ue_bad else ""))
    if ue_obj:
        add("warn" if ue_warn else "ok", "Übersetzungen innerhalb der Längengrenze der übersetzten Stufe" + (" – " + cut(ue_warn) if ue_warn else ""))
    # Regel 14
    abr = g.get("antwortbrief") if is_obj(g.get("antwortbrief")) else None
    ab_bad = []
    if abr is None:
        ab_bad.append("fehlt")
    else:
        for f in AB_FELDER:
            v = abr.get(f)
            if not isinstance(v, str) or not v.strip():
                ab_bad.append(f + " leer")
            elif len(v) > LIM_AB[f]:
                ab_bad.append(f + " (" + str(len(v)) + ")")
    add("bad" if ab_bad else "ok", "Antwortbrief: 6 Felder, Längengrenzen eingehalten" + (" – " + cut(ab_bad) if ab_bad else ""))
    # Regel 15
    add("ok" if isinstance(g.get("luecken"), list) else "bad", "Lückenliste vorhanden")
    # Regel 16
    alt = [k for k in ("geschichte", "plan", "teamnamen", "absenden_text") if k in g]
    add("bad" if alt else "ok", "Keine Felder aus früheren Schemata" + (" – " + cut(alt) if alt else ""))
    # Regel 17
    if lg is not None and is_int(lg.get("tablets")):
        nv = len(expected_variants(lg))
        add("ok" if lg["tablets"] >= nv else "warn", "Tablets (" + str(lg["tablets"]) + ") reichen für alle Varianten (" + str(nv) + ")")
    return res


if __name__ == "__main__":
    import json, os, sys

    def arg(name):
        return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None

    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print("Aufruf: python3 werkzeuge/validate08.py materialien/<ID>.json [--lerngruppe DATEI] [--pictos DATEI]")
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
