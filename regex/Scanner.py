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
            '|': TokenType.OR,
            ',': TokenType.COMMA,
            ':': TokenType.COLON
        }
        self.escape_map = {
            'w': TokenType.ANY_WORD,
            'W': TokenType.ANY_WORD_INVERTED,
            'd': TokenType.ANY_DIGIT,
            'D': TokenType.ANY_DIGIT_INVERTED,
            's': TokenType.ANY_WHITE_SPACE,
            'S': TokenType.ANY_WHITE_SPACE_INVERTED,
            'b': TokenType.WORD_BOUND,
            'B': TokenType.NON_WORD_BOUND,
            'A': TokenType.START_OF_STRING_ONLY,
            'z': TokenType.END_OFF_STRING_ONLY_NOT_NEWLINE,
            'Z': TokenType.END_OFF_STRING_ONLY,
            'G': TokenType.PRE_MATCH_END
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF))
        return self.tokens

    def is_end(self) -> bool:
        return self.current >= len(self.input)

    def _scan_token(self):
        char = self.advance()
        token_type = self.token_map.get(char, None)
        # can be normal char or invalid char
        if not token_type:
            if self.is_valid_char(char):
                if char.isdigit():
                    self.add_token(TokenType.INT, char)
                elif (65 <= ord(char) <= 90) or (97 <= ord(char) <= 122):
                    self.add_token(TokenType.LETTER, char)
                elif char.isascii():
                    self.add_token(TokenType.ASCII, char)
                else:
                    self.add_token(TokenType.CHAR, char)
            else:
                raise ValueError(f"character {char} at {self.current} not supported")
        else:
            if token_type == TokenType.ESCAPE:
                # escapes
                next_char = self.peek()
                if next_char == '\0':
                    self.add_token(TokenType.ASCII, char)
                else:
                    if next_char in self.token_map:
                        # TODO
                        self.advance()
                        self.add_token(TokenType.ASCII, next_char)
                    elif next_char in self.escape_map:
                        self.advance()
                        self.add_token(self.escape_map[next_char], next_char)
                    else:
                        self.add_token(TokenType.ESCAPE, char)
                        #  raise ValueError(f"character {char} at {self.current} can't be escaped")
            else:
                self.add_token(token_type, char)

    def advance(self) -> str:
        self.current += 1
        return self.input[self.current - 1]

    def add_token(self, token_type: TokenType, value: str = None):
        self.tokens.append(Token(token_type, value))

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
