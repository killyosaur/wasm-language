from Infrastructure.switcher import Switcher
from Parser.node import Node
from Parser.node import ExpressionNode
from Parser.node import StatementNode

class ParserException(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

class Parser(object):
    def __init__(self, tokens: list):
        self.iterator = iter(tokens)
        self.eatToken()

    def eatToken(self):
        self.currentToken = next(self.iterator, None)

    def parseExpression(self):
        def getNumber():
            node = ExpressionNode("numberLiteral", self.currentToken.value)
            print(f"get Number: {self.currentToken.value}")
            self.eatToken()
            return node

        dictionary = {
            "number": getNumber
        }
        parseSwitch = Switcher(dictionary, lambda: None)
        return parseSwitch.switch(self.currentToken.type)

    def parseStatement(self):
        def printStmt():
            self.eatToken()
            print(f"print statement: {self.currentToken.value}")
            return StatementNode("printStatement", self.parseExpression())
        
        if self.currentToken.type == "keyword":
            keywordSwitcher = Switcher({
                "print": printStmt 
            }, lambda: None)
            return keywordSwitcher.switch(self.currentToken.value)
    
    def parser(self):
        nodes = []
        while self.currentToken != None:
            print(f"token is: {self.currentToken.value}")
            nodes.append(self.parseStatement())
        
        print(f"the end of parse: {self.currentToken}")
        return nodes
