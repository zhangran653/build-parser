import unittest

from PrattParse.Lexer import Lexer
from PrattParse.Tests import TestParser

passed = 0
failed = 0
def test(source: str, expected: str):
    """Parses the given chunk of code and verifies that it matches the expected pretty-printed
    result."""
    global failed, passed
    lexer = Lexer(source)
    parser = TestParser(lexer)
    try:
        result = parser.parse_expression()
    except RuntimeError as ex:
        failed += 1
        print(f"[FAIL] Expected: {expected}")
        print(f"          Error: {ex.args}")
    else:
        actual = result.show()
        if expected == actual:
            passed += 1
        else:
            failed += 1
            print(f"[FAIL] Expected: {expected}")
            print(f"         Actual: {actual}")
class LL1Test(unittest.TestCase):
    def test1(self):
        test("b ? c : d", "(b ? c : d)")
        test("a()", "a()")
        test("a(b)", "a(b)")
        test("a(b, c)", "a(b, c)")
        test("a(b)(c)", "a(b)(c)")
        test("a(b) + c(d)", "(a(b) + c(d))")
        test("a(b?c:d,e+f)", "a((b ? c : d), (e + f))")
        # Unary precedence.
        test("~!-+a", "(~(!(-(+a))))")
        test("a!!!", "(((a!)!)!)")
        # Unary and binary predecence.
        test("-a * b", "((-a) * b)")
        test("!a + b", "((!a) + b)")
        test("~a ^ b", "((~a) ^ b)")
        test("-a!", "(-(a!))")
        test("!a!", "(!(a!))")
        # Binary precedence.
        test("a = b + c * d ^ e - f / g",
             "(a = ((b + (c * (d ^ e))) - (f / g)))")
        # Binary associativity.
        test("a = b = c", "(a = (b = c))")
        test("a + b - c", "((a + b) - c)")
        test("a * b / c", "((a * b) / c)")
        test("a ^ b ^ c", "(a ^ (b ^ c))")
        # Conditional operator.
        test("a ? b : c ? d : e", "(a ? b : (c ? d : e))")
        test("a ? b ? c : d : e", "(a ? (b ? c : d) : e)")
        test("a + b ? c * d : e / f", "((a + b) ? (c * d) : (e / f))")
        # Grouping.
        test("a + (b + c) + d", "((a + (b + c)) + d)")
        test("a ^ (b + c)", "(a ^ (b + c))")
        test("(!a)!", "((!a)!)")
        # Show the results.
        if failed == 0:
            print(f"Passed all {passed} tests.")
        else:
            total = failed + passed
            print("----")
            print(f"Failed {failed} out of {total} tests.")
