"""Deterministic, balanced partitioning of a master file into outputs."""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Iterable


def _round_robin(n: int, parts: int) -> list[int]:
    return [i % parts for i in range(n)]


def split_rows(
    rows: list[dict[str, str]],
    parts: int,
    *,
    seed: int | None = None,
    shuffle: bool = True,
) -> list[list[dict[str, str]]]:
    """Split `rows` into `parts` balanced buckets, optionally shuffled first."""
    if parts < 1:
        raise ValueError("parts must be >= 1")
    data = list(rows)
    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(data)
    buckets: list[list[dict[str, str]]] = [[] for _ in range(parts)]
    for i, row in enumerate(data):
        buckets[i % parts].append(row)
    return buckets


def write_csv(path: str, rows: Iterable[dict[str, str]], fieldnames: list[str]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, quoting=csv.QUOTE_NONE, escapechar="\\"
        )
        writer.writeheader()
        writer.writerows(rows)
