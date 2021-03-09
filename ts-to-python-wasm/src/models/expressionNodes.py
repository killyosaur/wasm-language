from models.node import Operator, ExpressionNode, StatementNode

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
