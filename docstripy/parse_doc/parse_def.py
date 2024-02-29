"""Parse def lines (function signatures)."""

from typing import List

from docstripy.lines_routines import clean_comment


def parse_def(lines: List[str]) -> tuple[str, List[str], List[dict]]:
    """Parse funbction signature ("def ...")."""
    lines = clean_comment(lines)
    lines = [line.strip() for line in lines]
    def_line = " ".join(lines).strip()
    parenthesis1_split = def_line.split("(", maxsplit=1)
    fn_name = parenthesis1_split[0].replace("def ", "").strip()
    parenthesis2_split = parenthesis1_split[1].rsplit(")", maxsplit=1)
    if "->" in parenthesis2_split[1]:
        rtype_str = parenthesis2_split[1].replace("->", "").replace(":", "").strip()
        if rtype_str.startswith("Tuple["):
            rtype_str = rtype_str[6:]
            rtype_str = rtype_str.rsplit("]", maxsplit=1)[0].strip()
            rtypes = split_comma(rtype_str)
        else:
            rtypes = [rtype_str]

    else:
        rtypes = []
    comma_split = split_comma(parenthesis2_split[0])
    comma_split = [
        split.strip() for split in comma_split if split.strip() not in ("*", "/", "")
    ]
    args = [parse_def_args(split) for split in comma_split]
    return fn_name, rtypes, args


def parse_def_args(split: str) -> dict:
    """Parse function arguments on def line."""
    arg_name, arg_type, arg_default = "", "", ""
    if ":" in split:
        arg_name, arg_default_type = split.split(":", maxsplit=1)
        arg_default_type = arg_default_type.strip()
        if "=" in split:
            arg_type, arg_default = arg_default_type.split("=", maxsplit=1)
        else:
            arg_type = arg_default_type
            arg_default = ""
    elif "=" in split:
        arg_name, arg_default = split.split("=", maxsplit=1)
        arg_type = ""
    else:
        arg_name = split
    arg_name = arg_name.strip()
    arg_default = arg_default.strip()
    arg_type = arg_type.strip()
    return {
        "name": arg_name,
        "type": arg_type,
        "default": arg_default,
        "optional": arg_default != "",
    }


def split_comma(line: str) -> List[str]:
    """Parse by comma."""
    line = line.strip()
    count_spec_chars = {
        ("(", ")"): 0,
        ("[", "]"): 0,
        ("{", "}"): 0,
    }
    count_quote = {
        '"': 0,
        "'": 0,
    }
    splits = []
    current_split = ""
    for char in line:
        for spec_char in count_spec_chars:
            if char == spec_char[0]:
                count_spec_chars[spec_char] += 1
            elif char == spec_char[1]:
                count_spec_chars[spec_char] -= 1
        for quote in count_quote:
            if char == quote:
                count_quote[quote] += 1
        if (
            char == ","
            and all(count == 0 for count in count_spec_chars.values())
            and all(count % 2 == 0 for count in count_quote.values())
        ):
            splits.append(current_split.strip())
            current_split = ""
        else:
            current_split += char
    if current_split.strip():
        splits.append(current_split.strip())
    return splits
