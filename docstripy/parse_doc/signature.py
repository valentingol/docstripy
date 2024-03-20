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
    if "_parameters" in sections_docstr:
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
    if "_returns" in sections_docstr and len(sections_docstr["_returns"]) in (
        len(rtypes),
        0,
    ):
        # NOTE: only add/update return info if already any is provided in the doc
        if sections_docstr["_returns"]:
            for i, return_arg in enumerate(sections_docstr["_returns"]):
                if "type" not in return_arg or not return_arg["type"]:
                    return_arg["type"] = rtypes[i]
        else:
            sections_docstr["_returns"] = [{"type": rtype} for rtype in rtypes]
    return sections_docstr


def find_range_matching(
    ranges_def: List[List[int]],
    ranges_docstr: List[List[int]],
    lines: Optional[List[str]] = None,
) -> List[List[int]]:
    """Find the ranges in ranges_docstr that matches ranges_def.

    Parameters
    ----------
    ranges_def : List[List[int]]
        Range of signature lines.
    ranges_docstr : List[List[int]]
        Ranges of all the docstrings of the file.
    lines : Optional[List[str]], optional
        Lines of the whole file. Only used to find class docstrings.
        By default, not specified (None).

    Returns
    -------
    corresp_ranges_docstr : List[List[int]]
        Ranges of the docstrings that matches the ranges in ranges_def.
    """
    corresp_ranges_docstr = [[-1, -1] for _ in ranges_def]
    # Check the above line
    for i_def, range_def in enumerate(ranges_def):
        for i_doc, range_docstr in enumerate(ranges_docstr):
            if range_docstr[0] - range_def[1] == 0:
                corresp_ranges_docstr[i_def] = range_docstr
                del ranges_docstr[i_doc]
                continue
    # If not in the above line: check the above line again
    for i_def, range_def in enumerate(ranges_def):
        if corresp_ranges_docstr[i_def] == [-1, -1]:
            for i_doc, range_docstr in enumerate(ranges_docstr):
                if range_docstr[0] - range_def[1] == 1:
                    corresp_ranges_docstr[i_def] = range_docstr
                    del ranges_docstr[i_doc]
                    continue
    # Case where the function is __init__ and the docstring can be
    # right under the class definition
    for i_def, range_def in enumerate(ranges_def):
        if (
            lines
            and corresp_ranges_docstr[i_def] == [-1, -1]
            and "def __init__" in lines[range_def[0]]
        ):
            sorted_ranges = sorted(
                [rang for rang in ranges_docstr if rang[1] <= range_def[0]],
                key=lambda x: x[0],
                reverse=True,
            )
            if sorted_ranges and are_lines_class_head(
                lines[sorted_ranges[0][1] : range_def[0]]
            ):
                corresp_ranges_docstr[i_def] = sorted_ranges[0]
                del ranges_docstr[ranges_docstr.index(sorted_ranges[0])]
    return corresp_ranges_docstr


def are_lines_class_head(lines: List[str]) -> bool:
    """Return if the lines are the head of a class."""
    lines = lines.copy()
    lines = [line.rsplit("#", maxsplit=1)[0].rstrip() for line in lines]
    indent = find_indent(lines)
    return all(not line or line[indent] != " " for line in lines)


def make_title_from_func_name(fn_name: str) -> List[str]:
    """Make title from function name."""
    fn_name = fn_name.strip("_")
    title = " ".join(fn_name.split("_")).capitalize()
    if " " not in title:
        title += " function"
    title += ".\n"
    return [title]
