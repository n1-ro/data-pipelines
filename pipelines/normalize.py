"""Data normalization helpers (phone, name, casing)."""

from __future__ import annotations

import re


def normalize_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


def normalize_name(raw: str) -> str:
    """Title-case a name, collapsing whitespace."""
    return " ".join(w.capitalize() for w in (raw or "").split())


def normalize_email(raw: str) -> str:
    return (raw or "").strip().lower()


def normalize_zip(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    return digits[:5]
