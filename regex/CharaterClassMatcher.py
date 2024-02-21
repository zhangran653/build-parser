from __future__ import annotations


class ClassMatcher:
    def matches(self, c: str):
        raise NotImplementedError()


class RangeMatcher(ClassMatcher):
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end

    def matches(self, c: str):
        return self.start <= c <= self.end


class IndividualCharMatcher(ClassMatcher):
    def __init__(self, chars: list[str]):
        self.chars = set(chars)

    def matches(self, c: str):
        return c in self.chars


class ComplexMatcher(ClassMatcher):
    def __init__(self, matchers: list[ClassMatcher], negative=False):
        self.matchers = matchers
        self.negative = negative

    def matches(self, c: str):
        for matcher in self.matchers:
            if matcher.matches(c):
                return True if not self.negative else False
        return False if not self.negative else True


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
