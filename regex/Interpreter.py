from functools import reduce

from regex.EngineNFA import EngineNFA
from regex.NFAMatcher import ClassMatcher, CHARACTER_CLASSES_MATCHER, RangeMatcher, ComplexMatcher, \
    IndividualCharMatcher
from regex.NFAMatcher import Matcher, EpsilonMatcher, CharacterMatcher, CustomMatcher, StartOfStringMatcher, \
    EndOfStringMatcher, StartOfLineMatcher, EndOfLineMatcher, BackReferenceMatcher, QuantifierCounter, \
    QuantifierGateMatcher, QuantifierCountMatcher, QuantifierLoopMatcher
from regex.Facade import Visitor
from regex.Parser import RangeQuantifier, Character, Backreference, CharRange, \
    CharacterGroup, Match, Group, SubExpression, Expression, CharClassAnyWord, CharClassAnyWordInverted, \
    CharClassAnyDecimalDigit, CharClassAnyDecimalDigitInverted, CharClassAnyWhitespace, CharClassAnyWhitespaceInverted, \
    ZeroOrOneQuantifier, OneOrMoreQuantifier, ZeroOrMoreQuantifier, AnyChar, AnchorStartOfString, AnchorEndOfString, \
    AnchorWordBoundary, AnchorNonWordBoundary, AnchorStartOfStringOnly, AnchorEndOfStringOnlyNotNewline, \
    AnchorEndOfStringOnly, AnchorPreviousMatchEnd


class StateNameGenerator:
    def __init__(self):
        self.id = 0

    def next(self):
        name = f'q{self.id}'
        self.id += 1
        return name

    def reset(self):
        self.id = 0


class Symbol:
    def __init__(self, char: str = None):
        self.char = char

    def eps(self):
        return self.char is None


def c(char: str) -> Symbol:
    return Symbol(char)


def e() -> Symbol:
    return Symbol()


class Interpreter(Visitor):
    """
    Interpret AST to NFA
    """

    def __init__(self, ast: Expression, **mode):
        self.mode = mode
        self.ast = ast
        self.sg = StateNameGenerator()
        self.nfa = None
        # a [group_id:group_name] map, used for capture group name
        self.group_name_map = {}
        # for generate group id
        self.group_id_stack = []
        self.counters = []
        self.group_count = 0

    def build_nfa(self) -> EngineNFA:
        self.sg.reset()
        # by default the root of the tree is a group
        group = 0
        self.group_name_map[group] = None
        self.nfa = self.ast.accept(self)
        self.nfa.add_group(self.nfa.initial_state, self.nfa.ending_states[0], group)
        self.nfa.counters = self.counters
        return self.nfa

    def _next_id(self) -> str:
        return self.sg.next()

    def _basic_nfa(self, matcher: Matcher) -> EngineNFA:
        """
        A basic nfa with one step:

            a --(matcher)--> [b]
            ^                 ^
            |                 |
        init_state       end_state

        :param matcher:
        :return:
        """
        a = self._next_id()
        b = self._next_id()
        nfa = EngineNFA()
        nfa.add_states(a, b)
        nfa.initial_state = a
        nfa.ending_states = [b]
        nfa.add_transition(a, b, matcher)
        return nfa

    def _empty_expr(self) -> EngineNFA:
        """
        An empty expression is translated to an epsilon transition:

        q0 ---ε---> [q1]

        :return:
        """
        return self._basic_nfa(EpsilonMatcher())

    def _single_symbol_nfa(self, symbol: Symbol) -> EngineNFA:
        """
        A single symbol is translated to a single transition that consumes that character

          q0 ---c---> [q1]

        :param symbol:
        :return:
        """
        matcher = EpsilonMatcher() if symbol.eps() else CharacterMatcher(symbol.char)
        return self._basic_nfa(matcher)

    def _alternative_nfa(self, nfa1: EngineNFA, nfa2: EngineNFA) -> EngineNFA:
        """
        Get the union of two NFA

        - nfa1:  q1 ---a---> [q2]
        - nfa2:  q3 ---b---> [q4]
        - union:
                    q2
                 a/   \ε
                 /     \
              q0        [q5]
                \       /
                 b\   /ε
                   q4
        :param nfa1:
        :param nfa2:
        :return:
        """
        # 1. create a new nfa with a starting state
        nfa = EngineNFA()
        start = self._next_id()
        nfa.add_state(start)
        nfa.initial_state = start

        ending_states = nfa1.ending_states + nfa2.ending_states

        # 2. append nfa1,nfa2 to nfa
        nfa.append_nfa(nfa1, start)
        nfa.append_nfa(nfa2, start)

        # 3. point the end of 2 nfas to the new nfa
        end = self._next_id()
        nfa.add_state(end)
        for es in ending_states:
            nfa.add_transition(es, end, EpsilonMatcher())
        nfa.ending_states = [end]
        return nfa

    def _asterisk(self, nfa: EngineNFA, lazy: bool) -> EngineNFA:
        return self._asterisk_plus(nfa, lazy, True)

    def _plus(self, nfa: EngineNFA, lazy: bool) -> EngineNFA:
        return self._asterisk_plus(nfa, lazy, False)

    def _asterisk_plus(self, nfa: EngineNFA, lazy: bool, asterisk: bool) -> EngineNFA:
        """
        The kleene star (r∗) matches zero or more r. To achieve this, we'll get the NFA of r,
        add a new initial and final state (q_i and q_f) and add four epsilon transitions:

        - A transition from the end state of r to the initial state of r.
          This one allows repeating r multiple times.
        - A transition from q_i to q_f. This is the transition that doesn't match any r.
        - A transition from q_i to the initial state of r and a transition from the
          ending state of r to q_f

               ________________ε__________________
              |                                   |
              |                                   ↓
            q_i ---ε---> {r--------[r]} ---ε---> q_f
                          ^         .
                          |         |
                          |____ε____|

        This rule can be modified slightly to translate the + quantifier.
        Just need to remove the epsilon transition from q_i to q_f.

            q_i ---ε---> {r--------[r]} ---ε---> q_f
                          ^         .
                          |         |
                          |____ε____|

        :param nfa:
        :param lazy:
        :param asterisk:
        :return:
        """
        new_init = self._next_id()
        new_end = self._next_id()
        nfa.add_states(new_init, new_end)
        # lazy quantifier prioritizes the transitions of skip the loop and exit the loop
        # while eager quantifier trends to stay in the loop.
        # Both options add the same transitions but in different orders
        if lazy:
            if asterisk:
                # q_i -> q_f (Skip the loop)
                nfa.add_transition(new_init, new_end, EpsilonMatcher())
            # r_i -> r_f (Enter the loop)
            nfa.add_transition(new_init, nfa.initial_state, EpsilonMatcher())
            #  r_f -> q_f (Exit the loop)
            nfa.add_transition(nfa.ending_states[0], new_end, EpsilonMatcher())
            # r_f -> r_i (Stay in the loop)
            nfa.add_transition(nfa.ending_states[0], nfa.initial_state, EpsilonMatcher())

        else:
            # r_i -> r_f (Enter the loop)
            nfa.add_transition(new_init, nfa.initial_state, EpsilonMatcher())
            # r_f -> r_i (Stay in the loop)
            nfa.add_transition(nfa.ending_states[0], nfa.initial_state, EpsilonMatcher())
            #  r_f -> q_f (Exit the loop)
            nfa.add_transition(nfa.ending_states[0], new_end, EpsilonMatcher())
            if asterisk:
                # q_i -> q_f (Skip the loop)
                nfa.add_transition(new_init, new_end, EpsilonMatcher())

        nfa.initial_state = new_init
        nfa.ending_states = [new_end]
        return nfa

    def _optional(self, nfa: EngineNFA, lazy: bool) -> EngineNFA:
        """
        match 0 or 1 times

        :param nfa:
        :param lazy:
        :return:
        """
        if lazy:
            # adds a transition to first transition gives it the max priority
            nfa.add_transition_to_first(nfa.initial_state, nfa.ending_states[0], EpsilonMatcher())
        else:
            nfa.add_transition(nfa.initial_state, nfa.ending_states[0], EpsilonMatcher())
        return nfa

    def _range_quantifier(self, nfa: EngineNFA, low: int, up: int, fix_bound: bool, lazy: bool) -> EngineNFA:
        """
        A range quantifier {n,m} specifies that the preceding element must occur at least n times and at most m times.
        To implement a range quantifier in regular expression engine, adding a specific Matcher that can handle range
        quantification seems like a good approach.

                                    LoopMatcher *----------------------------------------
                                        ↓                                               |
                           ____________LM____________                                   |
                          |                          |                                  |
                          ↓                          |                                  |
        new_init ---ε---> {r--------[r]} ---CM---> new_gate ---GM---> new_end           |
                                            ^                  ^                        |
                                            |                  |                        |
                                        CountMatcher        GateMatcher                 |
                                              *                   *                     |
                                              |                   |                     |
                                              |______        _____|                     |
                                                    ↓       ↓                           |
                                                 [A Shared Counter] ← -------------------

        There are two special matchers designed for range quantifier.
        - CountMatcher
            A matcher with a counter starts with 0. Consume 0 input and increase the counter by 1.
        - GateMatcher
            A matcher with a counter shared with CountMatcher. Consume 0 input if the counter's value is in range of
            {n,m}
        - LoopMatcher
            A matcher with a counter shared with CountMatcher and GateMatcher. Consume 0 input if the current
            counter value is compatible with {n,m}. An early false returned by this matcher will reduce back track
            and transit to the GateMatcher sooner.

        Lazy quantifier will affect the order of transitions of GateMatcher and EpsilonMatcher from new_gate.


        :param nfa:
        :return:
        """
        counter = QuantifierCounter()
        self.counters.append(counter)
        count_matcher = QuantifierCountMatcher(counter)
        gate_matcher = QuantifierGateMatcher(counter, low, up, fix_bound)
        loop_matcher = QuantifierLoopMatcher(counter, low, up, fix_bound)

        new_init = self._next_id()
        new_gate = self._next_id()
        new_end = self._next_id()

        nfa.add_states(new_init, new_end, new_gate)

        nfa.add_transition(new_init, nfa.initial_state, EpsilonMatcher())
        nfa.add_transition(nfa.ending_states[0], new_gate, count_matcher)

        if lazy:
            nfa.add_transition(new_gate, new_end, gate_matcher)
            nfa.add_transition(new_gate, nfa.initial_state, loop_matcher)
        else:
            nfa.add_transition(new_gate, nfa.initial_state, loop_matcher)
            nfa.add_transition(new_gate, new_end, gate_matcher)

        nfa.initial_state = new_init
        nfa.ending_states = [new_end]

        nfa.states[new_end].clear_counter.append(counter)
        return nfa

    def visit_expression(self, expr: Expression) -> EngineNFA:
        if expr.alternation:
            nfa = self._alternative_nfa(expr.subexpression.accept(self), expr.alternation.accept(self))
        else:
            nfa = expr.subexpression.accept(self)
        return nfa

    def visit_subexpression(self, expr: SubExpression) -> EngineNFA:
        """
        concat NFAs in subexpression

        :param expr:
        :return:
        """
        item_nfa = []
        for exp in expr.items:
            nfa = exp.accept(self)
            item_nfa.append(nfa)
        if len(item_nfa) == 1:
            return item_nfa[0]
        return reduce(lambda nfa1, nfa2: nfa1.append_nfa(nfa2, nfa1.ending_states[0]), item_nfa)

    def visit_group(self, expr: Group) -> EngineNFA:
        nfa = expr.expression.accept(self)
        if expr.atomic:
            nfa.set_atomic_state(nfa.ending_states[0])
        if expr.non_capturing:
            return nfa

        group_id = self.group_id_stack.pop()
        self.group_name_map[group_id] = expr.group_name
        nfa.add_group(nfa.initial_state, nfa.ending_states[0], group_id)
        return nfa

    def visit_match(self, expr: Match) -> EngineNFA:
        return expr.match_item.accept(self)

    def visit_character_group(self, expr: CharacterGroup) -> EngineNFA:
        """
        CharacterGroup ::= "[" "^"? (CharacterClass | CharacterRange | Char - "]")+ "]"
        :param expr:
        :return:
        """
        # get matchers in transitions and compose them into one matcher
        matchers = []
        chars = []
        for item in expr.items:
            if isinstance(item, CharRange):
                matchers.append(item.accept(self))
            elif isinstance(item, Character):
                chars.append(item.token.value)
            else:
                # will generate a nfa. but in character class, the matcher is needed instead of nfa
                # so extract the matcher in it and leave the nfa
                nfa = item.accept(self)
                matchers.append(nfa.states[nfa.initial_state].transitions[0][0].matcher)
        if len(chars) > 0:
            matchers.append(IndividualCharMatcher(chars))
        mather = ComplexMatcher(matchers, expr.negative)
        return self._basic_nfa(CustomMatcher(mather))

    def visit_char_class_any_word(self, expr: CharClassAnyWord) -> EngineNFA:
        # \w
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\w'])
        return self._basic_nfa(mather)

    def visit_char_class_any_word_inv(self, expr: CharClassAnyWordInverted) -> EngineNFA:
        # \W
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\W'])
        return self._basic_nfa(mather)

    def visit_char_class_any_digit(self, expr: CharClassAnyDecimalDigit) -> EngineNFA:
        # \d
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\d'])
        return self._basic_nfa(mather)

    def visit_char_class_any_digit_inv(self, expr: CharClassAnyDecimalDigitInverted) -> EngineNFA:
        # \D
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\D'])
        return self._basic_nfa(mather)

    def visit_char_class_any_white_space(self, expr: CharClassAnyWhitespace) -> EngineNFA:
        # \s
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\s'])
        return self._basic_nfa(mather)

    def visit_char_class_any_white_space_inv(self, expr: CharClassAnyWhitespaceInverted) -> EngineNFA:
        # \S
        mather = CustomMatcher(CHARACTER_CLASSES_MATCHER[r'\S'])
        return self._basic_nfa(mather)

    def visit_character_range(self, expr: CharRange) -> ClassMatcher:
        return RangeMatcher(expr.start.value, expr.to.value)

    def visit_any_char(self, expr: AnyChar) -> EngineNFA:
        """
        Dot(.) matches any character except line breaks.
        The definition of what a line break is varies with the languages.
        As regular-expressions.info states: \n is always a line break,
        Javascript also considers \r, \u2028 and \u2029 and Java even adds \u0085.
        For simplicity only add \n and \r.
        :param expr:
        :return:
        """
        mather = CustomMatcher(ComplexMatcher([IndividualCharMatcher(["\n", "\r"])], True))
        return self._basic_nfa(mather)

    def visit_backreference(self, expr: Backreference) -> EngineNFA:
        """
        Backreferences are used to match the same text that has already matched in a previous capturing group.
        For example: (['"])[a-zA-Z]+(['"]) matches "foo" and 'foo' but not "foo' or 'foo".

        Corner cases that need to take into account:
            1. Empty groups
            For example: regex ()\1a with input "a".
            The 1st group technically matches an empty string (ε/""), so \1 also matches an empty string and it
            succeeds.

            * This implementation will follow as PCRE. Mainly because empty group is not syntax valid.

            2. Unmatched groups
            For example: regex (b)?\1a with input "a".
            The 1st group fails to match, but since it's optional, it continues trying the rest and arrives \1.
            In PCRE: unmatched backreferences always fails.
            In JS: unmatched group is the same as an empty group, so \1 matches an empty string and succeeds.

            * This implementation will follow as JS, that is to match an empty string and success

            3. Backreference before or even inside the group
            For example: regex \1(a) and (a\1).
            In PCRE: it always fails.
            In JS: equivalent to regex (a).

            * This implementation will follow as PCRE.

            4. Backreference in an alternative
            For example: regex (\1b|a)+. It looks like a recursion.
            In PCRE: Every time the capture group matches the value of group 1 is overwritten, which changes
            the definition of \1 for the next match.
            In JS: \1 matches an empty string, so it's equivalent to (b|a).

            * This implementation will follow as PCRE.

        :param expr:
        :return:
        """
        if expr.number > self.group_count:
            raise ValueError(f'back reference group id out of range. should be in [0,{self.group_count}]')
        return self._basic_nfa(BackReferenceMatcher(expr.number))

    def visit_character(self, expr: Character) -> EngineNFA:
        return self._single_symbol_nfa(c(expr.token.value))

    def visit_range_quantifier(self, expr: RangeQuantifier) -> EngineNFA:
        nfa = expr.expr.accept(self)
        return self._range_quantifier(nfa, expr.low_bound, expr.up_bound, expr.fixed_bound, expr.lazy)

    def visit_zero_or_more_quantifier(self, expr: ZeroOrMoreQuantifier) -> EngineNFA:
        return self._asterisk(expr.expr.accept(self), expr.lazy)

    def visit_one_or_more_quantifier(self, expr: OneOrMoreQuantifier) -> EngineNFA:
        return self._plus(expr.expr.accept(self), expr.lazy)

    def visit_zero_or_one_quantifier(self, expr: ZeroOrOneQuantifier) -> EngineNFA:
        return self._optional(expr.expr.accept(self), expr.lazy)

    def visit_anchor_start_of_string(self, expr: AnchorStartOfString) -> EngineNFA:
        return self._basic_nfa(StartOfLineMatcher() if self.mode.get('m', None) else StartOfStringMatcher())

    def visit_anchor_end_of_string(self, expr: AnchorEndOfString) -> EngineNFA:
        return self._basic_nfa(EndOfLineMatcher() if self.mode.get('m', None) else EndOfStringMatcher())

    def visit_anchor_word_bound(self, expr: AnchorWordBoundary) -> EngineNFA:
        raise NotImplementedError()

    def visit_anchor_non_word_bound(self, expr: AnchorNonWordBoundary) -> EngineNFA:
        raise NotImplementedError()

    def visit_anchor_start_of_string_only(self, expr: AnchorStartOfStringOnly) -> EngineNFA:
        raise NotImplementedError()

    def visit_anchor_start_of_string_only_nnl(self, expr: AnchorEndOfStringOnlyNotNewline) -> EngineNFA:
        raise NotImplementedError()

    def visit_anchor_end_of_string_only(self, expr: AnchorEndOfStringOnly) -> EngineNFA:
        raise NotImplementedError()

    def visit_anchor_pre_match_end(self, expr: AnchorPreviousMatchEnd) -> EngineNFA:
        raise NotImplementedError()
