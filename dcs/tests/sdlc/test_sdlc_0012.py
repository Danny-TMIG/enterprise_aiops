"""Auto-generated stub for SDLC-0012 — IEEE 830: Requirements."""
import json
from pathlib import Path

MANIFEST = Path("dcs/standards/sdlc.json")

def test_sdlc_0012_schema():
    data = json.loads(MANIFEST.read_text())
    proc = next((r for r in data["requirements"] if r["id"] == "SDLC-0012"), None)
    assert proc is not None, "SDLC-0012 missing"
    assert proc["identity"]["body"] in data["derived_from"]
    assert proc["state"] in {"UNKNOWN","TRUE","FALSE","CONFLICT"}
