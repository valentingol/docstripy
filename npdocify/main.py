"""Main functions for parsing and building docstrings."""
import argparse
import os

from npdocify.build_doc.main_builder import build_docstring
from npdocify.difference import Diff
from npdocify.file_parser import docstring_parse
from npdocify.lines_routines import add_indent, find_indent


def write_file(file_path: str, docstr_config: dict) -> None:
    """Write new docstrings on a file."""
    with open(file_path, encoding="utf-8") as file:
        file_lines = file.readlines()
    try:
        range_docstrs, sections_list = docstring_parse(file_lines)
    except (IndexError, ValueError) as err:
        raise ValueError("Error found during docstring parsing.") from err
    new_lines = []
    for range_doc, sections in zip(range_docstrs, sections_list):
        try:
            indent_base = find_indent(file_lines[range_doc[0]:range_doc[1]])
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
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(file_new_lines)


def write_files_recursive(
    folder_path: str,
    docstr_config: dict,
) -> None:
    """Write new docstrings on all files in a folder."""
    error_paths = []
    for dir_path, _, file_names in os.walk(folder_path):
        for file_name in file_names:
            if file_name.endswith(".py"):
                file_path = os.path.join(dir_path, file_name)
                try:
                    write_file(file_path=file_path, docstr_config=docstr_config)
                except (IndexError, ValueError):
                    error_paths.append(file_path)
    if error_paths:
        err_message = "Error when parsing file(s):\n"
        err_message += "\n".join(error_paths)
        err_message += "\nRun `npdocify` on individual files to get lines error."
        print(err_message)


def parse_args() -> dict:
    """Command line parser for npdocify."""
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="File path or root directory path.", type=str)
    parser.add_argument(
        "-s",
        "--style",
        help="Style of the docstring",
        type=str,
        default="numpy"
    )
    parser.add_argument(
        "--indent",
        help="Base indentation size (2, 4, ...)",
        type=int,
        default=4
    )
    parser.add_argument(
        "-l",
        "--length",
        help="Maximum lenght of lines in the docstring.",
        type=int,
        default=88,
    )
    args = parser.parse_args()
    docstr_config = {
        "style": args.style,
        "max_len": args.length,
        "indent": args.indent,
    }
    return args.path, docstr_config


def main():
    """Rewrite file(s) docstrings main function."""
    path, docstr_config = parse_args
    if os.path.isfile(path):
        write_file(file_path=path, docstr_config=docstr_config)
    write_files_recursive(folder_path=path, docstr_config=docstr_config)


if __name__ == '__main__':
    main()
