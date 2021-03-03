class Node(object):
    def __init__(self, type):
        self.type = type

class StatementNode(Node):
    def __init__(self, type, value):
        super().__init__(type)
        self.value = value

class ExpressionNode(Node):
    def __init__(self, type, expression):
        super().__init__(type)
        self.expression = expression

class Program(list[StatementNode]):
    def forEach(self, callback: callable):
        for i in self:
            callback(i)

class NumberLiteralNode(ExpressionNode):
    def __init__(self, value):
        super().__init__('numberLiteral', value)

class PrintStatementNode(StatementNode):
    def __init__(self, expression):
        super().__init__('printStatement', expression)