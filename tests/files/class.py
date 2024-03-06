# type: ignore
"""A test module.

Contains some classes for testing the parser.
"""


class MyClass:
    """My class.

    Parameters
    ----------
    attr:
        The attribute
    """

    # A comment
    cls_attr: 0  # some class attribute

    def __init__(self, attr: int = 0) -> None:
        self.attr = attr


class MyOtherClass:
    """My other class.

    Parameters
    ----------
    attr: int
        The attribute.
    """

    def forward(self, str_in: str) -> None:  # noqa
        return str_in
