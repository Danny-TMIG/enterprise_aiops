"""Root conftest: shared CLI options, hooks, and session fixtures."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python"


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False,
                     help="run tests marked slow")
    parser.addoption("--runintegration", action="store_true", default=False,
                     help="run tests marked integration")


def pytest_collection_modifyitems(config, items):
    skip_slow = pytest.mark.skip(reason="needs --runslow")
    skip_int = pytest.mark.skip(reason="needs --runintegration")
    for item in items:
        if "slow" in item.keywords and not config.getoption("runslow"):
            item.add_marker(skip_slow)
        if "integration" in item.keywords and not config.getoption("runintegration"):
            item.add_marker(skip_int)


def pytest_report_header(config):
    return [
        f"repo:        {REPO_ROOT}",
        f"python:      {sys.version.split()[0]}",
        f"venv:        {VENV_PYTHON.exists()}",
        f"runslow:     {config.getoption('runslow')}",
        f"integration: {config.getoption('runintegration')}",
    ]


@pytest.fixture(scope="session")
def repo_root():
    return REPO_ROOT


@pytest.fixture(scope="session")
def venv_python():
    if not VENV_PYTHON.exists():
        pytest.skip("no .venv/bin/python")
    return VENV_PYTHON


@pytest.fixture(scope="session")
def run_cmd(venv_python):
    """Run a command; fail with captured output on nonzero."""
    def _run(args, *, cwd=REPO_ROOT, timeout=60, check=True, env=None):
        r = subprocess.run(
            [str(a) for a in args], cwd=str(cwd),
            capture_output=True, text=True, timeout=timeout,
            env={**os.environ, **(env or {})},
        )
        if check and r.returncode != 0:
            pytest.fail(
                f"cmd failed: {' '.join(str(a) for a in args)}
"
                f"rc={r.returncode}
"
                f"stdout={r.stdout[-2000:]}
"
                f"stderr={r.stderr[-2000:]}"
            )
        return r
    return _run
