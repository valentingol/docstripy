"""Tests for file parsing functions."""

import pytest_check as check

from docstripy.google.parse_doc import is_define_section
from docstripy.parse_doc.main_parser import parse_docstring


def test_parse_docstring() -> None:
    """Test docstring file parser."""
    with open("tests/files/test1.py", encoding="utf-8") as file:
        lines_test1 = file.readlines()
    range_docstr, _, to_insert = parse_docstring(lines_test1)
    # check.equal(False)
    check.equal(range_docstr, [[8, 24], [32, 33], [54, 58], [62, 63]])
    check.equal(to_insert, [False, False, False, True])

    with open("tests/files/test4.py", encoding="utf-8") as file:
        lines_test4 = file.readlines()
    _, sections_list, _ = parse_docstring(lines_test4)
    check.equal(len(sections_list), 3)
    expected_dict = {
        "_escaped": True,
        "_title": [
            "A function.\n",
            "\n",
            "It does something not important but the title\n",
            "is in multiple line.\n",
        ],
        "_parameters": [
            {
                "name": "name1",
                "type": "List[bool]",
                "optional": False,
                "description": ["A list of bools.\n"],
                "default": "",
            },
            {
                "name": "name2",
                "type": "list | str",
                "optional": True,
                "description": [
                    "A list or a string.\n",
                    "\n",
                    "This parameter is very important.\n",
                ],
                "default": '""',
            },
            {
                "name": "name3",
                "type": "Dict[str, int]",
                "optional": True,
                "description": ["A dictionary.\n"],
                "default": '{"a,b": 1}',
            },
        ],
        "_raises": [
            {
                "name": "ValueError",
                "type": "",
                "description": ["When something happened.\n"],
            },
            {
                "name": "ValueError",
                "type": "",
                "description": ["When something else happened.\n"],
            },
        ],
        "_returns": [
            {
                "name": "result",
                "type": "int",
                "description": ["The first result of the function.\n"],
            },
            {
                "name": "",
                "type": "list",
                "description": [],
            },
            {
                "name": "result3",
                "type": "int",
                "description": [],
            },
        ],
        "_yields": [
            {
                "name": "",
                "type": "int",
                "description": ["A number.\n"],
            },
        ],
        "_attributes": [{"name": "nothing", "type": "", "description": []}],
        "Example": [
            ">>> myfunc_rest([True])\n",
            "1, [], 1\n",
            """>>> myfunc_rest([True], "\\n")\n""",
            "0, [], 0\n",
        ],
        "Notes": [
            "* This always works\n",
            "* This is a note\n",
        ],
    }
    for i in range(3):
        for key, val in expected_dict.items():
            if key != "_parameters":
                check.equal(
                    sections_list[i][key],
                    val,
                    f"Error with style {i} and key {key}.",
                )
        for j, param in enumerate(sections_list[i]["_parameters"]):
            check.equal(
                param,
                expected_dict["_parameters"][j],  # type: ignore
                f"Error with style {i} and parameter {j}.",
            )
    with open("tests/files/test5.py", encoding="utf-8") as file:
        lines_test5 = file.readlines()
    ranges_docstr, _, to_insert = parse_docstring(lines_test5)
    check.equal(ranges_docstr, [[8, 12], [15, 16], [16, 20]])
    check.equal(to_insert, [False, True, False])
    ranges_docstr, _, to_insert = parse_docstring(lines_test5, add_missing=False)
    check.equal(ranges_docstr, [[8, 12], [16, 20]])
    check.equal(to_insert, [False, False])


def test_define_google_section() -> None:
    """Test is_define_section of google parsing doc."""
    check.is_true(is_define_section("Example :\n"))
    check.is_false(is_define_section("Another example :\n"))
    check.is_false(is_define_section(" Example :\n"))
    check.is_false(is_define_section("Example\n"))


def test_parse_rest_attr() -> None:
    """Test ReST attributes parsing."""
    with open("tests/files/test6.py", encoding="utf-8") as file:
        lines_test6 = file.readlines()
    _, sections_list, _ = parse_docstring(lines_test6)
    check.equal(len(sections_list[0]["_attributes"]), 3)
    check.equal(sections_list[0]["_attributes"][0]["name"], "integer")
    check.equal(sections_list[0]["_attributes"][1]["name"], "str")
    check.equal(sections_list[0]["_attributes"][2]["name"], "bool")
