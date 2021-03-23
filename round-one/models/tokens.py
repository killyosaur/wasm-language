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


class Token(object):
    def __init__(self, typeVal: TokenType, value: str):
        self.type = typeVal
        self.value = value
        self.line = -1
        self.char = -1
