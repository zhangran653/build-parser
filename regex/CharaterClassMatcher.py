from __future__ import annotations


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
