"""Evidence chain: capture, store, sign, verify."""
import hashlib
import hmac
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PASS = "PASS"
FAIL = "FAIL"
PARTIAL = "PARTIAL"
BLOCKED = "BLOCKED"
NOT_RUN = "NOT_RUN"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _file_sha(p):
    return _sha(Path(p).read_bytes())


def _now():
    return datetime.now(timezone.utc).isoformat()


class EvidenceRecord:
    def __init__(self, **kw):
        self.data = kw

    def to_json(self):
        return json.dumps(self.data, sort_keys=True, indent=2)

    @classmethod
    def from_json(cls, s):
        return cls(**json.loads(s))

    @property
    def id(self):
        return self.data.get("id")

    @property
    def result(self):
        return self.data.get("result")


class EvidenceChain:
    def __init__(self, store_dir):
        self.store = Path(store_dir)
        self.store.mkdir(parents=True, exist_ok=True)

    def capture(self, claim, requirement_ref, implementation, test, command, timeout=60):
        rec = {
            "schema": "dcs.evidence.v1",
            "claim": claim,
            "requirement_ref": requirement_ref,
            "implementation": {"path": str(implementation), "sha256": _file_sha(implementation)},
            "test": {"path": str(test), "sha256": _file_sha(test)},
            "command": command,
            "started_at": _now(),
            "environment": {"python": sys.version.split()[0], "platform": sys.platform, "cwd": os.getcwd()},
            "observation": None,
            "result": NOT_RUN,
            "signature": None,
        }
        try:
            r = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout)
            rec["observation"] = {
                "returncode": r.returncode,
                "stdout": r.stdout[-4000:],
                "stderr": r.stderr[-4000:],
                "stdout_sha256": _sha(r.stdout.encode()),
                "stderr_sha256": _sha(r.stderr.encode()),
            }
            rec["result"] = PASS if r.returncode == 0 else FAIL
        except subprocess.TimeoutExpired:
            rec["observation"] = {"returncode": None, "note": "timeout"}
            rec["result"] = BLOCKED
        rec["completed_at"] = _now()
        key = json.dumps({k: rec[k] for k in ["claim", "requirement_ref", "command", "started_at"]}, sort_keys=True).encode()
        rec["id"] = _sha(key)[:16]
        return EvidenceRecord(**rec)

    def verify(self, record, timeout=60):
        rec = record.data
        impl_match = _file_sha(rec["implementation"]["path"]) == rec["implementation"]["sha256"]
        test_match = _file_sha(rec["test"]["path"]) == rec["test"]["sha256"]
        obs = rec.get("observation") or {}
        if "stdout_sha256" not in obs:
            return EvidenceRecord(**{**rec, "verification": {"note": "no comparable observation"},
                                     "verified_at": _now(), "verification_result": PARTIAL})
        try:
            r = subprocess.run(rec["command"], shell=True, capture_output=True, text=True, timeout=timeout)
            stdout_match = _sha(r.stdout.encode()) == obs["stdout_sha256"]
            stderr_match = _sha(r.stderr.encode()) == obs["stderr_sha256"]
            rc_match = r.returncode == obs["returncode"]
        except subprocess.TimeoutExpired:  # pragma: no cover
            return EvidenceRecord(**{**rec, "verification_result": BLOCKED, "verified_at": _now()})
        all_match = impl_match and test_match and stdout_match and rc_match
        return EvidenceRecord(**{**rec,
            "verification": {"impl": impl_match, "test": test_match, "stdout": stdout_match,
                             "stderr": stderr_match, "rc": rc_match},
            "verified_at": _now(),
            "verification_result": PASS if all_match else PARTIAL,
        })

    def _canonical(self, record):
        return json.dumps({k: v for k, v in record.data.items() if k != "signature"}, sort_keys=True).encode()

    def sign(self, record, key_hex):
        record.data["signature"] = hmac.new(bytes.fromhex(key_hex), self._canonical(record), hashlib.sha256).hexdigest()
        return record

    def verify_signature(self, record, key_hex):
        stored = record.data.get("signature")
        expect = hmac.new(bytes.fromhex(key_hex), self._canonical(record), hashlib.sha256).hexdigest()
        return stored == expect

    def store_record(self, record, name=None):
        p = self.store / (name or f"{record.id}.json")
        p.write_text(record.to_json())
        return p

    def load_record(self, name):
        return EvidenceRecord.from_json((self.store / name).read_text())
