from regex.Facade import Expression, SubExpression, AnyChar, Expr, Match, RangeQuantifier, ZeroOrMoreQuantifier, \
    OneOrMoreQuantifier, ZeroOrOneQuantifier, Group, AnchorStartOfString, AnchorWordBoundary, AnchorNonWordBoundary, \
    AnchorStartOfStringOnly, AnchorEndOfStringOnlyNotNewline, AnchorEndOfStringOnly, AnchorPreviousMatchEnd, \
    AnchorEndOfString, CharacterGroup, CharRange, Backreference, CharClassAnyWhitespaceInverted, CharClassAnyWhitespace, \
    CharClassAnyWord, CharClassAnyWordInverted, CharClassAnyDecimalDigit, CharClassAnyDecimalDigitInverted, Character
from regex.Scanner import Token
from regex.Scanner import TokenType

# Anchor ::= "^" | "\b" | "\B" | "\A" | "\z" | "\Z" | "\G" | "$"
ANCHORS = [TokenType.S_ANCHOR,
           TokenType.WORD_BOUND,
           TokenType.NON_WORD_BOUND,
           TokenType.START_OF_STRING_ONLY,
           TokenType.END_OFF_STRING_ONLY,
           TokenType.END_OFF_STRING_ONLY_NOT_NEWLINE,
           TokenType.PRE_MATCH_END,
           TokenType.E_ANCHOR]

# CharacterClass ::= "\w" | "\W" | "\d" | "\D" | "\s" | "\S"
CHAR_CLASS = [
    TokenType.ANY_WORD,
    TokenType.ANY_WORD_INVERTED,
    TokenType.ANY_DIGIT,
    TokenType.ANY_DIGIT_INVERTED,
    TokenType.ANY_WHITE_SPACE,
    TokenType.ANY_WHITE_SPACE_INVERTED
]

# Char ::= #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]
CHAR_NO_RIGHT_BRACKET = [
    # TokenType.RIGHT_BRACKET,
    TokenType.RIGHT_BRACE,
    TokenType.LEFT_BRACE,
    TokenType.COMMA,
    TokenType.COLON,
    TokenType.LESS,
    TokenType.GREAT,
    TokenType.MINUS,
    TokenType.INT,
    TokenType.LETTER,
    TokenType.ASCII,
    TokenType.CHAR,
]

CHAR = CHAR_NO_RIGHT_BRACKET + [TokenType.RIGHT_BRACKET]

# in character group [], these tokens are seen as literal char
CHAR_GROUP_LITERALS = CHAR_NO_RIGHT_BRACKET + [TokenType.LEFT_PAREN,
                                               TokenType.RIGHT_PAREN,
                                               TokenType.DOT,
                                               TokenType.PLUS,
                                               TokenType.STAR,
                                               TokenType.S_ANCHOR,
                                               TokenType.E_ANCHOR,
                                               TokenType.OR]

# Match ::= ( "." | CharacterGroup | CharacterClass | Char ) Quantifier?
MATCH_EXPR_TYPES = [TokenType.DOT] + [TokenType.LEFT_BRACKET] + CHAR_CLASS + CHAR

# Quantifier ::= ( "*" | "+" | "?" | "{" Integer ( "," Integer? )? "}" ) LazyModifier?
QUANTIFIER = [
    TokenType.STAR,
    TokenType.PLUS,
    TokenType.QUESTION,
    TokenType.LEFT_BRACE
]


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        if not self.at_end():
            return self.expression()
        return None

    def expression(self) -> Expression:
        sub_expr = self.subexpression()
        expression = Expression(sub_expr)
        if self.match(TokenType.OR):
            expression.alternation = self.expression()
        return expression

    def subexpression(self) -> SubExpression:
        """
        Subexpression ::= (Match | Group | Anchor | Backreference)+
        :return:
        """
        items = []
        if self.match(*ANCHORS):
            items.append(self.anchor())
        elif self.match(TokenType.LEFT_PAREN):
            items.append(self.group())
        elif self.match(*MATCH_EXPR_TYPES):
            items.append(self.match_expr())
        elif self.match(TokenType.ESCAPE):
            items.append(self.back_reference())
        else:
            raise ValueError(f"{self.peek()} not expected: expect sub expression")

        while True:
            if self.match(*ANCHORS):
                items.append(self.anchor())
            elif self.match(TokenType.LEFT_PAREN):
                items.append(self.group())
            elif self.match(*MATCH_EXPR_TYPES):
                items.append(self.match_expr())
            elif self.match(TokenType.ESCAPE):
                items.append(self.back_reference())
            else:
                break
        sub_expr = SubExpression(items)
        return sub_expr

    def match_expr(self):
        """
        Match ::= ( "." | CharacterGroup | CharacterClass | Char ) Quantifier?
        CharacterGroup ::= "[" "^"? (CharacterClass | CharacterRange | Char - "]")+ "]"
        CharacterClass ::= "\w" | "\W" | "\d" | "\D" | "\s" | "\S"
        CharacterRange ::= Char "-" Char
        :return:
        """
        if self.previous().type == TokenType.DOT:
            item = self.any_char()
        elif self.previous().type == TokenType.LEFT_BRACKET:
            item = self.char_group()
        elif self.previous().type in CHAR_CLASS:
            item = self.char_class()
        else:
            item = self.char()
        match = Match(item)
        if self.match(*QUANTIFIER):
            return self.quantifier(match)
        return match

    def any_char(self) -> AnyChar:
        """
        MatchAnyCharacter ::= "."
        :return:
        """
        return AnyChar()

    def quantifier(self, expr: Expr):
        """
        Range Quantifiers can only be applied to:
        - Individual characters: For example, a{2,4} matches "aa", "aaa", or "aaaa".
        - Character classes: For example, [a-z]{2,4} matches any lowercase letter sequence of length 2 to 4.
        - Grouped expressions: For example, (abc){2,4} matches "abcabc", "abcabcabc", or "abcabcabcabc".
        - Character sets with special meaning: . \d \w \s
        - Negated character classes:\D \W \S
        - Backreferences

        Quantifier ::= ( "*" | "+" | "?" | "{" Integer+ ( "," Integer* )? "}" ) LazyModifier?
        :return:
        """
        token = self.previous()
        if token.type == TokenType.LEFT_BRACE:
            self.consume(TokenType.INT, "expect integer for range quantifier lower bound")
            low_bound = self.previous()
            low = int(low_bound.value)
            while self.match(TokenType.INT):
                low_bound = self.previous()
                low = low * 10 + int(low_bound.value)
            rq = RangeQuantifier(expr, low)

            if self.match(TokenType.COMMA):
                rq.fixed_bound = False
                if self.match(TokenType.INT):
                    up_bound = self.previous()
                    u = int(up_bound.value)
                    while self.match(TokenType.INT):
                        up_bound = self.previous()
                        u = u * 10 + int(up_bound.value)
                    if low > u:
                        raise ValueError(f"{up_bound}: upper bound must greater than lower bound:{u}<{low}")
                    rq.up_bound = u
            self.consume(TokenType.RIGHT_BRACE, "expect '}' for range quantifier ends")
            expr = rq
        elif token.type == TokenType.STAR:
            expr = ZeroOrMoreQuantifier(expr)
        elif token.type == TokenType.PLUS:
            expr = OneOrMoreQuantifier(expr)
        else:
            expr = ZeroOrOneQuantifier(expr)

        if self.match(TokenType.QUESTION):
            expr.lazy = True
        return expr

    def group(self):
        """
        Group ::= "(" ( "?:" | "?<" (Letters | Integer)+ ">" )? Expression ")" Quantifier?
        :return:
        """
        non_capturing = False
        group_name = None
        atomic = False
        if self.check(TokenType.QUESTION) and self.check_next(TokenType.COLON):
            self.consume(TokenType.QUESTION, "")
            self.consume(TokenType.COLON, "")
            non_capturing = True
        elif self.check(TokenType.QUESTION) and self.check_next(TokenType.LESS):
            self.consume(TokenType.QUESTION, "")
            self.consume(TokenType.LESS, "")
            group_name = self.group_name()
        elif self.check(TokenType.QUESTION) and self.check_next(TokenType.GREAT):
            self.consume(TokenType.QUESTION, "")
            self.consume(TokenType.GREAT, "")
            # atomic groups are non-capturing group
            atomic = True
            non_capturing = True

        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "expect ')' at group end")
        g = Group(expr, non_capturing, group_name, atomic)
        if self.match(*QUANTIFIER):
            return self.quantifier(g)
        return g

    def group_name(self) -> str:
        """
        (Letters | Integer)+ ">"
        :return:
        """
        name = ''
        while self.match(TokenType.LETTER, TokenType.INT):
            name = f'{name}{self.previous().value}'
        if len(name) == 0:
            raise ValueError(f"{self.peek()} not expected. expect letter or integer for group name")
        self.consume(TokenType.GREAT, "expect '>' for end of group name")
        return name

    def anchor(self):
        """
        Anchor ::= "^" | "\b" | "\B" | "\A" | "\z" | "\Z" | "\G" | "$"
        :return:
        """
        token = self.previous()
        if token.type == TokenType.S_ANCHOR:
            return AnchorStartOfString(token)
        elif token.type == TokenType.WORD_BOUND:
            return AnchorWordBoundary(token)
        elif token.type == TokenType.NON_WORD_BOUND:
            return AnchorNonWordBoundary(token)
        elif token.type == TokenType.START_OF_STRING_ONLY:
            return AnchorStartOfStringOnly(token)
        elif token.type == TokenType.END_OFF_STRING_ONLY_NOT_NEWLINE:
            return AnchorEndOfStringOnlyNotNewline(token)
        elif token.type == TokenType.END_OFF_STRING_ONLY:
            return AnchorEndOfStringOnly(token)
        elif token.type == TokenType.PRE_MATCH_END:
            return AnchorPreviousMatchEnd(token)
        else:
            return AnchorEndOfString(token)

    def char_group(self):
        """
        CharacterGroup ::= "[" "^"? (CharacterClass | CharacterRange | Char - "]")+ "]"
        :return:
        """
        negative = False
        if self.match(TokenType.S_ANCHOR):
            negative = True

        items = []
        """
        "-" must between two characters, otherwise it's a normal character instead of range
        [-a] : '-'|'a'
        [z-] : 'z'|'-'
        [a-z]: 'a' to 'z' , 'a' must <= 'z'
        
        +, *, ?, {} . and more keywords in character group means match literal
        """
        if self.check(TokenType.RIGHT_BRACKET):
            raise ValueError(f"{self.peek()} not expected")
        if self.at_end():
            raise ValueError(f"expect character group")

        is_last_match_char = True
        while not self.at_end() and not self.check(TokenType.RIGHT_BRACKET):
            if self.match(*CHAR_CLASS):
                is_last_match_char = False
                items.append(self.char_class())
            else:
                # match char
                self.advance()
                if is_last_match_char and self.check(TokenType.MINUS) and (
                        not self.check_next(TokenType.EOF, TokenType.RIGHT_BRACKET, *CHAR_CLASS)):
                    items.append(self.char_range())
                else:
                    items.append(self.char())
                is_last_match_char = True

        if self.at_end():
            raise ValueError(f"expect ']' after character group")
        self.consume(TokenType.RIGHT_BRACKET, "")
        cg = CharacterGroup(items, negative)
        return cg

    def char_range(self) -> CharRange:
        """
        # CharacterRange ::= Char ("-" Char)?
        :return:
        """
        c = self.previous()
        cr = CharRange(c)
        self.consume(TokenType.MINUS, "")
        self.advance()
        cr.to = self.previous()
        if ord(cr.start.value) > ord(cr.to.value):
            raise ValueError(f"{cr.to}: character range is out of order,{cr.start.value}-{cr.to.value}")
        return cr

    def char_class(self):
        """
        # CharacterClass ::= "\w" | "\W" | "\d" | "\D" | "\s" | "\S"
        :return:
        """
        token = self.previous()
        if token.type == TokenType.ANY_WORD:
            return CharClassAnyWord(token)
        elif token.type == TokenType.ANY_WORD_INVERTED:
            return CharClassAnyWordInverted(token)
        elif token.type == TokenType.ANY_DIGIT:
            return CharClassAnyDecimalDigit(token)
        elif token.type == TokenType.ANY_DIGIT_INVERTED:
            return CharClassAnyDecimalDigitInverted(token)
        elif token.type == TokenType.ANY_WHITE_SPACE:
            return CharClassAnyWhitespace(token)
        elif token.type == TokenType.ANY_WHITE_SPACE_INVERTED:
            return CharClassAnyWhitespaceInverted(token)

    def back_reference(self):
        self.consume(TokenType.INT, "expect integer in back reference")
        group_id = f'{self.previous().value}'
        while self.match(TokenType.INT):
            group_id = f'{group_id}{self.previous().value}'

        return Backreference(int(group_id))

    def char(self) -> Character:
        c = self.previous()
        return Character(c)

    def at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.at_end():
            self.current += 1
        return self.previous()

    def match(self, *token_types) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type: TokenType, msg: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise ValueError(f"char at pos [{self.current}] not expected: {msg}")

    def check(self, *token_type) -> bool:
        if self.at_end():
            return False
        for t in token_type:
            if self.peek().type == t:
                return True
        return False

    def check_next(self, *token_type) -> bool:
        if self.at_end():
            return False
        if self.tokens[self.current + 1].type == TokenType.EOF:
            return False
        for t in token_type:
            if self.tokens[self.current + 1].type == t:
                return True
        return False
