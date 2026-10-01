"""Integration test: sdlc.json is attached to the DCS self-fold."""
import json
from dcs.self import MANIFESTS


def test_sdlc_in_manifests():
    assert any(p.name == "sdlc.json" for p in MANIFESTS), "sdlc.json missing from MANIFESTS"


def test_sdlc_loads():
    sdlc_path = next(p for p in MANIFESTS if p.name == "sdlc.json")
    assert sdlc_path.exists(), f"sdlc.json not found at {sdlc_path}"
    data = json.loads(sdlc_path.read_text())
    assert len(data["requirements"]) == 1485
    assert data["requirements"][0]["id"] == "SDLC-0001"


def test_all_manifests_load():
    for path in MANIFESTS:
        if path.exists():
            data = json.loads(path.read_text())
            assert isinstance(data, dict)
