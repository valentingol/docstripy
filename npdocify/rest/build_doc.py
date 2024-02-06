"""Docstring building functions for numpy style."""

from typing import Any, Dict, List

from npdocify.line_break import line_break
from npdocify.lines_routines import remove_eol


def build_doc_rest(sections_dict: Dict[str, Any], indent: int) -> List[str]:
    """Build docstring for rest style."""
    docstring = sections_dict["_title"]
    docstring[0] = '"""' + docstring[0]
    if len(sections_dict) == 1 and len(docstring) == 1:
        docstring[0] += '"""'
        return docstring
    for section_name in ("_parameters", "_attributes", "_raises", "_returns"):
        if section_name in sections_dict:
            doc_params = build_section_params_rest(
                sections_dict[section_name],
                indent=indent,
                section_name=section_name,
            )
            docstring.extend(doc_params)
    for section_name in sections_dict:
        if not section_name.startswith("_"):
            docstring.append("\n")
            docstring.append(section_name + ":\n")
            docstring.extend(sections_dict[section_name])
    docstring.append('"""\n')
    return docstring


def build_section_params_rest(
    param_dicts: List[dict],
    indent: int,
    section_name: str,
) -> List[str]:
    """Build parameters, returns, raises, and attributes sections for google style."""
    docstring = []
    name_to_keyword = {
        "_parameters": ("param", "type"),
        "_raises": ("raises", ""),
        "_returns": ("return", "rtype"),
        "_attributes": ("atribute", "type"),
    }
    keyword, type_keyword = name_to_keyword[section_name]
    for param_dict in param_dicts:
        param_docstring = []
        first_line = ""
        if "name" in param_dict or "description" in param_dict:
            if "name" in param_dict:
                first_line = f":{keyword} {param_dict['name']}:"
            else:
                first_line = f":{keyword}:"
        if "description" in param_dict and len(param_dict["description"]) > 0:
            first_line += " " + param_dict["description"][0].rstrip("\n")
        if first_line:
            param_docstring.append(first_line + "\n")
        if "description" in param_dict and len(param_dict["description"]) > 1:
            param_docstring.extend(param_dict["description"][1:])
        if "default" in param_dict:
            if "description" not in param_dict:
                line = "Defaults to " + param_dict["default"] + ".\n"
                param_docstring.append(line)
            else:
                param_docstring[-1] = param_docstring[-1].rstrip("\n")
                param_docstring[-1] += ", defaults to " + param_dict["default"] + ".\n"
        param_docstring = remove_eol(param_docstring)
        param_docstring = line_break(param_docstring, 88 - indent * 2)
        for i, line in enumerate(param_docstring):
            if not line.startswith(":"):
                param_docstring[i] = " " * indent + line
            param_docstring[i] += "\n"
        if "type" in param_dict:
            if "name" in param_dict:
                line = f":{type_keyword} {param_dict['name']}:"
            else:
                line = f":{type_keyword}:"
            line += " " + param_dict["type"]
            if "optional" in param_dict:
                line += ", optional"
            param_docstring.append(line + "\n")
        docstring.extend(param_docstring)
    return docstring


if __name__ == "__main__":
    sections_dict = {
        "_title": ["This is a title.\n", "\n", "This is a subtitle.\n"],
        "_parameters": [
            {
                "name": "param1",
                "type": ":obj:`int`",
                "description": [
                    "This is a parameter.\n",
                    "The description can be multiline, and it can be very very long. "
                    "Even longer than this.\n",
                    "\n",
                    "And it can have a default value.\n",
                    "The default value can be very long too. It is an int, and it was "
                    "discovered by a very long process.\n",
                ],
                "optional": True,
                "default": "0",
            },
            {
                "name": "param2",
                "type": "str",
                "description": ["This is another parameter.\n"],
                "optional": True,
                "default": "''",
            },
        ],
        "_raises": [
            {
                "name": "ValueError",
                "description": ["If something goes wrong.\n"],
            }
        ],
        "_returns": [
            {
                "type": "int",
            },
            {
                "name": "result2",
                "type": "str",
                "description": ["The second result.\n"],
            },
        ],
        "_attributes": [
            {
                "name": "attr1",
                "type": "int",
                "description": ["This is an attribute.\n"],
                "default": "0",
            },
        ],
        "Example": [
            "    This is an example.\n",
            ">>> function(1, 'a')\n",
            "0\n",
            "\n",
            "    This is another example.\n",
            ">>> function(2, 'b')\n",
            "0\n",
        ],
        "Notes": ["    This is a note.\n"],
    }
    docstring = build_doc_rest(sections_dict, 4)
    docstring_str = "".join(docstring)
