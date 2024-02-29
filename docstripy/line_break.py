"""Line break function."""

from typing import List

from docstripy.lines_routines import add_eol, clean_trailing_spaces, remove_eol


def line_break(lines: List[str], max_line_length: int) -> List[str]:
    """Break lines at a given length."""
    new_lines = remove_eol(lines)
    new_lines = rec_line_break(new_lines, max_line_length=max_line_length)
    new_lines = clean_trailing_spaces(new_lines)
    new_lines = add_eol(new_lines)
    return new_lines


def rec_line_break(lines: List[str], max_line_length: int) -> List[str]:
    """Break lines recursively."""
    new_lines = []
    remaining_lines = []
    if max_line_length <= 0:
        return lines
    for i_l, line in enumerate(lines):
        if len(line) <= max_line_length:
            new_lines.append(line)
        else:
            words = line.split(" ")
            new_line = ""
            remaining_lines = lines[i_l + 1 :]
            i_w = 0
            for word in words:
                i_w += 1
                if len(new_line + " " + word) <= max_line_length:
                    new_line = new_line + " " + word if new_line else word
                else:
                    break
            new_lines.append(new_line)
            remaining_words = " ".join(words[i_w - 1 :])
            if remaining_lines:
                if remaining_lines[0].strip() == "":
                    new_lines.extend(line_break([remaining_words], max_line_length))
                    new_lines.append("")
                    remaining_lines = remaining_lines[1:]
                else:
                    remaining_lines[0] = remaining_words + " " + remaining_lines[0]
            else:
                remaining_lines = [remaining_words]
            break
    if remaining_lines:
        remaining_lines = line_break(remaining_lines, max_line_length)
        new_lines.extend(remaining_lines)
    return new_lines
