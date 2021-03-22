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

class StatementNode(Node):
    def __init__(self, type, expression):
        super().__init__(type)
        self.expression = expression

class ExpressionNode(Node):
    def __init__(self, type):
        super().__init__(type)

Program = list[StatementNode]
