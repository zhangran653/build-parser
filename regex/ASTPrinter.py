from regex.Parser import Visitor, RangeQuantifier, Character, Backreference, CharRange, \
    CharacterGroup, Match, Group, SubExpression, Expression, CharClassAnyWord, CharClassAnyWordInverted, \
    CharClassAnyDecimalDigit, CharClassAnyDecimalDigitInverted, CharClassAnyWhitespace, CharClassAnyWhitespaceInverted


class ASTPrinter(Visitor):

    def visit_expression(self, expr: Expression):
        if expr.alternation:
            return f'{{"type":"Alternation","subexpression":{expr.subexpression.accept(self)}, "alternation": {expr.alternation.accept(self)} }}'
        return expr.subexpression.accept(self)

    def visit_subexpression(self, expr: SubExpression):
        return f'{{ "type":"Concat", "expressions": [{",".join(x.accept(self) for x in expr.items)}] }}'

    def visit_group(self, expr: Group):
        return f'{{"type":"Group","expression":{expr.expression.accept(self)} ,"non_capturing": {1 if expr.non_capturing else 0}, "quantifier":{expr.quantifier.accept(self) if expr.quantifier else "null"} }}'

    def visit_match(self, expr: Match):
        return f'{{"type":"Match","quantifier":{expr.quantifier.accept(self) if expr.quantifier else "null"}, "match_item":{expr.match_item.accept(self)} }}'

    def visit_character_group(self, expr: CharacterGroup):
        return f'{{"type":"CharacterGroup","negative":"{expr.negative}","items":[{",".join(x.accept(self) for x in expr.items)}] }}'

    def visit_char_class_any_word(self, expr: CharClassAnyWord):
        return f'{{"type":"CharClassAnyWord","token":"{expr.value.value}" }}'

    def visit_char_class_any_word_inv(self, expr: CharClassAnyWordInverted):
        return f'{{"type":"CharClassAnyWordInv","token":"{expr.value.value}" }}'

    def visit_char_class_any_digit(self, expr: CharClassAnyDecimalDigit):
        return f'{{"type":"CharClassAnyDigit","token":"{expr.value.value}" }}'

    def visit_char_class_any_digit_inv(self, expr: CharClassAnyDecimalDigitInverted):
        return f'{{"type":"CharClassAnyDigitInv","token":"{expr.value.value}" }}'

    def visit_char_class_any_white_space(self, expr: CharClassAnyWhitespace):
        return f'{{"type":"CharClassAnyWhiteSpace","token":"{expr.value.value}" }}'

    def visit_char_class_any_white_space_inv(self, expr: CharClassAnyWhitespaceInverted):
        return f'{{"type":"CharClassAnyWhiteSpaceInv","token":"{expr.value.value}" }}'

    def visit_character_range(self, expr: CharRange):
        return f'{{"type":"CharacterRange","from":"{self.escape_json_string(expr.start.value)}","to":"{self.escape_json_string(expr.to.value) if expr.to else "null"}" }}'

    def visit_backreference(self, expr: Backreference):
        return f'{{"type":"Backreference","token":"{expr.number.value}"}}'

    def visit_any_char(self, expr):
        return f'{{"type":"MatchAnyCharacter","token":"."}}'

    def visit_character(self, expr: Character):
        return f'{{"type":"Character","token":"{self.escape_json_string(expr.token.value)}"}}'

    def visit_range_quantifier(self, expr: RangeQuantifier):
        return f'{{"type":"RangeQuantifier","low_bound":{expr.low_bound},"fixed_bound":{1 if expr.fixed_bound else 0}, "up_bound":{expr.up_bound if expr.up_bound else "null"} }}'

    def visit_zero_or_more_quantifier(self, expr):
        return f'{{"type":"ZeroOrMoreQuantifier","token":"*"}}'

    def visit_one_or_more_quantifier(self, expr):
        return f'{{"type":"OneOrMoreQuantifier","token":"+"}}'

    def visit_zero_or_one_quantifier(self, expr):
        return f'{{"type":"ZeroOrOneQuantifier","token":"?"}}'

    def visit_anchor_start_of_string(self, expr):
        return f'{{"type":"AnchorEndOfString","token":"^"}}'

    def visit_anchor_end_of_string(self, expr):
        return f'{{"type":"AnchorEndOfString","token":"$"}}'

    def visit_anchor_word_bound(self, expr):
        return f'{{"type":"AnchorWordBoundary","token":"\\b"}}'

    def visit_anchor_non_word_bound(self, expr):
        return f'{{"type":"AnchorNonWordBoundary","token":"\\B"}}'

    def visit_anchor_start_of_string_only(self, expr):
        return f'{{"type":"AnchorStartOfStringOnly","token":"\\A"}}'

    def visit_anchor_start_of_string_only_nnl(self, expr):
        return f'{{"type":"AnchorEndOfStringOnlyNotNewline","token":"\\z"}}'

    def visit_anchor_end_of_string_only(self, expr):
        return f'{{"type":"AnchorEndOfStringOnly","token":"\\Z"}}'

    def visit_anchor_pre_match_end(self, expr):
        return f'{{"type":"AnchorPreviousMatchEnd","token":"\\G"}}'

    @staticmethod
    def escape_json_string(s: str) -> str:
        escaped_string = ""
        for char in s:
            if char == '\\':
                escaped_string += '\\\\'
            elif char == '"':
                escaped_string += '\\"'
            # Add more conditions here for other special characters as needed.
            else:
                escaped_string += char
        return escaped_string

    def ast_string(self, exprs: Expression):
        if exprs:
            return exprs.accept(self)
        return "{}"
