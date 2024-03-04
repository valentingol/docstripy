"""Classes and functions to manage difference between files."""

from typing import List, Tuple, Union


def satenize_ranges(ranges: List[List[int]]) -> List[List[int]]:
    """Check if the ranges are overlapping."""
    for i, range1 in enumerate(ranges):
        for range2 in ranges[i + 1 :]:
            if range1[0] <= range2[0] < range1[1]:
                raise ValueError("Found overlapping ranges.")
            if range2[0] <= range1[0] < range2[1]:
                raise ValueError("Found overlapping ranges.")
    return ranges


def order_lists(
    ranges: List[List[int]],
    lines: List[str],
    to_insert: List[bool],
) -> Tuple[List[List[int]], List[str], List[bool]]:
    """Order the ranges in descending order and lines accordingly."""
    sort_indices = sorted(range(len(ranges)), key=lambda i: ranges[i][0])
    ranges = [ranges[i] for i in sort_indices[::-1]]
    lines = [lines[i] for i in sort_indices[::-1]]
    to_insert = [to_insert[i] for i in sort_indices[::-1]]
    return ranges, lines, to_insert


def split_line(line: str) -> List[str]:
    r"""Split a line in multiple lines using '\n'."""
    if line[-1] == "\n":
        line = line[:-1]
    return [single_line + "\n" for single_line in line.split("\n")]


def apply_diff(
    ranges: List[List[int]],
    lines: List[str],
    old_lines: List[str],
    *,
    to_insert: Union[bool, List[bool]] = False,
) -> List[str]:
    """Apply the difference to a list of lines.

    Parameters
    ----------
    ranges : List[List[int]]
        List of ranges of docstring line numbers [start, end]. Includes line at start,
        excludes line at end.
    lines : List[str]
        List of lines to add to the file.
    old_lines : List[str]
        List of lines of the original file.
    to_insert : Union[bool, List[bool]], optional
        Whether to insert the lines or overwrite them instead.
        If a list is given, it should have the same
        length as ranges. Otherwise, the same value will be used for all ranges.
        By default False.
    """
    if isinstance(to_insert, bool):
        to_insert_list = [to_insert] * len(ranges)
    else:
        to_insert_list = to_insert
    ranges, lines, to_insert_list = order_lists(ranges, lines, to_insert_list)
    ranges = satenize_ranges(ranges)
    new_lines = old_lines.copy()
    for i, line in enumerate(lines):
        start, end = ranges[i]
        to_insert_line = to_insert_list[i]
        if not to_insert_line:
            del new_lines[start:end]
        new_lines[start:start] = split_line(line)
    return new_lines
