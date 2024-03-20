# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""


def my_func() -> None:
    """The function title.

    This is a function where the ending quotes
    are in the same line as the title"""  # noqa


def nested_func() -> None:  # noqa
    def aux_func() -> None:
        """This is a nested function.

        This is a nested function with a nested docstring.
        """  # noqa
