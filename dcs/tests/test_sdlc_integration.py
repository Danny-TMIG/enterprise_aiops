"""Integration test: sdlc.json is attached to the DCS self-fold."""
import json
import tempfile
from pathlib import Path

import pytest

from dcs.sdlc_engine import BELNAP_STATES, REQUIRED_FIELDS, SDLCEngine
from dcs.self import MANIFESTS


def _sdlc_path():
    return next(p for p in MANIFESTS if p.name == "sdlc.json")


def test_sdlc_in_manifests():
    assert any(p.name == "sdlc.json" for p in MANIFESTS)


def test_sdlc_loads():
    engine = SDLCEngine(_sdlc_path())
    data = engine.load()
    assert data["schema"] == "dcs.sdlc.v2"
    assert len(data["requirements"]) > 0


def test_sdlc_validate_before_load():
    engine = SDLCEngine(_sdlc_path())
    assert engine.data is None
    assert engine.validate() is True
    assert engine.data is not None


def test_sdlc_process_all_fresh():
    engine = SDLCEngine(_sdlc_path())
    ids = engine.process_all()
    assert len(ids) > 0
    assert ids[0].startswith("SDLC-")


def test_sdlc_process_all_already_loaded():
    engine = SDLCEngine(_sdlc_path())
    engine.load()
    ids = engine.process_all()
    assert len(ids) > 0


def test_sdlc_by_body():
    engine = SDLCEngine(_sdlc_path())
    bodies = engine.by_body()
    assert "ISO" in bodies
    assert "IEEE" in bodies
    assert "NIST" in bodies
    assert "OWASP" in bodies
    assert len(bodies) > 20


def test_sdlc_by_category():
    engine = SDLCEngine(_sdlc_path())
    cats = engine.by_category()
    for c in ["Requirements", "Design", "Implementation", "Verification"]:
        assert c in cats


def test_sdlc_by_body_empty():
    """Cover the branch where requirements list is empty."""
    bad = {"schema": "x", "requirements": []}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(bad, f)
        p = Path(f.name)
    try:
        engine = SDLCEngine(p)
        engine.load()
        assert engine.by_body() == {}
        assert engine.by_category() == {}
    finally:
        p.unlink()


def test_sdlc_missing_field_raises():
    bad = {"schema": "x", "requirements": [{"id": "SDLC-BAD", "state": "UNKNOWN"}]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(bad, f)
        p = Path(f.name)
    try:
        with pytest.raises(ValueError, match="missing"):
            SDLCEngine(p).validate()
    finally:
        p.unlink()


def test_sdlc_invalid_state_raises():
    req = {f: None for f in REQUIRED_FIELDS}
    req["id"] = "SDLC-BAD"
    req["state"] = "BOGUS"
    bad = {"schema": "x", "requirements": [req]}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(bad, f)
        p = Path(f.name)
    try:
        with pytest.raises(ValueError, match="invalid state"):
            SDLCEngine(p).validate()
    finally:
        p.unlink()


def test_all_manifests_load():
    for path in MANIFESTS:
        if path.exists():
            assert isinstance(json.loads(path.read_text()), dict)


def test_belnap_states_defined():
    assert BELNAP_STATES == {"UNKNOWN", "TRUE", "FALSE", "CONFLICT"}
