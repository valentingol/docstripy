# Npdocify - Convert any docstring to any format docstring

Transform your python docstrings with the format you want :sparkles:

Support Nympydoc, Google and ReStructuredText as output styles.
The input style should be either Numpy, Google, ReST or even a mix of both.

[![Release](https://img.shields.io/github/v/tag/valentingol/npdocify?label=Pypi&logo=pypi&logoColor=yellow)](https://pypi.org/project/npdocify/)
![PythonVersion](https://img.shields.io/badge/Python-3.7%20%7E%203.11-informational)
[![License](https://img.shields.io/github/license/valentingol/npdocify?color=999)](https://stringfixer.com/fr/MIT_license)

[![Ruff_logo](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Black_logo](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Ruff](https://github.com/valentingol/npdocify/actions/workflows/ruff.yaml/badge.svg)](https://github.com/valentingol/npdocify/actions/workflows/ruff.yaml)
[![Flake8](https://github.com/valentingol/npdocify/actions/workflows/flake.yaml/badge.svg)](https://github.com/valentingol/npdocify/actions/workflows/flake.yaml)
[![Pydocstyle](https://github.com/valentingol/npdocify/actions/workflows/pydocstyle.yaml/badge.svg)](https://github.com/valentingol/npdocify/actions/workflows/pydocstyle.yaml)
[![MyPy](https://github.com/valentingol/npdocify/actions/workflows/mypy.yaml/badge.svg)](https://github.com/valentingol/npdocify/actions/workflows/mypy.yaml)
[![PyLint](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/valentingol/5816178f37cee2c013f2e656666c898a/raw/npdocify_pylint.json)](https://github.com/valentingol/npdocify/actions/workflows/pylint.yaml)

[![Tests](https://github.com/valentingol/npdocify/actions/workflows/tests.yaml/badge.svg)](https://github.com/valentingol/npdocify/actions/workflows/tests.yaml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/valentingol/6fd638b90ac10eced712b8d5ca83b04f/raw/npdocify_tests.json)](https://github.com/valentingol/npdocify/actions/workflows/tests.yaml)

## How to use

Install the library via pip:

```bash
pip install git+https://github.com/valentingol/npdocify
```

Use it like that to write the files in place.
Set a directory path to transform all python files in it.

```bash
npdocify <dir-or-file_path> -s=<style> -o=<output_path>
```

Available styles (`style`) are:

* "numpy": Numpy doc style (default)
* "google": Google style
* "rest": ReST style

## Cool features

### Overwrite the files directly

You can use the `-w` (or `--overwrite`) option to write the files in place.

```bash
npdocify <dir-or-file_path> -s=<style> -w
```

*Note*: The module takes into account the fonction definitions.
If the definition of the function bring new information, this will be added to the docstring.
In case of a conflict, the information in **the function definition will be prioritized**.
It means that npdocify will automatically update your docstring if you update your functions!

### Max line length

You can control the max line length of the docstring with the `--len` option.
By default, there is no limit. The line lenght take into account the indentation
found in the file.

### 2 spaces indentation

If your files are indented with 2 spaces, you can use the `--n_indent=2` option to
the command line.

```bash
npdocify <dir-or-file_path> -s=<style> --n_indent=2
```

Note that the default value is 4 spaces but you can set any value you want.
