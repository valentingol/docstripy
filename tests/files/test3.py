# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""

from typing import Dict, List


def myfunc_rest(  # pylint: disable=W0102
    name1: List[bool],
    name2: list | str = "",
    name3: Dict[str, int] = {"a": 1},
):
    """A function.

    It does something not important but the docstring
    is in ReST style.

    :param name1: A list of bools.
    :type name1: List[bool]
    :param name2: A list or a string.
    This parameter is very important.

    Very important.
        Default is an empty list
    :type name2: list | str, optional
    :param name3: A dictionary, default is {"a": 1}.
    :type name3: Dict[str, int] optional

    :return result: the result of the function
    :rtype result: int
    """  # noqa: D401
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1
    return 0


def myfunc_rest2(a: int = 2):
    """Do nothing, a function without indices in docstring.

    :param a:
    """
    return a


def myfunc_numpy(  # pylint: disable=W0102
    name1: List[bool],
    name2: list | str = "",
    name3: Dict[str, int] = {"a": 1},
):
    """A function.

    It does something not important but the docstring
    is in Numpy style.

    Parameters
    ----------
    name1 : List[bool]
        A list of bools.
    name2 : list | str, optional
        A list or a string.
        This parameter is very important.

        Very important.
            Default is an empty list.
    name3 : Dict[str, int] optional
        A dictionary, default is {"a": 1}.

    Returns
    -------
    result : int
        the result of the function
    """  # noqa: D401
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1
    return 0


def myfunc_numpy2(a: int = 2):
    """Do nothing, a function without indices in docstring.

    Parameters
    ----------
    a
    """
    return a


def myfunc_google(  # pylint: disable=W0102
    name1: List[bool], name2: list | str = "", name3: Dict[str, int] = {"a": 1}
):
    """Do nothing, a function without indices in docstring.

    Args:
        name1 (List[bool]): A list of bools.
        name2 (list | str, optional): A list or a string.
            This parameter is very important.

            Very important.
                Default is an empty list.
        name3 (Dict[str, int], optional): A dictionary, default is {"a": 1}.

    Returns:
        result (int): the result of the function
    """  # noqa: D406 D407
    if name1[0] and len(name2) == 0 and name3["a"] == 1:
        return 1
    return 0


def myfunc_google2(a: int = 2):
    """Do nothing, a function without indices in docstring.

    Args:
        a
    """  # noqa: D406 D407
    return a
