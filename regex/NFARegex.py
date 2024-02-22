from typing import Optional

from regex.EngineNFA import CaptureGroup, EngineNFA
from regex.Interpreter import Interpreter
from regex.Parser import Parser
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
        self._nfa = self.interpreter.build_nfa()
        self.group_name_map = self.interpreter.group_name_map
        return self._nfa

    def compute(self, string: str, pos: int = 0):
        capture_groups = self._nfa.compute(string, pos) if self._nfa else None
        if not capture_groups:
            self.groups = {}
            return self.groups
        for k, v in capture_groups.items():
            if v[1] is not None:
                self.groups[k] = CaptureGroup(k, v[0], v[1], string[v[0]:v[1]], self.group_name_map[k])

        return self.groups

    def find(self, string: str):
        """
        for a single match. each time call the find method returns the next match

        :param string:
        :return:
        """
        for i in range(self._pos, len(string)):
            self.compute(string, i)
            if not self.groups:
                continue
            # update position as end position of group 0
            self._pos = self.groups[0].pos_e
            return self.groups

        # still not found
        self._pos = len(string)
        return None

    def find_all(self, string: str):
        """
        always start at position 0. finds a match and keeps looking for more

        :return:
        """
        matches = []
        p = 0
        while p < len(string):
            self.compute(string, p)
            if self.groups:
                matches.append(self.groups)
                p = p + 1 if self.groups[0].pos_e == p else self.groups[0].pos_e
            else:
                p += 1
        return matches
