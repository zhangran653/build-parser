from regex.Scanner import Token
from regex.Scanner import TokenType


class Expr:
    def accept(self, visitor):
        raise NotImplementedError()


class Visitor:

    @staticmethod
    def visit_expression(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_subexpression(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_group(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_match(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_character_group(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_character_class(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_character_range(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_backreference(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_any_char(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_character(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_range_quantifier(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_zero_or_more_quantifier(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_one_or_more_quantifier(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_zero_or_one_quantifier(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_start_of_string(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_end_of_string(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_word_bound(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_non_word_bound(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_start_of_string_only(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_start_of_string_only_nnl(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_end_of_string_only(expr):
        raise NotImplementedError()

    @staticmethod
    def visit_anchor_pre_match_end(expr):
        raise NotImplementedError()


class Expression(Expr):
    def __init__(self, subexpression, alternation=None):
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
    def __init__(self, match_item, quantifier=None):
        self.match_item = match_item
        self.quantifier = quantifier

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
    def __init__(self, expression, non_capturing=False, quantifier=None):
        self.expression = expression
        self.non_capturing = non_capturing
        self.quantifier = quantifier

    def accept(self, visitor):
        return visitor.visit_group(self)


class CharacterGroup(Expr):
    def __init__(self, items, negative=False):
        self.items = items
        self.negative = negative

    def accept(self, visitor):
        return visitor.visit_character_group(self)


class CharacterClass(Expr):
    def __init__(self, value: Token):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_character_class(self)


class Backreference(Expr):
    def __init__(self, number):
        self.number = number

    def accept(self, visitor):
        return visitor.visit_backreference(self)


class Character(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_character(self)


class RangeQuantifier(Expr):
    def __init__(self, low_bound: Token, up_bound: Token = None):
        self.low_bound = low_bound
        self.up_bound = up_bound

    def accept(self, visitor):
        return visitor.visit_range_quantifier(self)


class ZeroOrMoreQuantifier(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_zero_or_more_quantifier(self)


class OneOrMoreQuantifier(Expr):
    def __init__(self, token: Token):
        self.token = token

    def accept(self, visitor):
        return visitor.visit_one_or_more_quantifier(self)


class ZeroOrOneQuantifier(Expr):
    def __init__(self, token: Token):
        self.token = token

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
CHAR = [
    TokenType.RIGHT_BRACKET,
    TokenType.RIGHT_BRACE,
    TokenType.RIGHT_PAREN,
    TokenType.LEFT_BRACE,
    TokenType.COMMA,
    TokenType.COLON,
    TokenType.MINUS,
    TokenType.INT,
    TokenType.LETTER,
    TokenType.ASCII,
    TokenType.CHAR,
]

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

    def parse(self) -> list[Expr]:
        expressions = []
        while not self.at_end():
            expressions.append(self.expression())
        return expressions

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
        elif self.match(TokenType.ESCAPE):
            items.append(self.back_reference())
        elif self.match(TokenType.LEFT_PAREN):
            items.append(self.group())
        elif self.match(*MATCH_EXPR_TYPES):
            items.append(self.match_expr())
        else:
            raise ValueError(f"{self.peek()} not expected: expect sub expression")

        while True:
            if self.match(*ANCHORS):
                items.append(self.anchor())
            elif self.match(TokenType.ESCAPE):
                items.append(self.back_reference())
            elif self.match(TokenType.LEFT_PAREN):
                items.append(self.group())
            elif self.match(*MATCH_EXPR_TYPES):
                items.append(self.match_expr())
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
            match.quantifier = self.quantifier()
        return match

    def any_char(self) -> AnyChar:
        """
        MatchAnyCharacter ::= "."
        :return:
        """
        return AnyChar()

    def quantifier(self):
        """
        Quantifier ::= ( "*" | "+" | "?" | "{" Integer ( "," Integer? )? "}" ) LazyModifier?
        :return:
        """
        token = self.previous()
        if token.type == TokenType.LEFT_BRACE:
            self.consume(TokenType.INT, "expect integer for range quantifier lower bound")
            low_bound = self.previous()
            rq = RangeQuantifier(low_bound)
            if self.match(TokenType.COMMA) and self.match(TokenType.INT):
                up_bound = self.previous()
                rq.up_bound = up_bound
            self.consume(TokenType.RIGHT_BRACE, "expect '}' for range quantifier ends")
            expr = rq
        elif token.type == TokenType.STAR:
            expr = ZeroOrMoreQuantifier(token)
        elif token.type == TokenType.PLUS:
            expr = OneOrMoreQuantifier(token)
        else:
            expr = ZeroOrOneQuantifier(token)

        if self.match(TokenType.QUESTION):
            expr.lazy = True
        return expr

    def group(self):
        """
        Group ::= "(" ( "?:" )? Expression ")" Quantifier?
        :return:
        """
        non_capturing = False
        if self.check(TokenType.QUESTION) and self.check_next(TokenType.COLON):
            self.consume(TokenType.QUESTION, "")
            self.consume(TokenType.COLON, "")
            non_capturing = True

        expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "expect ')' at group end")
        g = Group(expr, non_capturing)
        if self.match(*QUANTIFIER):
            q = self.quantifier()
            g.quantifier = q
        return g

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

        if self.match(*CHAR_CLASS):
            items.append(self.char_class())
        elif self.match(*CHAR):
            if self.check(TokenType.MINUS):
                items.append(self.char_range())
            else:
                items.append(self.char())
        else:
            raise ValueError(f"{self.peek()} not expected: expect char_group")

        while True:
            if self.match(*CHAR_CLASS):
                items.append(self.char_class())
            elif self.match(*CHAR):
                if self.check(TokenType.MINUS):
                    items.append(self.char_range())
                else:
                    items.append(self.char())
            else:
                break
        self.consume(TokenType.RIGHT_BRACKET, "expect ']' after character group")
        cg = CharacterGroup(items, negative)
        return cg

    def char_range(self) -> CharRange:
        """
        # CharacterRange ::= Char "-" (Char)?
        :return:
        """
        c = self.previous()
        cr = CharRange(c)
        self.consume(TokenType.MINUS, "")
        if self.match(*CHAR):
            cr.to = self.previous()
        return cr

    def char_class(self) -> CharacterClass:
        """
        # CharacterClass ::= "\w" | "\W" | "\d" | "\D" | "\s" | "\S"
        :return:
        """
        return CharacterClass(self.previous())

    def back_reference(self):
        self.consume(TokenType.INT, "expect integer in backreference")
        return Backreference(self.previous())

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
        raise ValueError(f"{self.peek()} not expected: {msg}")

    def check(self, token_type: TokenType) -> bool:
        if self.at_end():
            return False
        return self.peek().type == token_type

    def check_next(self, token_type: TokenType) -> bool:
        if self.at_end():
            return False
        if self.tokens[self.current + 1].type == TokenType.EOF:
            return False
        return self.tokens[self.current + 1].type == token_type
