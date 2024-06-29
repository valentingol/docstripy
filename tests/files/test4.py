# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""

from typing import Dict, List, Tuple


def myfunc_rest(  # pylint: disable=W0102
    name1: List[bool],  # noqa
    name2: list | str = "",
    name3: Dict[str, int] = {"a,b": 1},
):
    r"""A function.

    It does something not important but the title
    is in multiple line.

    :param name1: A list of bools.
    :param name2: A list or a string.

        This parameter is very important.
    :type name2: list | bool, optional
    :param name3: A dictionary.
    :type name3: Dict[str, int] optional
    :raises ValueError: When something happened
    :raises ValueError: When something else happened
    :var nothing:
    :return result: The first result of the function
    :rtype: int
    :rtype: list
    :rtype result3: int
    :yield: A number
    :rtype: int

    Example:
        >>> myfunc_rest([True])
        1, [], 1
        >>> myfunc_rest([True], "\n")
        0, [], 0

    Notes:
        * This always works
        * This is a note
    """  # noqa: D401 D406 D407
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1, [], 1
    return 0, [], 0


def myfunc_numpy(  # pylint: disable=W0102,W9010
    name1: List[bool], name2: list | str = "", name3: Dict[str, int] = {"a,b": 1}
) -> Tuple[int, List, int]:
    r"""A function.

    It does something not important but the title
    is in multiple line.

    Parameters
    ----------
    name1 :
        A list of bools.
    name2 :
        A list or a string.

        This parameter is very important.
    name3 : Dict[str, int] optional
        A dictionary, default is {"a,b": 1}.

    Raises
    ------
    ValueError :
        When something happened
    ValueError :
        When something else happened

    Attributes
    ----------
    nothing

    Returns
    -------
    result : int
        The first result of the function
    list
    result3 : int

    Yields
    ------
    int :
        A number

    Example
    -------
    >>> myfunc_rest([True])
    1, [], 1
    >>> myfunc_rest([True], "\n")
    0, [], 0

    Notes
    -----
    * This always works
    * This is a note
    """  # noqa: D401
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1, [], 1
    return 0, [], 0


def myfunc_google(  # pylint: disable=W0102,W9015,W9010
    name1: List[bool], name2: list | str = "", name3: Dict[str, int] = {"a,b": 1}
) -> Tuple[int, List, int]:
    r"""A function.

    It does something not important but the title
    is in multiple line.

    Args:
        name1: A list of bools.
        name2 (list | str, optional): A list or a string.

            This parameter is very important.
        name3 (Dict[str, int] optional): A dictionary, default is {"c": 1}.

    Raises:
        ValueError: When something happened
        ValueError: When something else happened

    Attributes:
        nothing

    Returns:
        result (int): The first result of the function
        list
        result3 (int)

    Yields:
        int: A number.

    Example:
        >>> myfunc_rest([True])
        1, [], 1
        >>> myfunc_rest([True], "\n")
        0, [], 0

    Notes:
        * This always works
        * This is a note
    """  # noqa: D406 D407 D401
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1, [], 1
    return 0, [], 0
