from regex.Interpreter import Interpreter
from regex.Parser import Parser
from regex.Scanner import Scanner


class NFARegex:
    def __init__(self, regex: str):
        self.source = regex
        self.scanner = Scanner(regex)
        self.ast = Parser(Scanner(regex).scan_tokens()).parse()
        self.nfa = None if self.ast is None else Interpreter(self.ast).build_nfa()

    def compute(self, string: str) -> bool:
        return self.nfa.compute(string) if self.nfa else False
