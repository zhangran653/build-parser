from __future__ import annotations


class Matcher:
    def matches(self, char):
        raise NotImplementedError()

    def is_epsilon(self):
        raise NotImplementedError()

    def get_label(self):
        raise NotImplementedError()


class CharacterMatcher(Matcher):

    def __init__(self, c):
        self.c = c

    def matches(self, char: str) -> bool:
        return self.c == char

    def is_epsilon(self) -> bool:
        return False

    def get_label(self) -> str:
        return self.c

    def __repr__(self):
        return f'{{ "CharacterMatcher":"{self.get_label()}" }}'


class EpsilonMatcher(Matcher):

    def matches(self, char) -> bool:
        return True

    def is_epsilon(self):
        return True

    def get_label(self):
        return 'epsilon'

    def __repr__(self):
        return f'{{ "EpsilonMatcher":"{self.get_label()}" }}'


class State:
    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.startGroups = []
        self.endGroups = []

    def add_transition(self, toState: State, matcher: Matcher):
        self.transitions.append([matcher, toState])

    def add_first_transition(self, toState: State, matcher: Matcher):
        self.transitions.insert(0, [matcher, toState])

    def __repr__(self):
        ts = [f'{{ "matcher": {m},"toState":"{t.name}" }}' for m, t in self.transitions]
        return f'{{ "name": "{self.name}","transitions":[{",".join(ts)}] }}'


class EngineNFA:
    def __init__(self):
        self.states = {}
        self.initial_state = None
        self.ending_states = None

    def add_state(self, name: str):
        self.states[name] = State(name)

    def add_states(self, *names: str):
        [self.add_state(n) for n in names]

    def add_transition(self, fromStateName: str, toStateName: str, matcher: Matcher):
        self.states[fromStateName].add_transition(self.states[toStateName], matcher)

    def add_transition_to_first(self, fromStateName: str, toStateName: str, matcher: Matcher):
        self.states[fromStateName].add_first_transition(self.states[toStateName], matcher)

    def compute(self, string: str):
        # (current position of string, current state, visited states through epsilon)
        stack = [(0, self.states[self.initial_state], set())]
        # push initial state. the i is current position of string
        while len(stack) > 0:
            i, current_state, visited = stack.pop()
            if current_state.name in self.ending_states:
                return True
            # TODO
            if i > len(string) - 1:
                return False
            char = string[i]

            for c in range(len(current_state.transitions) - 1, -1, -1):
                matcher, to_state = current_state.transitions[c]
                if matcher.matches(char):
                    # copy visited
                    cp = set(visited)
                    if matcher.is_epsilon:
                        # Don't follow the transition. Already have been in that state
                        if to_state.name in visited:
                            continue
                        # Remember that made this transition
                        cp.add(current_state.name)
                    else:
                        # transversing a non-epsilon transition, reset the visited counter
                        cp = set()
                    next_i = i if matcher.is_epsilon() else i + 1
                    stack.append((next_i, to_state, cp))

        return False
