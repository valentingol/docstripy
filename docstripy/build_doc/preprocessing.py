"""Preprocessing functions for some sections."""

from typing import List

from docstripy.line_break import line_break
from docstripy.lines_routines import split_first_line


def preprocess_title_build(lines: List[str], max_len: int) -> List[str]:
    """Post-process the title section."""
    lines = split_first_line(lines, max_line_length=max_len)
    lines = line_break(lines, max_line_length=max_len)
    return lines
