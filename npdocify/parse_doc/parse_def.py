"""Parse def lines (function signatures)."""
from typing import List

from npdocify.lines_routines import clean_comment


def parse_def(lines: List[str]):
    """Parse funbction signature ("def ...")."""
    lines = clean_comment(lines)
    lines = [line.strip() for line in lines]
    def_line = " ".join(lines).strip()
    parenthesis1_split = def_line.split("(", maxsplit=1)
    fn_name = parenthesis1_split[0].replace("def ", "").strip()
    parenthesis2_split = parenthesis1_split[1].rsplit(")", maxsplit=1)
    if "->" in parenthesis2_split[1]:
        rtype_str = parenthesis2_split[1].replace("->", "").replace(":", "")
        rtype = parse_return(rtype_str)
    else:
        rtype = []
    comma_split = parenthesis2_split[0].split(",")
    comma_split = [
        split.strip() for split in comma_split if split.strip() not in ("*", "/", "")
    ]
    print(comma_split)
    args = [parse_args(split) for split in comma_split]
    return fn_name, rtype, args


def parse_args(splits: str) -> List[dict]:
    """Parse function arguments."""
    arg_name, arg_type, arg_default = "", "", ""
    if ":" in splits:
        arg_name, arg_default_type = splits.split(":", maxsplit=1)
        arg_name = arg_name
        arg_default_type = arg_default_type.strip()
        if "=" in splits:
            arg_type, arg_default = arg_default_type.split("=", maxsplit=1)
            arg_type = arg_type
            arg_default = arg_default
        else:
            arg_type = arg_default_type
            arg_default = ""
    elif "=" in splits:
        arg_name, arg_default = splits.split("=", maxsplit=1)
        arg_name = arg_name
        arg_default = arg_default
        arg_type = ""
    arg_name = arg_name.strip()
    arg_default = arg_default.strip()
    arg_type = arg_type.strip()
    return {
        "name": arg_name,
        "type": arg_type,
        "default": arg_default,
        "optional": arg_default != ""
    }


def parse_return(line: str) -> List[str]:
    """Parse return type."""
    line = line.strip()
    if not line.startswith("Tuple["):
        return [line]
    line = line = line[6:]
    rtype_str = line.rsplit("]", maxsplit=1)[0]
    rtype = []
    brack = 0
    current_type = ""
    for char in rtype_str:
        if char == "[":
            brack += 1
        elif char == "]":
            brack -= 1
        if char == "," and brack == 0:
            rtype.append(current_type.strip())
            current_type = ""
        else:
            current_type += char
    if current_type.strip():
        rtype.append(current_type.strip())
    return rtype



if __name__ == '__main__':
    lines = [
        "def my_func(\n",
        "    arg1: int, # noqa\n",
        "    arg2: str = '5',\n",
        "    *,\n",
        "    arg3=5.0,\n",
        "    **kwargs: Any,\n",
        ") -> Tuple[List[Dict[str, Any]] | None, Tuple[Int, Float]]: # noqa\n",
    ]
    fn_name, rtype, args = parse_def(lines)
    print(fn_name)
    print(rtype)
    print(args)
