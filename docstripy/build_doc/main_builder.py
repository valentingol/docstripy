"""Global docstring building functions."""

from typing import List

from docstripy.build_doc.preprocessing import preprocess_title_build
from docstripy.google.build_doc import build_doc_google
from docstripy.line_break import line_break
from docstripy.numpy.build_doc import build_doc_numpy
from docstripy.rest.build_doc import build_doc_rest


def build_docstring(
    sections: dict,
    docstr_config: dict,
    indent_base: int,
) -> List[str]:
    """Build a docstring."""
    style = docstr_config["style"]
    max_len = docstr_config["max_len"]
    indent = docstr_config["indent"]
    build_fn = {
        "numpy": build_doc_numpy,
        "google": build_doc_google,
        "rest": build_doc_rest,
    }
    sections["_title"] = preprocess_title_build(
        sections["_title"],
        max_len=max_len - indent_base,
    )
    docstring = sections["_title"].copy()
    esc_char = "r" if sections["_escaped"] else ""
    docstring[0] = esc_char + '"""' + docstring[0]
    if len(sections) == 2 and len(docstring) == 1:  # one-line docstring
        docstring = line_break([docstring[0]], max_len - 6)
        if len(docstring) == 1:  # already one-line docstring after break
            docstring[0] = docstring[0][:-1] + '"""\n'
            return docstring
    docstring = build_fn[style](
        current_docstring=docstring,
        sections_dict=sections,
        max_len=max_len - indent_base,
        indent=indent,
    )
    return docstring
