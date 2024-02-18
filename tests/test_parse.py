"""Tests for file parsing functions."""

import pytest_check as check

from npdocify.parse_doc.main_parser import parse_docstring


def test_parse_docstring() -> None:
    """Test docstring file parser."""
    with open("tests/files/test1.py", encoding="utf-8") as file:
        lines_test1 = file.readlines()
    range_docstr, _ = parse_docstring(lines_test1)
    check.equal(range_docstr, [[8, 24], [32, 33], [43, 47]])
    with open("tests/files/test4.py", encoding="utf-8") as file:
        lines_test4 = file.readlines()
    _, sections_list = parse_docstring(lines_test4)
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
