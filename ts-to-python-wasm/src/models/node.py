from enum import Enum

Operator = Enum(
    value = 'Operator',
    names = [
        ('+', 1),
        ('-', 2),
        ('/', 3),
        ('*', 4),
        ('==', 5),
        ('>', 6),
        ('<', 7),
        ('&&', 8),
        ('||', 9)
    ]
)

class Node(object):
    def __init__(self, type):
        self.type = type

class ExpressionNode(Node):
    def __init__(self, type):
        super().__init__(type)

class StatementNode(Node):
    def __init__(self, type, expression):
        super().__init__(type)
        self.expression = expression

class Program(list[StatementNode]):
    def __init__(self):
        super().__init__()

class NumberLiteralNode(ExpressionNode):
    def __init__(self, value: str):
        super().__init__('numberLiteral')
        self.value = float(value)

class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, operator: Operator):
        super().__init__('binaryExpression')
        self.left = left
        self.right = right
        self.operator = operator

class PrintStatementNode(StatementNode):
    def __init__(self, expression):
        super().__init__('printStatement', expression)
