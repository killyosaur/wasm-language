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
