

class NumberModel(object):
    def __init__(self, name):
        self.name = name
        self.states = []
        self.numberState = None

    def AddState(self, state):
        self.states.append(state)

    def AddNumberState(self, numberState):
        self.numberState = numberState

    def UpdateStatesLikelihoods(self, likelihoodMatrixCol):
        for state in self.states:
            state.UpdateLikelihood(likelihoodMatrixCol)

    def Next(self):
        for state in self.states:
            state.Next()
        self.numberState.Next()

    def UpdateTokens(self):
        for state in self.states:
            state.UpdateToken()
        self.numberState.UpdateToken()
