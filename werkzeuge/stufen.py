"""Lesestufen und Leitlinie Lesemotivation im Sachtext prüfen und bei Bedarf nachschärfen lassen.

Die Lesestufen ⭐ / ⭐⭐ / ⭐⭐⭐ sollen sich messbar unterscheiden. Dieses Werkzeug
misst je Stufe (beide Abschnitte zusammen) einfache Kennwerte, prüft sie gegen
heuristische Zielwerte und erzeugt bei Verfehlung einen Überarbeitungsauftrag
für das Sprachmodell. Die JavaScript-Fassung in index.html (Funktion
stufenPruefung) rechnet gleich; die Lehrkraft sieht davon nichts.

Aufruf aus dem Hauptordner des Repos:
  python3 werkzeuge/stufen.py materialien/<ID>.json
      Kennwerte, Prüfung und – falls nötig – den Überarbeitungsauftrag ausgeben.
  python3 werkzeuge/stufen.py materialien/<ID>.json --einsetzen ANTWORT.json
      Antwort des Modells (JSON mit "stufe1"/"stufe2"/"stufe3" als Listen je
      Abschnitt) in das Material einsetzen, neu prüfen und die Datei überschreiben.

Die Zielwerte sind heuristisch gesetzt, nicht empirisch normiert. Bei Texten
von rund 60 Wörtern sind Lesbarkeitsindizes nur grobe Anhaltspunkte; deshalb
prüft das Werkzeug vor allem Abstände zwischen den Stufen.
"""
import re

STUFEN = ["stufe1", "stufe2", "stufe3"]
STERNE = {"stufe1": "⭐", "stufe2": "⭐⭐", "stufe3": "⭐⭐⭐"}
LIM_TEXT = {"stufe1": 180, "stufe2": 300, "stufe3": 450}

# Zielwerte (heuristisch, siehe docs/Datenmodell_Programm_Lerngruppe_Material.md)
ZIEL = {
    "s1_wps_max": 8.0,        # ⭐: höchstens 8 Wörter je Satz
    "s1_ns_max": 0.0,         # ⭐: keine Nebensätze
    "s2_wps_plus": 1.0,       # ⭐⭐: mindestens 1 Wort je Satz mehr als ⭐
    "s2_ns_max": 0.34,        # ⭐⭐: höchstens jeder dritte Satz mit Nebensatz
    "s3_wps_plus": 2.0,       # ⭐⭐⭐: mindestens 2 Wörter je Satz mehr als ⭐⭐
    "s3_ns_min": 0.34,        # ⭐⭐⭐: mindestens jeder dritte Satz mit Nebensatz
    "s2_lix_plus": 2.0,       # LIX steigt von Stufe zu Stufe
    "s3_lix_plus": 3.0,
}

ABKUERZUNGEN = ["Mr", "Mrs", "Ms", "Dr", "Nr", "St", "Hr", "Fr", "ca", "bzw", "vgl"]
SATZ_RE = re.compile("".join(r"(?<!\b" + a + r"\.)" for a in ABKUERZUNGEN) + r"(?<=[.!?])\s+")
WORT_RE = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*")
SUBJ = r"(?:weil|dass|wenn|als|ob|damit|obwohl|während|nachdem|bevor|bis|sodass|seit|seitdem|indem|wo|wie|was|wer|wohin|woher|warum)"
REL = r"(?:der|die|das|dem|den|deren|dessen|denen|welche|welcher|welches|welchem|welchen)"
NS_RE = re.compile(r",\s*(?:(?:an|auf|aus|bei|durch|für|in|mit|nach|über|unter|von|vor|zu)\s+)?(?:" + SUBJ + r"|" + REL + r")\b([^,;:.!?]*)", re.IGNORECASE)
NS_ANFANG_RE = re.compile(r"^\s*(?:Weil|Wenn|Als|Ob|Nachdem|Bevor|Während|Obwohl|Damit|Sobald|Seit)\b[^,]*,")


def hat_nebensatz(satz):
    """Heuristik: Ein Nebensatz beginnt nach Komma mit Konjunktion oder Relativpronomen
    und endet auf ein kleingeschriebenes Wort (Verb am Ende). Aufzählungen wie
    „…, die Bilderbuchecke, die Sachbuchregale“ enden auf ein Nomen und zählen nicht."""
    satz = re.sub(r"\b(" + "|".join(ABKUERZUNGEN) + r")\.", r"\1", satz)
    if NS_ANFANG_RE.search(satz):
        return True
    for m in NS_RE.finditer(satz):
        w = WORT_RE.findall(m.group(1))
        if w and w[-1][0].islower():
            return True
    return False


def saetze(text):
    return [s for s in SATZ_RE.split(text.strip()) if WORT_RE.search(s)]


def kennwerte(texte):
    """Kennwerte für eine Liste von Texten (alle Abschnitte einer Stufe)."""
    ss = [s for t in texte for s in saetze(t)]
    woerter = [w for s in ss for w in WORT_RE.findall(s)]
    if not ss or not woerter:
        return None
    lang = [w for w in woerter if len(w.replace("-", "")) > 6]
    ns = [s for s in ss if hat_nebensatz(s)]
    wps = len(woerter) / len(ss)
    return {
        "zeichen": sum(len(t) for t in texte),
        "saetze": len(ss),
        "woerter": len(woerter),
        "wps": round(wps, 1),
        "lang": round(len(lang) / len(woerter), 2),
        "ns": round(len(ns) / len(ss), 2),
        "lix": round(wps + 100 * len(lang) / len(woerter), 1),
    }


def stufen_texte(d):
    ab = (((d or {}).get("generiert") or {}).get("sachtext") or {}).get("abschnitte") or []
    out = {}
    for s in STUFEN:
        t = [a["text"][s] for a in ab if isinstance(a, dict) and isinstance(a.get("text"), dict) and isinstance(a["text"].get(s), str)]
        if t and len(t) == len(ab):
            out[s] = t
    return out


def pruefen(d):
    """Gibt (kennwerte je Stufe, Liste von Befunden, Menge der nachzuschärfenden Stufen) zurück."""
    tx = stufen_texte(d)
    kw = {s: kennwerte(t) for s, t in tx.items()}
    kw = {s: k for s, k in kw.items() if k}
    befunde, neu = [], set()
    z = ZIEL
    k1, k2, k3 = kw.get("stufe1"), kw.get("stufe2"), kw.get("stufe3")
    if k1:
        if k1["wps"] > z["s1_wps_max"]:
            befunde.append(("stufe1", f"⭐ hat {k1['wps']} Wörter je Satz, Ziel höchstens {z['s1_wps_max']:g}.")); neu.add("stufe1")
        if k1["ns"] > z["s1_ns_max"]:
            befunde.append(("stufe1", f"⭐ enthält Nebensätze ({k1['ns']:.0%} der Sätze), Ziel keine.")); neu.add("stufe1")
    if k2:
        if k1 and k2["wps"] < k1["wps"] + z["s2_wps_plus"]:
            befunde.append(("stufe2", f"⭐⭐ hat {k2['wps']} Wörter je Satz, ⭐ {k1['wps']}; Ziel mindestens {k1['wps'] + z['s2_wps_plus']:.1f}.")); neu.add("stufe2")
        if k2["ns"] > z["s2_ns_max"]:
            befunde.append(("stufe2", f"⭐⭐ hat zu viele Nebensätze ({k2['ns']:.0%}), Ziel höchstens jeder dritte Satz.")); neu.add("stufe2")
        if k1 and k2["lix"] < k1["lix"] + z["s2_lix_plus"]:
            befunde.append(("stufe2", f"⭐⭐ ist nicht schwerer als ⭐ (LIX {k2['lix']:g} gegenüber {k1['lix']:g}).")); neu.add("stufe2")
    if k3:
        if k2 and k3["wps"] < k2["wps"] + z["s3_wps_plus"]:
            befunde.append(("stufe3", f"⭐⭐⭐ hat {k3['wps']} Wörter je Satz, ⭐⭐ {k2['wps']}; Ziel mindestens {k2['wps'] + z['s3_wps_plus']:.1f}.")); neu.add("stufe3")
        if k3["ns"] < z["s3_ns_min"]:
            befunde.append(("stufe3", f"⭐⭐⭐ hat zu wenige Nebensätze ({k3['ns']:.0%}), Ziel mindestens jeder dritte Satz.")); neu.add("stufe3")
        if k2 and k3["lix"] < k2["lix"] + z["s3_lix_plus"]:
            befunde.append(("stufe3", f"⭐⭐⭐ ist nicht schwerer als ⭐⭐ (LIX {k3['lix']:g} gegenüber {k2['lix']:g}).")); neu.add("stufe3")
    return kw, befunde, neu


# ----- Leitlinie Lesemotivation (Regel 19) -----
# L1 Bezug zum Lesen: je Fassung mindestens ein Satz, in dem es ums Lesen geht oder
#    die Kinder etwas mit Büchern tun (aussuchen, entdecken, stöbern, ausleihen …).
# L2 Neugier: Abschnitt 1 jeder Fassung endet mit einer Frage, die der Besuch beantwortet.
# L3 Autonomie: keine kontrollierende Sprache (müssen, sollen, verboten …).
# L4 Lesen nicht als Pflicht: keine Schul- oder Prüfungswörter (lernen, üben, Test …).
LESEN_RE = re.compile(r"\b(?:lesen|lest|liest|lies|vorlesen|Lesen|Lesetipps?|Lesefutter)\b")
BUCH_RE = re.compile(r"\b(?:Buch|Bücher|Büchern|Buches)\b")
BUCH_TUN_RE = re.compile(r"\b(?:aussuchen|sucht|sucht euch|entdeck\w*|stöber\w*|ausleih\w*|leiht|find\w*|anschau\w*|schaut|blätter\w*|mitnehm\w*|nehmt)\b", re.IGNORECASE)
KONTROLLE_RE = re.compile(r"\b(?:müsst|müssen|muss|sollt|sollen|soll|dürft nicht|darf nicht|nicht erlaubt|verboten|Pflicht)\b", re.IGNORECASE)
SCHULE_RE = re.compile(r"\b(?:lernen|lernt|lerne|lernst|üben|übt|Übung\w*|Test\w*|Prüfung\w*|Noten?|Hausaufgabe\w*|Unterricht)\b", re.IGNORECASE)


def lesebezug(texte):
    for t in texte:
        for satz in saetze(t):
            if LESEN_RE.search(satz) or (BUCH_RE.search(satz) and BUCH_TUN_RE.search(satz)):
                return True
    return False


def leitlinie(d):
    """Gibt (Befunde im Sachtext als (stufe, text), übrige Befunde als text, Menge der nachzuschärfenden Stufen) zurück."""
    tx = stufen_texte(d)
    st, sonst, neu = [], [], set()
    for s, texte in tx.items():
        if not lesebezug(texte):
            st.append((s, f"{STERNE[s]}: Kein Satz zum Lesen oder zu Büchern, mit denen die Kinder etwas tun (L1).")); neu.add(s)
        if texte and not texte[0].rstrip().endswith("?"):
            st.append((s, f"{STERNE[s]}: Abschnitt 1 endet nicht mit einer Frage, die der Besuch beantwortet (L2).")); neu.add(s)
        for t in texte:
            m = KONTROLLE_RE.search(t)
            if m:
                st.append((s, f"{STERNE[s]}: kontrollierende Sprache „{m.group(0)}“ (L3).")); neu.add(s); break
        for t in texte:
            m = SCHULE_RE.search(t)
            if m:
                st.append((s, f"{STERNE[s]}: Schul- oder Prüfungswort „{m.group(0)}“ (L4).")); neu.add(s); break
    g = (d or {}).get("generiert") or {}
    brief = ((g.get("brief") or {}).get("text")) or ""
    rahmen = " ".join(v for v in (g.get("antwortbrief") or {}).values() if isinstance(v, str))
    for name, t, regeln in (("Fridos Brief", brief, (KONTROLLE_RE, SCHULE_RE)), ("Antwortbrief-Rahmen", rahmen, (KONTROLLE_RE,))):
        for r in regeln:
            m = r.search(t)
            if m:
                sonst.append(f"{name}: „{m.group(0)}“ ({'L3' if r is KONTROLLE_RE else 'L4'}).")
    return st, sonst, neu


def auftrag(d):
    """Überarbeitungsauftrag für den Sachtext als Nachricht an das Sprachmodell (oder None)."""
    kw, befunde, neu = pruefen(d)
    lb, _, lneu = leitlinie(d)
    neu = neu | lneu
    if not neu:
        return None
    tx = stufen_texte(d)
    stufen = [s for s in STUFEN if s in neu]
    z = []
    z.append("Der Sachtext erfüllt noch nicht alle Vorgaben. Überarbeite nur die Fassungen " + ", ".join(STERNE[s] + " (" + s + ")" for s in stufen) + ".")
    z.append("")
    z.append("Gemessen:")
    for _, t in befunde + lb:
        z.append("- " + t)
    z.append("")
    z.append("So sollen sich die Stufen unterscheiden:")
    z.append("- ⭐: kurze Hauptsätze, höchstens 8 Wörter je Satz, keine Nebensätze.")
    z.append("- ⭐⭐: kurze Sätze, im Schnitt etwas länger als ⭐, höchstens jeder dritte Satz mit Nebensatz.")
    z.append("- ⭐⭐⭐: im Schnitt mindestens 2 Wörter je Satz mehr als ⭐⭐; mindestens jeder dritte Satz mit Nebensatz (weil, dass, wenn, der/die/das …); abwechslungsreichere Wörter, aber Wortschatz der Grundschule.")
    z.append("")
    z.append("Leitlinie Lesemotivation (für jede Fassung):")
    z.append("- L1: Mindestens ein Satz spricht das Lesen oder Bücher an, mit denen die Kinder beim Besuch etwas tun – nur, was das Programmprofil hergibt (zum Beispiel Regale, Bücher zum Thema, Ausleihe).")
    z.append("- L2: Abschnitt 1 endet mit einer Frage zum Motiv des Programms, die erst der Besuch beantwortet.")
    z.append("- L3: einladend statt kontrollierend: „ihr könnt“, „ihr sucht euch aus“, nicht „ihr müsst“, „ihr sollt“.")
    z.append("- L4: keine Schul- oder Prüfungswörter (lernen, üben, Test). Steht so etwas im Profil, umschreiben („ihr findet heraus, wo welche Bücher stehen“).")
    z.append("")
    z.append("Regeln: Inhalt und Informationen bleiben gleich, nichts dazuerfinden, nichts weglassen. Jede Fassung bleibt innerhalb ihrer Zeichengrenze (⭐ 180, ⭐⭐ 300, ⭐⭐⭐ 450 je Abschnitt). Alle anderen Felder bleiben unverändert.")
    z.append("")
    z.append("Bisherige Fassungen:")
    for s in stufen:
        for i, t in enumerate(tx[s]):
            z.append(f"{STERNE[s]} Abschnitt {i + 1}: {t}")
    z.append("")
    z.append("Antworte nur mit JSON in dieser Form, ein Eintrag je Abschnitt:")
    z.append("{" + ", ".join(f'"{s}": ["<Abschnitt 1>", "<Abschnitt 2>"]' for s in stufen) + "}")
    return "\n".join(z)

def einsetzen(d, antwort):
    """Antwort des Modells einsetzen; gibt Liste von Fehlermeldungen zurück (leer = eingesetzt)."""
    ab = d["generiert"]["sachtext"]["abschnitte"]
    fehler = []
    for s, liste in antwort.items():
        if s not in STUFEN or not isinstance(liste, list) or len(liste) != len(ab):
            fehler.append(f"{s}: erwartet Liste mit {len(ab)} Texten"); continue
        for i, t in enumerate(liste):
            if not isinstance(t, str) or not t.strip():
                fehler.append(f"{s}, Abschnitt {i + 1}: leer")
            elif len(t) > LIM_TEXT[s]:
                fehler.append(f"{s}, Abschnitt {i + 1}: {len(t)} Zeichen, erlaubt {LIM_TEXT[s]}")
    if fehler:
        return fehler
    for s, liste in antwort.items():
        for i, t in enumerate(liste):
            ab[i]["text"][s] = t.strip()
    return []


def bericht(kw):
    z = ["Stufe   Zeichen  Sätze  Wörter/Satz  Nebensätze  lange Wörter  LIX"]
    for s in STUFEN:
        k = kw.get(s)
        if k:
            z.append(f"{STERNE[s]:<6} {k['zeichen']:>7}  {k['saetze']:>5}  {k['wps']:>11}  {k['ns']:>10.0%}  {k['lang']:>12.0%}  {k['lix']:>4g}")
    return "\n".join(z)


if __name__ == "__main__":
    import json, sys

    if len(sys.argv) < 2:
        print("Aufruf: python3 werkzeuge/stufen.py materialien/<ID>.json [--einsetzen ANTWORT.json]")
        sys.exit(2)
    pfad = sys.argv[1]
    d = json.load(open(pfad, encoding="utf-8"))
    if "--einsetzen" in sys.argv:
        antwort = json.load(open(sys.argv[sys.argv.index("--einsetzen") + 1], encoding="utf-8"))
        fehler = einsetzen(d, antwort)
        if fehler:
            print("Nicht eingesetzt:\n- " + "\n- ".join(fehler)); sys.exit(1)
        json.dump(d, open(pfad, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(pfad, "a", encoding="utf-8").write("\n")
        print("Eingesetzt und gespeichert.")
    kw, befunde, neu = pruefen(d)
    lb, ls, lneu = leitlinie(d)
    print(bericht(kw))
    print()
    print("✓ Die Lesestufen unterscheiden sich ausreichend." if not befunde else "\n".join("! " + t for _, t in befunde))
    print("✓ Leitlinie Lesemotivation eingehalten." if not (lb or ls) else "\n".join("! " + t for t in [t for _, t in lb] + ls))
    if not (neu or lneu):
        sys.exit(0)
    print("\n----- Überarbeitungsauftrag (als nächste Nachricht im selben Chat senden) -----\n")
    print(auftrag(d))
    sys.exit(0)
