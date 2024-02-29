"""Routines on code source lines."""

from typing import List, Tuple


def add_eol(lines: List[str]) -> List[str]:
    """Add end of lines."""
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        if not line.endswith("\n"):
            new_lines[i] = line + "\n"
    return new_lines


def remove_eol(lines: List[str]) -> List[str]:
    """Remove end of lines."""
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        if line.endswith("\n"):
            new_lines[i] = line[:-1]
    return new_lines


def remove_indent(lines: List[str]) -> List[str]:
    """Remove indent from lines."""
    indent = find_indent(lines)
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        new_lines[i] = line[indent:] if line not in ("", "\n") else line
    return new_lines


def add_indent(lines: List[str], indent: int) -> List[str]:
    """Add indent from lines."""
    new_lines = lines.copy()
    for i, line in enumerate(lines):
        new_lines[i] = " " * indent + line if line not in ("", "\n") else line
    return new_lines


def find_indent(lines: List[str]) -> int:
    """Find indentation of a docstring."""
    if len([line for line in lines if line not in ("", "\n")]) == 0:
        return 0
    return min(
        len(line) - len(line.lstrip()) for line in lines if line not in ("", "\n")
    )


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
            if dash and len(lines) <= i + 1:
                continue
            if dash and len(lines) > i + 1 and not lines[i + 1].startswith("---"):
                continue
            start = i
            for j, line in enumerate(lines[i + 1 :]):
                if not line.startswith(prefix_continue):
                    end = i + j + 1
                    break
            break
    return start, end


def clean_empty(lines: List[str]) -> List[str]:
    """Clean all empty lines."""
    new_lines = lines.copy()
    for line in lines:
        if line.strip() not in ("", "\n"):
            new_lines.append(line)
    return new_lines


def clean_leading_empty(lines: List[str]) -> List[str]:
    """Clean leading empty lines."""
    new_lines = lines.copy()
    while len(new_lines) > 0 and new_lines[0].strip(" ") == "\n":
        del new_lines[0]
    return new_lines


def clean_trailing_empty(lines: List[str]) -> List[str]:
    """Clean trailing empty lines."""
    new_lines = lines.copy()
    while len(new_lines) > 0 and new_lines[-1].strip(" ") == "\n":
        del new_lines[-1]
    return new_lines


def remove_quotes(lines: List[str]) -> Tuple[List[str], bool]:
    """Remove triple quotes and return whether the docstring is escaped or not."""
    escaped = False
    new_lines = lines.copy()
    for comment_pattern in ("'''#", "''' #", "'''  #", '"""#', '""" #', '"""  #'):
        if comment_pattern in new_lines[-1]:
            ind = new_lines[-1].index(comment_pattern)
            new_lines[-1] = new_lines[-1][:ind]
            break

    for i, line in enumerate(lines):
        if "r'''" in line or 'r"""' in line:
            escaped = True
            new_lines[i] = line.replace("r'''", "").replace('r"""', "")
        if "'''" in new_lines[i] or '"""' in new_lines[i]:
            new_lines[i] = line.replace("'''", "").replace('"""', "")
    new_lines = add_eol(new_lines)  # Add end of lines if removed
    return new_lines, escaped


def clean_trailing_spaces(lines: List[str]) -> List[str]:
    """Clean trailing spaces."""
    new_lines = []
    for line in lines:
        have_eol = line and line[-1] == "\n"
        line = line.rstrip("\n")
        line = line.rstrip(" ")
        if have_eol:
            line += "\n"
        new_lines.append(line)
    return new_lines


def clean_comment(lines: List[str]) -> List[str]:
    """Clean comment lines."""
    new_lines = []
    for line in lines:
        if "#" in line:
            line = line[: line.index("#")]
        new_lines.append(line)
    return new_lines
