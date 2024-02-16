# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""


def factorial_rest(n):
    r"""Return factorial of '\n'.

    :param n: Number to compute factorial of.
    :type n: int
    :return: Factorial of n.
    :rtype: int
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial_rest(n - 1)


def factorial_google(n):
    r"""Return factorial of '\n'.

    Args:
        n (int): Number to compute factorial of.

    Returns:
        int: Factorial of n.

    Examples:
    >>> factorial_google(5)
    120

    Notes:
        This is a note.

    Raises:
        ValueError: If n is negative.
    """  # noqa: D406, D407, D205
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial_google(n - 1)


def factorial_numpy(n):
    r"""Return factorial of '\n'.

    Parameters
    ----------
    n : int
        Number to compute factorial of.

    Returns
    -------
    int :
        Factorial of n.

    Notes
    -----
    This is a note.

    Examples
    --------
    >>> factorial_numpy(5)
    120
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial_google(n - 1)


def factorial_nothing(n):
    r"""Return factorial of '\n'."""
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial_google(n - 1)
