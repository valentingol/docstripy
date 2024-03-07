"""Main functions for parsing and building docstrings."""

import os
import os.path as osp
from typing import List

import nbformat

from docstripy.build_doc.main_builder import build_docstring
from docstripy.difference import apply_diff
from docstripy.lines_routines import add_eol, add_indent, find_indent
from docstripy.parse_doc.main_parser import parse_docstring


def generate_new_file(file_lines: List[str], docstr_config: dict) -> List[str]:
    """Generate new file with the updated docstrings."""
    try:
        range_docstrs, sections_list, to_insert = parse_docstring(file_lines)
    except (
        IndexError,
        ValueError,
        KeyError,
        ArithmeticError,
        IndentationError,
        NameError,
        ValueError,
    ) as err:
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
        except (
            IndexError,
            ValueError,
            KeyError,
            ArithmeticError,
            IndentationError,
            NameError,
            ValueError,
        ) as err:
            raise ValueError(
                f"Error found at lines {range_doc[0]}-{range_doc[1]} "
                "during docstring building. Please check above error."
            ) from err
        docstring = add_indent(docstring, indent_base)
        new_lines.append("".join(docstring))
    file_new_lines = apply_diff(
        ranges=range_docstrs,
        lines=new_lines,
        old_lines=file_lines,
        to_insert=to_insert,
    )
    return file_new_lines


def write_file_py(
    in_path: str,
    out_path: str,
    *,
    overwrite: bool,
    docstr_config: dict,
) -> None:
    """Write new docstrings on a file."""
    if out_path and not out_path.endswith(".py"):
        raise ValueError(f"Output file must be a .py file (found {out_path}).")
    with open(in_path, encoding="utf-8") as file:
        file_lines = file.readlines()
    file_new_lines = generate_new_file(file_lines, docstr_config)
    out_path = in_path if overwrite else out_path
    if osp.dirname(out_path):
        os.makedirs(osp.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as file:
        file.writelines(file_new_lines)


def write_file_ipynb(
    in_path: str,
    out_path: str,
    *,
    overwrite: bool,
    docstr_config: dict,
) -> None:
    """Write new docstrings on a file."""
    if out_path and not out_path.endswith(".ipynb"):
        raise ValueError(f"Output file must be a .ipynb file (found {out_path}).")
    with open(in_path, encoding="utf-8") as file:
        file_dict = nbformat.read(file, as_version=nbformat.NO_CONVERT)
    for i_cell, cell in enumerate(file_dict["cells"]):
        cell_lines = cell["source"].split("\n")
        cell_lines = add_eol(cell_lines)
        cell_new_lines = generate_new_file(cell_lines, docstr_config)
        file_dict["cells"][i_cell]["source"] = "".join(cell_new_lines)
    out_path = in_path if overwrite else out_path
    if osp.dirname(out_path):
        os.makedirs(osp.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as file:
        nbformat.write(file_dict, file)


def write_files_recursive(
    in_path: str,
    out_path: str,
    *,
    overwrite: bool,
    docstr_config: dict,
) -> None:
    """Write new docstrings on all files in a folder."""
    error_paths = []
    write_func = {
        ".py": write_file_py,
        ".ipynb": write_file_ipynb,
    }
    for dir_path, _, file_names in os.walk(in_path):
        for file_name in file_names:
            if file_name.endswith(tuple(write_func.keys())):
                ext = osp.splitext(file_name)[1]
                file_path = osp.join(dir_path, file_name)
                rel_path = osp.relpath(file_path, in_path)
                file_out_path = osp.join(out_path, rel_path)
                try:
                    write_func[ext](
                        in_path=file_path,
                        out_path=file_out_path,
                        overwrite=overwrite,
                        docstr_config=docstr_config,
                    )
                except (IndexError, ValueError):
                    error_paths.append(file_path)
    if error_paths:
        err_message = "Error when parsing file(s):\n"
        err_message += "\n".join(error_paths)
        err_message += (
            "\nRun `docstripy` on those files individually to get error lines."
        )
        print(err_message)
