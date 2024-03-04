"""Test params parsing."""

import pytest_check as check

from docstripy.lines_routines import remove_indent
from docstripy.parse_doc.parse_params import parse_params_all


def test_params() -> None:
    """Test params parsing."""
    with open("tests/files/test3.py", "r", encoding="utf-8") as file:
        lines = file.readlines()
    rest_doc1 = remove_indent(lines[19:30])
    params_rest = parse_params_all(rest_doc1, style="rest")
    np_doc1 = remove_indent(lines[56:69])
    params_np = parse_params_all(np_doc1, style="numpy")
    google_doc1 = remove_indent(lines[94:103])
    params_google = parse_params_all(google_doc1, style="google")
    expected_list = [
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
                "This parameter is very important.\n",
                "\n",
                "Very important.\n",
            ],
            "default": "an empty list",
        },
        {
            "name": "name3",
            "type": "Dict[str, int]",
            "optional": True,
            "description": ["A dictionary.\n"],
            "default": '{"a": 1}',
        },
    ]
    check.equal(params_rest, expected_list)
    check.equal(params_np, expected_list)
    check.equal(params_google, expected_list)

    rest_doc2 = remove_indent(lines[41:42])
    params_dict_rest2 = parse_params_all(rest_doc2, style="rest")
    np_doc2 = remove_indent(lines[82:85])
    params_dict_np2 = parse_params_all(np_doc2, style="numpy")
    google_doc2 = remove_indent(lines[114:116])
    params_dict_google2 = parse_params_all(google_doc2, style="google")
    expected_dict = [
        {"name": "a", "type": "", "optional": False, "description": [], "default": ""},
    ]
    check.equal(params_dict_rest2, expected_dict)
    check.equal(params_dict_np2, expected_dict)
    check.equal(params_dict_google2, expected_dict)
