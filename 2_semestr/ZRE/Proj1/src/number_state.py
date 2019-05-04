import sys
sys.path.insert(0, 'tools')
from token import Token

class NumberState(object):
    def __init__(self, name, input, token):
        self.name = name
        self.input = input
        self.token = token

    def GetTokenCopy(self):
        t = Token(self.token.value)
        for n in self.token.passedNumbers:
            t.AddPassedNumber(n)
        t.AddPassedNumber(self.name)
        return t

    def Next(self):
        pass

    def UpdateToken(self):
        self.token = self.input.token
