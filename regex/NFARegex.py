from typing import List

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

    def _build_nfa(self) -> EngineNFA:
        self.ast = Parser(Scanner(self._source).scan_tokens()).parse()
        return None if self.ast is None else Interpreter(self.ast, **self.mode).build_nfa()

    def compute(self, string: str) -> List[CaptureGroup]:
        self.groups = self._nfa.compute(string) if self._nfa else []
        return self.groups
