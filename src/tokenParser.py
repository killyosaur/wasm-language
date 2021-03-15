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
    nextToken = next(iterator)

    def eatToken(value: str = None):
        nonlocal currentToken
        nonlocal nextToken

        if value != None and currentToken.value != value:
            raise ParserException(f"Unexpected token value, expected {value}, received {currentToken.value}", currentToken)
        
        currentToken = nextToken
        nextToken = next(iterator, None)
    
    def parseCommaSeparatedList(action: callable):
        args = []
        eatToken('(')
        while currentToken.value !== ')':
            args.append(action())
            if(currentToken.value == ','):
                eatToken(',')
        eatToken(')')
        return args

    def parseExpression(parseThis: TokenType = None):
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
        
        if parseThis != None and currentToken.type != parseThis:
            raise ParserException(f'Expected token of type {parseThis}', currentToken)

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
        def callStatement():
            name = currentToken.value
            eatToken()

            args = parseCommaSeparatedList(parseExpression)

            return stn.CallStatementNode(args)
        def varIdentifierParser():
            if nextToken.value == '=':
                return varAssignStatement()
            else:
                return callStatement()
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

                if currentToken.type == TokenType.CodeBlock:
                    return stn.WhileStatementNode(expression, parseExpression())
                
                return stn.WhileStatementNode(expression, parseStatement())

            def setpixelStatement():
                eatToken('setpixel')
                return stn.SetPixelStatementNode(parseExpression(), parseExpression(), parseExpression())
            def procStatement():
                eatToken('method')

                name = currentToken.value
                eatToken()

                def getParams():
                    arg = exn.IdentifierNode(currentToken.value)
                    eatToken()
                    return arg                    

                args = parseCommaSeparatedList(getParams)

                expression = parseExpression(TokenType.CodeBlock)

                return ProcStatementNode(name, args, expression)
            def ifStatement():
                eatToken('if')

                expression = parseExpression()

                if expression.type != 'binaryExpression':
                    raise ParserException('expected a logical expression', currentToken)

                consequent = None
                alternate = None
                if currentToken.type == TokenType.CodeBlock:
                    consequent = parseExpression()
                else:
                    consequent = parseStatement()

                if currentToken.value == 'else':
                    eatToken('else')
                    if currentToken.type == TokenType.CodeBlock:
                        alternate = parseExpression()
                    else:
                        alternate = parseStatement()
                
                return stn.IfStatementNode(expression, consequent, alternate)

            def default():
                raise ParserException(f'Unknown keyword {currentToken.value}', currentToken)
        
            return switch(tokenValue, {
                'print': printStatement,
                'var': varDeclareStatement,
                'while': whileStatement,
                'setpixel': setpixelStatement,
                'if': ifStatement,
                'proc': procStatement
            }, default)
        
        return switch(currentToken.type, {
            TokenType.Keyword: lambda: keywordSwitch(currentToken.value),
            TokenType.Identifier: varIdentifierParser
        }, lambda: None)
    
    nodes = []
    while currentToken != None:
        nodes.append(parseStatement())
    
    return nodes
