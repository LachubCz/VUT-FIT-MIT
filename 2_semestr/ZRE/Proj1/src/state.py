from math import log
import sys
sys.path.insert(0, 'tools')
from token import Token

class State(object):
    def __init__(self, name, input, token, likelihoodMatrixColIndex):
        self.name = name
        self.input = input
        self.token = token
        self.likelihoodMatrixColIndex = likelihoodMatrixColIndex
        self.likelihood = 0

    def GetTokenCopy(self):
        t = Token(self.token.value)
        for n in self.token.passedNumbers:
            t.AddPassedNumber(n)
        return t

    def UpdateLikelihood(self, likelihoodMatrixCol):
        self.likelihood = likelihoodMatrixCol[self.likelihoodMatrixColIndex]

    def Next(self):
        #take max of two incomming tokens (input and self loop)
        if self.input.token.value >= self.token.value:
            self.tmpToken = self.input.GetTokenCopy()
        else:
            self.tmpToken = self.token

    def UpdateToken(self):
        self.token = self.tmpToken
        if "pau" in self.name:
            self.token.value += log(0.5) + log(self.likelihood)
        else:   
            self.token.value += log(0.5) + log(self.likelihood)
