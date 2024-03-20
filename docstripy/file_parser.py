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
    in_docstr, double_quotes, in_def = False, None, False
    states = {
        "ranges_docstr": ranges_docstr,
        "ranges_def": ranges_def,
        "current_docstr_range": current_docstr_range,
        "current_def_range": current_def_range,
        "in_docstr": in_docstr,
        "double_quotes": double_quotes,
        "in_def": in_def,
    }
    for ind_line, line in enumerate(lines):
        states = docstring_parse_range(
            line=line,
            ind_line=ind_line,
            states=states,
        )
        if not in_docstr:
            states = def_parse_range(
                line=line,
                ind_line=ind_line,
                states=states,
            )
    ranges_docstr = states["ranges_docstr"]  # type: ignore
    ranges_def = states["ranges_def"]  # type: ignore
    return ranges_docstr, ranges_def


def docstring_parse_range(
    line: str,
    ind_line: int,
    states: dict,
) -> dict:
    """Parse docstring lines range from source code."""
    ranges = states["ranges_docstr"]
    current_range = states["current_docstr_range"]
    in_docstr = states["in_docstr"]
    double_quotes = states["double_quotes"]
    docstring_starters = ('"""', "'''", 'r"""', "r'''")
    strip_line = line.strip()
    strip_wo_comment = line.rsplit("#", maxsplit=1)[0].strip()
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
                double_quotes = strip_line.startswith(('"""', 'r"""'))
            elif (double_quotes and strip_wo_comment.endswith('"""')) or (
                not double_quotes and strip_wo_comment.endswith("'''")
            ):
                current_range.append(ind_line + 1)
                ranges.append(current_range)
                in_docstr = False
                double_quotes = None
    elif in_docstr and (
        (double_quotes and strip_wo_comment.endswith('"""'))
        or (not double_quotes and strip_wo_comment.endswith("'''"))
    ):
        current_range.append(ind_line + 1)
        ranges.append(current_range)
        in_docstr = False
        double_quotes = None
    elif in_docstr and is_def_line(strip_line):
        # Probably not in a docstring
        in_docstr = False
        double_quotes = None
        current_range = []
    states["ranges_docstr"] = ranges
    states["current_docstr_range"] = current_range
    states["in_docstr"] = in_docstr
    states["double_quotes"] = double_quotes
    return states


def is_def_line(strip_line: str) -> bool:
    """Return whether the line is a function or class definition."""
    return (
        strip_line.startswith(("def ", "class "))
        and "(" in strip_line
        and strip_line.split("(", maxsplit=1)[0].count(" ") == 1
    )


def def_parse_range(
    line: str,
    ind_line: int,
    states: dict,
) -> dict:
    """Parse signature lines range from source code."""
    ranges = states["ranges_def"]
    current_range = states["current_def_range"]
    in_def = states["in_def"]
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
    states["ranges_def"] = ranges
    states["current_def_range"] = current_range
    states["in_def"] = in_def
    return states
