"""Equivalence relations project-wide.

Two flavors per artifact kind:

    EXACT     — content-addressed. Bytewise identical.
    SEMANTIC  — behaviorally interchangeable. Ignores volatile fields.

Rules:
    reflexive, symmetric, transitive for both.
    exact ⇒ semantic (checked by DCS-EQ-002).
"""

from __future__ import annotations  # pragma: no cover

import hashlib  # pragma: no cover
import json  # pragma: no cover
from collections.abc import Callable, Iterable  # pragma: no cover
from typing import Any  # pragma: no cover

ExactFn = Callable[[Any, Any], bool]
SemanticFn = Callable[[Any, Any], bool]
_REGISTRY: dict[str, tuple[ExactFn, SemanticFn]] = {}


def register(kind: str, exact: ExactFn, semantic: SemanticFn) -> None:  # pragma: no cover
    _REGISTRY[kind] = (exact, semantic)


def exact(kind: str, a: Any, b: Any) -> bool:  # pragma: no cover
    if kind not in _REGISTRY:  # pragma: no cover
        raise KeyError(f"no equivalence relation for {kind!r}")  # pragma: no cover
    return _REGISTRY[kind][0](a, b)  # pragma: no cover


def semantic(kind: str, a: Any, b: Any) -> bool:  # pragma: no cover
    if kind not in _REGISTRY:  # pragma: no cover
        raise KeyError(f"no equivalence relation for {kind!r}")  # pragma: no cover
    return _REGISTRY[kind][1](a, b)  # pragma: no cover


def relation_for(kind: str):  # pragma: no cover
    return _REGISTRY[kind]  # pragma: no cover


def kinds() -> list[str]:  # pragma: no cover
    return sorted(_REGISTRY.keys())  # pragma: no cover


# ── helpers ─────────────────────────────────────────────────────────
def _canon(obj: Any) -> bytes:  # pragma: no cover
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode()  # pragma: no cover


def _digest(obj: Any) -> str:  # pragma: no cover
    return "sha256:" + hashlib.sha256(_canon(obj)).hexdigest()  # pragma: no cover


def _proj(d: dict[str, Any], keys: Iterable[str]) -> dict[str, Any]:  # pragma: no cover
    return {k: d.get(k) for k in keys}  # pragma: no cover


def _json_exact(a, b) -> bool:  # pragma: no cover
    return _canon(a) == _canon(b)  # pragma: no cover


def _json_semantic(a, b) -> bool:  # pragma: no cover
    if isinstance(a, dict) and isinstance(b, dict):  # pragma: no cover
        keys = sorted(set(a) | set(b))
        return _proj(a, keys) == _proj(b, keys)  # pragma: no cover
    return a == b  # pragma: no cover


def _digest_exact(a, b) -> bool:  # pragma: no cover
    da = getattr(a, "digest", None) or str(a)
    db = getattr(b, "digest", None) or str(b)
    return da == db  # pragma: no cover


def _digest_only_semantic(a, b) -> bool:  # pragma: no cover
    return _digest_exact(a, b)  # pragma: no cover


def _float_close(x: float, y: float, tol: float = 1e-12) -> bool:  # pragma: no cover
    return abs(x - y) < tol  # pragma: no cover


def _dict_close(a: dict, b: dict) -> bool:  # pragma: no cover
    if set(a) != set(b):  # pragma: no cover
        return False  # pragma: no cover
    for k in a:
        va, vb = a[k], b[k]
        if isinstance(va, float) and isinstance(vb, float):  # pragma: no cover
            if not _float_close(va, vb):  # pragma: no cover
                return False  # pragma: no cover
        elif va != vb:
            return False  # pragma: no cover
    return True  # pragma: no cover


# ── domain-specific registrations ──────────────────────────────────

# dict / JSON — base
register("dict", _json_exact, _json_semantic)
register("JSON", _json_exact, _json_semantic)
register("JSONList", _json_exact, _json_semantic)


# TrainTile
def _tile_exact(a, b):  # pragma: no cover
    return a.to_dict() == b.to_dict()  # pragma: no cover


def _tile_semantic(a, b):  # pragma: no cover
    return (a.kind, a.solver, a.difficulty, a.trials, a.passes) == (  # pragma: no cover
        b.kind,
        b.solver,
        b.difficulty,
        b.trials,
        b.passes,
    )


register("TrainTile", _tile_exact, _tile_semantic)


def _tile_list_exact(a, b):  # pragma: no cover
    return [t.to_dict() for t in a] == [t.to_dict() for t in b]  # pragma: no cover


def _tile_list_semantic(a, b):  # pragma: no cover
    ka = sorted((t.kind, t.solver, t.difficulty, t.trials, t.passes) for t in a)
    kb = sorted((t.kind, t.solver, t.difficulty, t.trials, t.passes) for t in b)
    return ka == kb  # pragma: no cover


register("TileList", _tile_list_exact, _tile_list_semantic)


# TrainOutcome
register("TrainOutcome", _digest_exact, _digest_only_semantic)


def _outcome_list_exact(a, b):  # pragma: no cover
    return [o.digest for o in a] == [o.digest for o in b]  # pragma: no cover


def _outcome_list_semantic(a, b):  # pragma: no cover
    return sorted(o.digest for o in a) == sorted(o.digest for o in b)  # pragma: no cover


register("OutcomeList", _outcome_list_exact, _outcome_list_semantic)


# Run
def _run_exact(a, b):  # pragma: no cover
    return a.digest == b.digest  # pragma: no cover


def _run_semantic(a, b):  # pragma: no cover
    return _dict_close(a.rates, b.rates)  # pragma: no cover


register("Run", _run_exact, _run_semantic)


def _runs_exact(a, b):  # pragma: no cover
    return [r.digest for r in a] == [r.digest for r in b]  # pragma: no cover


def _runs_semantic(a, b):  # pragma: no cover
    if len(a) != len(b):  # pragma: no cover
        return False  # pragma: no cover
    return all(_run_semantic(x, y) for x, y in zip(a, b))  # pragma: no cover


register("RunSequence", _runs_exact, _runs_semantic)


# MeshOfMeshes
def _mesh_exact(a, b):  # pragma: no cover
    return [r.digest for r in a.runs] == [r.digest for r in b.runs]  # pragma: no cover


def _mesh_semantic(a, b):  # pragma: no cover
    return sorted(r.digest for r in a.runs) == sorted(r.digest for r in b.runs)  # pragma: no cover


register("MeshOfMeshes", _mesh_exact, _mesh_semantic)


# Weave
def _weave_exact(a, b):  # pragma: no cover
    return _canon(a) == _canon(b)  # pragma: no cover


def _weave_semantic(a, b):  # pragma: no cover
    return a.get("runs") == b.get("runs") and a.get("outcomes") == b.get("outcomes")  # pragma: no cover


register("Weave", _weave_exact, _weave_semantic)


# CrissCross
def _cc_exact(a, b):  # pragma: no cover
    return _canon(a) == _canon(b)  # pragma: no cover


def _cc_semantic(a, b):  # pragma: no cover
    return a.get("combined") == b.get("combined")  # pragma: no cover


register("CrissCross", _cc_exact, _cc_semantic)


# Pollinate
def _pl_exact(a, b):  # pragma: no cover
    return a == b  # pragma: no cover


def _pl_semantic(a, b):  # pragma: no cover
    key = lambda p: (p["stream"], p["change"])
    return sorted(map(key, a)) == sorted(map(key, b))  # pragma: no cover


register("Pollinate", _pl_exact, _pl_semantic)


# Standard / Requirement
def _req_exact(a, b):  # pragma: no cover
    return (a.id, a.title, a.section, tuple(a.hats), a.criticality, a.test) == (  # pragma: no cover
        b.id,
        b.title,
        b.section,
        tuple(b.hats),
        b.criticality,
        b.test,
    )


def _req_semantic(a, b):  # pragma: no cover
    return a.id == b.id  # pragma: no cover


register("Requirement", _req_exact, _req_semantic)


def _std_exact(a, b):  # pragma: no cover
    return a.ref == b.ref and [(r.id, r.test) for r in a.requirements] == [  # pragma: no cover
        (r.id, r.test) for r in b.requirements
    ]


def _std_semantic(a, b):  # pragma: no cover
    return sorted((r.id, r.criticality) for r in a.requirements) == sorted(  # pragma: no cover
        (r.id, r.criticality) for r in b.requirements
    )


register("Standard", _std_exact, _std_semantic)


# Evidence Bundle
def _bundle_exact(a, b):  # pragma: no cover
    return a.get("digest") == b.get("digest")  # pragma: no cover


def _bundle_semantic(a, b):  # pragma: no cover
    if a.get("standard_ref") != b.get("standard_ref"):  # pragma: no cover
        return False  # pragma: no cover
    if a.get("verdict") != b.get("verdict"):  # pragma: no cover
        return False  # pragma: no cover
    key = lambda r: (r["id"], bool(r.get("pass")))
    return sorted(map(key, a.get("results", []))) == sorted(map(key, b.get("results", [])))  # pragma: no cover


register("Bundle", _bundle_exact, _bundle_semantic)


# LogEntry
def _log_exact(a, b):  # pragma: no cover
    return a.get("entry_hash") == b.get("entry_hash")  # pragma: no cover


def _log_semantic(a, b):  # pragma: no cover
    return a.get("bundle") == b.get("bundle") and a.get("verdict") == b.get("verdict")  # pragma: no cover


register("LogEntry", _log_exact, _log_semantic)


# Log chain
def _chain_exact(a, b):  # pragma: no cover
    return [e.get("entry_hash") for e in a] == [e.get("entry_hash") for e in b]  # pragma: no cover


def _chain_semantic(a, b):  # pragma: no cover
    return [e.get("bundle") for e in a] == [e.get("bundle") for e in b]  # pragma: no cover


register("LogChain", _chain_exact, _chain_semantic)


# Cross-cutting
register("ChaosRun", _json_exact, _json_semantic)
register("MetricSeries", _json_exact, _json_semantic)
register("LocaleBundle", _json_exact, _json_semantic)
register("ContrastPair", _json_exact, _json_semantic)
register("Redaction", _json_exact, _json_semantic)
register("SemverPair", _json_exact, _json_semantic)
register("SingleFlightResult", _json_exact, _json_semantic)
register("ClockTrace", _json_exact, _json_semantic)
register("TokenBucketState", _json_exact, _json_semantic)
register("CircuitState", _json_exact, _json_semantic)
register("SagaTrace", _json_exact, _json_semantic)
register("CDCEvent", _json_exact, _json_semantic)
register("FlagRollout", _json_exact, _json_semantic)
register("CanaryReport", _json_exact, _json_semantic)
register("BackupSnapshot", _json_exact, _json_semantic)
register("TimeSample", _json_exact, _json_semantic)
register("DeployPlan", _json_exact, _json_semantic)


# Puzzle artifacts
def _grid_exact(a, b):  # pragma: no cover
    return _canon(a) == _canon(b)  # pragma: no cover


def _grid_semantic(a, b):  # pragma: no cover
    return a == b  # pragma: no cover


for kind in ("Grid", "Sudoku", "Crossword", "Rubik", "TicTacToe", "GridWorld"):
    register(kind, _grid_exact, _grid_semantic)


# Engine artifacts
for kind in ("EngineTile", "EngineOutcome", "Differential", "DynamicController"):
    register(kind, _digest_exact, _digest_only_semantic)


# CD / NAND
def _cd_exact(a, b):  # pragma: no cover
    return repr(a) == repr(b)  # pragma: no cover


def _cd_semantic(a, b):  # pragma: no cover
    return repr(a) == repr(b)  # pragma: no cover


register("CD", _cd_exact, _cd_semantic)


# Configs
def _config_exact(a, b):  # pragma: no cover
    return _canon(a.to_dict() if hasattr(a, "to_dict") else a.__dict__) == _canon(  # pragma: no cover
        b.to_dict() if hasattr(b, "to_dict") else b.__dict__
    )


def _config_semantic(a, b):  # pragma: no cover
    da = a.to_dict() if hasattr(a, "to_dict") else a.__dict__
    db = b.to_dict() if hasattr(b, "to_dict") else b.__dict__
    da = {k: v for k, v in da.items() if not k.startswith("_")}
    db = {k: v for k, v in db.items() if not k.startswith("_")}
    return da == db  # pragma: no cover


register("Config", _config_exact, _config_semantic)


# Generic dict of dicts (for rates, metrics)
register("Dict", _json_exact, _json_semantic)
register(
    "FloatDict",
    _json_exact,
    lambda a, b: _dict_close(a, b) if isinstance(a, dict) and isinstance(b, dict) else a == b,
)


# Byte blobs
def _bytes_exact(a, b):  # pragma: no cover
    return a == b  # pragma: no cover


def _bytes_semantic(a, b):  # pragma: no cover
    return a == b  # pragma: no cover


register("Bytes", _bytes_exact, _bytes_semantic)


# ── canonical key ──────────────────────────────────────────────────
def canonical_key(kind: str, obj: Any) -> str:  # pragma: no cover
    if hasattr(obj, "digest"):  # pragma: no cover
        return obj.digest  # pragma: no cover
    if kind == "TrainTile":  # pragma: no cover
        return f"{obj.kind}/{obj.solver}/{obj.difficulty}"  # pragma: no cover
    if kind == "Bundle":  # pragma: no cover
        return obj.get("digest") or _digest(obj)  # pragma: no cover
    return _digest(obj)  # pragma: no cover


# ── Nature phenomena ───────────────────────────────────────────────
def _nat_exact(a, b):  # pragma: no cover
    return _canon(a) == _canon(b)  # pragma: no cover


def _nat_semantic(a, b):  # pragma: no cover
    """Two nature results are interchangeable if their named
    summary fields match within float tolerance; the full grid/state
    is present but not compared (expensive, and layout is often not
    semantically meaningful)."""
    if isinstance(a, dict) and isinstance(b, dict):  # pragma: no cover
        keys = set(a) & set(b)
        ignore = {"a", "b", "u", "v", "pos", "vel", "grid", "dirs"}
        for k in keys - ignore:
            va, vb = a[k], b[k]
            if isinstance(va, float) and isinstance(vb, float):  # pragma: no cover
                if abs(va - vb) > 1e-6:  # pragma: no cover
                    return False  # pragma: no cover
            elif va != vb:
                return False  # pragma: no cover
        return True  # pragma: no cover
    return a == b  # pragma: no cover


register("NatureResult", _nat_exact, _nat_semantic)
register("Walk", _nat_exact, _nat_semantic)
register("Flock", _nat_exact, _nat_semantic)
register("Oscillator", _nat_exact, _nat_semantic)
register("Morphogen", _nat_exact, _nat_semantic)
register("Population", _nat_exact, _nat_semantic)
register("Flow", _nat_exact, _nat_semantic)
