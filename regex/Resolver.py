from regex.CharaterClassMatcher import ClassMatcher, CHARACTER_CLASSES_MATCHER, RangeMatcher, ComplexMatcher, \
    IndividualCharMatcher
from regex.EngineNFA import Matcher, EngineNFA, EpsilonMatcher, CharacterMatcher, CustomMatcher, StartOfStringMatcher, \
    EndOfStringMatcher, StartOfLineMatcher, EndOfLineMatcher, BackReferenceMatcher, QuantifierCounter, \
    QuantifierGateMatcher, QuantifierCountMatcher, QuantifierLoopMatcher
from regex.Interpreter import Interpreter
from regex.Parser import Visitor, RangeQuantifier, Character, Backreference, CharRange, \
    CharacterGroup, Match, Group, SubExpression, Expression, CharClassAnyWord, CharClassAnyWordInverted, \
    CharClassAnyDecimalDigit, CharClassAnyDecimalDigitInverted, CharClassAnyWhitespace, CharClassAnyWhitespaceInverted, \
    ZeroOrOneQuantifier, OneOrMoreQuantifier, ZeroOrMoreQuantifier, AnyChar, AnchorStartOfString, AnchorEndOfString, \
    AnchorWordBoundary, AnchorNonWordBoundary, AnchorStartOfStringOnly, AnchorEndOfStringOnlyNotNewline, \
    AnchorEndOfStringOnly, AnchorPreviousMatchEnd


class Resolver(Visitor):
    """
    # TODO back reference number resolve. Make it in range of group ids
    # TODO  Range Quantifiers can only be applied to:
    #         - Individual characters: For example, a{2,4} matches "aa", "aaa", or "aaaa".
    #         - Character classes: For example, [a-z]{2,4} matches any lowercase letter sequence of length 2 to 4.
    #         - Grouped expressions: For example, (abc){2,4} matches "abcabc", "abcabcabc", or "abcabcabcabc".
    #         - Character sets with special meaning: . \d \w \s
    #         - Negated character classes:\D \W \S
    #         - Backreferences

    """

    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter

    def visit_expression(self, expr):
        if expr.alternation:
            expr.alternation.accept(self)
        expr.subexpression.accept(self)

    def visit_subexpression(self, expr):
        raise NotImplementedError()

    def visit_group(self, expr):
        raise NotImplementedError()

    def visit_match(self, expr):
        raise NotImplementedError()

    def visit_character_group(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_word(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_word_inv(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_digit(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_digit_inv(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_white_space(self, expr):
        raise NotImplementedError()

    def visit_char_class_any_white_space_inv(self, expr):
        raise NotImplementedError()

    def visit_character_range(self, expr):
        raise NotImplementedError()

    def visit_backreference(self, expr):
        raise NotImplementedError()

    def visit_any_char(self, expr):
        raise NotImplementedError()

    def visit_character(self, expr):
        raise NotImplementedError()

    def visit_range_quantifier(self, expr):
        raise NotImplementedError()

    def visit_zero_or_more_quantifier(self, expr):
        raise NotImplementedError()

    def visit_one_or_more_quantifier(self, expr):
        raise NotImplementedError()

    def visit_zero_or_one_quantifier(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string(self, expr):
        raise NotImplementedError()

    def visit_anchor_end_of_string(self, expr):
        raise NotImplementedError()

    def visit_anchor_word_bound(self, expr):
        raise NotImplementedError()

    def visit_anchor_non_word_bound(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string_only(self, expr):
        raise NotImplementedError()

    def visit_anchor_start_of_string_only_nnl(self, expr):
        raise NotImplementedError()

    def visit_anchor_end_of_string_only(self, expr):
        raise NotImplementedError()

    def visit_anchor_pre_match_end(self, expr):
        raise NotImplementedError()
