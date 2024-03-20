from abc import ABC, abstractmethod

from PrattParse.Expression import Expression, NameExpression, AssignExpression, OperatorExpression, CallExpression, \
    PrefixExpression, PostfixExpression, ConditionalExpression
from PrattParse.Parser import Parser, PrefixParselet, InfixParselet
from PrattParse.Precedence import Precedence
from PrattParse.Token import Token, TokenType



class NameParselet(PrefixParselet):
    """Simple parselet for a named variable like "abc"."""

    def parse(self, parser: Parser, token: Token) -> Expression:
        return NameExpression(token.text)


class GroupParselet(PrefixParselet):
    """Parses parentheses used to group an expression, like "a * (b + c)"."""

    def parse(self, parser: Parser, token: Token) -> Expression:
        expression = parser.parse_expression()
        parser.consume(TokenType.RIGHT_PAREN)
        return expression


class AssignParselet(InfixParselet):
    """
    Parses assignment expressions like "a = b".

    The left side of an assignment
    expression must be a simple name like "a", and expressions are
    right-associative. (In other words, "a = b = c" is parsed as "a = (b = c)").
    """

    def parse(self, parser: Parser, left: Expression, token: Token) -> Expression:
        if not isinstance(left, NameExpression):
            raise ValueError(
                "The left-hand side of an assignment must be a name.")
        # To handle right-associative operators, we allow a slightly lower precedence
        # when parsing the right-hand side.
        # so the precedence is ASSIGNMENT -1, which is BELOW_ASSIGNMENT
        right = parser.parse_expression(Precedence.BELOW_ASSIGNMENT)
        name = left.name
        return AssignExpression(name, right)

    def precedence(self) -> Precedence:
        return Precedence.ASSIGNMENT


class BinaryOperatorParselet(InfixParselet):
    """
    Generic infix parselet for a binary arithmetic operator.

    The only difference when parsing, "+", "-", "*", "/", and "^" is precedence and
    associativity, so we can use a single parselet class for all of those.
    """

    def __init__(self, precedence: Precedence, is_right: bool):
        super().__init__()
        self._precedence = precedence
        self._is_right = is_right

    def parse(self, parser: Parser, left: Expression, token: Token) -> Expression:
        # To handle right-associative operators like "^", we allow a slightly
        # lower precedence when parsing the right-hand side. This will let a
        # parselet with the same precedence appear on the right, which will then
        # take *this* parselet's result as its left-hand argument.
        precedence = self._precedence.one_lower() if self._is_right else self._precedence
        right = parser.parse_expression(precedence)
        return OperatorExpression(left, token.type, right)

    def precedence(self) -> Precedence:
        return self._precedence


class CallParselet(InfixParselet):
    def parse(self, parser: Parser, left: Expression, token: Token) -> Expression:
        args = []
        if not parser.match(TokenType.RIGHT_PAREN):
            while True:
                args.append(parser.parse_expression())
                if not parser.match(TokenType.COMMA):
                    break
            parser.consume(TokenType.RIGHT_PAREN)

        return CallExpression(left, args)

    def precedence(self) -> Precedence:
        return Precedence.CALL


class PrefixOperatorParselet(PrefixParselet):
    """
    Generic prefix parselet for an unary arithmetic operator.

    Parses prefix unary "-", "+", "~", and "!" expressions.
    """

    def __init__(self, precedence: Precedence):
        super().__init__()
        self._precedence = precedence

    def parse(self, parser: Parser, token: Token) -> Expression:
        right = parser.parse_expression(self._precedence)
        return PrefixExpression(token.type, right)

    def precedence(self):
        return self._precedence


class PostfixOperatorParselet(InfixParselet):
    """Generic infix parselet for an unary arithmetic operator.

    Parses postfix unary "?" expressions.
    """

    def __init__(self, precedence: Precedence):
        super().__init__()
        self._precedence = precedence

    def parse(self, parser: Parser, left: Expression, token: Token):
        return PostfixExpression(left, token.type)

    def precedence(self):
        return self._precedence


class ConditionalParselet(InfixParselet):
    """Parselet for the condition or ternary operator, like "a ? b : c"."""

    def parse(self, parser: Parser, left: Expression, token: Token):
        then_arm = parser.parse_expression()
        parser.consume(TokenType.COLON)
        else_arm = parser.parse_expression(Precedence.CONDITIONAL.one_lower())
        return ConditionalExpression(left, then_arm, else_arm)

    def precedence(self):
        return Precedence.CONDITIONAL
