

class PauseModel(object):
    def __init__(self):
        self.name = "pauza"
        self.states = []

    def AddState(self, state):
        self.states.append(state)

    def UpdateStatesLikelihoods(self, likelihoodMatrixCol):
        for state in self.states:
            state.UpdateLikelihood(likelihoodMatrixCol)

    def Next(self):
        for state in self.states:
            state.Next()

    def UpdateTokens(self):
        for state in self.states:
            state.UpdateToken()
