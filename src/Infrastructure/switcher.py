class Switcher(object):
    def __init__(self, statements, default):
        self.dictionary = statements
        self.default = default

    def switch(self, argument):
        result = self.dictionary.get(argument, self.default)

        if callable(result):
            return result()
        else:
            return result
