import numpy as np
import os
import sys
import argparse
sys.path.insert(0, 'tools')
from htk import readhtk
from collections import OrderedDict

from state import State
from token import Token

from number_model import NumberModel
from pause_model import PauseModel
from net_model import NetModel
from number_state import NumberState
from decision_state import DecisionState

megaNegNumber = -1000000000000

def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--likelihood-matrix', type=str, required=True, help="Input likelihood matrix to recognize.")
    parser.add_argument('--phonemes', type=str, required=True, help="phonemes file.")
    parser.add_argument('--zre-dict', type=str, required=True, help="zre.dict file.")
    parser.add_argument('--verbose', action="store_true", default=False,
                        help="if true prints everythink, if not prints only results")

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    if verbose:
        print( ' '.join(sys.argv))

    return args


def main():
    global megaNegNumber

    args = parseargs()
    likelihoodMatrix = readhtk(args.likelihood_matrix)
    if verbose:
        print(likelihoodMatrix)
        print(likelihoodMatrix.shape)
        print(likelihoodMatrix[0].shape)

    phonemesMapping = GetPhonemesMapping(args.phonemes)
    if verbose:
        print("PHONEMES MAPPING")
    for phonem, index in phonemesMapping.items():
        if verbose:
            print(phonem, index)
    if verbose:
        print("")

    numberModels, numberNames = GetNumberModels(args.zre_dict, phonemesMapping)
    if verbose:
        print("NUMBER MODELS")
    for numberModel in numberModels:
        if verbose:
            print(numberModel.name)
        for state in numberModel.states:
            if verbose:
                print(state.name, state.token.value)
        if verbose:
            print("")
    if verbose:
        print("")

    netModel = NetModel(numberModels, DecisionState(Token(0), numberNames))


    """
    MAIN LOOP
    """
    for t in range(likelihoodMatrix.shape[0]):
        netModel.UpdateModelsLikelihoods(likelihoodMatrix[t])
        netModel.Next()
        netModel.UpdateTokens()
        """
        print(likelihoodMatrix[t])
        for numberModel in netModel.numberModels:
            for state in numberModel.states:
                print(state.name, state.likelihoodMatrixColIndex, state.value)
            break
        break
        """
        
    for n in netModel.decisionState.token.passedNumbers:
        print(n)

def GetNumberModels(zreDict, phonemesMapping):
    numberModels = []
    numberNames = []
    with open(zreDict) as f:
        hmmModelsSpecificationLines = f.readlines()
        for hmmModelSpecification in hmmModelsSpecificationLines:
            numberModel = NumberModel(hmmModelSpecification.strip().split()[0])
            hmmModelSpecification = hmmModelSpecification.strip().split()[1:]
            if verbose:
                print(numberModel.name)
            previousState = None
            for phonem in hmmModelSpecification:
                # Generate three sub states fo each phonem
                for subPhonemIndex in range(3):
                    stateName = "{}_{}".format(phonem, subPhonemIndex)
                    likelihoodMatrixColIndex = phonemesMapping[phonem] * 3 + subPhonemIndex
                    previousState = State(stateName, previousState, Token(megaNegNumber), likelihoodMatrixColIndex)
                    numberModel.AddState(previousState)
            # Add dummy number state
            numberNames.append(numberModel.name)
            numberModel.AddNumberState(NumberState(numberModel.name, previousState, Token(megaNegNumber)))
            numberModels.append(numberModel)
    # Add pause model
    pauseModel = PauseModel()
    previousState = None
    for subPhonemIndex in range(3):
        stateName = "{}_{}".format("pau", subPhonemIndex)
        likelihoodMatrixColIndex = phonemesMapping["pau"] * 3 + subPhonemIndex
        previousState = State(stateName, previousState, Token(megaNegNumber), likelihoodMatrixColIndex)
        pauseModel.AddState(previousState)
    numberModels.append(pauseModel)
    numberNames.append(None)
    return numberModels, numberNames


def GetPhonemesMapping(phonemesFile):
    phonemesMapping = OrderedDict()
    with open(phonemesFile) as f:
        for i, line in enumerate(f.readlines()):
            phonemesMapping[line.strip()] = i
    return phonemesMapping


if __name__ == '__main__':
    main()
