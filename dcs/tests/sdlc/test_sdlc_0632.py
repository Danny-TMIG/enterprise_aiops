"""Auto-generated stub for SDLC-0632 — ISO/IEC 42001: Maintenance."""
import json
from pathlib import Path

MANIFEST = Path("dcs/standards/sdlc.json")

def test_sdlc_0632_schema():
    data = json.loads(MANIFEST.read_text())
    proc = next((r for r in data["requirements"] if r["id"] == "SDLC-0632"), None)
    assert proc is not None, "SDLC-0632 missing"
    assert proc["identity"]["body"] in data["derived_from"]
    assert proc["state"] in {"UNKNOWN","TRUE","FALSE","CONFLICT"}
