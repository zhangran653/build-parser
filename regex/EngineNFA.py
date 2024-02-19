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
        stack = [(0, self.states[self.initial_state])]
        # push initial state. the i is current position of string
        while len(stack) > 0:
            i, current_state = stack.pop()
            if current_state.name in self.ending_states:
                return True
            if i > len(string) - 1:
                return False
            char = string[i]

            """
            if (matcher.matches(input, i)) { 
                            // The memory has to be immutable. This is the simplest way to make a deep copy of 
                            // an object with only primitive values
                const copyMemory = JSON.parse(JSON.stringify(memory));
                if (matcher.isEpsilon()) {
                    // Don't follow the transition. We already have been in that state
                    if (memory.EPSILON_VISITED.includes(toState.name))
                        continue;
                    // Remember that you made this transition
                    copyMemory.EPSILON_VISITED.push(currentState.name);
                } else {
                    // We are transversing a non-epsilon transition, so reset the visited counter
                    copyMemory.EPSILON_VISITED = [];
                }
                // Reminder: Epsilon transitions don't consume input
                const nextI = matcher.isEpsilon() ? i : i+1;
                stack.push({i: nextI, currentState: toState, memory: copyMemory});
            }
            """
            for c in range(len(current_state.transitions) - 1, -1, -1):
                matcher, to_state = current_state.transitions[c]
                if matcher.matches(char):
                    next_i = i if matcher.is_epsilon() else i + 1
                    stack.append((next_i, to_state))

        return False
