from pipelines.dedupe import dedupe


def test_dedupe_keeps_one_row_per_phone():
    rows = [
        {"first": "A", "last": "B", "phone": "2125550100", "file": ""},
        {"first": "A", "last": "B", "phone": "2125550100", "file": "2026-0001"},
    ]
    out = dedupe(rows, key="phone")
    assert len(out) == 1
    assert out[0]["file"] == "2026-0001"


def test_dedupe_prefers_higher_quality_row():
    rows = [
        {"first": "", "last": "", "phone": "2125550100", "file": ""},
        {"first": "Jane", "last": "Smith", "phone": "2125550100", "file": ""},
    ]
    out = dedupe(rows, key="phone")
    assert out[0]["first"] == "Jane"


def test_dedupe_by_name():
    rows = [
        {"first": "Jane", "last": "Smith", "phone": "2125550100", "file": ""},
        {"first": "jane", "last": "smith", "phone": "9990001111", "file": ""},
    ]
    out = dedupe(rows, key="name")
    assert len(out) == 1
