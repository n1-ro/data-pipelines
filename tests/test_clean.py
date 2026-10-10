import pytest

from pipelines.clean import clean_phone, detect_columns, split_full_name, clean_row


def test_clean_phone_strips_formatting_and_leading_1():
    assert clean_phone("+1 (212) 555-0123") == "2125550123"
    assert clean_phone("1-212-555-0123") == "2125550123"
    assert clean_phone("") == ""


def test_split_full_name_first_last():
    assert split_full_name("Jane Smith") == ("Jane", "Smith")
    assert split_full_name("Jane Anne Smith") == ("Jane", "Anne Smith")
    assert split_full_name("Smith, Jane") == ("Jane", "Smith")


def test_detect_columns_finds_phone_and_names():
    cols = detect_columns(["First Name", "Last Name", "Phone Number", "File Number"])
    assert cols["phone"] == 2
    assert cols["first"] == 0
    assert cols["last"] == 1
    assert cols["file"] == 3


def test_clean_row_drops_blocked_phone():
    headers = ["First Name", "Last Name", "Phone"]
    cols = detect_columns(headers)
    row = {"First Name": "A", "Last Name": "B", "Phone": "0000000000"}
    assert clean_row(row, cols, headers) is None


def test_clean_row_drops_missing_names():
    headers = ["First Name", "Last Name", "Phone"]
    cols = detect_columns(headers)
    row = {"First Name": "", "Last Name": "", "Phone": "2125550100"}
    assert clean_row(row, cols, headers) is None
