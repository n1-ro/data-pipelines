from pipelines.split import split_rows


def test_split_is_balanced():
    rows = [{"i": str(n)} for n in range(10)]
    buckets = split_rows(rows, 4, shuffle=False)
    sizes = [len(b) for b in buckets]
    assert sum(sizes) == 10
    assert max(sizes) - min(sizes) <= 1


def test_split_preserves_all_rows():
    rows = [{"i": str(n)} for n in range(100)]
    buckets = split_rows(rows, 3)
    assert sum(len(b) for b in buckets) == 100


def test_split_shuffles_with_seed():
    rows = [{"i": str(n)} for n in range(50)]
    a = split_rows(rows, 5, seed=42)
    b = split_rows(rows, 5, seed=42)
    assert a == b
