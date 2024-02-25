from __future__ import annotations

from enum import Enum, auto


class TokenType(Enum):
    # single token
    LEFT_PAREN = auto()  # (
    RIGHT_PAREN = auto()  # )
    LEFT_BRACE = auto()  # {
    RIGHT_BRACE = auto()  # }
    DOT = auto()  # .
    PLUS = auto()  # +
    LEFT_BRACKET = auto()  # [
    RIGHT_BRACKET = auto()  # ]
    MINUS = auto()  # -
    STAR = auto()  # *
    QUESTION = auto()  # ?
    COMMA = auto()  # ,
    COLON = auto()  # :
    LESS = auto()  # <
    GREAT = auto()  # >
    S_ANCHOR = auto()  # ^
    E_ANCHOR = auto()  # $
    ESCAPE = auto()  # \
    OR = auto()  # |
    INT = auto()  # int
    LETTER = auto()  # a-zA-Z
    ASCII = auto()  # ascii expect for int and letter
    CHAR = auto()  # normal character EXCEPT INT, LETTER ,ASCII

    # ESCAPES
    ANY_WORD = auto()  # \w
    ANY_WORD_INVERTED = auto()  # \W
    ANY_DIGIT = auto()  # \d
    ANY_DIGIT_INVERTED = auto()  # \D
    ANY_WHITE_SPACE = auto()  # \s
    ANY_WHITE_SPACE_INVERTED = auto()  # \S

    WORD_BOUND = auto()  # \b
    NON_WORD_BOUND = auto()  # \B
    START_OF_STRING_ONLY = auto()  # \A
    END_OFF_STRING_ONLY_NOT_NEWLINE = auto()  # \z
    END_OFF_STRING_ONLY = auto()  # \Z
    PRE_MATCH_END = auto()  # \G

    EOF = auto()  # EOF


class Token:
    def __init__(self, type_: TokenType, value: str = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Expr:
    def accept(self, visitor: Visitor):
        raise NotImplementedError()


class Visitor:

    def visit_expression(self, expr):
        raise NotImplementedError()

    def visit_subexpression(self, expr):
        raise NotImplementedError()

    def visit_group(self, expr):
        raise NotImplementedError()

    def visit_match(self, expr):
        raise NotImplementedError()

    def visit_character_group(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_word(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_word_inv(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_digit(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_digit_inv(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_white_space(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_white_space_inv(self, expr):
        raise NotImplementedError()

    def visit_character_range(self, expr):
        raise NotImplementedError()

    def visit_backreference(self, expr):
        raise NotImplementedError()

    def visit_any_char(self, expr):
        raise NotImplementedError()

    def visit_character(self, expr):
        raise NotImplementedError()

    def visit_range_quantifier(self, expr):
        raise NotImplementedError()

    def visit_zero_or_more_quantifier(self, expr):
        raise NotImplementedError()

    def visit_one_or_more_quantifier(self, expr):
        raise NotImplementedError()

    def visit_zero_or_one_quantifier(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string(self, expr):
        raise NotImplementedError()

    def visit_anchor_end_of_string(self, expr):
        raise NotImplementedError()

    def visit_anchor_word_bound(self, expr):
        raise NotImplementedError()

    def visit_anchor_non_word_bound(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string_only(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string_only_nnl(self, expr):
        raise NotImplementedError()

    def visit_anchor_end_of_string_only(self, expr):
        raise NotImplementedError()

    def visit_anchor_pre_match_end(self, expr):
        raise NotImplementedError()


class Expression(Expr):
    def __init__(self, subexpression: SubExpression, alternation: Expression = None):
        self.subexpression = subexpression
        self.alternation = alternation

    def accept(self, visitor):
        return visitor.visit_expression(self)


class SubExpression(Expr):
    def __init__(self, items):
        self.items = items

    def accept(self, visitor):
        return visitor.visit_subexpression(self)


class Match(Expr):
    def __init__(self, match_item: Expr):
        self.match_item = match_item

    def accept(self, visitor):
        return visitor.visit_match(self)


class AnyChar(Expr):
    def accept(self, visitor):
        return visitor.visit_any_char(self)


class CharRange(Expr):
    def __init__(self, start: Token, to: Token = None):
        self.start = start
        self.to = to

    def accept(self, visitor):
        return visitor.visit_character_range(self)


class Group(Expr):
    def __init__(self, expression: Expression, non_capturing: bool = False, group_name: str = None,
                 atomic: bool = False):
        self.expression = expression
        self.non_capturing = non_capturing
        self.group_name = group_name
        self.atomic = atomic

    def accept(self, visitor):
        return visitor.visit_group(self)


class CharacterGroup(Expr):
    def __init__(self, items: list[Expr], negative=False):
        self.items = items
        self.negative = negative

    def accept(self, visitor):
        return visitor.visit_character_group(self)


class CharClassAnyWord(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_word(self)


class CharClassAnyWordInverted(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_word_inv(self)


class CharClassAnyDecimalDigit(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_digit(self)


class CharClassAnyDecimalDigitInverted(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_digit_inv(self)


class CharClassAnyWhitespace(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_white_space(self)


class CharClassAnyWhitespaceInverted(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_char_class_any_white_space_inv(self)


class Backreference(Expr):
    def __init__(self, number: int):
        self.number = number

    def accept(self, visitor):
        return visitor.visit_backreference(self)


class Character(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_character(self)


class RangeQuantifier(Expr):
    def __init__(self, expr: Expr, low_bound: int, up_bound: int = None, fixed_bound=True, lazy=False):
        self.expr = expr
        self.low_bound = low_bound
        self.up_bound = up_bound
        # {n} is fixed low bound,fixed. {n,} is >= low bound, not fixed
        self.fixed_bound = fixed_bound
        self.lazy = lazy

    def accept(self, visitor):
        return visitor.visit_range_quantifier(self)


class ZeroOrMoreQuantifier(Expr):
    def __init__(self, expr: Expr, lazy=False):
        self.expr = expr
        self.lazy = lazy

    def accept(self, visitor):
        return visitor.visit_zero_or_more_quantifier(self)


class OneOrMoreQuantifier(Expr):
    def __init__(self, expr: Expr, lazy=False):
        self.expr = expr
        self.lazy = lazy

    def accept(self, visitor):
        return visitor.visit_one_or_more_quantifier(self)


class ZeroOrOneQuantifier(Expr):
    def __init__(self, expr: Expr, lazy=False):
        self.expr = expr
        self.lazy = lazy

    def accept(self, visitor):
        return visitor.visit_zero_or_one_quantifier(self)


class AnchorWordBoundary(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_word_bound(self)


class AnchorNonWordBoundary(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_non_word_bound(self)


class AnchorStartOfStringOnly(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_start_of_string_only(self)


class AnchorEndOfStringOnlyNotNewline(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_start_of_string_only_nnl(self)


class AnchorEndOfStringOnly(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_end_of_string(self)


class AnchorPreviousMatchEnd(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_pre_match_end(self)


class AnchorStartOfString(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_start_of_string(self)


class AnchorEndOfString(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_anchor_end_of_string(self)
