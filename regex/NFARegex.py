from typing import Optional

from regex.EngineNFA import CaptureGroup, EngineNFA
from regex.Interpreter import Interpreter
from regex.Parser import Parser
from regex.Resolver import Resolver
from regex.Scanner import Scanner


class NFARegex:
    def __init__(self, regex: str, **mode):
        self.mode = mode
        self._source = regex
        self._pos = 0
        self._nfa = self._build_nfa()
        self.groups = {}

    def reset(self):
        self._pos = 0
        self.groups = {}

    def _build_nfa(self) -> Optional[EngineNFA]:
        self.ast = Parser(Scanner(self._source).scan_tokens()).parse()
        if not self.ast:
            return None
        self.interpreter = Interpreter(self.ast, **self.mode)
        Resolver(self.interpreter)
        self._nfa = self.interpreter.build_nfa()
        self.group_name_map = self.interpreter.group_name_map
        return self._nfa

    def compute(self, string: str, pos: int = 0):
        capture_groups = self._nfa.compute(string, pos) if self._nfa else None
        if not capture_groups:
            self.groups = {}
            return self.groups

        groups = {}
        for k, v in capture_groups.items():
            if v[1] is not None:
                groups[k] = CaptureGroup(k, v[0], v[1], string[v[0]:v[1]], self.group_name_map[k])
        self.groups = groups
        return groups

    def find(self, string: str):
        """
        for a single match. each time call the find method returns the next match

        :param string:
        :return:
        """
        if self._pos > len(string):
            return None

        i = self._pos
        while True:
            groups = self.compute(string, i)
            if not groups:
                i += 1
                if i > len(string) - 1:
                    self._pos = len(string) + 1
                    return None
            else:
                self._pos = i + 1 if groups[0].pos_e == i else groups[0].pos_e
                return groups

    def find_all(self, string: str):
        """
        always start at position 0. finds a match and keeps looking for more

        :return:
        """
        matches = []
        self._pos = 0
        while self.find(string):
            matches.append(self.groups)
        return matches

    def draw_nfa(self, path):
        self._nfa.draw_nfa(path, self._source)
