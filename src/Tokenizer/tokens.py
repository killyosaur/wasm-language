import re

tokens = ["print"]

class TokenizerException(Exception):
    def __init__(self, message, index):
        self.message = message
        self.index = index

class Token(object):
    def __init__(self, type, value, index):
        self.type = type
        self.value = value
        self.index = index

class Match(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class RegexMatcher:
    def __init__(self, regex, type):
        self.regex = re.compile(regex)
        self.type = type
    def match(self, input, index):
        m = self.regex.search(input[index:])
        if m != None:
            return Match(self.type, m.group(0))
        else:
            return Match(self.type, None)

keywordRegex = "|".join(tokens)
matchers = [
    RegexMatcher("^[.0-9]+", "number"),
    RegexMatcher(f"^({keywordRegex})", "keyword"),
    RegexMatcher("^\\s+", "whitespace")
]

def locationForIndex(input: str, index: int):
    return {
        "char": index - input.rindex("\n", beg=index),
        "line": input[0:index].s
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
        if match.value == None:
            raise TokenizerException(
                f'Unexpected token {input[index:index+1]}',
                index
            )
        index += len(match.value)
        if match.type == "whitespace":
            continue
        tokens.append(match)
    return tokens
