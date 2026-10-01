"""Integration test: sdlc.json is attached to the DCS self-fold."""
import json
from pathlib import Path
from dcs.self import MANIFESTS
from dcs.sdlc_engine import SDLCEngine


def test_sdlc_in_manifests():
    assert any(p.name == "sdlc.json" for p in MANIFESTS), "sdlc.json missing from MANIFESTS"


def test_sdlc_engine_processes_all():
    sdlc_path = next(p for p in MANIFESTS if p.name == "sdlc.json")
    engine = SDLCEngine(sdlc_path)
    ids = engine.process_all()
    assert len(ids) == 1485
    assert ids[0] == "SDLC-0001"


def test_all_manifests_load():
    for path in MANIFESTS:
        if path.exists():
            data = json.loads(path.read_text())
            assert isinstance(data, dict)
