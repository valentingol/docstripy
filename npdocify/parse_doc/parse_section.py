"""Parse sections."""
from typing import Dict, List


def parse_section(lines: List[str]) -> Dict:
    """Parse sections of a docstring."""
    i = 0
    # NOTE: work for 4 spaces indent
    while lines[0][i] == " ":
        i += 1
    indent = i // 4
    # Remove
    title = lines[0].strip()[3:]

