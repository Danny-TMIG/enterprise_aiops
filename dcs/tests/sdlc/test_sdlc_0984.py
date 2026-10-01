"""Auto-generated stub for SDLC-0984 — NIST CSF 2.0: Requirements."""
import json
from pathlib import Path

MANIFEST = Path("dcs/standards/sdlc.json")

def test_sdlc_0984_schema():
    data = json.loads(MANIFEST.read_text())
    proc = next((r for r in data["requirements"] if r["id"] == "SDLC-0984"), None)
    assert proc is not None, "SDLC-0984 missing"
    assert proc["identity"]["body"] in data["derived_from"]
    assert proc["state"] in {"UNKNOWN","TRUE","FALSE","CONFLICT"}
