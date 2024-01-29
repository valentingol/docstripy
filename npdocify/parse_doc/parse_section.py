"""Parse sections."""
from typing import Dict, List

from npdocify.lines_routines import find_prefix, remove_indent


def clean_section_ranges(ranges: Dict) -> Dict:
    """Clean section ranges."""
    items = list(ranges.items())
    for name, rng in items:
        # Remove empty section
        if rng[0] == -1:
            del ranges[name]
    return ranges


def delimit_section_ranges(ranges: Dict, last_ind: int) -> Dict:
    """Delimit section ranges."""
    starts = sorted([rng[0] for rng in ranges.values()])
    for rng in ranges.values():
        if rng[1] == -1:
            ind_sec = starts.index(rng[0])
            end = last_ind if ind_sec == len(starts) - 1 else starts[ind_sec + 1]
            rng[1] = end
    return ranges


def parse_sections(lines: List[str]) -> Dict:
    """Parse sections of a docstring."""
    indent = 0
    while lines[0][indent] == " ":
        indent += 1
    lines = remove_indent(lines, indent)
    # NOTE: order reST -> numpy -> google (each section overrides
    # the previous one in case of conflict)
    sec_ranges = {}
    for parse_func in (
        parse_rest_sections,
        parse_numpy_sections,
        parse_google_sections,
    ):
        ranges = parse_func(lines)
        ranges = clean_section_ranges(ranges)
        sec_ranges.update(ranges)
    sec_ranges.update(parse_wild_sections(lines))
    sec_ranges = delimit_section_ranges(sec_ranges, len(lines))
    return sec_ranges


def parse_google_sections(lines: List[str]) -> Dict:
    """Parse google sections of a docstring."""
    params_start, params_end = find_prefix(
        lines, ("Arg:", "Args:", "Param:", "Params:"), ("\n", " ")
    )
    raises_start, raises_end = find_prefix(lines, ("Raise:", "Raises:"), ("\n", " "))
    returns_start, returns_end = find_prefix(
        lines, ("Return:", "Returns:"), ("\n", " ")
    )
    return {
        "_parameters": [params_start, params_end],
        "_raises": [raises_start, raises_end],
        "_returns": [returns_start, returns_end],
    }


def parse_numpy_sections(lines: List[str]) -> Dict:
    """Parse numpy sections of a docstring."""
    params_start, _ = find_prefix(lines, ("Parameters", "Parameter"), (), dash=True)
    raises_start, _ = find_prefix(lines, ("Raises", "Raise"), (), dash=True)
    returns_start, _ = find_prefix(lines, ("Returns", "Return"), (), dash=True)
    return {
        "_parameters": [params_start, -1],
        "_raises": [raises_start, -1],
        "_returns": [returns_start, -1],
    }


def parse_rest_sections(lines: List[str]) -> Dict:
    """Parse reStructuredText sections to the docstring."""
    params_start, params_end = find_prefix(
        lines, (":param",), (":param", ":type", "\n", " ")
    )
    raises_start, raises_end = find_prefix(lines, (":raises",), (":raises", "\n", " "))
    returns_start, returns_end = find_prefix(
        lines, (":return",), (":return", ":rtype", "\n", " ")
    )
    return {
        "_parameters": [params_start, params_end],
        "_raises": [raises_start, raises_end],
        "_returns": [returns_start, returns_end],
    }


def parse_wild_sections(lines: List[str]) -> Dict:
    """Parse wild sections of a docstring."""
    sec_ranges = {}
    known_sections = [
        "parameter",
        "return",
        "raise",
        "arg",
    ]
    known_sections += [f"{name}s" for name in known_sections]  # add 's'
    for i, line in enumerate(lines):
        if not line.startswith(" ") and line.endswith(":\n"):
            section_name = line[:-2].strip()
            if section_name.lower() not in known_sections:
                sec_ranges[section_name] = [i]
    for section_name in sec_ranges:
        start, _ = find_prefix(lines, (section_name,), ())
        return {f"{section_name}": [start, -1]}
    return sec_ranges
