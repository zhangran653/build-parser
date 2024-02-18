import unittest

from regex.Parser import Parser
from regex.Scanner import Scanner


class RegexTest(unittest.TestCase):
    def test1(self):
        scanner = Scanner('')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test2(self):
        scanner = Scanner('a')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test3(self):
        scanner = Scanner('ab+')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test4(self):
        scanner = Scanner('[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test5(self):
        scanner = Scanner('[a-zA-Z]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test6(self):
        scanner = Scanner('[a-zA-Z\[]')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test7(self):
        scanner = Scanner('a{3,4}')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test8(self):
        scanner = Scanner('ad阿松大')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test9(self):
        scanner = Scanner('\s\\b\w\S\A\Z\G.|')
        tokens = scanner.scan_tokens()
        print(tokens)

    def test10(self):
        scanner = Scanner("")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expressions = parser.parse()
        print(expressions)

    def test11(self):
        scanner = Scanner("a")
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expressions = parser.parse()
        print(expressions)
