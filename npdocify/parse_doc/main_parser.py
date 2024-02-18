"""Global docstring parsing functions."""

from typing import List, Tuple

from npdocify.file_parser import parse_ranges
from npdocify.lines_routines import (
    clean_leading_empty,
    clean_trailing_empty,
    remove_indent,
    remove_quotes,
)
from npdocify.parse_doc.parse_def import parse_def
from npdocify.parse_doc.parse_params import parse_params_all
from npdocify.parse_doc.postprocessing import postprocess_title_parse
from npdocify.parse_doc.section_ranges import parse_sections_ranges


def parse_docstring(lines: List[str]) -> Tuple[List[List[int]], List[dict]]:
    """Docstring parser."""
    ranges_docstr, ranges_def = parse_ranges(lines)
    sections_list = []
    for range_docstr in ranges_docstr:
        range_def = find_range_matching(range_docstr, ranges_def)
        lines_docstr = lines[range_docstr[0] : range_docstr[1]]
        lines_def = lines[range_def[0] : range_def[1]]
        sections = parse_all(lines_docstr)
        sections = merge_docstr_def(sections, lines_def)
        sections_list.append(sections)
    return ranges_docstr, sections_list


def parse_all(lines_docstr: List[str]) -> dict:
    r"""Parse the whole docstring.

    Parameters
    ----------
    lines_docstr : List[str]
        Lines of the docstring.

    Returns
    -------
    sections : Dict
        Parsed sections. Can contain the following keys:
        - _title (List[str])
        - _parameters (List[Dict])
        - _returns (List[Dict])
        - _attributes (List[Dict])
        - _raises (List[Dict])
        - any other section name found in the docstring (List[str])

    Examples
    --------
    One can parse a docstring as follows:
    {
        '_title': ['This is a title\n', '\n', 'This is a description\n'],
        '_parameters': [
            {
                'name': 'param1',
                'type': 'int',
                'optional': False,
                'description': ['Description of param1\n'],
            },
            {
                'name': 'param2',
                'type': 'str',
                'optional': True,
                'description': ['Description of param2\n'],
                'default': '""',
            },
        ],
        '_returns': [
            {
                'type': 'int',
                'description': ['Description of the return\n'],
            },
        ],
        'Example': ['Example of a section\n'],
    }
    """
    lines, escaped = remove_quotes(lines_docstr)
    sec_ranges, style = parse_sections_ranges(lines)
    # Preprocess sections
    sections: dict = {}
    sections = {
        sec_name: lines[inds[0] : inds[1]] for (sec_name, inds) in sec_ranges.items()
    }
    sections = {
        sec_name: clean_trailing_empty(lines) for (sec_name, lines) in sections.items()
    }
    sections = {
        sec_name: clean_leading_empty(lines) for (sec_name, lines) in sections.items()
    }
    sections = {
        sec_name: remove_indent(lines) for (sec_name, lines) in sections.items()
    }
    # Manage param, return, attribute, raises using parse_params_all
    section_names_for_parse_params_all = {
        "_parameters": "param",
        "_returns": "return",
        "_yields": "yield",
        "_attributes": "attribute",
        "_raises": "raises",
    }
    for section_unders, section_name in section_names_for_parse_params_all.items():
        if section_unders in sections:
            section = parse_params_all(
                sections[section_unders],
                style=style,
                section_name=section_name,
            )
            if section:
                sections[section_unders] = section
    # Manage wild sections : remove header
    for section_name in sections:
        if not section_name.startswith("_"):
            header_len = 1
            if style == "numpy" and sections[section_name][1].strip().startswith("---"):
                header_len = 2
            sections[section_name] = sections[section_name][header_len:]
            if style in ("rest", "google"):
                sections[section_name] = remove_indent(sections[section_name])
    # NOTE : not necessary to modify _title section
    sections["_title"] = postprocess_title_parse(sections["_title"])
    sections["_escaped"] = escaped
    return sections


def merge_docstr_def(
    sections_docstr: dict,
    lines_def: List[str],
) -> dict:
    """Merge docstring and definition ranges."""
    if not lines_def:
        return sections_docstr
    fn_name, rtypes, args = parse_def(lines_def)
    if "_title" not in sections_docstr or not clean_leading_empty(
        sections_docstr["_title"]
    ):
        sections_docstr["_title"] = [" ".join(fn_name.split("_")).capitalize() + ".\n"]
    if "_parameters" not in sections_docstr:
        sections_docstr["_parameters"] = args
    else:
        for param in sections_docstr["_parameters"]:
            for arg in args:
                if param["name"] in (arg["name"], arg["name"].lstrip("*")):
                    param_name = param["name"]
                    # Priority to the docstring
                    for key in arg:
                        if arg[key]:
                            param[key] = arg[key]
                    param["name"] = param_name
        for arg in args:
            if arg["name"].lstrip("*") not in [
                param["name"].lstrip("*") for param in sections_docstr["_parameters"]
            ]:
                sections_docstr["_parameters"].append(arg)
    if "_returns" not in sections_docstr or not sections_docstr["_returns"]:
        sections_docstr["_returns"] = [{"name": "", "type": rtype} for rtype in rtypes]
    elif len(rtypes) == len(sections_docstr["_returns"]):
        for i, return_arg in enumerate(sections_docstr["_returns"]):
            if "type" not in return_arg or not return_arg["type"]:
                return_arg["type"] = rtypes[i]
    return sections_docstr


def find_range_matching(
    range_docstr: List[int],
    ranges_def: List[List[int]],
) -> List[int]:
    """Find the range in ranges_def that matches range_docstr."""
    for range_def in ranges_def:
        if 0 <= range_docstr[0] - range_def[1] <= 1:
            return range_def
    return [-1, -1]
