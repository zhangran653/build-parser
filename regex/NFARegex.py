from typing import Optional

from regex.EngineNFA import CaptureGroup, EngineNFA
from regex.Interpreter import Interpreter
from regex.Parser import Parser
from regex.Scanner import Scanner


class NFARegex:
    def __init__(self, regex: str, **mode):
        self.mode = mode
        self._source = regex
        self._nfa = self._build_nfa()
        self.groups = {}

    def _build_nfa(self) -> Optional[EngineNFA]:
        self.ast = Parser(Scanner(self._source).scan_tokens()).parse()
        if not self.ast:
            return None
        self.interpreter = Interpreter(self.ast, **self.mode)
        self._nfa = self.interpreter.build_nfa()
        self.group_name_map = self.interpreter.group_name_map
        return self._nfa

    def compute(self, string: str) -> dict[int:CaptureGroup]:
        capture_groups = self._nfa.compute(string) if self._nfa else {}
        if not capture_groups:
            self.groups = {}
            return self.groups
        for k, v in capture_groups.items():
            if v[1] is not None:
                self.groups[k] = CaptureGroup(k, v[0], v[1], string[v[0]:v[1]], self.group_name_map[k])

        return self.groups
