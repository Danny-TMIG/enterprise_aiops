#!/usr/bin/env python3
"""Seven-layer causal projection + symbolic atlas."""
import json, re, sys
from collections import defaultdict
from pathlib import Path

BASES = ("Δ", "Π", "Λ", "τ")
VERB  = {"Δ": "distinguish", "Π": "preserve", "Λ": "link",   "τ": "transform"}
TARG  = {"Δ": "unit",        "Π": "state",    "Λ": "pair",   "τ": "process"}
MODE  = {"Δ": "local",       "Π": "temporal", "Λ": "structural", "τ": "behavioral"}
LAYERS = ["ontology","logic","causality","conation",
          "norms","verification","closure"]

def codons(seq):
    return [seq[i:i+3] for i in range(0, len(seq)-2, 3)]

def project_7layer(seq):
    cs = codons(seq)
    out = {L: [] for L in LAYERS}
    for i, c in enumerate(cs):
        v, t, m = VERB[c[0]], TARG[c[1]], MODE[c[2]]
        out["ontology"].append(     {"step": i, "entity": t, "role": v})
        out["logic"].append(        {"step": i, "rule": f"{v}({t})", "well_formed": True})
        out["causality"].append(    {"step": i, "effect": f"{t}→{v}",
                                     "real": m != "local"})
        out["conation"].append(     {"step": i, "drive": f"toward {t}"})
        out["norms"].append(        {"step": i, "constraint": f"{v}∈{m}"})
        out["verification"].append( {"step": i, "evidence": f"trace[{c}]",
                                     "hash": hex(hash(c) & 0xffffff)})
    out["closure"].append({
        "boundary": len(seq),
        "leakage":  len(seq) % 3,
        "closed":   len(seq) % 3 == 0,
        "total_steps": len(cs),
    })
    return {"sequence": seq, "codons": cs, **out}

# ── symbolic atlas ─────────────────────────────────────────────────
SYMBOLS_TEXT = r"""
Angel|Messenger|Dan 8:16; 9:21; Luk 1:19,26; Heb 1:14
Ark of Testimony|Ark of the covenant / mercy seat where God dwells|Exo 25:10-22; Psa 80:1
Babylon|Religious apostasy / confusion|Gen 10:8-10; 11:6-9; Rev 18:2-3; 17:1-5
Balaam, Doctrine of|Compromise, idolatry|Num 22:5-25
Beast|Kingdom, government, political power|Dan 7:23
Bear|Destructive power / Medo-Persia|Pro 28:15; 2Ki 2:23-24; Dan 7:5
Binding of Satan|A symbolic chain of circumstances|Isa 14:12-20
Black|Moral darkness, sin, apostasy|Exo 10:21-23; Jer 4:20-28; Joh 12:35
Blood|Life|Lev 17:11; Deu 12:23
Blue (color)|Law|Num 15:38-39
Bottomless pit|Earth in chaos, torn up, dark and empty|Gen 1:1,2; Jer 4:23-28; Isa 24:1-4
Bow|Success in battle against evil|Psa 7:11,12; Psa 45:4,5
Bread|Word of God|Joh 6:35, 51, 52, 63
Brass, Tin, Iron, Lead, Silver dross|Impure character|Eze 22:20-21
Corrupt Woman|Corrupt, apostate church|Eze 16:15-58; Hos 2:5; 3:1
Crowns|Kingship, victory|1Ch 20:2; 2Ki 11:12; Eze 21:26,27; Jam 1:12
Clothing|Character|Isa 64:6; Isa 59:6
Cup|Meted out suffering and judgments|Psa 11:6; Isa 51:12; Jer 25:12-17
Day|Literal year|Eze 4:6; Num 14:34
Door|Opportunity / Probation|2Co 2:12; Rev 3:20; Luk 12:24,25
Dove|Holy Spirit|Mar 1:10
Dragon|Satan or his agency|Isa 27:1; Psa 74:13,14; Rev 12:7,9; Eze 29:3
Eagle|Speed, power, vision, vengeance, protection|Deu 28:49; Hab 1:6-8; Rev 12:1-4
Eating of the book|Assimilating the message|Eze 3:1-3; Jer 15:16
Egypt|Symbol of atheism|Exo 5:2
Eyes|Spiritual discernment|Mat 13:10-17; 1Jo 2:11
Eye salve|Holy Spirit to help us see truth|Eph 1:12-19; Psa 119:18; 1Jo 2:20,27
Faithful witness|Christ|Joh 18:37; Joh 3:11; Rev 1:5; 3:14; 19:11
False Prophet|Apostate protestantism|Rev 16:13,14; 13:13,14; 19:20
Famine|Dearth of Truth|Amo 8:11
Feet|Your walk / Direction|Gen 19:2; Psa 119:105
Forehead|Mind|Rom 7:25; Eze 3:8,9
Fornication|Illicit connection between church and world|Eze 16:15,26; Isa 23:17; Jam 4:4
Four Beasts|Heavenly beings with special responsibilities|Rev 5:8-10; 4:6-9; 6:1-7; 14:3
Four corners of Earth|Four directions of compass|Jer 49:36
Fire|Holy Spirit|Luk 3:16
Fig Tree|A Nation that should bear fruit|Luk 13:6-9
Field|World|Mat 13:38; Joh 4:35
Fruit|Works / Actions|Ga 5:22
Garments|Covering of righteousness|Gen 35:2; Isa 61:10; Rom 13:14
Gold|True riches of heaven, faith, scripture|Psa 19:7-10; Gal 5:6; Jam 2:5
Goat|Greece|Dan 8:21
Hand|Symbol of Deeds / Works / Actions|Ecc 9:10; Isa 59:6
Harvest|End of World|Mat 13:39
Harlot|Apostate church / religion|Isa 1:21-27; Jer 3:1-3,6-9
Heads|Major powers / rulers / governments|Rev 17:3,9,10; Dan 7:6; 8:8,22
Healing|Salvation|Luk 5:23-24
Hidden Manna|Christ|Joh 6:49,50,53; Mat 13:44
Honey|Happy life|Eze 20:6; Deu 8:8-9
Horn|King or kingdom, power and strength|Dan 7:24; 8:5,21,22; Rev 17:12
Horse|Strength and power in battle|Job 39:19; Psa 147:10; Exo 15:21
Image|A likeness|Exo 20:4; Gen 1:26; 5:3
Incense|Prayers of God's people|Psa 141:2; Rev 5:8
Israel|True followers of Christ|Rom 9:6-8; 2:28,29; Gal 3:29
Jar / Vessel|Person|Jer 18:1-4; 2Co 4:7
Jezebel|Immorality, idolatry, apostasy|1Ki 21:25; 2Ki 9:22
Jordan|Death|Rom 6:4; Deu 4:22
Key of David|Power to open & close the sanctuary|Rev 3:7-9; Isa 22:22
Keys|Control / jurisdiction|Isa 22:22; Mat 16:19
Lamb|Jesus / sacrifice|Joh 1:29; 1Co 5:7; Gen 22:7,8
Lamp|Word of God|Psa 119:105
Lamb's Wife|New Jerusalem|Rev 19:7-9; 21:2,9,10
Lion|Jesus / powerful king|Rev 5:4-9; Jer 50:43-44; Dan 7:4,17,23
Locusts|Destruction|Joe 1:4; Deu 28:38
Leopard|Greece|Dan 7:6
Leprosy|Sin|Luk 5:23-24
Lords Day|The Sabbath|Isa 58:13; Mat 12:8; Exo 20:10
Man Child|Jesus|Psa 2:7-9; Rev 12:5
Mark|Sign / seal / mark of approval or disapproval|Rom 4:11; Eze 9:4; Rev 13:17
Measuring Rod|God's law|Jam 2:10-12; Ecc 12:13,14
Merchants|Advocates of Babylon's teachings|Isa 47:11-15; Nah 3:16; Rev 18:3,11,15
Moon|Permanence|Psa 89:35-37
Morning star|Jesus|Rev 22:16
Mountains|Political or religion-political powers|Isa 2:2,3; Jer 17:3; Dan 2:35
Mystery of God|The gospel|Eph 1:9,10; Col 1:26,27
New Jerusalem|The holy city of heaven|Rev 3:12; 21:2
Oil|Holy Spirit|Zec 4:2-6; Rev 4:5
Open Door|Unlimited opportunity|1Co 16:9; Joh 10:7-9; Hos 2:15
Purple|Royalty|Mar 15:17; Jdg 8:26
Rainbow|Token of covenant keeping|Gen 9:11-17
Ram|Medo-Persia|Dan 8:20
Red / Scarlet|Sin / corruption|Isa 1:18; Nah 2:3; Rev 17:1-4
Reapers|Angels|Mat 13:39
Reins|Seat of will, affections|Psa 7:9; Jer 17:10
Ring|Authority|Gen 41:42-43; Est 3:10-11
Rock|Jesus / truth|1Co 10:4; Isa 8:13,14; Mat 7:24
Seal|Sign or mark of approval or disapproval|Rom 4:11; Rev 7:2,3
Seed|Descendants / Jesus|Rom 9:8; Gal 3:16
Second Death|Lake of fire|Rev 21:8; 20:2
Serpent|Satan|Rev 12:9; 20:2
Seven Candle Sticks|Seven churches|Exo 25:31-40; Rev 1:20
Seven Heads|Seven political powers|Rev 17:9,10; Isa 2:2-4
Seven Lamps|Jesus, Word of God|Joh 9:5; Psa 119:105; Rev 4:5
Sickle|Symbol of harvest / end of world|Mat 13:39; Rev 14:14
Silver|Pure words & understanding|Pro 2:4; 3:13-14; Psa 12:6
Sodom|Moral degradations|Eze 16:46-55; Jer 23:14; Gen 19:4-14
Stars|Angels / messengers|Rev 1:16,20; 12:4,7-9; Job 38:7
Sun|Jesus / the gospel|Psa 84:11; Mal 4:2; Joh 8:12
Skin|Christ's righteousness|Exo 12:5; 1Pe 1:19; Isa 1:4-6
Sword|Word of God|Eph 6:17; Heb 4:12
Testimony of Jesus|Holy Spirit / Gift of prophecy|Rev 19:10; 22:9; 1Co 13:2
Thief|Unexpected|1Th 5:2-4; 2Pe 3:10
Thorns / Thorny Ground|Cares of this life|Mar 4:18-19
Tongue|Language / Speech|Exo 4:10
Time|360 Day (Literal Years)|Dan 4:16,23,35; 7:25; 11:13
Times|720 Days (Literal Years)|Dan 7:25; Rev 12:6,14; 13:5
Trumpet|Loud warning of God's approach|Exo 19:16-17; Jos 6:4-5
Tree|Cross; People / Nation|Deu 21:22-23; Psa 92:12
Torment|Test, prove by trial|1Co 3:13; Heb 12:29; Isa 33:14
Twenty-four elders|A group redeemed from earth|Rev 5:9-10; 4:4; 7:9-14
Two-edged Sword|God's word|Eph 6:17; Heb 4:12; Mat 10:34
Two witnesses|Old and New Testaments|Joh 5:39; Zec 4:1-14; Joh 12:48
Vineyard|Church that should bear fruit|Luk 20:9-16
Waters|Inhabited Area - People / Nations|Rev 17:15
Water|Holy Spirit / Everlasting Life|Joh 7:39; 4:14; Rev 22:17; Eph 5:26
White (Color)|Purity|Rev 12:9; 20:2
White Robes|Victory / righteousness|Rev 19:8; 3:5; 7:14
Winds|Strife, commotions, "winds of war"|Jer 25:31-33; Zec 7:14
Wings|Speed / Protection / Deliverance|Deu 28:49; Mat 23:37
Wine|Blood / covenant / doctrines|Luk 5:37; Isa 5:1-7
Woman, Pure|True church|Jer 6:2; 2Co 11:2; Eph 5:23-27
Wolf|Disguised enemies in a time of darkness|Mat 7:15
Wormwood|Sorrow / bitterness|Jer 9:15; 23:15; Lam 3:19
Wrath of God|Seven last plagues|Rev 15:1
""".strip()

def parse_symbols(text):
    out = []
    for line in text.splitlines():
        parts = line.split("|")
        if len(parts) != 3:
            continue
        sym, mean, refs = (p.strip() for p in parts)
        out.append({
            "symbol": sym,
            "meaning": mean,
            "refs": [r.strip() for r in refs.split(";")],
        })
    return out

def symbol_kernel(s):
    """Five-slot kernel for a symbolic entry."""
    return {
        "delta":     f"the distinction the symbol marks",
        "pi":        f"the meaning that persists: {s['meaning'][:60]}",
        "lambda":    f"the references that bind it: {len(s['refs'])} anchors",
        "tau":       f"what the symbol transforms when read",
        "epsilon":   f"grounding: {s['refs'][0] if s['refs'] else 'unattributed'}",
    }

def link_by_reference(symbols):
    by_book = defaultdict(list)
    for s in symbols:
        for r in s["refs"]:
            book = re.match(r"([1-3]?[A-Za-z]+)", r)
            if book:
                by_book[book.group(1)].append(s["symbol"])
    return dict(by_book)

def main():
    # ── 7-layer causal demo ────────────────────────────────────────
    s = "ΔΠΛτΛΠΔΔΠτ"
    print("=" * 60)
    print(f"7-LAYER CAUSAL PROJECTION")
    print(f"sequence: {s}   codons: {codons(s)}")
    print("=" * 60)
    r = project_7layer(s)
    for L in LAYERS:
        rows = r[L]
        print(f"\n{L.upper()}")
        for row in rows[:3]:
            print(f"  {json.dumps(row, ensure_ascii=False)}")
        if len(rows) > 3:
            print(f"  ... +{len(rows)-3}")

    # ── symbol atlas ───────────────────────────────────────────────
    symbols = parse_symbols(SYMBOLS_TEXT)
    for s in symbols:
        s["kernel"] = symbol_kernel(s)
    by_book = link_by_reference(symbols)

    out = Path("symbol_atlas")
    out.mkdir(exist_ok=True)
    atlas = {
        "version": "1.0",
        "source": "Scriptural symbolic lexicon",
        "count": len(symbols),
        "symbols": symbols,
        "by_book": by_book,
    }
    (out / "atlas.json").write_text(json.dumps(atlas, indent=2, ensure_ascii=False))

    print()
    print("=" * 60)
    print(f"SYMBOL ATLAS")
    print(f"count: {len(symbols)}")
    print(f"distinct books referenced: {len(by_book)}")
    print("=" * 60)
    print("\nTop books by symbol count:")
    for book, syms in sorted(by_book.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  {book:<10} {len(syms):>3}  e.g. {syms[0]}")
    print(f"\nwrote {out / 'atlas.json'}")

if __name__ == "__main__":
    main()
