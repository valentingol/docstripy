"""Main functions for parsing and building docstrings."""

import argparse
import os.path as osp

from docstripy.write import write_file, write_files_recursive


def parse_args() -> dict:
    """Command line parser for docstripy."""
    parser = argparse.ArgumentParser()
    parser.add_argument("in_path", help="File path or root directory path.", type=str)
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
        "in_path": args.in_path,
        "out_path": args.out_path,
        "docstr_config": docstr_config,
        "overwrite": args.overwrite,
    }


def main() -> None:
    """Rewrite file(s) docstrings main function."""
    cli_args = parse_args()
    if osp.isfile(cli_args["in_path"]):
        write_file(**cli_args)
    write_files_recursive(**cli_args)


if __name__ == "__main__":
    main()
