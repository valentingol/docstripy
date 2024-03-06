"""Parser for Numpy style docstrings."""

import re
from typing import Dict, List

from docstripy.lines_routines import find_prefix, remove_indent


def parse_params(lines: List[str], section_name: str = "param") -> List[dict]:
    """Parse parameter section from Numpy format.

    Parameters
    ----------
    lines : List[str]
        Lines of docstring.
    section_name : str, optional
        Name of the section, one of "param", "return", "attribute", "raises".
        By default, "param".
    """
    # Skip the 2 first lines
    lines = lines[2:]
    params_list: List[dict] = []
    for line in lines:
        if not line.startswith(" ") and line.strip() != "":
            split_dots = re.split(r":\s|\n", line, maxsplit=1)
            param_name = split_dots[0].strip()
            type_p, optional = "", False  # by default
            if len(split_dots) > 1:
                type_p = split_dots[1].strip()
                if type_p.endswith(", optional"):
                    type_p = type_p[:-10].strip()
                    optional = True
                elif type_p.endswith("optional"):
                    type_p = type_p[:-8].strip()
                    optional = True
                else:
                    type_p = type_p.strip()
                    optional = False
            params_list.append({})
            params_list[-1]["name"] = param_name
            params_list[-1]["description"] = []
            params_list[-1]["type"] = type_p
            params_list[-1]["optional"] = optional
        elif len(params_list) > 0:
            params_list[-1]["description"].append(line)
    for param_dict in params_list:
        param_dict["description"] = remove_indent(param_dict["description"])
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
    """Parse numpy sections of a docstring."""
    params_start, _ = find_prefix(lines, ("Parameters", "Parameter"), (), dash=True)
    raises_start, _ = find_prefix(lines, ("Raises", "Raise"), (), dash=True)
    returns_start, _ = find_prefix(lines, ("Returns", "Return"), (), dash=True)
    yields_start, _ = find_prefix(lines, ("Yields", "Yield"), (), dash=True)
    attr_start, _ = find_prefix(lines, ("Attributes", "Attribute"), (), dash=True)
    return {
        "_parameters": [params_start, -1],
        "_raises": [raises_start, -1],
        "_returns": [returns_start, -1],
        "_yields": [yields_start, -1],
        "_attributes": [attr_start, -1],
    }


def parse_wild_sections_ranges(lines: List[str]) -> Dict:
    """Parse wild sections of a docstring from numpy format."""
    sec_ranges = {}
    known_sections = [
        "parameter",
        "return",
        "raise",
        "arg",
        "attribute",
        "yield",
    ]
    known_sections += [f"{name}s" for name in known_sections]  # add 's'
    for i, line in enumerate(lines):
        if (
            not line.startswith(" ")
            and len(lines) > i + 1
            and lines[i + 1].startswith("---")
        ):
            section_name = line[:-1].strip()
            if section_name.lower() not in known_sections:
                sec_ranges[section_name] = [i]
    for section_name in sec_ranges:
        start, _ = find_prefix(lines, (section_name,), ())
        sec_ranges.update({f"{section_name}": [start, -1]})
    return sec_ranges
