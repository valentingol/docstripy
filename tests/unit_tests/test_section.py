"""Test docstring section parser."""

import pytest_check as check

from docstripy.parse_doc.main_parser import parse_all


def test_parse_section() -> None:
    """Test section parsing."""
    with open("tests/files/test1.py", "r", encoding="utf-8") as file:
        lines = file.readlines()
    sections1 = parse_all(lines[8:24])
    expected_sections = {
        "_escaped": False,
        "_title": ["Return factorial of n.\n"],
        "_parameters": [
            {
                "name": "n",
                "type": "int",
                "optional": False,
                "description": ["Number to compute factorial of.\n"],
                "default": "",
            },
        ],
        "_returns": [
            {
                "name": "",
                "type": "int",
                "description": ["Factorial of n.\n"],
            },
        ],
        "_raises": [{"name": "ValueError", "description": [], "type": ""}],
    }
    for key, val in expected_sections.items():
        check.equal(sections1[key], val, f"error with key {key}")
    sections2 = parse_all(lines[32:33])
    expected_sections = {
        "_escaped": False,
        "_title": ["Return nth Fibonacci number.\n"],
    }
    check.equal(sections2, expected_sections)

    sections3 = parse_all(lines[54:58])
    expected_sections = {
        "_escaped": True,
        "_title": [r"Return square." + "\n", "\n", r"Use \escaped characters." + "\n"],
    }
    check.equal(sections3, expected_sections)
