# How to use

Set a directory path to transform all python files in it.
Use the module like that to write the files in place:

```bash
docstripy <dir-or-file_path> -s=<style> -o=<output_path>
```

Available styles (`style`) are:

* "numpy": Numpy doc style (default)
* "google": Google style
* "rest": ReST style

Example conversion ReST style to Google style:

```python
def myfunc(param1: int = 0, param2: str = '') -> Tuple[int, str]:
    r"""This is a title.

    This is a subtitle.
    :param param1: This is a parameter. The description can be multiline,
        and it can be very very long. Even longer than this.

        And it can have a default value. The default value can be very long too.
        It is an int, and it was discovered by a very long process, defaults to
        0.
    :type param1: :obj:`int`, optional
    :param param2: This is another parameter, defaults to ''.
    :type param2: str, optional
    :raises ValueError: If something goes wrong.
    :rtype: int
    :return result2: The second result.
    :rtype result2: str
    :ivar attr1: This is an attribute, defaults to 0.
    :type attr1: int

    Example:
        This is an example.
        >>> function(1, '\n')
        0

        This is another example.
        >>> function(2, '\n')
        0

    Notes:
        This is a note.
    """
```

Turns into:

```python
def myfunc(param1: int = 0, param2: str = '') -> Tuple[int, str]:
    r"""This is a title.

    This is a subtitle.

    Args:
        param1 (:obj:`int`, optional): This is a parameter.
            The description can be multiline, and it can be very very long.
            Even longer than this.

            And it can have a default value. The default value can be very long
            too. It is an int, and it was discovered by a very long process.
            Defaults to 0.
        param2 (str, optional): This is another parameter. Defaults to ''.

    Raises:
        ValueError: If something goes wrong.

    Returns:
        int
        result2 (str): The second result.

    Attributes:
        attr1 (int): This is an attribute. Defaults to 0.

    Example:
        This is an example.
        >>> function(1, '\n')
        0

        This is another example.
        >>> function(2, '\n')
        0

    Notes:
        This is a note.
    """
```

And to Numpy style:

```python
def myfunc(param1: int = 0, param2: str = '') -> Tuple[int, str]:
    r"""This is a title.

    This is a subtitle.

    Parameters
    ----------
    param1 : :obj:`int`, optional
        This is a parameter. The description can be multiline, and it can be
        very very long. Even longer than this.

        And it can have a default value. The default value can be very long too.
        It is an int, and it was discovered by a very long process.
        By default, 0.
    param2 : str, optional
        This is another parameter. By default, ''.

    Raises
    ------
    ValueError :
        If something goes wrong.

    Returns
    -------
    int
    result2 : str
        The second result.

    Attributes
    ----------
    attr1 : int
        This is an attribute. By default, 0.

    Example
    -------
    This is an example.
    >>> function(1, '\n')
    0

    This is another example.
    >>> function(2, '\n')
    0

    Notes
    -----
    This is a note.
    """
```
