"""Docstring building functions for numpy style."""

from typing import Any, Dict, List

from docstripy.line_break import line_break
from docstripy.lines_routines import (
    add_indent,
    clean_trailing_empty,
    clean_trailing_spaces,
)


def build_doc_rest(
    current_docstring: List[str],
    sections_dict: Dict[str, Any],
    max_len: int,
    indent: int,
    *,
    include_type: bool = True,
) -> List[str]:
    """Build docstring for rest style."""
    docstring = current_docstring.copy()
    for section_name in (
        "_parameters",
        "_raises",
        "_returns",
        "_yields",
        "_attributes",
    ):
        if section_name in sections_dict and sections_dict[section_name]:
            doc_params = build_section_params_rest(
                sections_dict[section_name],
                max_len=max_len,
                indent=indent,
                section_name=section_name,
                include_type=include_type,
            )
            if clean_trailing_empty(doc_params):
                docstring.extend(doc_params)
            else:
                # Error if empty sections
                raise ValueError(f"Empty section found (section {section_name[1:]}).")
    for section_name in sections_dict:
        if not section_name.startswith("_"):
            docstring.append("\n")
            docstring.append(section_name + ":\n")
            section_content = line_break(
                sections_dict[section_name],
                max_line_length=max_len - indent,
            )
            docstring.extend(add_indent(section_content, indent))
    docstring.append('"""\n')
    docstring = clean_trailing_spaces(docstring)
    return docstring


def build_section_params_rest(
    param_dicts: List[dict],
    max_len: int,
    indent: int,
    section_name: str,
    *,
    include_type: bool = True,
) -> List[str]:
    """Build parameters, returns, raises, and attributes sections for google style."""
    docstring = []
    name_to_keyword = {
        "_parameters": ("param", "type"),
        "_raises": ("raises", ""),
        "_returns": ("return", "rtype"),
        "_attributes": ("ivar", "type"),
        "_yields": ("yield", "rtype"),
    }
    keyword, type_keyword = name_to_keyword[section_name]
    for param_dict in param_dicts:
        param_docstring = []
        first_line = ""
        if ("name" in param_dict and param_dict["name"]) or (
            "description" in param_dict and param_dict["description"]
        ):
            if "name" in param_dict and param_dict["name"]:
                first_line = f":{keyword} {param_dict['name']}:"
            else:
                first_line = f":{keyword}:"
        if "description" in param_dict and param_dict["description"]:
            first_line += " " + param_dict["description"][0].rstrip("\n")
        if first_line:
            param_docstring.append(first_line + "\n")
        if "description" in param_dict and len(param_dict["description"]) > 1:
            param_docstring.extend(param_dict["description"][1:])
        if "default" in param_dict and param_dict["default"]:
            if "description" not in param_dict:
                line = "Defaults to " + param_dict["default"] + ".\n"
                param_docstring.append(line)
            else:
                param_docstring[-1] = param_docstring[-1].rstrip("\n")
                param_docstring[-1] = param_docstring[-1].rstrip(".")
                param_docstring[-1] += ", defaults to " + param_dict["default"] + ".\n"
        param_docstring = line_break(param_docstring, max_len - indent)
        for i, line in enumerate(param_docstring):
            if not line.startswith(":") and line.strip():
                param_docstring[i] = " " * indent + line
        if include_type and "type" in param_dict and param_dict["type"]:
            if "name" in param_dict and param_dict["name"]:
                line = f":{type_keyword} {param_dict['name']}:"
            else:
                line = f":{type_keyword}:"
            line += " " + param_dict["type"]
            if "optional" in param_dict and param_dict["optional"]:
                line += ", optional"
            param_docstring.append(line + "\n")
        docstring.extend(param_docstring)
    return docstring
