from regex.Facade import Visitor
from regex.Parser import RangeQuantifier, Character, Backreference, CharRange, \
    CharacterGroup, Match, Group, SubExpression, Expression, CharClassAnyWord, CharClassAnyWordInverted, \
    CharClassAnyDecimalDigit, CharClassAnyDecimalDigitInverted, CharClassAnyWhitespace, CharClassAnyWhitespaceInverted, \
    ZeroOrOneQuantifier, OneOrMoreQuantifier, ZeroOrMoreQuantifier


class ASTPrinter(Visitor):

    def visit_expression(self, expr: Expression):
        if expr.alternation:
            return f'{{' \
                   f'   "type":"Alternation",' \
                   f'   "subexpression":{expr.subexpression.accept(self)}, ' \
                   f'   "alternation": {expr.alternation.accept(self)} ' \
                   f'}}'
        return expr.subexpression.accept(self)

    def visit_subexpression(self, expr: SubExpression):
        return f'{{' \
               f'   "type":"Concat", ' \
               f'   "expressions": [{",".join(x.accept(self) for x in expr.items)}]' \
               f'}}'

    def visit_group(self, expr: Group):
        return f'{{' \
               f'   "type":"Group",' \
               f'   "expression":{expr.expression.accept(self)} ,' \
               f'   "non_capturing": {1 if expr.non_capturing else 0}, ' \
               f'   "group_name": "{expr.group_name if expr.group_name else "null"}" ' \
               f'}}'

    def visit_match(self, expr: Match):
        return f'{{' \
               f'   "type":"Match",' \
               f'   "match_item":{expr.match_item.accept(self)} ' \
               f'}}'

    def visit_character_group(self, expr: CharacterGroup):
        return f'{{' \
               f'   "type":"CharacterGroup",' \
               f'   "negative":{1 if expr.negative else 0},' \
               f'   "items":[{",".join(x.accept(self) for x in expr.items)}]' \
               f'}}'

    def visit_char_class_any_word(self, expr: CharClassAnyWord):
        return f'{{' \
               f'   "type":"CharClassAnyWord",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_char_class_any_word_inv(self, expr: CharClassAnyWordInverted):
        return f'{{' \
               f'   "type":"CharClassAnyWordInv",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_char_class_any_digit(self, expr: CharClassAnyDecimalDigit):
        return f'{{' \
               f'   "type":"CharClassAnyDigit",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_char_class_any_digit_inv(self, expr: CharClassAnyDecimalDigitInverted):
        return f'{{' \
               f'   "type":"CharClassAnyDigitInv",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_char_class_any_white_space(self, expr: CharClassAnyWhitespace):
        return f'{{' \
               f'   "type":"CharClassAnyWhiteSpace",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_char_class_any_white_space_inv(self, expr: CharClassAnyWhitespaceInverted):
        return f'{{' \
               f'   "type":"CharClassAnyWhiteSpaceInv",' \
               f'   "token":"{expr.value.value}" ' \
               f'}}'

    def visit_character_range(self, expr: CharRange):
        return f'{{' \
               f'   "type":"CharacterRange",' \
               f'   "from":"{self.escape_json_string(expr.start.value)}",' \
               f'   "to":"{self.escape_json_string(expr.to.value) if expr.to else "null"}" ' \
               f'}}'

    def visit_backreference(self, expr: Backreference):
        return f'{{' \
               f'   "type":"Backreference",' \
               f'   "token":{expr.number}' \
               f'}}'

    def visit_any_char(self, expr):
        return f'{{\n' \
               f'   "type":"MatchAnyCharacter",\n' \
               f'   "token":"."\n' \
               f'}}\n'

    def visit_character(self, expr: Character):
        return f'{{' \
               f'   "type":"Character",' \
               f'   "token":"{self.escape_json_string(expr.token.value)}"' \
               f'}}'

    def visit_range_quantifier(self, expr: RangeQuantifier):
        return f'{{' \
               f'   "type":"RangeQuantifier",' \
               f'   "expression":{expr.expr.accept(self)},' \
               f'   "low_bound":{expr.low_bound},' \
               f'   "fixed_bound":{1 if expr.fixed_bound else 0},' \
               f'   "up_bound":{expr.up_bound if expr.up_bound else "null"}, ' \
               f'   "lazy": {1 if expr.lazy else 0} ' \
               f'}}'

    def visit_zero_or_more_quantifier(self, expr: ZeroOrMoreQuantifier):
        return f'{{' \
               f'   "type":"ZeroOrMoreQuantifier",' \
               f'   "expression":{expr.expr.accept(self)}, ' \
               f'   "lazy": {1 if expr.lazy else 0}' \
               f'}}'

    def visit_one_or_more_quantifier(self, expr: OneOrMoreQuantifier):
        return f'{{' \
               f'   "type":"OneOrMoreQuantifier",' \
               f'   "expression":{expr.expr.accept(self)},' \
               f'   "lazy": {1 if expr.lazy else 0} ' \
               f'}}'

    def visit_zero_or_one_quantifier(self, expr: ZeroOrOneQuantifier):
        return f'{{' \
               f'   "type":"ZeroOrOneQuantifier",' \
               f'   "expression":{expr.expr.accept(self)}, ' \
               f'   "lazy": {1 if expr.lazy else 0} ' \
               f'}}'

    def visit_anchor_start_of_string(self, expr):
        return f'{{' \
               f'   "type":"AnchorEndOfString",' \
               f'   "token":"^"' \
               f'}}'

    def visit_anchor_end_of_string(self, expr):
        return f'{{' \
               f'   "type":"AnchorEndOfString",' \
               f'   "token":"$"' \
               f'}}'

    def visit_anchor_word_bound(self, expr):
        return f'{{' \
               f'   "type":"AnchorWordBoundary",' \
               f'   "token":"\\b"' \
               f'}}'

    def visit_anchor_non_word_bound(self, expr):
        return f'{{' \
               f'   "type":"AnchorNonWordBoundary",' \
               f'   "token":"\\B"' \
               f'}}'

    def visit_anchor_start_of_string_only(self, expr):
        return f'{{' \
               f'   "type":"AnchorStartOfStringOnly",' \
               f'   "token":"\\A"' \
               f'}}'

    def visit_anchor_start_of_string_only_nnl(self, expr):
        return f'{{' \
               f'   "type":"AnchorEndOfStringOnlyNotNewline",' \
               f'   "token":"\\z"' \
               f'}}'

    def visit_anchor_end_of_string_only(self, expr):
        return f'{{' \
               f'   "type":"AnchorEndOfStringOnly",' \
               f'   "token":"\\Z"' \
               f'}}'

    def visit_anchor_pre_match_end(self, expr):
        return f'{{' \
               f'   "type":"AnchorPreviousMatchEnd",' \
               f'   "token":"\\G"' \
               f'}}'

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
