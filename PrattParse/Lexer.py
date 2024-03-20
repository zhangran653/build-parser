from PrattParse.Token import TokenType, Token


class Lexer:
    """
    A very primitive lexer.

    Takes a string and splits it into a series of Tokens. Operators and
    punctuation are mapped to unique keywords. Names,
    which can be any series of letters, are turned into NAME tokens. All other
    characters are ignored (except to separate names). Numbers and strings are
    not supported. This is really just the bare minimum to give the parser
    something to work with.
    """

    def __init__(self, source: str):
        self.index = 0
        self.source = source
        # Register all of the TokenTypes that are explicit punctuators.
        self.punctuators: dict[str, TokenType] = {}
        for _type in TokenType:
            p = _type.punctuator()
            if p is not None:
                self.punctuators[p] = _type

    def next(self) -> Token:
        while self.index < len(self.source):
            c = self.source[self.index]
            self.index += 1
            if c in self.punctuators:
                # punctuations
                return Token(self.punctuators[c], c)
            if c.isalpha():
                # names
                start = self.index - 1
                while self.index < len(self.source) and self.source[self.index].isalpha():
                    self.index += 1

                name = self.source[start:self.index]
                return Token(TokenType.NAME, name)
            # Ignore all other characters (whitespace, etc.)
        return Token(TokenType.EOF, "")
