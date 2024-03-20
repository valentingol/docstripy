"""Test line break."""

import pytest_check as check

from docstripy.line_break import line_break


def test_line_break() -> None:
    """Test line break."""
    lines = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n",
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n",
        "Ut enim ad minim veniam, quis nostrud. Exercitation ullamco laboris nisi\n",
        "ut aliquip ex ea commodo consequat...\n",
        "Excepteur sint occaecat cupidatat:\n",
        "- aute irure dolor\n",
        "- dolor in reprehenderit\n",
        "\n",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum!\n",
        "\n",
        "Dolore eu fugiat nulla pariatur.\n",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui\n",
        "officia deserunt mollit anim id est laborum.\n",
        "Et dolorum fuga...\n",
    ]
    expected_lines = [
        "Lorem ipsum dolor sit\n",
        "amet, consectetur adipiscing elit. Sed do eiusmod\n",
        "tempor incididunt ut labore et dolore magna\n",
        "aliqua. Ut enim ad minim veniam, quis nostrud.\n",
        "Exercitation ullamco laboris nisi ut aliquip ex ea\n",
        "commodo consequat... Excepteur sint occaecat\n",
        "cupidatat:\n",
        "- aute irure dolor\n",
        "- dolor in reprehenderit\n",
        "\n",
        "Duis aute irure dolor in reprehenderit in\n",
        "voluptate velit esse cillum!\n",
        "\n",
        "Dolore eu fugiat nulla pariatur. Excepteur sint\n",
        "occaecat cupidatat non proident, sunt in culpa qui\n",
        "officia deserunt mollit anim id est laborum.\n",
        "Et dolorum fuga...\n",
    ]
    lines = line_break(lines=lines, max_line_length=50, num_add_char=25)
    check.equal(len(lines), len(expected_lines))
    for i, line in enumerate(lines):
        check.equal(
            bytes(line, encoding="utf-8"),
            bytes(expected_lines[i], encoding="utf-8"),
            f"Error with line {i}",
        )
