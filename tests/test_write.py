"""Test file writting."""

import pytest
import pytest_check as check

from docstripy.difference import Diff


def test_diff() -> None:
    """Test difference class."""
    file_path = "tests/files/test1.py"
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    range_docstr = [[8, 24], [32, 33]]
    text = [
        '    r"""New function."""\n',
        '    """Other new function.\n    On multiple lines.\n    """\n',
    ]
    new_lines = Diff(range_docstr, text).apply_diff(lines)

    check.equal(new_lines[8], '    r"""New function."""\n')
    check.equal(new_lines[9], "    if n < 0:\n")
    check.equal(new_lines[17], '    """Other new function.\n')
    check.equal(new_lines[18], "    On multiple lines.\n")
    check.equal(new_lines[19], '    """\n')

    new_lines = Diff(range_docstr[::-1], text[::-1]).apply_diff(lines)

    check.equal(new_lines[8], '    r"""New function."""\n')
    check.equal(new_lines[9], "    if n < 0:\n")
    check.equal(new_lines[17], '    """Other new function.\n')
    check.equal(new_lines[18], "    On multiple lines.\n")
    check.equal(new_lines[19], '    """\n')

    with pytest.raises(ValueError, match="Found overlapping ranges."):
        Diff([[7, 23], [15, 32]], text).apply_diff(lines)
