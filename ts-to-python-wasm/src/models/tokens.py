class Token(object):
    def __init__(self, typeVal, value, index = -1):
        self.type = typeVal
        self.value = value
        self.index = index
