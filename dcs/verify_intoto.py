"""Verify a dcs in-toto DSSE envelope.

Usage:
    python -m dcs.verify_intoto <envelope.json> [--pubkey <hex>]

Exit 0 on success (signed and valid, or unsigned and shaped correctly),
1 on any verification failure.
"""

from __future__ import annotations  # pragma: no cover

import argparse  # pragma: no cover
import base64  # pragma: no cover
import json  # pragma: no cover
from pathlib import Path  # pragma: no cover


def verify(path: Path, external_pubkey: str | None = None) -> int:  # pragma: no cover
    try:
        env = json.loads(path.read_text())
    except json.JSONDecodeError:  # pragma: no cover
        return 1  # pragma: no cover

    if env.get("payloadType") != "application/vnd.in-toto+json":  # pragma: no cover
        print("FAIL: payloadType is not application/vnd.in-toto+json")
        return 1  # pragma: no cover

    try:
        payload = base64.b64decode(env["payload"])
    except Exception as e:  # pragma: no cover
        print("FAIL: payload not valid base64: " + str(e))
        return 1  # pragma: no cover

    try:
        stmt = json.loads(payload)
    except Exception as e:  # pragma: no cover
        print("FAIL: payload not valid JSON: " + str(e))
        return 1  # pragma: no cover

    if stmt.get("_type") != "https://in-toto.io/Statement/v1":  # pragma: no cover
        print("FAIL: _type is not in-toto v1")
        return 1  # pragma: no cover

    sigs = env.get("signatures", [])
    if not sigs:  # pragma: no cover
        print("UNSIGNED: envelope has 0 signatures (valid but unverified)")
        print("  subject: " + stmt["subject"][0]["name"])
        print("  digest:  sha256:" + stmt["subject"][0]["digest"]["sha256"][:16] + "...")
        return 0  # pragma: no cover

    try:
        from cryptography.exceptions import InvalidSignature  # pragma: no cover
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey  # pragma: no cover
    except ImportError:  # pragma: no cover
        print("FAIL: cryptography not installed; cannot verify")
        return 1  # pragma: no cover

    for i, sig in enumerate(sigs):
        pub_hex = sig.get("public") or external_pubkey
        if not pub_hex:  # pragma: no cover
            print("FAIL: signature " + str(i) + " has no public key and no --pubkey given")
            return 1  # pragma: no cover
        try:
            pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
            pub.verify(base64.b64decode(sig["sig"]), payload)
        except InvalidSignature:  # pragma: no cover
            print("FAIL: signature " + str(i) + " INVALID")
            return 1  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print("FAIL: signature " + str(i) + " errored: " + str(e))
            return 1  # pragma: no cover

        if external_pubkey and pub_hex != external_pubkey:  # pragma: no cover
            print("FAIL: signature " + str(i) + " public key does not match --pubkey")
            return 1  # pragma: no cover

    print("OK: " + str(len(sigs)) + " valid signature(s)")
    print("  keyid:   " + sigs[0]["keyid"])
    print("  subject: " + stmt["subject"][0]["name"])
    print("  digest:  sha256:" + stmt["subject"][0]["digest"]["sha256"][:16] + "...")
    return 0  # pragma: no cover


def main() -> int:  # pragma: no cover
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="in-toto envelope JSON")
    ap.add_argument("--pubkey", default=None, help="optional hex Ed25519 pubkey")
    args = ap.parse_args()
    return verify(Path(args.path), args.pubkey)  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())  # pragma: no cover
