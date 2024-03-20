"""Save output docstring to txt file."""

import argparse
import os
from typing import List

from docstripy.file_parser import parse_ranges


def extract_docstrs(dir_path: str) -> List[str]:
    """Extract all docstrings from files in dir_path."""
    all_docstrs = []
    for dir_path, _, file_names in os.walk(dir_path):
        for file_name in file_names:
            if file_name.endswith(".py"):
                path = os.path.join(dir_path, file_name)
                all_docstrs.append(f">>> PATH: {path}\n")
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                ranges_docstr, _ = parse_ranges(lines)
                for range_docstr in ranges_docstr:
                    line_docstr = lines[range_docstr[0] : range_docstr[1]]
                    all_docstrs.extend(line_docstr)
    return all_docstrs


def get_args() -> dict:
    """Get command line args."""
    parser = argparse.ArgumentParser(description="Save output docstring to txt file.")
    parser.add_argument("input", type=str, help="Input dir path")
    parser.add_argument("output", type=str, help="Ouptout .txt file path")
    args = parser.parse_args()
    return {"input": args.input, "output": args.output}


def main() -> None:
    """Save output docstring to txt file."""
    args = get_args()
    all_docstrs = extract_docstrs(args["input"])
    os.makedirs(os.path.dirname(args["output"]), exist_ok=True)
    with open(args["output"], "w", encoding="utf-8") as file:
        file.writelines(all_docstrs)


if __name__ == "__main__":
    main()
