"""Tests for parsing functions."""
import pytest_check as check

from npdocify.parser import docstring_parse_file


def test_docstring_parse_file() -> None:
    """Test docstring file parser."""
    with open("tests/files/test1.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
    range_docstr = docstring_parse_file(lines)
    check.equal(range_docstr, [[8, 24], [32, 33], [43, 47]])
