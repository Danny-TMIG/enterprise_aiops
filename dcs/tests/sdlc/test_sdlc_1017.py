"""Auto-generated stub for SDLC-1017 — PCI DSS 4.0: Requirements."""
import json
from pathlib import Path

MANIFEST = Path("dcs/standards/sdlc.json")

def test_sdlc_1017_schema():
    data = json.loads(MANIFEST.read_text())
    proc = next((r for r in data["requirements"] if r["id"] == "SDLC-1017"), None)
    assert proc is not None, "SDLC-1017 missing"
    assert proc["identity"]["body"] in data["derived_from"]
    assert proc["state"] in {"UNKNOWN","TRUE","FALSE","CONFLICT"}
