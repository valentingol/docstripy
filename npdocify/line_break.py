"""Line break function."""

from typing import List


def line_break(lines: List[str], max_line_length: int) -> List[str]:
    """Break lines at a given length."""
    new_lines = []
    remaining_lines = []
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


if __name__ == "__main__":
    docstring = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi "
        "ut aliquip ex ea commodo consequat. ",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum ",
        "",
        "dolore eu fugiat nulla pariatur. ",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui "
        "officia deserunt mollit anim id est laborum.",
    ]
    lines = line_break(docstring, 50)
    for line in lines:
        print(line)
