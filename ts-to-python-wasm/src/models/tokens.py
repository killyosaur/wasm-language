from enum import Enum

class TokenType(Enum):
    Number = 'number'
    Keyword = 'keyword'
    Whitespace = 'whitespace'
    Parenthesis = 'parens'
    Operator = 'operator'

class Token(object):
    def __init__(self, typeVal: TokenType, value: str):
        self.type = typeVal
        self.value = value
        self.line = -1
        self.char = -1
