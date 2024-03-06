# Docstripy - Convert any docstring to any format docstring

Transform your python docstrings to the format you want :sparkles:

Support Nympydoc, Google and ReStructuredText as output styles.
The input style should be either Numpy, Google, ReST or even a mix of both.

[![Release](https://img.shields.io/github/v/tag/valentingol/docstripy?label=Pypi&logo=pypi&logoColor=yellow)](https://pypi.org/project/docstripy/)
![PythonVersion](https://img.shields.io/badge/Python-3.7%20%7E%203.11-informational)
[![License](https://img.shields.io/github/license/valentingol/docstripy?color=999)](https://stringfixer.com/fr/MIT_license)

[![Ruff_logo](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Black_logo](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Ruff](https://github.com/valentingol/docstripy/actions/workflows/ruff.yaml/badge.svg)](https://github.com/valentingol/docstripy/actions/workflows/ruff.yaml)
[![Flake8](https://github.com/valentingol/docstripy/actions/workflows/flake.yaml/badge.svg)](https://github.com/valentingol/docstripy/actions/workflows/flake.yaml)
[![MyPy](https://github.com/valentingol/docstripy/actions/workflows/mypy.yaml/badge.svg)](https://github.com/valentingol/docstripy/actions/workflows/mypy.yaml)
[![PyLint](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/valentingol/5816178f37cee2c013f2e656666c898a/raw/npdocify_pylint.json)](https://github.com/valentingol/docstripy/actions/workflows/pylint.yaml)

[![Tests](https://github.com/valentingol/docstripy/actions/workflows/tests.yaml/badge.svg)](https://github.com/valentingol/docstripy/actions/workflows/tests.yaml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/valentingol/6fd638b90ac10eced712b8d5ca83b04f/raw/npdocify_tests.json)](https://github.com/valentingol/docstripy/actions/workflows/tests.yaml)

## How to use

Install the library via pip:

```bash
pip install docstripy
```

Use it like that to write the files in place.
Set a directory path to transform all python files in it.

```bash
docstripy <dir-or-file_path> -s=<style> -o=<output_path>
```

Available styles (`style`) are:

* "numpy": Numpy doc style (default)
* "google": Google style
* "rest": ReST style

## Cool features

### Overwrite the files directly

You can use the `-w` (or `--overwrite`) option to write the files in place.

```bash
docstripy <dir-or-file_path> -s=<style> -w
```

*Notes*:

1) **The module takes into account the fonction definitions**.
If the definition of the function bring new information, this will be added to the docstring.
In case of a conflict, the information in **the function definition will be prioritized**.
It means that docstripy will automatically update your docstring if you update your functions!
2) If the old docstring not already contains information on parameters and/or
return elements, the output docstring will not specify those elements either.
However, if the function definition contains more information, the docstring will
be updated with all the corresponding information available in the signature.

For instance:

```python

def my_function(a: int, b: int) -> int:
    """My function
    Parameters
    ----------
    a : str
        The first argument.
    """
    # Here the type of `a` is wrong and the type of `b` is missing.
    # Plus, no information is given on the return type.
    return a + b
```

Results in:

```python
def my_function(a: int, b: int) -> int:
    """My function.

    Parameters
    ----------
    a : int
        The first argument.
    b : int
    """
    # The type of `a` is fixed, the type of `b` is added.
    # No information is given on the return type as it was not present
    # in the old docstring.
    # Fix some syntax issues (end of line dot and in-between spaces).
    return a + b
```

### Max line length

You can control the max line length of the docstring with the `--len` option.
By default, there is no limit. The line lenght take into account the indentation
found in the file.

### 2 spaces indentation

If your files are indented with 2 spaces, you can use the `--n_indent=2` option to
the command line.

```bash
docstripy <dir-or-file_path> -s=<style> --n_indent=2
```

Note that the default value is 4 spaces but you can set any value you want.

### Create a short docstring when missing

When a function has no docstring, a short one will be created based on
the function name. For instance:

```python
def clean_trailing_spaces(line: str) -> new_line: str:
    return line.rstrip()
```

Results in:

```python
def clean_trailing_spaces(line: str) -> new_line: str:
    """Clean trailing spaces."""
    return line.rstrip()
```

### Class docstring

The class docstring is updated based on the class definition with the signature
of `__init__` method. For instance:

```python
class MyClass:
    """My class.

    Parameters
    ----------
    attr:
        The attribute
    """

    # A comment
    cls_attr: 0  # Class attribute

    def __init__(self, attr: int = 0) -> None:
        self.attr = attr
```

Results in:

```python
class MyClass:
    """My class.

    Parameters
    ----------
    attr : int, optional
        The attribute. By default, 0.
    """

    # A comment
    cls_attr: 0  # some class attribute

    def __init__(self, attr: int = 0) -> None:
        self.attr = attr
```
