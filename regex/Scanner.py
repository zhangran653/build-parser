from enum import Enum


class TokenType(Enum):
    # single token
    LEFT_PAREN = 0  # (
    RIGHT_PAREN = 1  # )
    LEFT_BRACE = 2  # {
    RIGHT_BRACE = 3  # }
    DOT = 4  # .
    PLUS = 5  # +
    LEFT_BRACKET = 6  # [
    RIGHT_BRACKET = 7  # ]
    MINUS = 8  # -
    STAR = 9  # *
    QUESTION = 10  # ?
    # EQUAL = 11  # =
    S_ANCHOR = 12  # ^
    E_ANCHOR = 13  # $
    ESCAPE = 14  # \
    OR = 15  # |
    CHAR = 16  # normal character

    EOF = -1  # EOF


class Token:
    def __init__(self, type_: TokenType, value: str = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Scanner:
    def __init__(self, input_):
        self.input = input_
        self.tokens = []
        self.start = 0
        self.current = 0
        self.token_map = {
            '(': TokenType.LEFT_PAREN,
            ')': TokenType.RIGHT_PAREN,
            '[': TokenType.LEFT_BRACKET,
            ']': TokenType.RIGHT_BRACKET,
            '{': TokenType.LEFT_BRACE,
            '}': TokenType.RIGHT_BRACE,
            '.': TokenType.DOT,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '?': TokenType.QUESTION,
            # '=': TokenType.EQUAL,
            '^': TokenType.S_ANCHOR,
            '$': TokenType.E_ANCHOR,
            '\\': TokenType.ESCAPE,
            '|': TokenType.OR
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF))
        return self.tokens

    def is_end(self) -> bool:
        return self.current >= len(self.input)

    def scan_token(self):
        char = self.advance()
        token_type = self.token_map.get(char, None)
        if not token_type:
            if self.is_valid_char(char):
                self.add_token(TokenType.CHAR)
            else:
                raise ValueError(f"character {char} not supported")
        else:
            pass

    def advance(self) -> str:
        self.current += 1
        return self.input[self.current - 1]

    def add_token(self, token_type: TokenType):
        self.tokens.append(Token(token_type))

    def match(self, expected: str) -> bool:
        if self.is_end():
            return False
        if self.input[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_end():
            return '\0'
        return self.input[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.input):
            return '\0'
        return self.input[self.current + 1]

    def is_valid_char(self, char):
        code_point = ord(char)
        return (
                code_point == 0x9 or
                code_point == 0xA or
                code_point == 0xD or
                0x20 <= code_point <= 0xD7FF or
                0xE000 <= code_point <= 0xFFFD or
                0x10000 <= code_point <= 0x10FFFF
        )
