from enum import Enum
from typing import Union


class ProgramNode:
    def __init__(self, type: str):
        self.type = type


Operator = Enum(
    value='Operator',
    names=[
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


class ExpressionNode(ProgramNode):
    def __init__(self, type: str):
        super().__init__(type)


class StatementNode(ProgramNode):
    def __init__(self, type: str):
        super().__init__(type)


Program = list[StatementNode]


class VariableDeclarationNode(StatementNode):
    def __init__(self, name: str, initializer: ExpressionNode):
        super().__init__('variableDeclaration')
        self.name = name
        self.initializer = initializer


class VariableAssignmentNode(StatementNode):
    def __init__(self, name: str, value: ExpressionNode):
        super().__init__('variableAssignment')
        self.name = name
        self.value = value


class NumberLiteralNode(ExpressionNode):
    def __init__(self, value: float):
        super().__init__('numberLiteral')
        self.value = value


class IdentifierNode(ExpressionNode):
    def __init__(self, value: str):
        super().__init__('identifier')
        self.value = value


class BinaryExpressionNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, right: ExpressionNode, operator: Operator):
        super().__init__('binaryExpression')
        self.left = left
        self.right = right
        self.operator = operator


class BlockExpressionNode(ExpressionNode):
    def __init__(self, statements: list[StatementNode]):
        super().__init__('blockExpression')
        self.statements = statements


class CallStatementNode(StatementNode):
    def __init__(self, name: str, args: list[ExpressionNode], type: str = 'callStatement'):
        super().__init__(type)
        self.name = name
        self.args = args


class PrintStatementNode(CallStatementNode):
    def __init__(self, arg: ExpressionNode):
        super().__init__('print', [arg])


class SetPixelStatementNode(CallStatementNode):
    def __init__(self, args: list[ExpressionNode]):
        super().__init__('setpixel', args)


class WhileStatementNode(StatementNode):
    def __init__(self, expression: ExpressionNode, body: Union[StatementNode, BlockExpressionNode]):
        self.body = body
        self.expression = expression
        super().__init__('whileStatement')


class IfStatementNode(StatementNode):
    def __init__(self, expression: ExpressionNode, consequent: Union[StatementNode, BlockExpressionNode], alternate: Union[StatementNode, BlockExpressionNode] = None):
        self.consequent = consequent
        self.alternate = alternate
        self.expression = expression
        super().__init__('ifStatement')


class ProcStatementNode(StatementNode):
    def __init__(self, name: str, args: list[IdentifierNode], statements: BlockExpressionNode):
        super().__init__('procStatement')
        self.name = name
        self.args = args
        self.statements = statements
