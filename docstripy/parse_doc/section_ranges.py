"""Parse sections."""
from typing import Dict, List, Tuple

from docstripy.google.parse_doc import (
    parse_sections_ranges as parse_google_sections_ranges,
)
from docstripy.google.parse_doc import (
    parse_wild_sections_ranges as parse_wild_sections_google_ranges,
)
from docstripy.lines_routines import remove_indent
from docstripy.numpy.parse_doc import (
    parse_sections_ranges as parse_numpy_sections_ranges,
)
from docstripy.numpy.parse_doc import (
    parse_wild_sections_ranges as parse_wild_sections_numpy_ranges,
)
from docstripy.rest.parse_doc import parse_sections_ranges as parse_rest_sections_ranges


def parse_sections_ranges(lines: List[str]) -> Tuple[Dict, str]:
    """Parse sections of a docstring and detect docstring style.

    Parameters
    ----------
    lines : List[str]
        Lines of the docstring.

    Returns
    -------
    sec_ranges : Dict
        Section ranges.
        Example: {'_title': [0, 2], '_parameters': [3, 5], "Note": [6, 9]}
    style : str
        Style of the docstring (one of 'numpy', 'google' or 'rest').

    """
    lines = remove_indent(lines)
    sec_ranges = {"_title": [0, -1]}
    parse_funcs = {
        "google": parse_google_sections_ranges,
        "rest": parse_rest_sections_ranges,
        "numpy": parse_numpy_sections_ranges,
    }
    style = "numpy"
    # NOTE: order google -> rest -> numpy (each section overrides
    # the previous one in case of conflict). The style is
    # determine in this order, overriding previous ones. Default numpy.
    for style_name in ("google", "rest", "numpy"):
        ranges = parse_funcs[style_name](lines)
        ranges = clean_section_ranges(ranges)
        if len(ranges) > 0:
            style = style_name
        sec_ranges.update(ranges)
    if style == "numpy":  # Found numpy section(s) => numpy-doc style
        sec_ranges.update(parse_wild_sections_numpy_ranges(lines))
    else:
        sec_ranges.update(parse_wild_sections_google_ranges(lines))
    sec_ranges = delimit_section_ranges(sec_ranges, len(lines))
    return sec_ranges, style


def clean_section_ranges(ranges: Dict) -> Dict:
    """Clean section ranges.

    If a section is empty, remove it.
    """
    items = list(ranges.items())
    for name, rng in items:
        # Remove empty section
        if rng[0] == -1:
            del ranges[name]
    return ranges


def delimit_section_ranges(ranges: Dict, last_ind: int) -> Dict:
    """Delimit section ranges.

    Determine the end of each section if not already found.
    """
    starts = sorted([rng[0] for rng in ranges.values()])
    for rng in ranges.values():
        if rng[1] == -1:
            ind_sec = starts.index(rng[0])
            end = last_ind if ind_sec == len(starts) - 1 else starts[ind_sec + 1]
            rng[1] = end
    return ranges
