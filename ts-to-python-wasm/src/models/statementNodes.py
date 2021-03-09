from models.node import StatementNode, ExpressionNode
from models.expressionNodes import BinaryExpressionNode, CodeBlockNode
from typing import Union

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

class SetPixelStatementNode(StatementNode):
    def __init__(self, x: ExpressionNode, y: ExpressionNode, color: ExpressionNode):
        self.x = x
        self.y = y
        self.color = color
        super().__init__('setPixelStatement', None)