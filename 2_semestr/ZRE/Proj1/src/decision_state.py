import sys
sys.path.insert(0, 'tools')
from token import Token

class DecisionState(object):
    def __init__(self, token, numberNameList):
        self.inputs = []
        self.token = token
        self.numberNameList = numberNameList
        self.iter = 0

    def GetTokenCopy(self):
        t = Token(self.token.value)
        for n in self.token.passedNumbers:
            t.AddPassedNumber(n)
        return t

    def Next(self):
        # Pick token with maximum value
        self.tmpToken = self.inputs[0].token
        self.iter += 1
        for inputState, numberName in zip(self.inputs, self.numberNameList):
            if inputState.token.value >= self.tmpToken.value:
                self.tmpToken = inputState.GetTokenCopy()
                if numberName is not None:
                    self.tmpToken.AddPassedNumber(numberName)

    def UpdateToken(self):
        self.token = self.tmpToken
