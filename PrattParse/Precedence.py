from enum import Enum


class Precedence(Enum):
    """
    Defines the different precedence levels used by the infix parsers.

    These determine how a series of infix expressions will be grouped. For example,
    "a + b * c - d" will be parsed as "(a + (b * c)) - d" because "*" has higher
    precedence than "+" and "-". Here, bigger numbers mean higher precedence.
    """
    # In order of increasing precedence.
    BELOW_ASSIGNMENT = 0
    ASSIGNMENT = 1
    CONDITIONAL = 2
    SUM = 3
    PRODUCT = 4
    EXPONENT = 5
    PREFIX = 6
    POSTFIX = 7
    CALL = 8

    def one_lower(self) -> 'Precedence':
        return Precedence(self.value - 1)

    def __lt__(self, other: 'Precedence'):
        return self.value < other.value