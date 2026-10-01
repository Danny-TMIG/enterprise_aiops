#!/usr/bin/env python3
"""Run the qualification profile for evidence_capture and produce a signed record."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "governance/qualification/profiles/evidence_capture.json"
STORE = ROOT / "dcs/evidence/qualifications"
KEY_FILE = ROOT / "dcs/key.hex"

def load_key():
    if KEY_FILE.exists() and len(KEY_FILE.read_text().strip()) == 64:
        return KEY_FILE.read_text().strip()
    import secrets
    k = secrets.token_hex(32)
    KEY_FILE.write_text(k)
    return k

def main():
    sys.path.insert(0, str(ROOT))
    from dcs.evidence_chain import PASS, EvidenceChain
    profile = json.loads(PROFILE.read_text())
    impl = ROOT / profile["implementation"]
    test = ROOT / profile["test"]
    print(f"profile: {profile['id']} v{profile['version']}")
    print(f"claim:   {profile['claim']}")
    r = subprocess.run(
        [".venv/bin/pytest", str(test), "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=str(ROOT), capture_output=True, text=True)
    print(f"tests:   rc={r.returncode}")
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-2000:]); return 1
    chain = EvidenceChain(str(STORE))
    command = (
        ".venv/bin/python -c \"from dcs.sdlc_engine import SDLCEngine; "
        "e=SDLCEngine('dcs/standards/sdlc.json'); ids=e.process_all(); "
        "assert len(ids)==1485; print('OK', len(ids))\""
    )
    rec = chain.capture(
        claim=profile["claim"],
        requirement_ref=f"{profile['id']}@{profile['version']}",
        implementation=impl, test=test, command=command)
    if rec.result != PASS:
        print(f"capture: {rec.result}"); return 1
    key = load_key()
    chain.sign(rec, key)
    p = chain.store_record(rec, f"{profile['id']}.json")
    print(f"record:  {p.relative_to(ROOT)}")
    print(f"id:      {rec.id}")
    print(f"result:  {rec.result}")
    print(f"sha256:  {rec.data['implementation']['sha256'][:16]} (impl)")
    print(f"sig:     {rec.data['signature'][:16]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
