"""Signature related functions."""

from typing import List, Optional

from docstripy.lines_routines import clean_leading_empty, find_indent
from docstripy.parse_doc.parse_signature import parse_signature


def merge_docstr_signature(
    sections_docstr: dict,
    lines_signature: List[str],
) -> dict:
    """Merge docstring and definition ranges."""
    if not lines_signature:
        return sections_docstr
    fn_name, rtypes, args = parse_signature(lines_signature)

    if "_title" not in sections_docstr or not clean_leading_empty(
        sections_docstr["_title"]
    ):
        sections_docstr["_title"] = make_title_from_func_name(fn_name)
    if "_parameters" in sections_docstr and sections_docstr["_parameters"]:
        # NOTE: only add/update param info if already any is provided in the doc
        for arg in args:
            arg_name = arg["name"].lstrip("*")
            if (
                arg_name
                not in [
                    param["name"].lstrip("*")
                    for param in sections_docstr["_parameters"]
                ]
                and arg_name != "self"  # Do not document self
            ):
                sections_docstr["_parameters"] = [arg] + sections_docstr["_parameters"]
            else:
                for param in sections_docstr["_parameters"]:
                    if param["name"] == arg["name"].lstrip("*"):
                        # Priority to the docstring
                        for key in arg:
                            if arg[key]:
                                param[key] = arg[key]
    if (
        "_returns" in sections_docstr
        and sections_docstr["_returns"]
        and len(rtypes) == len(sections_docstr["_returns"])
    ):
        # NOTE: only add/update return info if already any is provided in the doc
        for i, return_arg in enumerate(sections_docstr["_returns"]):
            if "type" not in return_arg or not return_arg["type"]:
                return_arg["type"] = rtypes[i]
    return sections_docstr


def find_range_matching(
    range_def: List[int],
    ranges_docstr: List[List[int]],
    *,
    lines: Optional[List[str]] = None,
) -> List[int]:
    """Find the range in ranges_def that matches range_docstr.

    Parameters
    ----------
    range_def : List[int]
        Range of signature lines.
    ranges_docstr : List[List[int]]
        Ranges of all the docstrings of the file.
    lines : Optional[List[str]], optional
        Lines of the whole file. Only used to find class docstrings.
        By default, not specified (None).
    """
    for range_docstr in ranges_docstr:
        if 0 <= range_docstr[0] - range_def[1] <= 1:
            return range_docstr
    if "def __init__" in lines[range_def[0]]:
        # Case where the function is __init__ and the docstring can be
        # right under the class definition
        candidate = sorted(
            [rang for rang in ranges_docstr if rang[1] <= range_def[0]],
            key=lambda x: x[0],
        )[0]
        if are_lines_class_head(lines[candidate[1] : range_def[0]]):
            return candidate
    return [-1, -1]


def are_lines_class_head(lines: List[str]):
    """Return if the lines are the head of a class."""
    lines = lines.copy()
    lines = [line.strip().rsplit("#", maxsplit=1)[0].rstrip() for line in lines]
    indent = find_indent(lines)
    return all(not line or line[indent] != " " for line in lines)


def make_title_from_func_name(fn_name: str) -> List[str]:
    """Make title from function name."""
    fn_name = fn_name.strip("_")
    return [" ".join(fn_name.split("_")).capitalize() + ".\n"]
