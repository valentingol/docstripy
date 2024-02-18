"""Postprocessing functions for some sections."""

from typing import List


def postprocess_title_parse(lines: List[str]) -> List[str]:
    """Post-process the title section."""
    new_lines = lines.copy()
    if new_lines[0].strip():
        new_lines[0] = new_lines[0].strip(" ")
        new_lines[0] = new_lines[0][0].capitalize() + new_lines[0][1:]
        if (
            (len(new_lines) >= 3 and not new_lines[1].strip()) or len(new_lines) == 1
        ) and new_lines[0][-2] not in (".", "!", "?"):
            new_lines[-1] = new_lines[-1][:-1] + ".\n"
    return new_lines
