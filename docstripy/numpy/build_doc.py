"""Docstring building functions for numpy style."""

from typing import Any, Dict, List

from docstripy.line_break import line_break
from docstripy.lines_routines import clean_trailing_empty, clean_trailing_spaces


def build_doc_numpy(
    current_docstring: List[str],
    sections_dict: Dict[str, Any],
    max_len: int,
    indent: int,
) -> List[str]:
    """Build docstring for numpy style."""
    docstring = current_docstring.copy()
    for section_name in (
        "_parameters",
        "_raises",
        "_returns",
        "_yields",
        "_attributes",
    ):
        if section_name in sections_dict and sections_dict[section_name]:
            docstr_sec = []
            header = section_name[1:].capitalize()
            docstr_sec.append("\n")
            docstr_sec.append(header + "\n")
            docstr_sec.append("-" * len(header) + "\n")
            doc_params = build_section_params_numpy(
                sections_dict[section_name],
                max_len=max_len,
                indent=indent,
            )
            if clean_trailing_empty(doc_params):
                docstr_sec.extend(doc_params)
                docstring.extend(docstr_sec)
            else:
                # Error if empty sections
                raise ValueError(f"Empty section found (section {section_name[1:]}).")
    for section_name in sections_dict:
        if not section_name.startswith("_"):
            docstring.append("\n")
            docstring.append(section_name + "\n")
            docstring.append("-" * len(section_name) + "\n")
            docstring.extend(
                line_break(
                    sections_dict[section_name],
                    max_line_length=max_len,
                )
            )
    docstring.append('"""\n')
    docstring = clean_trailing_spaces(docstring)
    return docstring


def build_section_params_numpy(
    param_dicts: List[dict],
    max_len: int,
    indent: int,
) -> List[str]:
    """Build parameters, returns, raises, and attributes sections for numpy style."""
    docstring = []
    for param_dict in param_dicts:
        param_docstring = []
        first_line = ""
        if "name" in param_dict and param_dict["name"]:
            first_line += param_dict["name"] + " : "
        if "type" in param_dict and param_dict["type"]:
            first_line += param_dict["type"]
            if "optional" in param_dict and param_dict["optional"]:
                first_line += ", optional"
        if "description" in param_dict and param_dict["description"]:
            param_docstring.extend(param_dict["description"])
        if "default" in param_dict and param_dict["default"]:
            if (
                not param_docstring
                or "description" not in param_dict
                or (max_len > 0 and len(param_docstring[-1]) > max_len * 0.75)
            ):
                line = "By default, " + param_dict["default"] + ".\n"
                param_docstring.append(line)
            else:
                param_docstring[-1] = param_docstring[-1].rstrip("\n")
                param_docstring[-1] += " By default, " + param_dict["default"] + ".\n"
        param_docstring = [first_line + "\n"] + line_break(
            param_docstring, max_len - indent
        )
        for i, line in enumerate(param_docstring):
            if i > 0:
                param_docstring[i] = " " * indent + line
        docstring.extend(param_docstring)
    return docstring
