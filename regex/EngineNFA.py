from __future__ import annotations

from regex.CharaterClassMatcher import ClassMatcher
from graphviz import Digraph


class Matcher:
    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        """
        Take input string, current position and a previous group map.
        Return a tuple in which:
         - first element for matches or not.
         - second element for the number of characters that this matcher consumes if
           successfully matched.

        :param string:
        :param pos:
        :param previous_group:
        :return:
        """
        raise NotImplementedError()

    def get_label(self) -> str:
        raise NotImplementedError()


class CharacterMatcher(Matcher):

    def __init__(self, c):
        self.c = c

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos > len(string) - 1:
            return False, None
        if self.c == string[pos]:
            return True, 1
        else:
            return False, None

    def get_label(self) -> str:
        return self.c

    def __repr__(self):
        return f'{{ "CharacterMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class EpsilonMatcher(Matcher):

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        return True, 0

    def get_label(self):
        return 'ε'

    def __repr__(self):
        return f'{{ "EpsilonMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class StartOfStringMatcher(Matcher):

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos == 0:
            return True, 0
        else:
            return False, None

    def get_label(self) -> str:
        return "^"

    def __repr__(self):
        return f'{{ "StartOfStringMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class StartOfLineMatcher(Matcher):

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos == 0 or string[pos - 1] == '\n':
            return True, 0
        else:
            return False, None

    def get_label(self) -> str:
        return "^"

    def __repr__(self):
        return f'{{ "StartOfLineMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class EndOfStringMatcher(Matcher):

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos == len(string):
            return True, 0
        return False, None

    def get_label(self) -> str:
        return "$"

    def __repr__(self):
        return f'{{ "EndOfStringMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class EndOfLineMatcher(Matcher):

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos == len(string) or string[pos] == '\n':
            return True, 0
        return False, None

    def get_label(self) -> str:
        return "$"

    def __repr__(self):
        return f'{{ "EndOfSLineMatcher":"{self.get_label()}" }}'

    def __str__(self):
        return self.__repr__()


class BackReferenceMatcher(Matcher):
    def __init__(self, group_id: int):
        self.group_id = group_id

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        group_pos = kwargs['group_map'].get(self.group_id, None)
        if not group_pos:
            return False, None
        start, end = group_pos[0], group_pos[1]
        if pos + (end - start) > len(string):
            return False, None
        if string[start:end] == string[pos:pos + end - start]:
            return True, end - start
        return False, None

    def get_label(self) -> str:
        return f"\\{self.group_id}"


class CustomMatcher(Matcher):
    def __init__(self, class_matcher: ClassMatcher):
        self.matcher = class_matcher

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if pos > len(string) - 1:
            return False, None
        return self.matcher.matches(string, pos, **kwargs)

    def get_label(self):
        return self.matcher.get_label()


class QuantifierCounter:
    def __init__(self):
        self._count = 0

    def count(self):
        self._count += 1

    def reset(self):
        self._count = 0

    def get_count(self) -> int:
        return self._count

    def __repr__(self):
        return f'{{ "QuantifierCounter":{self.get_count()} }}'

    def __str__(self):
        return self.__repr__()


class QuantifierCountMatcher(Matcher):
    def __init__(self, counter: QuantifierCounter):
        self.counter = counter

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        self.counter.count()
        return True, 0

    def get_label(self):
        return 'CM'

    def __repr__(self):
        return f'{{ "QuantifierCountMatcher":{self.counter.get_count()} }}'

    def __str__(self):
        return self.__repr__()


class QuantifierLoopMatcher(Matcher):
    def __init__(self, counter: QuantifierCounter, low: int, up: int, fix_bound: bool):
        self.counter = counter
        self.low = low
        self.up = up
        self.fix_bound = fix_bound

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if self.fix_bound:
            match = (True, 0) if self.counter.get_count() < self.low else (False, None)
        elif self.up is not None:
            match = (True, 0)
        else:
            match = (True, 0) if self.counter.get_count() < self.up else (False, None)

        return match

    def __repr__(self):
        return f'{{ "QuantifierLoopMatcher":{{  }} }}'

    def __str__(self):
        return self.__repr__()

    def get_label(self):
        return f'LM'


class QuantifierGateMatcher(Matcher):
    def __init__(self, counter: QuantifierCounter, low: int, up: int, fix_bound: bool):
        self.counter = counter
        self.low = low
        self.up = up
        self.fix_bound = fix_bound

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if self.fix_bound:
            match = (True, 0) if self.counter.get_count() == self.low else (False, None)
        elif self.up is not None:
            match = (True, 0) if self.low <= self.counter.get_count() <= self.up else (False, None)
        else:
            match = (True, 0) if self.low <= self.counter.get_count() else (False, None)

        return match

    def __repr__(self):
        return f'{{ "QuantifierGateMatcher":{{ "low":{self.low},"up":{self.up},"fixed":{1 if self.fix_bound else 0} }} }}'

    def __str__(self):
        return self.__repr__()

    def get_label(self):
        return f'GM{{{self.low}{"," if not self.fix_bound else ""}{self.up}}}'


class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.start_groups = []
        self.end_groups = []
        self.atomic_group_end = False
        self.clear_counter = []

    def add_transition(self, toState: State, matcher: Matcher):
        self.transitions.append([matcher, toState])

    def add_first_transition(self, toState: State, matcher: Matcher):
        self.transitions.insert(0, [matcher, toState])

    def __repr__(self):
        ts = [f'{{ "matcher": {m},"toState":"{t.name}" }}' for m, t in self.transitions]
        return f'{{ "name": "{self.name}","transitions":[{",".join(ts)}] }}'

    def __str__(self):
        return self.__repr__()


class CaptureGroup:
    def __init__(self, gid: int, pos_s: int, pos_e: int, substring: str, name: str = None):
        self.gid = gid
        self.pos_s = pos_s
        self.pos_e = pos_e
        self.substring = substring
        self.name = name

    def __repr__(self):
        return f'Group {self.gid if not self.name else self.name}: {self.substring}. Pos: [{self.pos_s}-{self.pos_e}] '

    def __str__(self):
        return self.__repr__()


class EngineNFA:
    def __init__(self):
        self.states = {}
        self.initial_state = None
        self.ending_states = []
        self.group_name_map = {}
        self.group_matches = {}
        self.counters = []

    def draw_nfa(self, path: str, label: str = None):
        dot = Digraph(comment='NFA')
        dot.graph_attr['rankdir'] = 'LR'
        dot.attr(label=label)
        dot.attr(fontsize='16')

        for s in self.states.keys():
            # add node
            if s == self.ending_states[0]:
                dot.node(s, shape='doublecircle')
            elif s == self.initial_state:
                dot.node(s, shape='diamond')
            else:
                dot.node(s)

        for s in self.states.values():
            # add edges
            for index, [matcher, to] in enumerate(s.transitions):
                dot.edge(s.name, to.name, f"{index}.{matcher.get_label()}")
        dot.render(path, format='png')

    def __repr__(self):
        formatted_map = "{" + ", ".join(f'"{key}": {value}' for key, value in self.states.items()) + "}"
        return f'{{ "state":{formatted_map},"initial_state":"{self.initial_state}","ending_states":["{",".join(self.ending_states)}"] }}'

    def __str__(self):
        return self.__repr__()

    def add_state(self, name: str):
        self.states[name] = State(name)

    def add_states(self, *names: str):
        [self.add_state(n) for n in names]

    def add_transition(self, fromStateName: str, toStateName: str, matcher: Matcher):
        self.states[fromStateName].add_transition(self.states[toStateName], matcher)

    def add_transition_to_first(self, fromStateName: str, toStateName: str, matcher: Matcher):
        self.states[fromStateName].add_first_transition(self.states[toStateName], matcher)

    def add_group(self, start_state: str, end_state: str, group: int):
        self.states[start_state].start_groups.append(group)
        self.states[end_state].end_groups.append(group)

    def set_atomic_state(self, state: str):
        self.states[state].atomic_group_end = True

    def append_nfa(self, other: EngineNFA, joint_state: str) -> EngineNFA:
        """
        Concatenate 2 nfa. concat this nfa's joint_state ot other naf's initial state.This will destruct the
        other nfa's initial state and may change this nfa's ending states.

        :param other:
        :param joint_state:
        :return:
        """
        # 1. copy the states of other nfa to this nfa
        for n, s in other.states.items():
            self.states[n] = s

        # 2. remove init states of other nfa
        del self.states[other.initial_state]

        # 3. all the outward transitions of 'other.initialState' now belong to 'joint_state'
        for matcher, to_state in other.states[other.initial_state].transitions:
            self.add_transition(joint_state, to_state.name, matcher)

        # move groups
        for g in other.states[other.initial_state].start_groups:
            self.states[joint_state].start_groups.append(g)
        for g in other.states[other.initial_state].end_groups:
            self.states[joint_state].end_groups.append(g)

        # 4. if the joint_state is an end state,
        #  then the end states of the appended nfa are also end states of the fusion.
        if joint_state in self.ending_states:
            self.ending_states.remove(joint_state)
            self.ending_states.append(*other.ending_states)

        return self

    def compute_groups(self, state: State, groups: dict[int:list[int, int]], pos: int):
        for g in state.start_groups:
            groups[g] = [pos, None]
        for g in state.end_groups:
            groups[g][1] = pos
            self.group_matches[g] = [groups[g][0], groups[g][1]]

    def reset_state_counter(self, state: State):
        for c in state.clear_counter:
            c.reset()

    def reset_counter(self):
        for c in self.counters:
            c.reset()

    def compute(self, string: str, pos: int = 0) -> dict[int:list[int, int]]:
        self.reset_counter()
        # (current position of string, current state, visited states through epsilon,group map)
        stack = [(pos, self.states[self.initial_state], set(), {})]
        # push initial state. the i is current position of string
        while len(stack) > 0:
            i, current_state, visited, groups = stack.pop()
            # group is a right-open interval [l, r)
            self.compute_groups(current_state, groups, i)
            self.reset_state_counter(current_state)
            if current_state.name in self.ending_states:
                # compute_groups function may set groups that will be backtracked
                for k, v in self.group_matches.items():
                    if groups[k][0] != self.group_matches[k][0]:
                        groups[k] = [self.group_matches[k][0], self.group_matches[k][1]]
                return groups
            if current_state.atomic_group_end:
                stack = []
            for c in range(len(current_state.transitions) - 1, -1, -1):
                matcher, to_state = current_state.transitions[c]
                matched, consumed = matcher.matches(string, i, group_map=self.group_matches)
                if matched:
                    if consumed == 0:
                        # Don't follow the transition. Already have been in that state
                        if to_state.name in visited:
                            continue
                        # copy visited
                        cp = set(visited)
                        # Remember that made this transition
                        cp.add(current_state.name)
                    else:
                        # transversing a non-epsilon transition, reset the visited counter
                        cp = set()
                    next_i = i + consumed
                    stack.append((next_i, to_state, cp, groups))
        return None
