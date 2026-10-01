"""Pytest mastery showcase: parametrize, fixtures, markers, hooks."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO))

BODIES = [
    "ISO", "IEEE", "NIST", "OWASP", "CMMI", "ITIL", "PMI", "SAFe",
    "TOGAF", "ISACA", "IEC", "ANSI", "BSI", "CENELEC", "RTCA",
    "Automotive", "CERT", "Privacy", "Audit", "US-Gov", "CC",
    "Supply", "Signing", "AI", "Cloud", "FinTech",
]
CATEGORIES = [
    "Requirements", "Design", "Implementation", "Verification",
    "Validation", "Deployment", "Operations", "Maintenance",
    "Configuration", "Quality", "Security", "Governance",
]


@pytest.mark.parametrize("body", BODIES, ids=[b.lower() for b in BODIES])
def test_body_present(sdlc_manifest, body):
    assert body in sdlc_manifest["derived_from"]


@pytest.mark.parametrize("category", CATEGORIES, ids=[c.lower() for c in CATEGORIES])
def test_category_present(sdlc_manifest, category):
    cats = {r["category"] for r in sdlc_manifest["requirements"]}
    assert category in cats


@pytest.fixture(params=["SDLC-0001", "SDLC-0002", "SDLC-0500",
                        "SDLC-1000", "SDLC-1485"])
def sample_id(request):
    return request.param


def test_sample_id_in_manifest(sdlc_manifest, sample_id):
    ids = {r["id"] for r in sdlc_manifest["requirements"]}
    assert sample_id in ids


def test_registry_size(standards_registry):
    assert len(standards_registry) >= 80


def test_registry_no_defaults(standards_registry):
    defaults = [k for k, v in standards_registry.items()
                if v["clauses"][:1] == ["Clause 1"]]
    assert not defaults, f"on default: {defaults}"


def test_engine_processes_all(sdlc_engine):
    ids = sdlc_engine.process_all()
    assert len(ids) == 1485
    assert ids[0] == "SDLC-0001"
    assert ids[-1] == "SDLC-1485"


def test_engine_by_body_roundtrip(sdlc_engine):
    bodies = sdlc_engine.by_body()
    total = sum(len(v) for v in bodies.values())
    assert total == 1485
    assert len(bodies) >= 26


def test_engine_by_category_roundtrip(sdlc_engine):
    cats = sdlc_engine.by_category()
    total = sum(len(v) for v in cats.values())
    assert total == 1485
    assert set(cats.keys()) == set(CATEGORIES)


def test_engine_loads_from_copy(tmp_path, sdlc_manifest):
    from dcs.sdlc_engine import SDLCEngine
    p = tmp_path / "m.json"
    p.write_text(json.dumps(sdlc_manifest))
    assert len(SDLCEngine(p).process_all()) == 1485


@pytest.mark.evidence
def test_evidence_capture_and_verify(evidence_chain, repo_root):
    impl = repo_root / "dcs/evidence_chain.py"
    test = repo_root / "dcs/tests/test_pytest_mastery.py"
    rec = evidence_chain.capture(
        claim="pytest mastery test",
        requirement_ref="pytest-mastery@1.0.0",
        implementation=impl, test=test,
        command='.venv/bin/python -c "print(42)"',
    )
    assert rec.result == "PASS"
    v = evidence_chain.verify(rec)
    assert v.data["verification_result"] == "PASS"


def test_capsys(capsys):
    print("hello")
    assert capsys.readouterr().out == "hello\n"


def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("DCS_TEST_FLAG", "1")
    import os
    assert os.environ["DCS_TEST_FLAG"] == "1"


def test_missing_field_raises(tmp_path):
    from dcs.sdlc_engine import SDLCEngine
    bad = {"schema": "x", "requirements": [{"id": "SDLC-BAD", "state": "UNKNOWN"}]}
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad))
    with pytest.raises(ValueError, match="missing"):
        SDLCEngine(p).validate()


def test_invalid_state_raises(tmp_path):
    from dcs.sdlc_engine import SDLCEngine, REQUIRED_FIELDS
    req = {f: None for f in REQUIRED_FIELDS}
    req["id"] = "SDLC-BAD"
    req["state"] = "BOGUS"
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"schema": "x", "requirements": [req]}))
    with pytest.raises(ValueError, match="invalid state"):
        SDLCEngine(p).validate()


@pytest.mark.xfail(reason="placeholder", strict=True)
def test_future_capability():
    raise NotImplementedError


@pytest.mark.skip(reason="requires external service")
def test_external_service():
    pass


@pytest.mark.slow
def test_slow_marker(sdlc_engine):
    assert sdlc_engine is not None


@pytest.mark.integration
def test_integration_marker(repo_root):
    assert (repo_root / ".venv").exists()


try:
    from hypothesis import given, settings, strategies as st

    @settings(max_examples=50, deadline=None)
    @given(st.text(min_size=1, max_size=20))
    def test_slug_never_empty(text):
        s = "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")
        assert s or not text.strip()

except ImportError:
    pass
