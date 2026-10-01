# enterprise_aiops

`~/enterprise_aiops` is a Python repository that records claims about software
development lifecycle compliance as signed evidence and re-executes the
underlying test before treating any claim as verified. The repository contains
the `dcs` package, a manifest of 1,485 SDLC processes derived from 80 standards
published by 26 standards bodies (ISO, IEEE, NIST, OWASP, CMMI, ITIL, GDPR,
FedRAMP, PCI DSS, EU AI Act, and others), a standards registry that assigns
each process a clause and control family from its source standard, an evidence
chain that hashes the implementation file, the test file, and the command
output, signs the record with HMAC-SHA256, and stores the record on disk, and a
verification program that re-runs the recorded command and confirms that the
implementation hash, test hash, stdout hash, and return code all match the
stored record. The purpose of the repository is to make the boundary between a
stated claim and a supported claim machine-checkable: a record receives the
result `PASS` only when an independent re-run reproduces the same hashes, and
any divergence downgrades the record to `PARTIAL` or `BLOCKED`.

## Layout

- `dcs/evidence_chain.py` — capture, sign, store, verify a single claim
- `dcs/qualify_evidence.py` — run a qualification profile and write a signed record
- `dcs/verify_evidence.py` — re-execute a stored record and compare hashes
- `dcs/sdlc_engine.py` — load the SDLC manifest and iterate processes
- `dcs/standards/sdlc.json` — 1,485 SDLC processes
- `dcs/standards/registry.json` — 80 standards, each with clauses, controls, evidence
- `dcs/tests/` — pytest suite with strict markers, warnings-as-errors, 100% coverage on tracked files
- `governance/` — SBOM, SLSA provenance, compliance matrix, threat model, license audit, formal invariants
- `pytest.ini`, `conftest.py` — strict test configuration

## Qualify and verify

```
.venv/bin/python dcs/qualify_evidence.py
.venv/bin/python dcs/verify_evidence.py
```

## What the repository is not

The repository does not certify compliance with any standard. The repository
does not replace an accredited assessor, penetration test, or legal review.
The records the repository produces describe software behavior that can be
reproduced by an independent run. Conformance claims against FedRAMP, PCI DSS,
HIPAA, SOC 2, and similar programs require an authorized assessor and are not
produced by this repository.
