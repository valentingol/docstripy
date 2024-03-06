"""Postprocessing functions for some sections."""

from typing import List

from docstripy.lines_routines import (
    add_eol,
    clean_trailing_empty,
    clean_trailing_spaces,
)


def postprocess_title_parse(lines: List[str]) -> List[str]:
    """Post-process the title section."""
    new_lines = lines.copy()
    if not new_lines:
        return new_lines
    if new_lines[0].strip():
        new_lines[0] = new_lines[0].strip(" ")
        new_lines[0] = new_lines[0][0].capitalize() + new_lines[0][1:]
        if (
            (len(new_lines) >= 3 and not new_lines[1].strip()) or len(new_lines) == 1
        ) and new_lines[0][-2] not in (".", "!", "?"):
            new_lines[-1] = new_lines[-1][:-1] + ".\n"
    return new_lines


def postprocess_description(lines: List[str]) -> List[str]:
    """Post process description."""
    lines = clean_trailing_spaces(lines)
    lines = add_eol(lines)
    lines = clean_trailing_empty(lines)
    if lines and len(lines[-1]) > 1 and lines[-1][-2] not in (".", "?", "!"):
        lines[-1] = lines[-1][:-1] + ".\n"
    # Capitalize first letter
    if len(lines) > 0:
        first_line_desc = lines[0]
        if 97 <= ord(first_line_desc[0]) <= 122:
            cap_letter = first_line_desc[0].capitalize()
            lines[0] = cap_letter + first_line_desc[1:]
    return lines


def postprocess_default_val(default: str) -> str:
    """Post process default value string."""
    if default == "":
        return default
    default.replace("\n", " ")  # remove new lines characters
    return default
