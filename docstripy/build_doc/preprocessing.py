"""Preprocessing functions for some sections."""

from typing import List

from docstripy.line_break import line_break


def preprocess_title_build(lines: List[str], max_len: int) -> List[str]:
    """Post-process the title section."""
    return line_break(lines, max_line_length=max_len)
