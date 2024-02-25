from regex.Facade import Visitor
from regex.Interpreter import Interpreter
from regex.Parser import RangeQuantifier, CharacterGroup, Match, Group, SubExpression, Expression, CharClassAnyWord, \
    ZeroOrOneQuantifier, OneOrMoreQuantifier, ZeroOrMoreQuantifier, AnchorStartOfString, AnchorEndOfString, \
    AnchorWordBoundary, AnchorNonWordBoundary, AnchorStartOfStringOnly, AnchorEndOfStringOnlyNotNewline, \
    AnchorEndOfStringOnly, AnchorPreviousMatchEnd


class GroupNameGenerator:
    def __init__(self):
        self.id = 1

    def next(self):
        name = self.id
        self.id += 1
        return name

    def reset(self):
        self.id = 1


class Resolver(Visitor):

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.gg = GroupNameGenerator()
        self.interpreter.ast.accept(self)
        self.interpreter.group_count = len(self.interpreter.group_id_stack)

    def visit_expression(self, expr: Expression):
        if expr.alternation:
            expr.alternation.accept(self)
        expr.subexpression.accept(self)

    def visit_subexpression(self, expr: SubExpression):
        for exp in expr.items:
            exp.accept(self)

    def visit_group(self, expr: Group):
        if not expr.non_capturing:
            self.interpreter.group_id_stack.append(self.gg.next())
        expr.expression.accept(self)

    def visit_match(self, expr: Match):
        expr.match_item.accept(self)

    def visit_character_group(self, expr: CharacterGroup):
        for item in expr.items:
            item.accept(self)

    def visit_char_class_any_word(self, expr: CharClassAnyWord):
        pass

    def visit_char_class_any_word_inv(self, expr):
        pass

    def visit_char_class_any_digit(self, expr):
        pass

    def visit_char_class_any_digit_inv(self, expr):
        pass

    def visit_char_class_any_white_space(self, expr):
        pass

    def visit_char_class_any_white_space_inv(self, expr):
        pass

    def visit_character_range(self, expr):
        pass

    def visit_backreference(self, expr):
        pass

    def visit_any_char(self, expr):
        pass

    def visit_character(self, expr):
        pass

    def visit_range_quantifier(self, expr: RangeQuantifier):
        """
        Range Quantifiers can only be applied to:
             - Individual characters: For example, a{2,4} matches "aa", "aaa", or "aaaa".
             - Character classes: For example, [a-z]{2,4} matches any lowercase letter sequence of length 2 to 4.
             - Grouped expressions: For example, (abc){2,4} matches "abcabc", "abcabcabc", or "abcabcabcabc".
             - Character sets with special meaning: . \d \w \s
             - Negated character classes:\D \W \S
             - Backreferences
        :param expr:
        :return:
        """

        not_quantifiable = (
            ZeroOrMoreQuantifier, OneOrMoreQuantifier, ZeroOrOneQuantifier, AnchorStartOfString, AnchorWordBoundary,
            AnchorNonWordBoundary, AnchorStartOfStringOnly, AnchorEndOfStringOnlyNotNewline, AnchorEndOfStringOnly,
            AnchorPreviousMatchEnd, AnchorEndOfString, RangeQuantifier)

        if isinstance(expr.expr, Match):
            if isinstance(expr.expr.match_item, not_quantifiable):
                raise ValueError(f"The preceding expression {expr.expr.match_item} is not quantifiable")

        elif isinstance(expr.expr, not_quantifiable):
            raise ValueError(f"The preceding expression {expr.expr} is not quantifiable")

        expr.expr.accept(self)

    def visit_zero_or_more_quantifier(self, expr: ZeroOrMoreQuantifier):
        expr.expr.accept(self)

    def visit_one_or_more_quantifier(self, expr: OneOrMoreQuantifier):
        expr.expr.accept(self)

    def visit_zero_or_one_quantifier(self, expr: ZeroOrOneQuantifier):
        expr.expr.accept(self)

    def visit_anchor_start_of_string(self, expr):
        pass

    def visit_anchor_end_of_string(self, expr):
        pass

    def visit_anchor_word_bound(self, expr):
        pass

    def visit_anchor_non_word_bound(self, expr):
        pass

    def visit_anchor_start_of_string_only(self, expr):
        pass

    def visit_anchor_start_of_string_only_nnl(self, expr):
        pass

    def visit_anchor_end_of_string_only(self, expr):
        pass

    def visit_anchor_pre_match_end(self, expr):
        pass
