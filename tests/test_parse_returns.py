"""Test raises parsing."""

from typing import List

import pytest_check as check

from npdocify.lines_routines import remove_indent
from npdocify.parse_doc.parse_params import parse_params_all


def test_returns() -> None:
    """Test return parsing."""
    with open("tests/files/test3.py", "r", encoding="utf-8") as file:
        lines = file.readlines()
    rest_doc1 = remove_indent(lines[29:31])
    returns_rest = parse_params_all(rest_doc1, style="rest", section_name="return")
    np_doc1 = remove_indent(lines[68:72])
    returns_np = parse_params_all(np_doc1, style="numpy", section_name="return")
    google_doc1 = remove_indent(lines[102:104])
    returns_google = parse_params_all(
        google_doc1, style="google", section_name="return"
    )
    expected_list = [
        {
            "name": "result",
            "type": "int",
            "description": ["The result of the function.\n"],
        },
    ]
    check.equal(returns_rest, expected_list)
    check.equal(returns_np, expected_list)
    check.equal(returns_google, expected_list)

    doc_empty: List[str] = []
    returns_rest = parse_params_all(doc_empty, style="rest", section_name="return")
    returns_np = parse_params_all(doc_empty, style="numpy", section_name="return")
    returns_google = parse_params_all(doc_empty, style="google", section_name="return")
    check.equal(returns_rest, [])
    check.equal(returns_np, [])
    check.equal(returns_google, [])
