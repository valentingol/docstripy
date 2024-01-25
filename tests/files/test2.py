"""A test module.

Contains some functions for testing the parser.
"""


def factorial(n):
    r"""Return factorial of '\n'.

    Parameters
    ----------
    n : int
        Number to compute factorial of.
    """
    if n < 0:
        raise ValueError("Cannot compute factorial of negative number.")
    if n == 0:
        return 1
    return n * factorial(n - 1)
