from enum import Enum
from typing import Union

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

Program = list[StatementNode]

class NumberLiteralNode(ExpressionNode):
    def __init__(self, value: float):
        super().__init__('numberLiteral')
        self.value = value

class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, operator: Operator):
        super().__init__('binaryExpression')
        self.left = left
        self.right = right
        self.operator = operator

class CodeBlockNode(ExpressionNode):
    def __init__(self, nodes: list[StatementNode]):
        super().__init__('codeBlockExpression')
        self.nodes = nodes

class IdentifierNode(ExpressionNode):
    def __init__(self, value: str):
        super().__init__('identifier')
        self.value = value

class PrintStatementNode(StatementNode):
    def __init__(self, expression):
        super().__init__('printStatement', expression)

class WhileStatementNode(StatementNode):
    def __init__(self, expression: BinaryExpressionNode, body: Union[CodeBlockNode, StatementNode]):
        super().__init__('whileStatement', expression)
        self.body = body

class VariableDeclarationNode(StatementNode):
    def __init__(self, name: str, initializer):
        super().__init__('variableDeclaration', initializer)
        self.name = name

class VariableAssignmentNode(StatementNode):
    def __init__(self, name: str, value):
        super().__init__('variableAssignment', value)
        self.name = name
