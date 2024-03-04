# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""


def factorial(n):
    """Return factorial of n.

    Parameters
    ----------
    n : int
        Number to compute factorial of.

    Returns
    -------
    int
        Factorial of n.

    Raises
    ------
    ValueError
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    """Return nth Fibonacci number."""
    if n < 0:
        raise ValueError("Cannot compute Fibonacci number of negative index.")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def square(n):
    r"""Return square.

    Use \escaped characters.
    """
    return n * n


def empty_function() -> None:  # noqa: D103
    pass
