import re
from models.tokens import Token

escapeRegEx = lambda text: re.sub(r'([-[\]{}()*+?.,\\^$|#\s])', r'\\\1', text)

class RegexMatcher:
    def __init__(self, regex, typeVal):
        finalRegex = regex
        if(isinstance(regex, list)):
            regex = map(escapeRegEx, regex)
            finalRegex = '|^'.join(regex)

        self.regex = re.compile(f'^{finalRegex}')
        self.type = typeVal
    def match(self, input, index):
        m = self.regex.search(input[index:])
        if m != None:
            return Token(self.type, m.group(0))
        else:
            return Token(self.type, None)
