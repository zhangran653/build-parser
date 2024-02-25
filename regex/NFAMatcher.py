from __future__ import annotations

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


class ClassMatcher:
    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        raise NotImplementedError()

    def get_label(self):
        raise NotImplementedError()


class RangeMatcher(ClassMatcher):
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if self.start <= string[pos] <= self.end:
            return True, 1
        return False, None

    def get_label(self):
        return f'{self.start}-{self.end}'


class IndividualCharMatcher(ClassMatcher):
    def __init__(self, chars: list[str]):
        self.chars = set(chars)

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if string[pos] in self.chars:
            return True, 1
        return False, None

    def get_label(self):
        label = f''
        for c in self.chars:
            if c.isalpha():
                label = f'{label}{c}'
        return label


class ComplexMatcher(ClassMatcher):
    def __init__(self, matchers: list[ClassMatcher], negative=False):
        self.matchers = matchers
        self.negative = negative

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        for matcher in self.matchers:
            matched, consumed = matcher.matches(string, pos, **kwargs)
            if matched:
                return (True, consumed) if not self.negative else (False, None)
        return (False, None) if not self.negative else (True, 1)

    def get_label(self):
        label = f'{"^" if self.negative else ""}'
        for m in self.matchers:
            label = f"{label}{m.get_label()}"
        return f"{label}"


WHITE_SPACE = [" ", "\f", "\n", "\r", "\t", "\v", "\u00a0", "\u1680", "\u2028", "\u2029", "\u202f", "\u205f", "\u3000"]

CHARACTER_CLASSES_MATCHER = {
    r"\d": ComplexMatcher([RangeMatcher('0', '9')]),
    r"\D": ComplexMatcher([RangeMatcher('0', '9')], True),
    r"\s": ComplexMatcher([IndividualCharMatcher(WHITE_SPACE), RangeMatcher("\u2000", "\u200a")]),
    r"\S": ComplexMatcher([IndividualCharMatcher(WHITE_SPACE), RangeMatcher("\u2000", "\u200a")], True),
    r"\w": ComplexMatcher(
        [IndividualCharMatcher(["_"]), RangeMatcher("a", "z"), RangeMatcher("A", "Z"), RangeMatcher("0", "9")]),
    r"\W": ComplexMatcher(
        [IndividualCharMatcher(["_"]), RangeMatcher("a", "z"), RangeMatcher("A", "Z"), RangeMatcher("0", "9")], True),
}
