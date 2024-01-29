"""Classes and functions to manage difference between files."""
from typing import List, Optional


class Diff:
    """Difference class to store the difference between two versions of a file.

    Parameters
    ----------
    ranges : Optional[List[List[int]]], optional
        List of ranges of docstring line numbers [start, end]. Includes line at start,
        excludes line at end. By default empty list.
        Note: the ranges will be represented in descending order.
    lines : Optional[List[str]], optional
        List of lines to add to the file. By default empty list.
    """

    def __init__(self, ranges: Optional[List[List[int]]], lines: Optional[List[str]]):
        self.ranges: List[List[int]] = ranges if ranges is not None else []
        self.lines: List[str] = lines if lines is not None else []
        self.satenize_check()

    def satenize_check(self) -> None:
        """Check if the ranges are overlapping."""
        for i, range1 in enumerate(self.ranges):
            for range2 in self.ranges[i + 1 :]:
                if range1[0] <= range2[0] < range1[1]:
                    raise ValueError("Found overlapping ranges.")

    def order_lists(self) -> None:
        """Order the ranges in descending order and lines accordingly."""
        sort_indices = sorted(range(len(self.ranges)), key=lambda i: self.ranges[i][0])
        self.ranges = [self.ranges[i] for i in sort_indices[::-1]]
        self.lines = [self.lines[i] for i in sort_indices[::-1]]

    @staticmethod
    def split_line(line: str) -> List[str]:
        r"""Split a line in multiple lines using '\n'."""
        if line[-1] == "\n":
            line = line[:-1]
        return [single_line + "\n" for single_line in line.split("\n")]

    def apply_diff(self, lines: List[str]) -> List[str]:
        """Apply the difference to a list of lines."""
        self.order_lists()
        self.satenize_check()
        new_lines = lines.copy()
        for i, line in enumerate(self.lines):
            start, end = self.ranges[i]
            del new_lines[start:end]
            new_lines[start:start] = self.split_line(line)
        return new_lines
