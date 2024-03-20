"""Test docstring section parser."""

import pytest_check as check

from docstripy.parse_doc.section_ranges import parse_sections_ranges


def test_parse_section_ranges() -> None:
    """Test docstring section parser."""
    with open("tests/files/test2.py", "r", encoding="utf-8") as file:
        lines = file.readlines()
    sections_rest = lines[8:15]
    ranges, style = parse_sections_ranges(sections_rest)
    check.equal(style, "rest")
    expected_ranges = {
        "_title": [0, 2],
        "_parameters": [2, 4],
        "_returns": [4, 6],
    }
    check.equal(ranges, expected_ranges)

    sections_google = lines[23:41]
    ranges, style = parse_sections_ranges(sections_google)
    check.equal(style, "google")
    expected_ranges = {
        "_title": [0, 2],
        "_parameters": [2, 5],
        "_returns": [5, 8],
        "_raises": [15, 18],
        "Examples": [8, 12],
        "Notes": [12, 15],
    }
    check.equal(ranges, expected_ranges)

    sections_numpy = lines[49:70]
    ranges, style = parse_sections_ranges(sections_numpy)
    check.equal(style, "numpy")
    expected_ranges = {
        "_title": [0, 2],
        "_parameters": [2, 7],
        "_returns": [7, 12],
        "Notes": [12, 16],
        "Examples": [16, 21],
    }
    check.equal(ranges, expected_ranges)

    sections_nothing = lines[78:79]
    ranges, style = parse_sections_ranges(sections_nothing)
    check.equal(style, "numpy")  # default
    check.equal(ranges, {"_title": [0, 1]})
