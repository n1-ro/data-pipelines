import pytest

from pipelines.merge import merge


def test_merge_projects_to_shared_schema():
    rows = [
        [{"first": "A", "last": "B", "phone": "1", "extra": "x"}],
        [{"first": "C", "last": "D", "phone": "2"}],
    ]
    out = merge(rows, ["first", "last", "phone"])
    assert len(out) == 2
    assert out[0]["first"] == "A"
    assert "extra" not in out[0]
    assert out[1]["phone"] == "2"
