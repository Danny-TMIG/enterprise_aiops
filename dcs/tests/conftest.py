"""Domain fixtures for DCS tests."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
DCS = HERE.parent
REPO = DCS.parent
sys.path.insert(0, str(REPO))


@pytest.fixture(scope="session")
def sdlc_manifest():
    return json.loads((DCS / "standards/sdlc.json").read_text())


@pytest.fixture(scope="session")
def standards_registry():
    return json.loads((DCS / "standards/registry.json").read_text())["registry"]


@pytest.fixture(scope="session")
def sdlc_engine():
    from dcs.sdlc_engine import SDLCEngine
    return SDLCEngine(DCS / "standards/sdlc.json")


@pytest.fixture
def evidence_chain(tmp_path):
    from dcs.evidence_chain import EvidenceChain
    return EvidenceChain(tmp_path / "evidence")
