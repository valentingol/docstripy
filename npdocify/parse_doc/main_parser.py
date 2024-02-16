"""Global docstring parsing functions."""

from typing import List

from npdocify.file_parser import docstring_parse_file_range
from npdocify.line_break import line_break
from npdocify.lines_routines import (
    clean_leading_empty,
    clean_trailing_empty,
    remove_indent,
    remove_quotes,
)
from npdocify.parse_doc.parse_params import parse_params_all
from npdocify.parse_doc.section_ranges import parse_sections_ranges


def parse_docstring(lines: List[str]) -> List[dict]:
    """Docstring parser."""
    range_docstrs = docstring_parse_file_range(lines)
    sections_list = []
    for range_docstr in range_docstrs:
        lines_docstr = lines[range_docstr[0]:range_docstr[1]]
        sections_list.append(parse_all(lines_docstr))
    return range_docstrs, sections_list


def parse_all(lines: List[str]):
    r"""Parse the whole docstring.

    Parameters
    ----------
    lines : List[str]
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
    lines, escaped = remove_quotes(lines)
    sec_ranges, style = parse_sections_ranges(lines)
    # Preprocess sections
    sections = {
        sec_name: lines[inds[0]:inds[1]] for (sec_name, inds) in sec_ranges.items()
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
        "_raises": "raises"
    }
    for section_name in section_names_for_parse_params_all:
        if section_name in sections:
            sections[section_name] = parse_params_all(
                sections[section_name],
                style=style,
                section_name=section_names_for_parse_params_all[section_name]
            )
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
    sections["_title"] = postprocess_title(sections["_title"])
    sections["_escaped"] = escaped
    return sections


def postprocess_title(lines: List[str]) -> List[str]:
    """Post-process the title section."""
    new_lines = lines.copy()
    if new_lines[0].strip():
        new_lines[0] = new_lines[0].strip(" ")
        new_lines[0] = new_lines[0][0].capitalize() + new_lines[0][1:]
        if (
            ((len(new_lines) >= 3 and not new_lines[1].strip())
            or len(new_lines) == 1)
            and new_lines[0][-2] not in (".", "!", "?")
        ):
            new_lines[-1] = new_lines[-1][:-1] + ".\n"
    return new_lines
