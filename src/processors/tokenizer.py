import re
from models.tokenizer import Token, TokenType

tokens = [
  {'type': TokenType.Keyword, 'value': [
    'print', 'var', 'while', 'setpixel', 'if', 'else', 'proc']},
  {'type': TokenType.Operator, 'value': [
    '+', '*', '-', '/', '==', '<', '>', '&&', '||', ',']},
  {'type': TokenType.Whitespace, 'value': '\\s+'},
  {'type': TokenType.Number, 'value': '([0-9]+)?(\.)?[0-9]+'},
  {'type': TokenType.Parenthesis, 'value': '[()]{1}'},
  {'type': TokenType.CodeBlock, 'value': '[\{\}]{1}'},
  {'type': TokenType.Assignment, 'value': '='},
  {'type': TokenType.Identifier, 'value': '[_a-zA-Z]{1}[a-zA-Z0-9_]*'}
]


class TokenizerException(Exception):
  def __init__(self, message, index):
    self.message = message
    self.index = index


def escapeRegEx(text): return re.sub(
  r'([-[\]{}()*+?.,\\^$|#\s])', r'\\\1', text)


class RegexMatcher:
  def __init__(self, regex, typeVal):
    finalRegex = regex
    if(isinstance(regex, list)):
      regex = map(escapeRegEx, regex)
      finalRegex = '|^'.join(regex)

    self.regex = re.compile(f'^{finalRegex}')
    self.type = typeVal

  def match(self, input: str, index: int):
    substr = input[index:]
    m = self.regex.search(substr)
    if m != None:
      return Token(self.type, m.group(0))
    else:
      return Token(self.type, None)


matchers = [RegexMatcher(i['value'], i['type']) for i in tokens]


def locationForIndex(input: str, index: int):
  return {
    "char": index - input.rfind("\n", index) - 1,
    "line": len(input[0:index].split('\n')) - 1
  }


def Matcher(input: str, index: int):
  for x in matchers:
    match = x.match(input, index)
    if (match.value != None):
      return match
  return None


def Tokenize(input: str):
  tokens = []
  index = 0
  while index < len(input):
    match = Matcher(input, index)
    tokLoc = locationForIndex(input, index)

    if match.value == None:
      raise TokenizerException(
        f'Unexpected token {input[index:index+1]}',
        index
      )
    index += len(match.value)
    if match.type == TokenType.Whitespace:
      continue

    match.char = tokLoc["char"]
    match.line = tokLoc["line"]
    tokens.append(match)
  return tokens
