"""Docstring building functions for numpy style."""

from typing import Any, Dict, List

from docstripy.line_break import line_break
from docstripy.lines_routines import add_indent, clean_trailing_spaces


def build_doc_google(
    current_docstring: List[str],
    sections_dict: Dict[str, Any],
    max_len: int,
    indent: int,
) -> List[str]:
    """Build docstring for google style."""
    docstring = current_docstring.copy()
    section_to_header = {
        "_parameters": "Args:",
        "_raises": "Raises:",
        "_returns": "Returns:",
        "_attributes": "Attributes:",
    }
    for section_name in (
        "_parameters",
        "_raises",
        "_returns",
        "_yields",
        "_attributes",
    ):
        if section_name in sections_dict and sections_dict[section_name]:
            docstring.append("\n")
            header = section_to_header[section_name]
            docstring.append(header + "\n")
            doc_params = build_section_params_google(
                sections_dict[section_name],
                max_len=max_len,
                indent=indent,
            )
            docstring.extend(doc_params)
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


def build_section_params_google(
    param_dicts: List[dict],
    max_len: int,
    indent: int,
) -> List[str]:
    """Build parameters, returns, raises, and attributes sections for google style."""
    docstring = []
    for param_dict in param_dicts:
        param_docstring = []
        first_line = ""
        if "name" in param_dict and param_dict["name"]:
            first_line += param_dict["name"]
        if "type" in param_dict and param_dict["type"]:
            if "name" in param_dict and param_dict["name"]:
                first_line += " ("
            first_line += param_dict["type"]
            if "optional" in param_dict and param_dict["optional"]:
                first_line += ", optional"
            if "name" in param_dict and param_dict["name"]:
                first_line += ")"
        first_line += ":"
        if "description" in param_dict and len(param_dict["description"]) > 0:
            first_line += " " + param_dict["description"][0].rstrip("\n")
        param_docstring.append(first_line + "\n")
        if "description" in param_dict and len(param_dict["description"]) > 1:
            param_docstring.extend(param_dict["description"][1:])
        if "default" in param_dict and param_dict["default"]:
            if "description" not in param_dict:
                line = "Defaults to " + param_dict["default"] + ".\n"
                param_docstring.append(line)
            else:
                param_docstring[-1] = param_docstring[-1].rstrip("\n")
                param_docstring[-1] += " Defaults to " + param_dict["default"] + ".\n"
        param_docstring = line_break(param_docstring, max_len - 2 * indent)
        for i, line in enumerate(param_docstring):
            if i > 0 and line.strip():
                param_docstring[i] = " " * indent + line
        # Global indentation
        param_docstring = [" " * indent + line for line in param_docstring]
        docstring.extend(param_docstring)
    return docstring
