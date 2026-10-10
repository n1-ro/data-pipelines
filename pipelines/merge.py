"""Merge multiple CSV files into one, normalizing a shared schema."""

from __future__ import annotations

import csv
from typing import Iterable


def read_rows(path: str) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def merge(rows_by_source: Iterable[list[dict[str, str]]], fieldnames: list[str]) -> list[dict[str, str]]:
    """Merge rows from multiple sources, projecting to `fieldnames` (missing → '')."""
    merged: list[dict[str, str]] = []
    for rows in rows_by_source:
        for row in rows:
            merged.append({k: row.get(k, "") for k in fieldnames})
    return merged


def concat_files(paths: Iterable[str]) -> list[dict[str, str]]:
    return merge((read_rows(p) for p in paths), fieldnames=[] or _union_headers(paths))


def _union_headers(paths: Iterable[str]) -> list[str]:
    headers: list[str] = []
    seen = set()
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            for h in csv.DictReader(f).fieldnames or []:
                if h not in seen:
                    seen.add(h)
                    headers.append(h)
    return headers
