"""Global docstring building functions."""
from typing import Dict, List

from npdocify.google.build_doc import build_doc_google
from npdocify.line_break import line_break
from npdocify.numpy.build_doc import build_doc_numpy
from npdocify.rest.build_doc import build_doc_rest


def build_docstring(
    sections: List[Dict],
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
