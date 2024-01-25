"""Tests for parsing functions."""
import pytest_check as check

from npdocify.parser import docstring_parse_file


def test_docstring_parse_file():
    """Test docstring file parser."""
    with open("tests/files/test1.py", "r") as f:
        lines = f.readlines()
    range_docstr = docstring_parse_file(lines)
    check.equal(range_docstr, [[7, 23], [31, 32], [42, 46]])
