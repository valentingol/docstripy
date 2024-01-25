"""Test docstring section parser."""
import pytest_check as check

from npdocify.parse_doc import parse_section


def test_parse_section():
    """Test docstring section parser."""
    with open("tests/files/test1.py", "r") as file:
        lines = file.readlines()

    sections1 = parse_section(lines[7:23])
    expected_sections = {
        "_indent_level": 1,
        "_rawstring": False,
        "_title": "Return factorial of n.",
        "_parameters": [
            {
                "name": "n",
                "type": "int",
                "optional": False,
                "description": "Number to compute factorial of.",
            },
        ],
        "_returns": [
            {
                "name": "",
                "type": "int",
                "optional": False,
                "description": "Factorial of n.",
            },
        ],
        "_raises": []
    }
    check.equal(sections1, expected_sections)

    sections2 = parse_section(lines[32:33])
    expected_sections = {
        "_indent_level": 1,
        "_rawstring": False,
        "_title": "Return nth Fibonacci number.",
        "_parameters": [],
        "_returns": [],
        "_raises": []
    }
    check.equal(sections2, expected_sections)

    sections3 = parse_section(lines[42:46])
    expected_sections = {
        "_indent_level": 1,
        "_rawstring": True,
        "_title": [r"Return square.", r"Use \escaped characters."],
        "_parameters": [],
        "_returns": [],
        "_raises": []
    }
    check.equal(sections3, expected_sections)
