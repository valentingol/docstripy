"""Routines on code source lines."""
from typing import List, Tuple


def remove_eol(lines: List[str]) -> List[str]:
    """Remove end of lines."""
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        if line.endswith("\n"):
            new_lines[i] = line[:-1]
    return new_lines


def remove_indent(lines: List[str], indent: int) -> List[str]:
    """Remove indent from lines."""
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        new_lines[i] = line[indent:]
    return new_lines


def find_prefix(
    lines: List[str],
    prefix_start: Tuple[str, ...],
    prefix_continue: Tuple[str, ...],
    *,
    dash: bool = False,
) -> Tuple[int, int]:
    """Find the index of consecutive lines starting with prefix.

    Parameters
    ----------
    lines : List[str]
        Lines of the docstring.
    prefix_start : Tuple[str, ...]
        Prefixes string of the first line.
    prefix_continue : Tuple[str, ...]
        Prefixes string of the following lines.
    dash : bool, optional
        Whether to expect a dash line after the first line, by default False.

    Returns
    -------
    start : int
        Index of the first line (or -1 if not found).
    end : int
        Index of the last line (or -1 if not found).
    """
    start, end = -1, -1
    if dash:
        prefix_continue += ("---",)
    for i, line in enumerate(lines):
        if line.startswith(prefix_start):
            if dash and len(lines) > i + 1 and not lines[i + 1].startswith("---"):
                continue
            start = i
            for j, line in enumerate(lines[i + 1 :]):
                if not line.startswith(prefix_continue):
                    end = i + j + 1
                    break
            break
    return start, end
