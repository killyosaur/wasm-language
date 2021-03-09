from infrastructure.switcher import switch
from models.tokens import Token, TokenType
from models.node import ExpressionNode, StatementNode, NumberLiteralNode, PrintStatementNode, Operator, BinaryExpressionNode, IdentifierNode, VariableDeclarationNode

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
            node = NumberLiteralNode(float(currentToken.value))
            eatToken()
            return node
        def getParens():
            eatToken('(')
            left = parseExpression()
            operator = currentToken.value
            eatToken()
            right = parseExpression()
            eatToken(')')
            return BinaryExpressionNode(left, right, asOperator(operator))
        def getCodeBlock():
            eatToken('{')
            nodes = []
            while currentToken.value != '}':
                if currentToken == None:
                    raise ParserException('Expected ending "}" bracket', currentToken)
        
                if currentToken.type == TokenType.Keyword:
                    nodes.append(parseStatement())
                else:
                    nodes.append(parseExpression())
            eatToken('}')
            return CodeBlockNode(nodes)
        def getIdentifier():
            node = IdentifierNode(currentToken.value)
            eatToken()
            return node
        def default():
            raise ParserException(f'Unexpected token type {currentToken.type}', currentToken)
        
        return switch(currentToken.type, {
            TokenType.Number: getNumber,
            TokenType.Parenthesis: getParens,
            TokenType.Identifier: getIdentifier
        }, default)
    
    def parseStatement():
        def keywordSwitch(tokenValue: str):
            def printStatement():
                eatToken('print')
                return PrintStatementNode(parseExpression())
            def varDeclareStatement():
                eatToken('var')
                name = currentToken.value
                eatToken()
                eatToken('=')
                return VariableDeclarationNode(name, parseExpression())
            def varAssignStatement():
                name = currentToken.value
                eatToken()
                eatToken('=')
                return VariableAssignmentNode(name, parseExpression())
            def whileStatement('while'):
                eatToken('while')
                expression = parseExpression()

                if expression.type != 'binaryExpression':
                    raise ParserException('expected a logical expression', currentToken)

                return WhileStatementNode(expression, parseExpression())
            def default():
                raise ParserException(f'Unknown keyword {currentToken.value}', currentToken)
        
            if currentToken.type == TokenType.Keyword:
                return switch(tokenValue, {
                    'print': printStatement,
                    'var': varStatement,
                    'while': whileStatement
                }, default)
            else if currentToken.type == TokenType.Identifier:
                return varAssignStatement()
        
        return switch(currentToken.type, {
            TokenType.Keyword: lambda: keywordSwitch(currentToken.value)
        }, lambda: None)
    
    nodes = []
    while currentToken != None:
        nodes.append(parseStatement())
    
    return nodes
