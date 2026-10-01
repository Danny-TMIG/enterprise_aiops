#!/usr/bin/env python3
"""Independent re-run and signature verification of a stored evidence record."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "dcs/evidence/qualifications"
KEY_FILE = ROOT / "dcs/key.hex"

def main():
    sys.path.insert(0, str(ROOT))
    from dcs.evidence_chain import PASS, EvidenceChain
    chain = EvidenceChain(str(STORE))
    name = sys.argv[1] if len(sys.argv) > 1 else "evidence_capture.json"
    rec = chain.load_record(name)
    key = KEY_FILE.read_text().strip()
    sig_ok = chain.verify_signature(rec, key)
    print(f"signature_valid: {sig_ok}")
    v = chain.verify(rec)
    vr = v.data.get("verification_result")
    print(f"re_run_result:   {vr}")
    print(f"details:         {v.data.get('verification')}")
    out = STORE / name.replace(".json", ".verification.json")
    out.write_text(v.to_json())
    print(f"written:         {out.relative_to(ROOT)}")
    return 0 if (sig_ok and vr == PASS) else 1

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
