"""Test file writting."""
import pytest
import pytest_check as check

from npdocify.difference import Diff
from npdocify.write import lines_change


def test_diff() -> None:
    """Test difference class."""
    file_path = "tests/files/test1.py"
    with open(file_path, "r") as file:
        lines = file.readlines()

    range_docstr = [[7, 23], [31, 32]]
    text = [
        '    r"""New function."""\n',
        '    """Other new function.\n    On multiple lines.\n    """\n',
    ]
    new_lines = lines_change(lines, Diff(range_docstr, text))

    check.equal(new_lines[7], '    r"""New function."""\n')
    check.equal(new_lines[8], "    if n < 0:\n")
    check.equal(new_lines[16], '    """Other new function.\n')
    check.equal(new_lines[17], "    On multiple lines.\n")
    check.equal(new_lines[18], '    """\n')

    new_lines = lines_change(lines, Diff(range_docstr[::-1], text[::-1]))

    check.equal(new_lines[7], '    r"""New function."""\n')
    check.equal(new_lines[8], "    if n < 0:\n")
    check.equal(new_lines[16], '    """Other new function.\n')
    check.equal(new_lines[17], "    On multiple lines.\n")
    check.equal(new_lines[18], '    """\n')

    with pytest.raises(ValueError, match="Found overlapping ranges."):
        lines_change(lines, Diff([[7, 23], [15, 32]], text))
