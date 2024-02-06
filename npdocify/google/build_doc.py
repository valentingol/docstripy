"""Docstring building functions for numpy style."""

from typing import Any, Dict, List

from npdocify.line_break import line_break
from npdocify.lines_routines import remove_eol


def build_doc_google(sections_dict: Dict[str, Any], indent: int) -> List[str]:
    """Build docstring for google style."""
    docstring = sections_dict["_title"]
    docstring[0] = '"""' + docstring[0]
    if len(sections_dict) == 1 and len(docstring) == 1:
        docstring[0] += '"""'
        return docstring
    section_to_header = {
        "_parameters": "Args:",
        "_raises": "Raises:",
        "_returns": "Returns:",
        "_attributes": "Attributes:",
    }
    for section_name in ("_parameters", "_raises", "_returns", "_attributes"):
        if section_name in sections_dict:
            docstring.append("\n")
            header = section_to_header[section_name]
            docstring.append(header + "\n")
            doc_params = build_section_params_google(
                sections_dict[section_name],
                indent=indent,
            )
            docstring.extend(doc_params)
    for section_name in sections_dict:
        if not section_name.startswith("_"):
            docstring.append("\n")
            docstring.append(section_name + ":\n")
            docstring.extend(sections_dict[section_name])
    docstring.append('"""\n')
    return docstring


def build_section_params_google(param_dicts: List[dict], indent: int) -> List[str]:
    """Build parameters, returns, raises, and attributes sections for google style."""
    docstring = []
    for param_dict in param_dicts:
        param_docstring = []
        first_line = ""
        if "name" in param_dict:
            first_line += param_dict["name"]
        if "type" in param_dict:
            if "name" in param_dict:
                first_line += " ("
            first_line += param_dict["type"]
            if "optional" in param_dict:
                first_line += ", optional"
            if "name" in param_dict:
                first_line += ")"
        first_line += ":"
        if "description" in param_dict and len(param_dict["description"]) > 0:
            first_line += " " + param_dict["description"][0].rstrip("\n")
        param_docstring.append(first_line + "\n")
        if "description" in param_dict and len(param_dict["description"]) > 1:
            param_docstring.extend(param_dict["description"][1:])
        if "default" in param_dict:
            if "description" not in param_dict:
                line = "Defaults to " + param_dict["default"] + ".\n"
                param_docstring.append(line)
            else:
                param_docstring[-1] = param_docstring[-1].rstrip("\n")
                param_docstring[-1] += " Defaults to " + param_dict["default"] + ".\n"
        param_docstring = remove_eol(param_docstring)
        param_docstring = line_break(param_docstring, 88 - indent * 3)
        for i, line in enumerate(param_docstring):
            if i > 0:
                param_docstring[i] = " " * indent + line
            param_docstring[i] += "\n"
        # Global indentation
        param_docstring = [" " * indent + line for line in param_docstring]
        docstring.extend(param_docstring)
    return docstring
