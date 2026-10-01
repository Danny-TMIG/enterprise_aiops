#!/usr/bin/env python3
"""Operations on dendritic_seeds/: query, traverse, reconfig, solve."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path("dendritic_seeds")

BELNAP = {
    "UNKNOWN":  {"PASS", "FAIL"},
    "PASS":     {"CONFLICT"},
    "FAIL":     {"CONFLICT"},
    "CONFLICT": {"UNKNOWN"},
}

OPS = ["move", "relink", "reclue", "rotate", "swap"]


def load():
    seeds = json.loads((ROOT / "seeds.json").read_text())
    anchors = json.loads((ROOT / "crossword_anchors.json").read_text())
    grid = json.loads((ROOT / "grid.json").read_text())
    by_id = {s["id"]: s for s in seeds}
    return seeds, anchors, grid, by_id


def step(state, op="advance"):
    nxt = BELNAP.get(state, set())
    if not nxt:
        return state
    return sorted(nxt)[0]


def cmd_ls(args):
    seeds, _, _, _ = load()
    for s in seeds:
        if args.depth is not None and s["depth"] != args.depth:
            continue
        print(f'{s["id"]:<70} {s["label"]}')
        if args.limit and args.limit == 0:
            break


def cmd_show(args):
    _, _, _, by_id = load()
    s = by_id.get(args.id)
    if not s:
        print(f'not found: {args.id}', file=sys.stderr)
        sys.exit(1)
    print(json.dumps(s, indent=2))


def cmd_walk(args):
    _, _, _, by_id = load()
    start = by_id.get(args.id)
    if not start:
        print(f'not found: {args.id}', file=sys.stderr)
        sys.exit(1)
    seen = {start["id"]}
    queue = [(start, 0)]
    while queue:
        node, depth = queue.pop(0)
        indent = "  " * depth
        print(f'{indent}{node["label"]}  [{node["id"]}]')
        for edge in node["dendrite"]["terminals"]:
            nxt = by_id.get(edge["to"])
            if not nxt or nxt["id"] in seen:
                continue
            seen.add(nxt["id"])
            queue.append((nxt, depth + 1))


def cmd_letters(args):
    seeds, anchors, _, _ = load()
    ids = anchors["by_letter"].get(args.letter.upper(), [])
    by_id = {s["id"]: s for s in seeds}
    for sid in ids[: args.limit]:
        s = by_id[sid]
        print(f'{s["crossword"]["word"]:<20} {s["id"]}')


def cmd_reconfig(args):
    seeds, _, _, by_id = load()
    s = by_id.get(args.id)
    if not s:
        print(f'not found: {args.id}', file=sys.stderr)
        sys.exit(1)
    op = args.op
    before = dict(s["config"])
    if op == "move":
        if args.arg:
            r, c = args.arg.split(",")
            s["config"]["position"] = [int(r), int(c)]
    elif op == "relink":
        s["lambda"]["parent"] = args.arg or s["lambda"]["parent"]
    elif op == "reclue":
        s["crossword"]["clue"] = args.arg or s["crossword"]["clue"]
    elif op == "rotate":
        s["config"]["orientation"] = (
            "down" if s["config"].get("orientation") == "across" else "across"
        )
    elif op == "swap":
        other = by_id.get(args.arg)
        if not other:
            print(f'swap target not found: {args.arg}', file=sys.stderr)
            sys.exit(1)
        s["config"]["state"], other["config"]["state"] = (
            other["config"]["state"],
            s["config"]["state"],
        )
    else:
        print(f'unknown op: {op}', file=sys.stderr)
        sys.exit(1)
    s["config"]["state"] = step(s["config"]["state"])
    (ROOT / "seeds.json").write_text(json.dumps(seeds, indent=2))
    print(f'{op}: {before} -> {s["config"]}')


def cmd_solve(args):
    seeds, anchors, grid, by_id = load()
    placed = {e["id"] for e in grid["entries"]}
    printed = 0
    for entry in grid["entries"]:
        if printed >= args.limit:
            break
        w = entry["word"]
        length = len(w)
        candidates = anchors["by_length"].get(str(length)) or anchors["by_length"].get(length) or []
        scored = []
        for cid in candidates:
            s = by_id[cid]
            cw = s["crossword"]["word"]
            overlap = sum(1 for a, b in zip(w, cw) if a == b)
            if overlap > 0:
                scored.append((overlap, cw, cid))
        scored.sort(reverse=True)
        print(f'placed: {w}  (len {length}, at {entry["row"]},{entry["col"]} {entry["orientation"]})')
        for overlap, cw, cid in scored[:3]:
            print(f'   alt: {cw}  overlap={overlap}  {cid}')
        printed += 1


def main():
    p = argparse.ArgumentParser(prog="dendritic_ops")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ls");          s.add_argument("--depth", type=int); s.add_argument("--limit", type=int, default=50); s.set_defaults(fn=cmd_ls)
    s = sub.add_parser("show");        s.add_argument("id");               s.set_defaults(fn=cmd_show)
    s = sub.add_parser("walk");        s.add_argument("id");               s.set_defaults(fn=cmd_walk)
    s = sub.add_parser("letters");     s.add_argument("letter");           s.add_argument("--limit", type=int, default=20); s.set_defaults(fn=cmd_letters)
    s = sub.add_parser("reconfig");    s.add_argument("id"); s.add_argument("op", choices=OPS); s.add_argument("arg", nargs="?"); s.set_defaults(fn=cmd_reconfig)
    s = sub.add_parser("solve");       s.add_argument("--limit", type=int, default=10); s.set_defaults(fn=cmd_solve)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
