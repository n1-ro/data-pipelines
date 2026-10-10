"""Exact and phone-keyed deduplication across one or many files."""

from __future__ import annotations

import csv
from typing import Iterable

from .clean import clean_phone, split_full_name


def _name_key(row: dict[str, str]) -> str:
    return "|".join((row.get("first", ""), row.get("last", ""))).lower()


def _row_quality(row: dict[str, str]) -> int:
    """Higher is better: prefer rows with a file number and complete names."""
    score = 0
    if row.get("file"):
        score += 4
    if row.get("first") and row.get("last"):
        score += 2
    if row.get("phone"):
        score += 1
    return score


def dedupe(rows: Iterable[dict[str, str]], key: str = "phone") -> list[dict[str, str]]:
    """Dedupe by key (exact 'name' or 'phone'), keeping the highest-quality row."""
    seen: dict[str, dict[str, str]] = {}
    for row in rows:
        if key == "phone":
            k = clean_phone(row.get("phone", ""))
        else:
            k = _name_key(row)
        if not k:
            continue
        if k not in seen or _row_quality(row) > _row_quality(seen[k]):
            seen[k] = row
    return list(seen.values())


def load_known_keys(paths: Iterable[str], key: str = "phone") -> set[str]:
    """Load keys from already-processed files to exclude from new output."""
    keys: set[str] = set()
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if key == "phone":
                    k = clean_phone(row.get("phone", row.get("number", row.get("Phone Number", ""))))
                else:
                    k = _name_key({"first": row.get("first", row.get("first_name", "")),
                                   "last": row.get("last", row.get("last_name", ""))})
                if k:
                    keys.add(k)
    return keys
