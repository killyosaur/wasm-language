class Node(object):
    def __init__(self, type):
        self.type = type

class ExpressionNode(Node):
    def __init__(self, type, value):
        super().__init__(type)
        self.value = value

class StatementNode(Node):
    def __init__(self, type, expression):
        super().__init__(type)
        self.expression = expression

class Program(list[StatementNode]):
    def __init__():
        super().__init__()

class NumberLiteralNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('numberLiteral', value)

class PrintStatementNode(StatementNode):
    def __init__(self, expression):
        super().__init__('printStatement', expression)