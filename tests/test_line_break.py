"""Test line break."""

import pytest_check as check

from docstripy.line_break import line_break


def test_line_break() -> None:
    """Test line break."""
    lines = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi\n",
        "ut aliquip ex ea commodo consequat.\n",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum\n",
        "\n",
        "dolore eu fugiat nulla pariatur.\n",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui\n",
        "officia deserunt mollit anim id est laborum.\n",
    ]
    expected_lines = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing\n",
        "elit. Sed do eiusmod tempor incididunt ut labore\n",
        "et dolore magna aliqua. Ut enim ad minim veniam,\n",
        "quis nostrud exercitation ullamco laboris nisi ut\n",
        "aliquip ex ea commodo consequat. Duis aute irure\n",
        "dolor in reprehenderit in voluptate velit esse\n",
        "cillum\n",
        "\n",
        "dolore eu fugiat nulla pariatur.\n",
        "Excepteur sint occaecat cupidatat non proident,\n",
        "sunt in culpa qui officia deserunt mollit anim id\n",
        "est laborum.\n",
    ]
    lines = line_break(lines, 50)
    check.equal(len(lines), len(expected_lines))
    for i, line in enumerate(lines):
        check.equal(
            bytes(line, encoding="utf-8"),
            bytes(expected_lines[i], encoding="utf-8"),
            f"Error with line {i}",
        )
