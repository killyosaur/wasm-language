from enum import Enum


class TokenType(Enum):
    Assignment = 'assignment'
    Number = 'number'
    Keyword = 'keyword'
    Identifier = 'identifier'
    Whitespace = 'whitespace'
    Parenthesis = 'parens'
    CodeBlock = 'block'
    Operator = 'operator'

class Token:
  def __init__(self, type: TokenType, value: str):
    self.type = type
    self.value = value
    self.line: int = None
    self.char: int = None
  
  def __str__(self):
    return f'{{"type": "{self.type}", "value": "{self.value}", "line": {self.line}, "char": {self.char}}}'
