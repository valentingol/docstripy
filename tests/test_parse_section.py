"""Test docstring section parser."""
import pytest_check as check

from npdocify.parse_doc.parse_section import parse_sections


def test_parse_section() -> None:
    """Test docstring section parser."""
    with open("tests/files/test2.py", "r", encoding="utf-8") as file:
        lines = file.readlines()
    sections_rest = lines[8:15]
    ranges = parse_sections(sections_rest)
    expected_ranges = {
        "_parameters": [2, 4],
        "_returns": [4, 6],
    }
    check.equal(ranges, expected_ranges)

    sections_google = lines[23:30]
    ranges = parse_sections(sections_google)
    expected_ranges = {
        "_parameters": [2, 4],
        "_returns": [5, 7],
    }
    check.equal(ranges, expected_ranges)

    sections_numpy = lines[39:51]
    ranges = parse_sections(sections_numpy)
    expected_ranges = {
        "_parameters": [2, 7],
        "_returns": [7, 12],
    }
    check.equal(ranges, expected_ranges)

    sections_nothing = lines[59:60]
    ranges = parse_sections(sections_nothing)
    check.equal(ranges, {})


#     sections1 = parse_section(lines[7:23])
#     expected_sections = {
#         "_indent_level": 1,
#         "_rawstring": False,
#         "_title": "Return factorial of n.",
#         "_parameters": [
#             {
#                 "name": "n",
#                 "type": "int",
#                 "optional": False,
#                 "description": "Number to compute factorial of.",
#             },
#         ],
#         "_returns": [
#             {
#                 "name": "",
#                 "type": "int",
#                 "optional": False,
#                 "description": "Factorial of n.",
#             },
#         ],
#         "_raises": [],
#     }
#     check.equal(sections1, expected_sections)

#     sections2 = parse_section(lines[32:33])
#     expected_sections = {
#         "_indent_level": 1,
#         "_rawstring": False,
#         "_title": "Return nth Fibonacci number.",
#         "_parameters": [],
#         "_returns": [],
#         "_raises": [],
#     }
#     check.equal(sections2, expected_sections)

#     sections3 = parse_section(lines[42:46])
#     expected_sections = {
#         "_indent_level": 1,
#         "_rawstring": True,
#         "_title": [r"Return square.", r"Use \escaped characters."],
#         "_parameters": [],
#         "_returns": [],
#         "_raises": [],
#     }
#     check.equal(sections3, expected_sections)
