"""Test def line parsing."""

import pytest_check as check

from docstripy.parse_doc.parse_def import parse_def


def test_parse_def() -> None:
    """Test parse_args function."""
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
    check.equal(fn_name, "my_func")
    check.equal(rtype, ["List[Dict[str, Any]] | None", "Tuple[Int, Float]"])
    expected_args = [
        {
            "name": "arg1",
            "type": "int",
            "default": "",
            "optional": False,
        },
        {
            "name": "arg2",
            "type": "str",
            "default": "'5'",
            "optional": True,
        },
        {
            "name": "arg3",
            "type": "",
            "default": "5.0",
            "optional": True,
        },
        {
            "name": "**kwargs",
            "type": "Any",
            "default": "",
            "optional": False,
        },
    ]
    check.equal(len(args), len(expected_args))
    for i, arg in enumerate(args):
        check.equal(arg, expected_args[i], f"Error at arg {i}")
    lines = ["def my_func(n):\n"]
    fn_name, rtype, args = parse_def(lines)
    check.equal(fn_name, "my_func")
    check.equal(rtype, [])
    expected_args = [
        {
            "name": "n",
            "type": "",
            "default": "",
            "optional": False,
        },
    ]
    check.equal(args, expected_args)
