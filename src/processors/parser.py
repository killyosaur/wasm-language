from infrastructure.switcher import switch
from models.tokenizer import Token, TokenType
from models.parser import ExpressionNode, StatementNode, Operator, Program
import models.parser as nodeType


class ParserException(Exception):
  def __init__(self, message, token):
    self.message = message
    self.token = token


def asOperator(op: str) -> Operator:
  return Operator[op]


def defaultError(message: str, currentToken: Token):
  raise ParserException(message, currentToken)

def Parse(tokens: list[Token]) -> Program:
  tokenIterator = iter(tokens)
  currentToken = next(tokenIterator)
  nextToken = next(tokenIterator)
  
  currentTokenIsKeyword = lambda name: currentToken.value == name and currentToken.type == TokenType.Keyword

  def eatToken(value: str = None):
    nonlocal currentToken
    nonlocal nextToken
    if value != None and value != currentToken.value:
      raise ParserException(
        f'Unexpected token value, expected {value}, received {currentToken.value}', currentToken)
    
    currentToken = nextToken
    nextToken = next(tokenIterator, None)

  def parseExpression() -> ExpressionNode:
    def parseNumber() -> nodeType.NumberLiteralNode:
      node = nodeType.NumberLiteralNode(float(currentToken.value))
      eatToken()
      return node

    def parseParenthesis() -> nodeType.BinaryExpressionNode:
      eatToken('(')
      left = parseExpression()
      operator = currentToken.value
      eatToken()
      right = parseExpression()
      eatToken(')')
      return nodeType.BinaryExpressionNode(left, right, asOperator(operator))

    def parseCodeBlock() -> nodeType.BlockExpressionNode:
      eatToken('{')
      statements = []
      while currentToken.value != '}':
        if currentToken == None:
          raise ParserException('Expected ending "}" bracket', currentToken)

        statements.append(parseStatement())
      
      eatToken('}')
      return nodeType.BlockExpressionNode(statements)
    
    def parseIdentifier() -> nodeType.IdentifierNode:
      node = nodeType.IdentifierNode(currentToken.value)
      eatToken()
      return node

    return switch(currentToken.type, {
      TokenType.Number: parseNumber,
      TokenType.Parenthesis: parseParenthesis,
      TokenType.Identifier: parseIdentifier,
      TokenType.CodeBlock: parseCodeBlock
    }, lambda: defaultError(f'Unexpected token type {currentToken.type}', currentToken))
  
  def parseCommaSeparatedList(parse: callable) -> list:
    args = []
    eatToken('(')
    while currentToken.value != ')':
      args.append(parse())
      if currentToken.value == ',':
        eatToken(',')
    eatToken(')')

    return args

  def parsePrintStatement() -> nodeType.PrintStatementNode:
    eatToken('print')
    return nodeType.PrintStatementNode(parseExpression())

  def parseIfStatement() -> nodeType.IfStatementNode:
    eatToken('if')

    expression = parseExpression()

    if expression.type != 'binaryExpression':
      raise ParserException(
        'expected a logical expression', currentToken)

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
    
    return nodeType.IfStatementNode(expression, consequent, alternate)
  
  def parseWhileStatement() -> nodeType.WhileStatementNode:
    eatToken('while')

    expression = parseExpression()

    if expression.type != 'binaryExpression':
      raise ParserException(
        'expected a logical expression', currentToken)

    if currentToken.type == TokenType.CodeBlock:
      return nodeType.WhileStatementNode(expression, parseExpression())
    
    return nodeType.WhileStatementNode(expression, parseStatement())

  def parseSetpixelStatement() -> nodeType.SetPixelStatementNode:
    eatToken('setpixel')
    args = parseCommaSeparatedList(parseExpression)

    if len(args) != 3:
      raise ParserException('expected 3 values to be passed in', currentToken)

    return nodeType.SetPixelStatementNode(args)

  def parseVariableAssignmentStatement() -> nodeType.VariableAssignmentNode:
    name = currentToken.value
    eatToken()
    eatToken('=')
    return nodeType.VariableAssignmentNode(name, parseExpression())

  def parseVariableDeclarationStatement() -> nodeType.VariableDeclarationNode:
    eatToken('var')
    name = currentToken.value
    eatToken()
    if currentToken.value != '=':
      return nodeType.VariableDeclarationNode(name, nodeType.NumberLiteralNode(0))

    eatToken('=')

    return nodeType.VariableDeclarationNode(name, parseExpression())

  def parseCallStatementNode() -> nodeType.CallStatementNode:
    name = currentToken.value
    eatToken()

    args = parseCommaSeparatedList(parseExpression)

    return nodeType.CallStatementNode(name, args)

  def parseProcStatement() -> nodeType.ProcStatementNode:
    eatToken('proc')

    name = currentToken.value
    eatToken()

    def parseProcParameters() -> nodeType.IdentifierNode:
      arg = nodeType.IdentifierNode(currentToken.value)
      eatToken()
      return arg

    args = parseCommaSeparatedList(parseProcParameters)

    if currentToken.type != TokenType.CodeBlock:
      raise ParserException(f'expected a code block, received a {currentToken.type}', currentToken)
    
    body = parseExpression()

    return nodeType.ProcStatementNode(name, args, body)
  
  def parseStatement() -> StatementNode:
    def keywordSwitch(tokenValue: str) -> StatementNode:
      return switch(tokenValue, {
        'print': parsePrintStatement,
        'setpixel': parseSetpixelStatement,
        'var': parseVariableDeclarationStatement,
        'if': parseIfStatement,
        'while': parseWhileStatement,
        'proc': parseProcStatement
      }, lambda: defaultError(f'Unknown keyword {currentToken.value}', currentToken))

    def identifierSwitch(nextTokenValue: str) -> StatementNode:
      if nextTokenValue == '=':
        return parseVariableAssignmentStatement()
      else:
        return parseCallStatementNode()

    return switch(currentToken.type, {
      TokenType.Keyword: lambda: keywordSwitch(currentToken.value),
      TokenType.Identifier: lambda: identifierSwitch(nextToken.value)
    }, lambda: None)

  nodes = []
  while currentToken != None:
    nodes.append(parseStatement())

  return nodes
