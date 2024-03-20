from __future__ import annotations

from abc import abstractmethod, ABC

from PrattParse import Lexer
from PrattParse.Expression import Expression
from PrattParse.Precedence import Precedence
from PrattParse.Token import Token, TokenType


class PrefixParselet(ABC):
    """
    One of the two interfaces used by the Pratt parser.

    A PrefixParselet is associated with a token that appears at the beginning of an
    expression. Its parse() method will be called with the consumed leading token, and
    the parselet is responsible for parsing anything that comes after that token.
    This interface is also used for single-token expressions like variables, in
    which case parse() simply doesn't consume any more tokens.
    """

    @abstractmethod
    def parse(self, parser: Parser, token: Token) -> Expression:
        pass


class InfixParselet(ABC):
    """
    One of the two parselet interfaces used by the Pratt parser.

    An InfixParselet is associated with a token that appears in the middle of the
    expression it parses. Its parse() method will be called after the left-hand
    side has been parsed, and it in turn is responsible for parsing everything
    that comes after the token. This is also used for postfix expressions, in
    which case it simply doesn't consume any more tokens in its parse() call.
    """

    @abstractmethod
    def parse(self, parser: Parser, left: Expression, token: Token) -> Expression:
        pass

    @abstractmethod
    def precedence(self) -> Precedence:
        pass


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.cached_token: list[Token] = []
        self.prefix_parselets: dict[TokenType, PrefixParselet] = {}
        self.infix_parselets: dict[TokenType, InfixParselet] = {}

    def match(self, expected: TokenType) -> bool:
        token = self.look_ahead(0)
        if token.type != expected:
            return False
        self.consume()
        return True

    def look_ahead(self, distance: int) -> Token:
        while distance >= len(self.cached_token):
            self.cached_token.append(self.lexer.next())
        return self.cached_token[distance]

    def _consume_0(self) -> Token:
        self.look_ahead(0)
        return self.cached_token.pop(0)

    def consume(self, expected: TokenType | None = None) -> Token:
        if not expected:
            return self._consume_0()
        token = self.look_ahead(0)
        if token.type != expected:
            raise ValueError(f"Expected token {expected} and found {token.type}")
        return self.consume()

    def parse_expression(self, precedence: Precedence = Precedence(0)) -> Expression:
        token = self.consume()
        prefix_parselet = self.prefix_parselets.get(token.type, None)
        if not prefix_parselet:
            raise ValueError(f"Could not parse \"{token.text}\".")

        left = prefix_parselet.parse(self, token)

        while precedence < self.precedence():
            infix_token = self.look_ahead(0)
            if infix_token.type == TokenType.EOF:
                break
            infix_parselet = self.infix_parselets.get(infix_token.type, None)
            if not infix_parselet:
                break
            token = self.consume()
            left = infix_parselet.parse(self, left, token)

        return left

    def precedence(self):
        parser = self.infix_parselets.get(self.look_ahead(0).type, None)
        if parser:
            return parser.precedence()
        return Precedence(0)

    def register(self, token: TokenType, parselet: PrefixParselet | InfixParselet):
        if isinstance(parselet, PrefixParselet):
            self.prefix_parselets[token] = parselet
        elif isinstance(parselet, InfixParselet):
            self.infix_parselets[token] = parselet
        else:
            raise NotImplementedError()
