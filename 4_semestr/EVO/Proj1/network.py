"""Class that represents the network to be evolved."""
import random
import logging
from train import train_and_score

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras import losses
from sklearn import metrics


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


    def train(self):
        """Train the network and record the accuracy.

        Args:
            dataset (str): Name of dataset to use.

        """
        if self.accuracy == 0.:
            self.accuracy = self.train_and_score()


    def print_network(self):
        """Print out a network."""
        logging.info(self.network)
        logging.info("Network accuracy: %.2f%%" % (self.accuracy * 100))


    def compile_model(self, nb_classes, input_shape):
        model = Sequential()

        model.add(Dense(self.layers[0][0], activation=self.layers[0][1], input_shape=input_shape))
        for i in range(self.nb_layers-1):
            model.add(Dense(self.layers[i][0], activation=self.layers[i][1]))
            #model.add(Dropout(0.2))

        model.add(Dense(nb_classes, activation="linear"))
        model.compile(loss="MSE", optimizer=self.optimizer, metrics=['accuracy'])

        return model


    def train_and_score(self):
        """Train the model, return test loss.

        Args:
            network (dict): the parameters of the network
            dataset (str): Dataset to use for training/evaluating

        """
        nb_classes = 1
        epochs = 2500
        batch_size = 1024
        input_shape = (50,)

        model = self.compile_model(nb_classes, input_shape)
        #X, Y = dataset.get_val_batch(typeisch)

        lowest = 1000000
        """
        logging.info("#####################################")
        logging.info(network)
        for eps in range(epochs):
            X_trn, Y_trn = dataset.get_trn_minibatch(batch_size, typeisch)
            X_val, Y_val = dataset.get_val_batch(typeisch)

            history = model.fit(X_trn, Y_trn, epochs=1, verbose=0)

            predictions = model.predict(X)
            test = metrics.log_loss(Y, np.squeeze(predictions, axis=1))

            if test < lowest:
                logging.info("############ LogLoss: {}".format(test))
                model.save_weights("./{}-neural_network-{}.h5".format(typeisch, test))
                lowest = test
            if eps == 100:
                if lowest == 1000000:
                    logging.info("This model doesn't learn.")
                    break

        logging.info("############ LogLoss Final: {}".format(lowest))
        """
        return lowest
