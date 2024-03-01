"""Test docstring building."""

import pytest
import pytest_check as check

from docstripy.build_doc.main_builder import build_docstring


@pytest.fixture()
def sections_dict() -> dict:
    """Return sections_dict."""
    sections_dict = {
        "_escaped": True,
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
            "This is an example.\n",
            ">>> function(1, '\\n')\n",
            "0\n",
            "\n",
            "This is another example.\n",
            ">>> function(2, '\\n')\n",
            "0\n",
        ],
        "Notes": ["This is a note.\n"],
    }
    return sections_dict


def test_build_docstring(sections_dict: dict) -> None:
    """Test build docstring for every styles."""
    with open("tests/files/docstr1.txt", "r", encoding="utf-8") as file:
        docstrings = file.readlines()
    expected_docstrs = {
        "rest": docstrings[:31],
        "google": docstrings[32:68],
        "numpy": docstrings[69:116],
    }
    docstr_config: dict = {"max_len": 76, "indent": 4}
    for style, expected_docstr in expected_docstrs.items():
        docstr_config["style"] = style
        docstring = build_docstring(
            sections=sections_dict, docstr_config=docstr_config, indent_base=0
        )
        check.equal(
            docstring,
            expected_docstr,
            f"\n**Style {style}**\n**Expected:**\n{''.join(expected_docstr)}"
            f"\n**Got:**\n{''.join(docstring)}",
        )
