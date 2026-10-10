"""Record-level validation for cleaned rows."""

from __future__ import annotations

import re

PHONE_RE = re.compile(r"^\d{10}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_RE.match(phone or ""))


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email or ""))


def validate_record(row: dict[str, str]) -> list[str]:
    """Return a list of validation errors (empty = valid)."""
    errors: list[str] = []
    if not row.get("first") or not row.get("last"):
        errors.append("missing name")
    if row.get("phone") and not is_valid_phone(row["phone"]):
        errors.append("invalid phone")
    if row.get("email") and not is_valid_email(row["email"]):
        errors.append("invalid email")
    return errors
