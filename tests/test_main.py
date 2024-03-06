"""Test entry points of docstripy."""

import os
import shutil
import sys

import pytest
import pytest_check as check

from docstripy.main import main, parse_args
from docstripy.write import write_file, write_files_recursive


def test_main() -> None:
    """Test main entry point."""
    old_argv = sys.argv.copy()
    if os.path.exists("tests/tmp"):
        shutil.rmtree("tests/tmp")
    os.system("docstripy --help")
    sys.argv = [
        "docstripy",
        "tests/files",
        "-o",
        "tests/tmp/google",
        "-s",
        "google",
        "--len",
        "88",
        "--indent",
        "2",
    ]
    main()
    sys.argv[3] = "tests/tmp/rest"
    sys.argv[5] = "rest"
    main()
    sys.argv[3] = "tests/tmp/numpy"
    sys.argv[5] = "numpy"
    main()
    for style in ("google", "numpy", "rest"):
        path = f"tests/tmp/{style}"
        check.is_true(os.path.exists(path), f"Directory not found: {path}")
        for i in range(1, 5):
            path = f"tests/tmp/{style}/test{i}.py"
            check.is_true(os.path.exists(path), f"File not found: {path}")
        path = f"tests/tmp/{style}/empty.py"
        check.is_true(os.path.exists(path), f"File not found: {path}")
        path = f"tests/tmp/{style}/class.py"
        check.is_true(os.path.exists(path), f"File not found: {path}")
    with open("tests/tmp/google/empty.py", encoding="utf-8") as file:
        lines = file.readlines()
    check.equal(lines[8], '    """Clean trailing spaces."""\n')
    if os.path.exists("tests/tmp"):
        shutil.rmtree("tests/tmp")
    run = os.system(
        "docstripy tests/files/class.py -o tests/tmp/class.py "
        "-s numpy --len 88 --indent 4"
    )
    check.equal(run, 0)
    check.is_true(os.path.exists("tests/tmp/class.py"))
    with open("tests/tmp/class.py", encoding="utf-8") as file:
        lines = file.readlines()
    check.equal("    attr : int, optional\n", lines[12])
    check.equal("        The attribute. By default, 0.\n", lines[13])
    check.equal("    attr : int\n", lines[28])
    check.equal('    """\n', lines[30])
    check.equal('        """Forward."""\n', lines[33])
    if os.path.exists("tests/tmp"):
        shutil.rmtree("tests/tmp")
    sys.argv = old_argv


def test_errors(capfd: pytest.CaptureFixture) -> None:
    """Test entry point when there are files errors."""
    with pytest.raises(ValueError, match="Error found during docstring parsing."):
        write_file(
            "tests/wrong_files/file1.py",
            "tests/tmp/file1.py",
            overwrite=False,
            docstr_config={"style": "numpy", "max_len": 88, "indent": 2},
        )
    for style in ("numpy", "rest", "google"):
        with pytest.raises(
            ValueError, match="Error found at lines 3-8 during docstring building.*"
        ):
            write_file(
                "tests/wrong_files/file2.py",
                "tests/tmp/file2.py",
                overwrite=False,
                docstr_config={"style": style, "max_len": 88, "indent": 2},
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
    # Case args errors
    old_argv = sys.argv.copy()
    sys.argv = ["docstripy", ".", "-o", "./out", "-w"]
    with pytest.raises(ValueError, match="Cannot use both.*"):
        parse_args()
    sys.argv = ["docstripy", "."]
    with pytest.raises(ValueError, match="You must specify an output path.*"):
        parse_args()
    sys.argv = old_argv
