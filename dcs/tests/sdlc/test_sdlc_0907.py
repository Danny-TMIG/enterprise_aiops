"""Auto-generated stub for SDLC-0907 — OWASP ASVS 4.0: Governance."""
import json
from pathlib import Path

MANIFEST = Path("dcs/standards/sdlc.json")

def test_sdlc_0907_schema():
    data = json.loads(MANIFEST.read_text())
    proc = next((r for r in data["requirements"] if r["id"] == "SDLC-0907"), None)
    assert proc is not None, "SDLC-0907 missing"
    assert proc["identity"]["body"] in data["derived_from"]
    assert proc["state"] in {"UNKNOWN","TRUE","FALSE","CONFLICT"}
