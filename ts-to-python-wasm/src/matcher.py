import re
from models.tokens import Token

class RegexMatcher:
    def __init__(self, regex, typeVal):
        self.regex = re.compile(regex)
        self.type = typeVal
    def match(self, input, index):
        m = self.regex.search(input[index:])
        if m != None:
            return Token(self.type, m.group(0), index)
        else:
            return Token(self.type, None)
