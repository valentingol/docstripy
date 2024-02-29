"""File parsing functions."""

from typing import List, Tuple


def parse_ranges(lines: List[str]) -> Tuple[List[List[int]], List[List[int]]]:
    """Parse source code lines ranges.

    Parameters
    ----------
    lines : List[str]
        List of lines to parse.

    Returns
    -------
    ranges_docstr : List[List[int]]
        Ranges of lines containing docstrings.
    ranges_def : List[List[int]]
        Ranges of lines containing function definitions.
    """
    ranges_docstr: List[List[int]] = []
    ranges_def: List[List[int]] = []
    current_docstr_range: List[int] = []
    current_def_range: List[int] = []
    in_docstr, in_def = False, False
    for ind_line, line in enumerate(lines):
        ranges_docstr, current_docstr_range, in_docstr = docstring_parse_range(
            ranges=ranges_docstr,
            current_range=current_docstr_range,
            in_docstr=in_docstr,
            line=line,
            ind_line=ind_line,
        )
        if not in_docstr:
            ranges_def, current_def_range, in_def = def_parse_range(
                ranges=ranges_def,
                current_range=current_def_range,
                in_def=in_def,
                line=line,
                ind_line=ind_line,
            )
    return ranges_docstr, ranges_def


def docstring_parse_range(
    ranges: List[List[int]],
    current_range: List[int],
    *,
    in_docstr: bool,
    line: str,
    ind_line: int,
) -> Tuple[List[List[int]], List[int], bool]:
    """Parse docstring lines range from source code."""
    docstring_starters = ('"""', "'''", 'r"""', "r'''")
    strip_line = line.strip()
    if strip_line.startswith(docstring_starters) and line.startswith(" "):
        # Case one-line docstring
        if (
            strip_line.count('"""') > 1 or strip_line.count("'''") > 1
        ) and not in_docstr:
            ranges.append([ind_line, ind_line + 1])
        else:
            # Case multi-line docstring
            if not in_docstr:
                current_range = [ind_line]
                in_docstr = True
            else:
                current_range.append(ind_line + 1)
                ranges.append(current_range)
                in_docstr = False
    elif in_docstr and strip_line.endswith('"""') or strip_line.endswith("'''"):
        current_range.append(ind_line + 1)
        ranges.append(current_range)
        in_docstr = False
    return ranges, current_range, in_docstr


def def_parse_range(
    ranges: List[List[int]],
    current_range: List[int],
    *,
    in_def: bool,
    line: str,
    ind_line: int,
) -> Tuple[List[List[int]], List[int], bool]:
    """Parse docstring lines range from source code."""
    strip_line = line.rsplit("#", maxsplit=1)[0].strip()
    if not in_def and strip_line.startswith("def "):
        if strip_line.endswith(":"):
            # Case one-line def
            ranges.append([ind_line, ind_line + 1])
        else:
            # Case multi-line def
            current_range = [ind_line]
            in_def = True
    elif in_def and strip_line.endswith(":"):
        current_range.append(ind_line + 1)
        ranges.append(current_range)
        in_def = False
    return ranges, current_range, in_def
