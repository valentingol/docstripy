"""Main functions for parsing and building docstrings."""

import argparse
import os

from docstripy.build_doc.main_builder import build_docstring
from docstripy.difference import Diff
from docstripy.lines_routines import add_indent, find_indent
from docstripy.parse_doc.main_parser import parse_docstring


def write_file(
    path: str,
    out_path: str,
    *,
    overwrite: bool,
    docstr_config: dict,
) -> None:
    """Write new docstrings on a file."""
    with open(path, encoding="utf-8") as file:
        file_lines = file.readlines()
    try:
        range_docstrs, sections_list = parse_docstring(file_lines)
    except (IndexError, ValueError) as err:
        raise ValueError("Error found during docstring parsing.") from err
    new_lines = []
    for range_doc, sections in zip(range_docstrs, sections_list):
        try:
            indent_base = find_indent(file_lines[range_doc[0] : range_doc[1]])
            docstring = build_docstring(
                sections=sections,
                docstr_config=docstr_config,
                indent_base=indent_base,
            )
        except (IndexError, ValueError) as err:
            raise ValueError(
                f"Error found at lines {range_doc[0]}-{range_doc[1]} "
                "during docstring building."
            ) from err
        docstring = add_indent(docstring, indent_base)
        new_lines.append("".join(docstring))
    # Write in file
    diff = Diff(range_docstrs, new_lines)
    file_new_lines = diff.apply_diff(file_lines)
    out_path = path if overwrite else out_path
    if os.path.dirname(out_path):
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as file:
        file.writelines(file_new_lines)


def write_files_recursive(
    path: str,
    out_path: str,
    *,
    overwrite: bool,
    docstr_config: dict,
) -> None:
    """Write new docstrings on all files in a folder."""
    error_paths = []
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            if file_name.endswith(".py"):
                file_path = os.path.join(dir_path, file_name)
                path_clean = path.rstrip(os.sep)
                out_path_clean = out_path.rstrip(os.sep)
                file_out_path = file_path.replace(path_clean, out_path_clean)
                try:
                    write_file(
                        path=file_path,
                        out_path=file_out_path,
                        overwrite=overwrite,
                        docstr_config=docstr_config,
                    )
                except (IndexError, ValueError):
                    error_paths.append(file_path)
    if error_paths:
        err_message = "Error when parsing file(s):\n"
        err_message += "\n".join(error_paths)
        err_message += "\nRun `docstripy` on individual files to get lines error."
        print(err_message)


def parse_args() -> dict:
    """Command line parser for docstripy."""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="File path or root directory path.", type=str)
    parser.add_argument(
        "-s", "--style", help="Style of the docstring", type=str, default="numpy"
    )
    parser.add_argument(
        "-o",
        "--out_path",
        help="Output files dir",
        type=str,
        default="",
    )
    parser.add_argument(
        "-w",
        "--overwrite",
        help="Whether to overwrite the files or not",
        action="store_true",
    )
    parser.add_argument(
        "--indent", help="Base indentation size (2, 4, ...)", type=int, default=4
    )
    parser.add_argument(
        "-l",
        "--length",
        help="Maximum lenght of lines in the docstring. By default, no limit.",
        type=int,
        default=-1,
    )
    args = parser.parse_args()
    docstr_config = {
        "style": args.style,
        "max_len": args.length,
        "indent": args.indent,
    }
    if args.out_path and args.overwrite:
        raise ValueError(
            "Cannot use both `--out_path`/`-o` and `--overwrite`/`-w` options."
        )
    if not args.out_path and not args.overwrite:
        raise ValueError(
            "You must specify an output path with `--out_path`/`-o` "
            "or overwrite file(s) with `--overwrite`/`-w` instead."
        )
    return {
        "path": args.path,
        "out_path": args.out_path,
        "docstr_config": docstr_config,
        "overwrite": args.overwrite,
    }


def main() -> None:
    """Rewrite file(s) docstrings main function."""
    cli_args = parse_args()
    if os.path.isfile(cli_args["path"]):
        write_file(**cli_args)
    write_files_recursive(**cli_args)


if __name__ == "__main__":
    main()
