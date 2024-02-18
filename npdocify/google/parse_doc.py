"""Parser for Google style docstrings."""

import re
from typing import Dict, List

from npdocify.lines_routines import find_prefix, remove_indent


def parse_params(lines: List[str], section_name: str) -> List[dict]:
    """Parse parameter section from Google format.

    Parameters
    ----------
    lines : List[str]
        Lines of docstring.
    section_name : str, optional
        Name of the section, one of "param", "return", "attribute", "raises".
    """
    # Find indentation
    if len(lines) < 2:
        return []
    # Skip the first line
    lines = lines[1:]
    lines = remove_indent(lines)
    params_list: List[dict] = []
    for line in lines:
        if not line.startswith(" ") and line.strip() != "":
            split_dots = re.split(r":\s|\n", line, maxsplit=1)
            param_name_type_opt = split_dots[0].strip()
            if "(" in param_name_type_opt:
                split_parenthesis = param_name_type_opt.split("(", maxsplit=1)
                param_name = split_parenthesis[0].strip()
                type_opt = split_parenthesis[1].split(")")[0].strip()
                if ", optional" in type_opt:
                    type_p = type_opt[:-10].strip()
                    optional = True
                elif "optional" in type_opt:
                    type_p = type_opt[:-8].strip()
                    optional = True
                else:
                    type_p = type_opt.strip()
                    optional = False
            else:
                param_name = param_name_type_opt.strip()
                type_p = ""
                optional = False  # by default
            params_list.append({})
            params_list[-1]["name"] = param_name
            params_list[-1]["type"] = type_p
            params_list[-1]["optional"] = optional
            params_list[-1]["description"] = []
            if len(split_dots) > 1:
                description = split_dots[1].lstrip()
                # Indent the first line of the description like other lines
                params_list[-1]["description"] = [description]
        elif len(params_list) > 0:
            params_list[-1]["description"].extend(remove_indent([line]))
    if section_name in ("return", "yield"):
        # When param_dict["type"] == "", it means that the name of the
        # return is not specified and param_dict["name"] is actually
        # the type.
        for param_dict in params_list:
            if param_dict["type"] == "":
                type_p = param_dict["name"]
                param_dict["name"] = param_dict["type"]
                param_dict["type"] = type_p
    return params_list


def parse_sections_ranges(lines: List[str]) -> Dict:
    """Parse google sections of a docstring."""
    params_start, params_end = find_prefix(
        lines, ("Arg:", "Args:", "Param:", "Params:"), ("\n", " ")
    )
    raises_start, raises_end = find_prefix(lines, ("Raise:", "Raises:"), ("\n", " "))
    returns_start, returns_end = find_prefix(
        lines, ("Return:", "Returns:"), ("\n", " ")
    )
    yields_start, yields_end = find_prefix(lines, ("Yields:", "Yield:"), ("\n", " "))
    attr_start, attr_end = find_prefix(
        lines, ("Attributes:", "Attribute:"), ("\n", " ")
    )
    return {
        "_parameters": [params_start, params_end],
        "_raises": [raises_start, raises_end],
        "_returns": [returns_start, returns_end],
        "_yields": [yields_start, yields_end],
        "_attributes": [attr_start, attr_end],
    }


def parse_wild_sections_ranges(lines: List[str]) -> Dict:
    """Parse wild sections of a docstring from google format."""
    sec_ranges = {}
    known_sections = [
        "parameter",
        "return",
        "raise",
        "arg",
        "attribute",
        "yield",
    ]
    known_sections += [f"{name}s" for name in known_sections]  # variations with s
    for i, line in enumerate(lines):
        if is_define_section(line):
            section_name = line[:-2].strip()
            if section_name.lower() not in known_sections:
                sec_ranges[section_name] = [i]
    for section_name in sec_ranges:
        start, _ = find_prefix(lines, (section_name,), ())
        sec_ranges.update({f"{section_name}": [start, -1]})
    return sec_ranges


def is_define_section(line: str) -> bool:
    """Check if a line define a Google wild section or not."""
    if not line or not line.endswith(":\n"):
        return False
    ord_n = ord(line[0])
    if not 65 <= ord_n <= 90:
        return False
    short_line = line[:-2].strip()
    if " " in short_line:
        # Multiple words
        return False
    return True
