from number_model import NumberModel

class NetModel(object):
    def __init__(self, numberModels, decisionState):
        self.numberModels = numberModels
        self.decisionState = decisionState
        # Connect number models with decision state
        inputsStatesForDecisionState = []
        for numberModel in self.numberModels:
            inputsStatesForDecisionState.append(numberModel.states[-1])
            # if type(numberModel) is NumberModel:
            #     inputsStatesForDecisionState.append(numberModel.numberState)
            # else:
                
        self.decisionState.inputs = inputsStatesForDecisionState
        # Connect decision state with number models
        for numberModel in self.numberModels:
            numberModel.states[0].input = self.decisionState

    def UpdateModelsLikelihoods(self, likelihoodMatrixCol):
        for numberModel in self.numberModels:
            numberModel.UpdateStatesLikelihoods(likelihoodMatrixCol)

    def Next(self):
        for numberModel in self.numberModels:
            numberModel.Next()
        self.decisionState.Next()

    def UpdateTokens(self):
        for numberModel in self.numberModels:
            numberModel.UpdateTokens()
        self.decisionState.UpdateToken()
