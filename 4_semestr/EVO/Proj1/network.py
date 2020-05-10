"""Class that represents the network to be evolved."""
import os
import copy
import logging
logging.basicConfig(filename=os.path.join(os.getcwd(), 'ga.log'), level=logging.DEBUG)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from dqn import train


class Network():
    """Represent a network and let us operate on it.

    Currently only works for an MLP.
    """
    def __init__(self, layers, optimizer):
        """Initialize our network.

        Args:
            nn_param_choices (dict): Parameters for the network, includes:
                nb_neurons (list): [64, 128, 256]
                nb_layers (list): [1, 2, 3, 4]
                activation (list): ['relu', 'elu']
                optimizer (list): ['rmsprop', 'adam']
        """
        self.accuracy = 0.

        self.nb_layers = len(layers)
        self.layers = layers
        self.optimizer = optimizer

    def create_set(self, network):
        """Set network properties.

        Args:
            network (dict): The network parameters

        """
        self.network = network


    def train(self, memory):
        """Train the network and record the accuracy.

        Args:
            dataset (str): Name of dataset to use.

        """
        self.accuracy = self.train_and_score(memory)
        self.print_network()


    def print_network(self):
        """Print out a network."""
        logging.info("{} - {}" .format(self.layers, self.optimizer))
        logging.info("Network score: {}" .format(self.accuracy))


    def compile_model(self, nb_classes, input_shape):
        model = Sequential()

        model.add(Dense(self.layers[0][0], activation=self.layers[0][1], input_shape=input_shape))
        for i in range(self.nb_layers-1):
            model.add(Dense(self.layers[i][0], activation=self.layers[i][1]))
            #model.add(Dropout(0.2))

        model.add(Dense(nb_classes, activation="linear"))
        model.compile(loss="MSE", optimizer=self.optimizer, metrics=['accuracy'])

        return model


    def train_and_score(self, memory):
        """Train the model, return test loss.

        Args:
            network (dict): the parameters of the network
            dataset (str): Dataset to use for training/evaluating

        """
        nb_classes = 2
        epochs = 500
        input_shape = (4,)

        model = self.compile_model(nb_classes, input_shape)
        memory = copy.deepcopy(memory)
        score = train('CartPole-v0', model, memory, epochs)

        return score
