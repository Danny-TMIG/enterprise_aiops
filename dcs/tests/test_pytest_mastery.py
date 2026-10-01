import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

@settings(max_examples=50, deadline=None)
@given(st.text(min_size=1, max_size=20))
def test_slug_never_empty(text):
    s = "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")
    assert s or not any(c.isalnum() for c in text)
