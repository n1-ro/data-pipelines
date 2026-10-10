import pytest

from pipelines.validate import is_valid_phone, is_valid_email, validate_record


def test_is_valid_phone():
    assert is_valid_phone("2125550123") is True
    assert is_valid_phone("12345") is False


def test_is_valid_email():
    assert is_valid_email("jane@example.com") is True
    assert is_valid_email("not-an-email") is False


def test_validate_record():
    assert validate_record({"first": "Jane", "last": "Smith", "phone": "2125550123"}) == []
    errors = validate_record({"first": "", "last": "", "phone": "123"})
    assert "missing name" in errors
    assert "invalid phone" in errors
