"""Global docstring parsing functions."""

from typing import List, Tuple

from docstripy.file_parser import parse_ranges
from docstripy.lines_routines import (
    clean_leading_empty,
    clean_trailing_empty,
    remove_indent,
    remove_quotes,
)
from docstripy.parse_doc.parse_params import parse_params_all
from docstripy.parse_doc.postprocessing import postprocess_title_parse
from docstripy.parse_doc.section_ranges import parse_sections_ranges
from docstripy.parse_doc.signature import find_range_matching, merge_docstr_signature


def parse_docstring(
    lines: List[str],
    *,
    add_missing: bool = True,
) -> Tuple[List[List[int]], List[dict], List[bool]]:
    """Docstring parser.

    Parameters
    ----------
    lines : List[str]
        Lines of the file.
    add_missing : bool, optional
        Whether to add missing docstrings, by default True.

    Returns
    -------
    ranges_docstr : List[List[int]]
        Ranges of the docstrings.
    sections_list : List[Dict]
        Parsed sections.
    to_insert : List[bool]
        Whether to insert a new docstring or overwrite the existing one.
    """
    ranges_docstr, ranges_def = parse_ranges(lines)
    out_rng_docstr = []  # output docstring ranges
    sections_list = []
    to_insert = []
    corresp_ranges_docstr = find_range_matching(
        ranges_def=ranges_def,
        ranges_docstr=ranges_docstr,
        lines=lines,
    )
    for rng_def, rng_docstr in zip(ranges_def, corresp_ranges_docstr):
        if rng_docstr == [-1, -1]:
            if add_missing:
                # No docstring: add one
                lines_docstr = ["\n"]
                out_rng_docstr.append([rng_def[1], rng_def[1] + 1])
                to_insert.append(True)
            else:
                continue
        else:
            lines_docstr = lines[rng_docstr[0] : rng_docstr[1]]
            out_rng_docstr.append(rng_docstr)
            to_insert.append(False)
        lines_def = lines[rng_def[0] : rng_def[1]]
        sections = parse_all(lines_docstr)
        sections = merge_docstr_signature(sections, lines_def)
        sections_list.append(sections)
    # Case class docstring
    for range_docstr in ranges_docstr:
        if (
            range_docstr not in corresp_ranges_docstr
            and "class" in lines[range_docstr[0] - 1]
        ):
            lines_docstr = lines[range_docstr[0] : range_docstr[1]]
            out_rng_docstr.append(range_docstr)
            to_insert.append(False)
            sections = parse_all(lines_docstr)
            sections_list.append(sections)
    clean_empty_sections(sections_list)
    return out_rng_docstr, sections_list, to_insert


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

        * _title (List[str])
        * _parameters (List[Dict])
        * _returns (List[Dict])
        * _attributes (List[Dict])
        * _raises (List[Dict])
        * any other section name found in the docstring (List[str])

    Examples
    --------
    One can parse a docstring as follows:

    .. code-block:: python

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
            section = clean_empty_param_section(section)
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


def clean_empty_param_section(sections: List[dict]) -> List[dict]:
    """Clean empty param dict."""
    new_sections = []
    for param_dict in sections:
        if not all(param_dict[key] in (None, "", False, []) for key in param_dict):
            new_sections.append(param_dict)
    return new_sections


def clean_empty_sections(sections_list: List[dict]) -> None:
    """Clean empty param section."""
    for sections in sections_list:
        items = list(sections.items())
        for key, value in items:
            if not value and key.startswith("_") and key not in ("_title", "_escaped"):
                sections.pop(key)
