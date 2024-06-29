# type: ignore
"""A test module.

Contains some functions for testing the parser.
"""


class TestAttr:
    """Test class for attributes.

    This is a function where the ending quotes
    are in the same line as the title.

    :cvar integer: The number
    :ivar str: The string
    :var bool: The boolean
    """

    integer = 0

    def __init__(self) -> None:
        self.str = "string"
        self.bool = True
