"""Column detection, normalization, and blocking for tabular data."""

from __future__ import annotations

import csv
import re
from typing import Iterable

# Column-name hints used for dynamic detection.
NAME_HINTS = ("first", "last", "name", "full", "contact", "debtor")
PHONE_HINTS = ("phone", "number", "mobile", "cell", "tel")
FILE_HINTS = ("file", "file_number", "fileno", "account", "acct")


def _normalize_header(h: str) -> str:
    return re.sub(r"[^a-z0-9_]", "", h.lower())


def detect_columns(headers: list[str]) -> dict[str, int | None]:
    """Return indices for phone, first, last, and file columns (None if absent)."""
    norm = [_normalize_header(h) for h in headers]
    out: dict[str, int | None] = {"phone": None, "first": None, "last": None, "file": None}

    for i, h in enumerate(norm):
        if out["phone"] is None and any(k in h for k in PHONE_HINTS):
            out["phone"] = i
        elif out["first"] is None and ("first" in h):
            out["first"] = i
        elif out["last"] is None and ("last" in h or "surname" in h):
            out["last"] = i
        elif out["file"] is None and any(k in h for k in FILE_HINTS):
            out["file"] = i

    # Fallbacks: a single "name"/"full_name" column → split into first/last.
    if out["first"] is None and out["last"] is None:
        for i, h in enumerate(norm):
            if "full" in h or h == "name":
                out["first"] = i  # marker: full name column; split downstream
                break

    return out


def clean_phone(raw: str) -> str:
    """Normalize a phone number to digits only (US-style)."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits


def split_full_name(value: str) -> tuple[str, str]:
    """Split a full name into (first, last). Handles 'Last, First' too."""
    v = (value or "").strip()
    if "," in v:
        last, _, first = v.partition(",")
        return first.strip(), last.strip()
    parts = v.split()
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


BLOCKED_PHONES = {
    "0000000000",
    "1111111111",
    "9999999999",
    "1234567890",
}


def iter_rows(path: str) -> Iterable[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def clean_row(
    row: dict[str, str],
    cols: dict[str, int | None],
    headers: list[str],
) -> dict[str, str] | None:
    """Normalize a row into {first,last,phone,file}. Returns None to drop it."""
    phone_idx = cols["phone"]
    phone = clean_phone(row[headers[phone_idx]]) if phone_idx is not None else ""

    if phone in BLOCKED_PHONES:
        return None

    first_idx = cols["first"]
    last_idx = cols["last"]
    if first_idx is not None and last_idx is not None:
        first = (row[headers[first_idx]] or "").strip()
        last = (row[headers[last_idx]] or "").strip()
    else:
        full = (row[headers[first_idx]] or "").strip() if first_idx is not None else ""
        first, last = split_full_name(full)

    if not first or not last:
        return None

    file_idx = cols["file"]
    file_no = (row[headers[file_idx]] or "").strip() if file_idx is not None else ""

    return {"first": first, "last": last, "phone": phone, "file": file_no}
