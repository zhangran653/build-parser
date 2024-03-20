from abc import ABC, abstractmethod

from PrattParse.Token import TokenType


class Expression(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def show(self):
        pass


class AssignExpression(Expression):
    """An assignment expression like "a = b"."""

    def __init__(self, name: str, right: Expression):
        self.name = name
        self.right = right

    def __str__(self):
        return f'{{"type":"assign", "name":{self.name}, "right":{self.right} }}'

    def show(self):
        return f"({self.name} = {self.right.show()})"


class CallExpression(Expression):
    """A function call like "a(b, c, d)"."""

    def __init__(self, function: Expression, args: list[Expression]):
        self.function = function
        self.args = args

    def __str__(self):
        return f'{{"type":"call", "function":{self.function}, "args":[{",".join(str(x) for x in self.args)}] }}'

    def show(self):
        return f"{self.function.show()}({', '.join(x.show() for x in self.args)})"


class ConditionalExpression(Expression):
    """A ternary conditional expression like "a ? b : c"."""

    def __init__(self, condition: Expression, then_exp: Expression, else_exp: Expression):
        self.condition = condition
        self.then_exp = then_exp
        self.else_exp = else_exp

    def __str__(self):
        return f'{{"type":"condition","condition":{self.condition}, "then_exp":{self.then_exp},"else_exp":{self.else_exp} }}'

    def show(self):
        return f"({self.condition.show() } ? {self.then_exp.show()} : {self.else_exp.show()})"


class NameExpression(Expression):
    """A simple variable name expression like "abc"."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'{{"type":"name", "name":{self.name} }}'

    def show(self):
        return self.name


class OperatorExpression(Expression):
    """A binary arithmetic expression like "a + b" or "c ^ d"."""

    def __init__(self, left: Expression, operator: TokenType, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f'{{"type":"binop", "left":{self.left},"operator":{self.operator.punctuator()}, "right":{self.right} }}'

    def show(self):
        return f"({self.left.show()} {self.operator.punctuator()} {self.right.show()})"


class PostfixExpression(Expression):
    """A postfix unary arithmetic expression like "a!"."""

    def __init__(self, left: Expression, operator: TokenType):
        self.left = left
        self.operator = operator

    def __str__(self):
        return f'{{"type":"postop", "left":{self.left},"operator":{self.operator.punctuator()} }}'

    def show(self):
        return f"({self.left.show()}{self.operator.punctuator()})"


class PrefixExpression(Expression):
    """A prefix unary arithmetic expression like "!a" or "-b"."""

    def __init__(self, operator: TokenType, right: Expression):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f'{{"type":"prefixop", "right":{self.right},"operator":{self.operator.punctuator()} }}'

    def show(self):
        return f"({self.operator.punctuator()}{self.right.show()})"
