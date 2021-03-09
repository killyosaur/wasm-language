from infrastructure.switcher import switch
from models.tokens import Token, TokenType
from models.node import ExpressionNode, StatementNode, Operator
import models.expressionNodes as exn
import models.statementNodes as stn

class ParserException(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

def asOperator(op: str) -> Operator:
    return Operator[op]

def Parse(tokens: list[Token]):
    iterator = iter(tokens)
    currentToken = next(iterator)

    def eatToken(value: str = None):
        nonlocal currentToken
        if value != None and currentToken.value != value:
            raise ParserException(f"Unexpected token value, expected {value}, received {currentToken.value}", currentToken)
        
        currentToken = next(iterator, None)
    
    def parseExpression():
        def getNumber():
            node = exn.NumberLiteralNode(float(currentToken.value))
            eatToken()
            return node
        def getParens():
            eatToken('(')
            left = parseExpression()
            operator = currentToken.value
            eatToken()
            right = parseExpression()
            eatToken(')')
            return exn.BinaryExpressionNode(left, right, asOperator(operator))
        def getCodeBlock():
            eatToken('{')
            nodes = []
            while currentToken.value != '}':
                if currentToken == None:
                    raise ParserException('Expected ending "}" bracket', currentToken)
        
                print(f'{currentToken.type}:{currentToken.value}')
                nodes.append(parseStatement())

            eatToken('}')
            return exn.CodeBlockNode(nodes)
        def getIdentifier():
            node = exn.IdentifierNode(currentToken.value)
            eatToken()
            return node
        def default():
            raise ParserException(f'Unexpected token type {currentToken.type}', currentToken)
        
        return switch(currentToken.type, {
            TokenType.Number: getNumber,
            TokenType.Parenthesis: getParens,
            TokenType.Identifier: getIdentifier,
            TokenType.CodeBlock: getCodeBlock
        }, default)
    
    def parseStatement():
        def varAssignStatement():
            name = currentToken.value
            eatToken()
            eatToken('=')
            return stn.VariableAssignmentNode(name, parseExpression())
        def keywordSwitch(tokenValue: str):
            def printStatement():
                eatToken('print')
                return stn.PrintStatementNode(parseExpression())
            def varDeclareStatement():
                eatToken('var')
                name = currentToken.value
                eatToken()
                eatToken('=')
                return stn.VariableDeclarationNode(name, parseExpression())
            def whileStatement():
                eatToken('while')
                expression = parseExpression()

                if expression.type != 'binaryExpression':
                    raise ParserException('expected a logical expression', currentToken)

                return stn.WhileStatementNode(expression, parseExpression())
            def setpixelStatement():
                eatToken('setpixel')
                return stn.SetPixelStatementNode(parseExpression(), parseExpression(), parseExpression())
            def default():
                raise ParserException(f'Unknown keyword {currentToken.value}', currentToken)
        
            return switch(tokenValue, {
                'print': printStatement,
                'var': varDeclareStatement,
                'while': whileStatement,
                'setpixel': setpixelStatement
            }, default)
        
        return switch(currentToken.type, {
            TokenType.Keyword: lambda: keywordSwitch(currentToken.value),
            TokenType.Identifier: varAssignStatement
        }, lambda: None)
    
    nodes = []
    while currentToken != None:
        nodes.append(parseStatement())
    
    return nodes
