"""Parser for ReST style docstrings."""

import re
from typing import Dict, List

from docstripy.lines_routines import find_prefix, remove_indent


def parse_params(
    lines: List[str], section_name: str = "param", pattern_type: str = "type"
) -> List[dict]:
    """Parse parameter section from reStructuredText format.

    Parameters
    ----------
    lines : List[str]
        Lines of docstring.
    section_name : str, optional
        Name of the section, one of "param", "return", "attribute", "raises".
        It is also the pattern before element name for description:
        `:<pattern> name: <description>`. By default, "param".
    pattern_type : str, optional
        Pattern before element name for type: `:<pattern> name: <type>`.
        By default, "type".
    """
    params_list: List[dict] = []
    len_pattern_1 = len(":" + section_name)
    len_pattern_2 = len(":" + pattern_type)
    for line in lines:
        if line.startswith(":" + section_name):
            split_dots = re.split(r":\s|\n", line[len_pattern_1:], maxsplit=1)
            param_name = split_dots[0].strip()
            description = split_dots[1].lstrip() if len(split_dots) > 1 else ""
            params_list.append({})
            params_list[-1]["name"] = param_name
            params_list[-1]["type"] = ""  # by default
            params_list[-1]["optional"] = False  # by default
            params_list[-1]["description"] = []
            if description not in ("", "\n"):
                params_list[-1]["description"] = [description]
        elif line.startswith(":" + pattern_type):
            split_dots = re.split(r":\s|\n", line[len_pattern_2:], maxsplit=1)
            param_name = split_dots[0].strip()
            type_p = split_dots[1].strip() if len(split_dots) > 1 else ""
            if type_p.endswith(", optional"):
                type_p = type_p[:-10].strip()
                optional = True
            elif type_p.endswith("optional"):
                type_p = type_p[:-8].strip()
                optional = True
            else:
                type_p = type_p.strip()
                optional = False
            if len(params_list) == 0 or params_list[-1]["type"] != "":
                # New param without description
                params_list.append({})
                params_list[-1]["name"] = param_name
                params_list[-1]["description"] = []
            params_list[-1]["type"] = type_p
            params_list[-1]["optional"] = optional
        elif len(params_list) > 0:
            params_list[-1]["description"].extend(remove_indent([line]))
    return params_list


def parse_sections_ranges(lines: List[str]) -> Dict:
    """Parse reStructuredText sections to the docstring."""
    params_start, params_end = find_prefix(
        lines, (":param", ":type"), (":param", ":type", "\n", " ")
    )
    raises_start, raises_end = find_prefix(lines, (":raises",), (":raises", "\n", " "))
    returns_start, returns_end = find_prefix(
        lines, (":return", ":rtype"), (":return", ":rtype", "\n", " ")
    )
    yields_start, yields_end = find_prefix(
        lines, (":yield",), (":yield", ":rtype", "\n", " ")
    )
    attr_start, attr_end = find_prefix(
        lines, (":attribute",), (":attribute", ":type", "\n", " ")
    )
    return {
        "_parameters": [params_start, params_end],
        "_raises": [raises_start, raises_end],
        "_returns": [returns_start, returns_end],
        "_yields": [yields_start, yields_end],
        "_attributes": [attr_start, attr_end],
    }
