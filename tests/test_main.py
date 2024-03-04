"""Test entry points of docstripy."""

import os
import shutil

import pytest
import pytest_check as check

from docstripy.main import write_file, write_files_recursive


def test_main() -> None:
    """Test main entry point."""
    if os.path.exists("tests/tmp"):
        shutil.rmtree("tests/tmp")
    run = os.system("docstripy --help")
    check.equal(run, 0)
    run = os.system(
        "docstripy tests/files -o tests/tmp/google -s google --len 88 --indent 2"
    )
    check.equal(run, 0)
    run = os.system(
        "docstripy tests/files -o tests/tmp/rest -s rest --len 88 --indent 2"
    )
    check.equal(run, 0)
    run = os.system(
        "docstripy tests/files -o tests/tmp/numpy -s numpy --len 88 --indent 2"
    )
    check.equal(run, 0)
    for style in ("google", "numpy", "rest"):
        path = f"tests/tmp/{style}"
        check.is_true(os.path.exists(path), f"Directory not found: {path}")
        for i in range(1, 5):
            path = f"tests/tmp/{style}/test{i}.py"
            check.is_true(os.path.exists(path), f"File not found: {path}")
    with open("tests/tmp/google/empty.py", encoding="utf-8") as file:
        lines = file.readlines()
    check.equal(lines[8], '    """Clean trailing spaces."""\n')
    if os.path.exists("tests/tmp"):
        shutil.rmtree("tests/tmp")


def test_errors(capfd: pytest.CaptureFixture) -> None:
    """Test entry point when there are files errors."""
    with pytest.raises(ValueError, match="Error found during docstring parsing."):
        write_file(
            "tests/wrong_files/file1.py",
            "tests/tmp/file1.py",
            overwrite=False,
            docstr_config={"style": "numpy", "max_len": 88, "indent": 2},
        )
    with pytest.raises(
        ValueError, match="Error found at lines 3-8 during docstring building.*"
    ):
        write_file(
            "tests/wrong_files/file2.py",
            "tests/tmp/file2.py",
            overwrite=False,
            docstr_config={"style": "numpy", "max_len": 88, "indent": 2},
        )
    # Case multiple files
    write_files_recursive(
        "tests/wrong_files",
        "tests/tmp",
        overwrite=False,
        docstr_config={"style": "numpy", "max_len": 88, "indent": 2},
    )
    out, _ = capfd.readouterr()
    check.is_true(out.startswith("Error when parsing file(s):\n"))
