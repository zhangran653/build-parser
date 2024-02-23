from __future__ import annotations


class ClassMatcher:
    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        raise NotImplementedError()


class RangeMatcher(ClassMatcher):
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if self.start <= string[pos] <= self.end:
            return True, 1
        return False, None


class IndividualCharMatcher(ClassMatcher):
    def __init__(self, chars: list[str]):
        self.chars = set(chars)

    def matches(self, string: str, pos: int, **kwargs) -> (bool, int):
        if string[pos] in self.chars:
            return True, 1
        return False, None


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
