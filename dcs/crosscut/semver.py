"""Semver range matching, IETF-style."""

import re  # pragma: no cover

from dcs.generate import requirement  # pragma: no cover

_VER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def parse(v):  # pragma: no cover
    m = _VER.match(v)
    return tuple(map(int, m.groups())) if m else None  # pragma: no cover


def satisfies(version: str, spec: str) -> bool:  # pragma: no cover
    v = parse(version)
    if v is None:  # pragma: no cover
        return False  # pragma: no cover
    if spec.startswith("^"):  # pragma: no cover
        lo = parse(spec[1:])
        return lo <= v < (lo[0] + 1, 0, 0)  # pragma: no cover
    if spec.startswith("~"):  # pragma: no cover
        lo = parse(spec[1:])
        return lo <= v < (lo[0], lo[1] + 1, 0)  # pragma: no cover
    return parse(spec) == v  # pragma: no cover


@requirement(
    id="DCS-XC-SEMVER-001",
    title="caret/tilde/exact match correctly",
    section="X.semver",
    hats=["REL", "PL"],
    criticality="MUST",
)
def test():  # pragma: no cover
    assert satisfies("1.2.3", "^1.0.0")
    assert not satisfies("2.0.0", "^1.0.0")
    assert satisfies("1.2.9", "~1.2.0")
    assert not satisfies("1.3.0", "~1.2.0")
    assert satisfies("1.2.3", "1.2.3")
