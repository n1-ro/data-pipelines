import pytest

from pipelines.normalize import normalize_phone, normalize_name, normalize_email, normalize_zip


def test_normalize_phone():
    assert normalize_phone("+1 (212) 555-0123") == "2125550123"


def test_normalize_name_title_cases():
    assert normalize_name("  jane   smith ") == "Jane Smith"


def test_normalize_email_lowercases():
    assert normalize_email(" Jane@Example.COM ") == "jane@example.com"


def test_normalize_zip_truncates():
    assert normalize_zip("10001-2345") == "10001"
