"""Functions that modify files with new docstrings."""

from typing import List

from npdocify.difference import Diff


def lines_change(lines: List[str], diff: Diff) -> List[str]:
    """Modify the lines of a file with a difference.

    Parameters
    ----------
    lines : List[str]
        List of lines of the file.
    diff : Diff
        Difference between the file and the new docstring.

    Returns
    -------
    new_lines : List[str]
        List of lines of the file with the difference.
    """
    return diff.apply_diff(lines)
