from infrastructure.switcher import switch
from models.tokens import Token
from models.node import ExpressionNode, StatementNode, NumberLiteralNode, PrintStatementNode

class ParserException(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

def Parse(tokens: list[Token]):
    iterator = iter(tokens)
    currentToken = next(iterator)

    def eatToken():
        nonlocal currentToken
        currentToken = next(iterator, None)
    
    def parseExpression():
        def getNumber():
            node = NumberLiteralNode(currentToken.value)
            eatToken()
            return node
        
        return switch(currentToken.type, {
            'number': getNumber
        }, lambda: None)
    
    def parseStatement():
        def keywordSwitch(tokenValue: str):
            def printStatement():
                eatToken()
                return PrintStatementNode(parseExpression())
        
            return switch(tokenValue, {
                'print': printStatement
            }, lambda: None)
        
        return switch(currentToken.type, {
            'keyword': lambda: keywordSwitch(currentToken.value)
        }, lambda: None)
    
    nodes = []
    while currentToken != None:
        nodes.append(parseStatement())
    
    return nodes
