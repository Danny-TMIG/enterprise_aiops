#!/usr/bin/env python3
"""Generative basis: 4 operators, 2 pairs, 64 codons, edit ops, projections."""
import itertools, json, random
from dataclasses import dataclass, field

# ─── bases ──────────────────────────────────────────────────────────
BASES = ("Δ", "Π", "Λ", "τ")
COMPLEMENT = {"Δ": "Π", "Π": "Δ", "Λ": "τ", "τ": "Λ"}

BASE_MEANING = {
    "Δ": "distinction",
    "Π": "persistence",
    "Λ": "linkage",
    "τ": "transformation",
}

# ─── codon table ────────────────────────────────────────────────────
# 64 codons, each = composition of three primitive ops.
# The meaning is a triple of (what, on-what, into-what).
CODONS = [a + b + c for a in BASES for b in BASES for c in BASES]
CODON_INDEX = {c: i for i, c in enumerate(CODONS)}

# Each codon is a small function spec: (operation, target, mode)
OP_VERB = {
    "Δ": "distinguish",
    "Π": "preserve",
    "Λ": "link",
    "τ": "transform",
}
TARGET = {
    "Δ": "unit",
    "Π": "state",
    "Λ": "pair",
    "τ": "process",
}
MODE = {
    "Δ": "local",
    "Π": "temporal",
    "Λ": "structural",
    "τ": "behavioral",
}


def codon_meaning(c):
    return {
        "verb": OP_VERB[c[0]],
        "target": TARGET[c[1]],
        "mode": MODE[c[2]],
        "code": c,
    }


# ─── sequence ───────────────────────────────────────────────────────
@dataclass
class Sequence:
    bases: str = ""
    edits: list = field(default_factory=list)

    def codons(self):
        # read in frame 0
        return [self.bases[i:i+3] for i in range(0, len(self.bases) - 2, 3)]

    def programs(self):
        return [codon_meaning(c) for c in self.codons()]

    def __repr__(self):
        return f"<Seq {self.bases!r} len={len(self.bases)} codons={len(self.codons())}>"


# ─── CRISPR-style operators ─────────────────────────────────────────
def cut(seq: Sequence, i: int, j: int) -> Sequence:
    """Remove bases [i, j)."""
    new = Sequence(seq.bases[:i] + seq.bases[j:], seq.edits + [("cut", i, j)])
    return new


def insert(seq: Sequence, i: int, bases: str) -> Sequence:
    """Insert bases at position i."""
    return Sequence(seq.bases[:i] + bases + seq.bases[i:],
                    seq.edits + [("insert", i, bases)])


def delete(seq: Sequence, i: int, length: int) -> Sequence:
    """Delete length bases starting at i."""
    return cut(seq, i, i + length)


def replace(seq: Sequence, i: int, length: int, bases: str) -> Sequence:
    """Replace length bases at i with new bases."""
    return Sequence(seq.bases[:i] + bases + seq.bases[i+length:],
                    seq.edits + [("replace", i, length, bases)])


def invert(seq: Sequence, i: int, j: int) -> Sequence:
    """Reverse the segment [i, j)."""
    seg = seq.bases[i:j][::-1]
    return Sequence(seq.bases[:i] + seg + seq.bases[j:],
                    seq.edits + [("invert", i, j)])


def duplicate(seq: Sequence, i: int, j: int) -> Sequence:
    """Duplicate segment [i, j) immediately after itself."""
    seg = seq.bases[i:j]
    return Sequence(seq.bases[:j] + seg + seq.bases[j:],
                    seq.edits + [("duplicate", i, j)])


def transpose(seq: Sequence, i: int, j: int, k: int) -> Sequence:
    """Swap segments [i,j) and [j,k)."""
    a, b, c = seq.bases[:i], seq.bases[i:j], seq.bases[j:k]
    rest = seq.bases[k:]
    return Sequence(a + c + b + rest,
                    seq.edits + [("transpose", i, j, k)])


EDIT_OPS = {
    "cut": cut, "insert": insert, "delete": delete,
    "replace": replace, "invert": invert,
    "duplicate": duplicate, "transpose": transpose,
}


# ─── domain interpreters (projections) ──────────────────────────────
def interp_graph(prog):
    """Interpret a program list as a directed graph spec."""
    nodes, edges = set(), set()
    current = "root"
    nodes.add(current)
    for step in prog:
        verb = step["verb"]; target = step["target"]
        if verb == "distinguish":
            new = f"{current}/{target}"
            nodes.add(new); edges.add((current, new)); current = new
        elif verb == "link":
            other = f"{current}~{target}"
            nodes.add(other); edges.add((current, other))
        elif verb == "transform":
            current = f"{current}>τ"
            nodes.add(current)
        elif verb == "preserve":
            edges.add((current, current))
    return {"kind": "graph", "nodes": sorted(nodes),
            "edges": sorted([list(e) for e in edges])}


def interp_state(prog):
    """Interpret a program list as a state machine."""
    states, trans = ["s0"], []
    cur = "s0"; n = 0
    for step in prog:
        n += 1
        nxt = f"s{n}"
        states.append(nxt)
        trans.append({"from": cur, "to": nxt, "on": step["verb"]})
        cur = nxt
    return {"kind": "state_machine", "states": states, "transitions": trans}


def interp_set(prog):
    """Interpret a program list as a set construction."""
    s = set()
    for step in prog:
        s.add((step["verb"], step["target"], step["mode"]))
    return {"kind": "set", "elements": sorted(list(s))}


def interp_text(prog):
    """Interpret a program list as a natural-language action sequence."""
    parts = []
    for step in prog:
        parts.append(f"{step['verb']} the {step['target']} in {step['mode']} mode")
    return {"kind": "text", "text": "; ".join(parts)}


def interp_lambda(prog):
    """Interpret a program list as a composition of pure functions."""
    fn = "x"
    for step in prog:
        v = step["verb"][0]
        fn = f"{v}({fn})"
    return {"kind": "lambda", "expression": f"λx.{fn}"}


INTERPRETERS = {
    "graph": interp_graph,
    "state": interp_state,
    "set": interp_set,
    "text": interp_text,
    "lambda": interp_lambda,
}


def project(seq: Sequence, domain: str):
    if domain not in INTERPRETERS:
        raise ValueError(f"unknown domain: {domain}")
    return INTERPRETERS[domain](seq.programs())


# ─── pairing / double strand ────────────────────────────────────────
def complement_strand(seq: Sequence) -> Sequence:
    return Sequence("".join(COMPLEMENT[b] for b in seq.bases))


def is_viable(seq: Sequence) -> bool:
    """A sequence is viable iff its length is a multiple of 3 and every codon
    resolves to a real operation (all do, since every triple is a codon)."""
    return len(seq.bases) % 3 == 0


# ─── random generation ──────────────────────────────────────────────
def random_sequence(n_codons: int) -> Sequence:
    return Sequence("".join(random.choice(BASES) for _ in range(n_codons * 3)))


# ─── CLI ────────────────────────────────────────────────────────────
def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "codons":
        print(f"{len(CODONS)} codons")
        for c in CODONS[:12]:
            m = codon_meaning(c)
            print(f"  {c}  {m['verb']:<12} {m['target']:<8} {m['mode']}")
        print("  ...")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        s = Sequence("ΔΠΛτΛΠΔΔΠτ")
        print(s)
        print("codons:", s.codons())
        for domain in INTERPRETERS:
            print(f"\n── {domain} ──")
            print(json.dumps(project(s, domain), indent=2)[:400])
        print("\ncomplement:", complement_strand(s))
        return

    # default: random sequence, all projections
    random.seed(0)
    s = random_sequence(4)
    print(f"random sequence: {s.bases}  ({len(s.codons())} codons)")
    for domain in INTERPRETERS:
        r = project(s, domain)
        print(f"\n── {domain} ──")
        print(json.dumps(r, indent=2)[:300])


if __name__ == "__main__":
    main()
