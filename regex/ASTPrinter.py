from regex.Parser import Visitor, RangeQuantifier, Character, Backreference, CharRange, CharacterClass, \
    CharacterGroup, Match, Group, SubExpression, Expression


class ASTPrinter(Visitor):

    def visit_expression(self, expr: Expression):
        if expr.alternation:
            return f'{{"type":"Alternation","subexpression":{expr.subexpression.accept(self)}, "alternation": {expr.alternation.accept(self)} }}'
        return expr.subexpression.accept(self)

    def visit_subexpression(self, expr: SubExpression):
        if len(expr.items) == 1:
            return expr.items[0].accept(self)
        else:
            return f'[{",".join(x.accept(self) for x in expr.items)}]'

    def visit_group(self, expr: Group):
        return f'{{"type":"Group","expression":{expr.expression.accept(self)} ,"non_capturing": {expr.non_capturing}, "quantifier":{expr.quantifier.accept(self)} }}'

    def visit_match(self, expr: Match):
        return f'{{"type":"Match","quantifier":{expr.quantifier.accept(self) if expr.quantifier else "null"}, "match_item":{expr.match_item.accept(self)} }}'

    def visit_character_group(self, expr: CharacterGroup):
        return f'{{"type":"CharacterGroup","negative":"{expr.negative}","items":[{",".join(x.accept(self) for x in expr.items)}] }}'

    def visit_character_class(self, expr: CharacterClass):
        return f'{{"type":"CharacterClass","token":"{expr.value.value}" }}'

    def visit_character_range(self, expr: CharRange):
        return f'{{"type":"CharacterRange","from":"{expr.start.value}","to":"{expr.to.value if expr.to else "null"}" }}'

    def visit_backreference(self, expr: Backreference):
        return f'{{"type":"Backreference","token":"{expr.number.value}"}}'

    def visit_any_char(self, expr):
        return f'{{"type":"MatchAnyCharacter","token":"."}}'

    def visit_character(self, expr: Character):
        return f'{{"type":"Character","token":"{expr.token.value}"}}'

    def visit_range_quantifier(self, expr: RangeQuantifier):
        return f'{{"type":"RangeQuantifier","low_bound":{expr.low_bound.value},"up_bound":{expr.up_bound.value if expr.up_bound else "null"} }}'

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

    def ast_string(self, exprs):
        ret = []
        for x in exprs:
            ret.append(x.accept(self))
        if len(ret) > 1:
            return f'[{",".join(x for x in ret)}]'
        else:
            return ret[0]
