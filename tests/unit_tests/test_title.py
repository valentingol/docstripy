"""Test title generation."""

import pytest_check as check

from docstripy.build_doc.preprocessing import preprocess_title_build
from docstripy.parse_doc.postprocessing import postprocess_title_parse


def test_process_title() -> None:
    """Test preprocess & postprocess title."""
    all_lines = [
        ["this is a title\n"],
        ["this is a very long title that should be split\n"],
        ["this is a title. This is a description.\n"],
        ["class.meth is method. This is a description.\n"],
        ["Title. Subtitle. Description.\n", "Another description.\n"],
        ["This is a very very very very long title. Description.\n"],
        ["This is... a title. Description.\n"],
        ["E.g a tile. Description.\n"],
        ["Title.  Description.\n"],  # 2 spaces
    ]
    expected = [
        ["This is a title.\n"],
        ["This is a very long title that\n", "should be split\n"],
        ["This is a title.\n", "\n", "This is a description.\n"],
        ["Class.meth is method.\n", "\n", "This is a description.\n"],
        ["Title.\n", "\n", "Subtitle. Description. Another\n", "description.\n"],
        ["This is a very very very very\n", "long title. Description.\n"],
        ["This is... a title.\n", "\n", "Description.\n"],
        ["E.g a tile.\n", "\n", "Description.\n"],
        ["Title.\n", "\n", "Description.\n"],
    ]
    max_len = 30
    for i, lines in enumerate(all_lines):
        lines = preprocess_title_build(lines, max_len)
        lines = postprocess_title_parse(lines)
        check.equal(lines, expected[i], f"Failed for lines at index {i}")
    long_line1 = [
        (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit "
            "nullam nec nunc nec nunccurabitur lorem ipsum dolor sit amet ipsum dolor. "
            "Description.\n"
        )
    ]
    lines1 = preprocess_title_build(long_line1, 0)
    lines1 = postprocess_title_parse(lines1)
    check.equal(
        lines1,
        [long_line1[0]],
    )
    long_line2 = [
        (
            "Lorem ipsum dolor sit amet. Consectetur adipiscing elit "
            "nullam nec nunc nec nunccurabitur lorem ipsum dolor sit amet ipsum dolor. "
            "Description.\n"
        )
    ]
    lines2 = preprocess_title_build(long_line2, 0)
    lines2 = postprocess_title_parse(lines2)
    check.equal(
        lines2,
        [long_line2[0][:27] + "\n", "\n", long_line2[0][28:]],
    )
