import os
import gym
import copy
import logging
logging.basicConfig(filename=os.path.join(os.getcwd(), 'records.log'), level=logging.DEBUG)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from dqn import train


class Network():
    def __init__(self, layers, optimizer):
        self.accuracy = 0.
        self.nb_layers = len(layers)
        self.layers = layers
        self.optimizer = optimizer


    def create_set(self, network):
        self.network = network


    def train(self, environment, memory):
        self.accuracy = self.train_and_score(environment, memory)
        self.print_network()


    def print_network(self):
        logging.info("{} - {}" .format(self.layers, self.optimizer))
        logging.info("Network score: {}" .format(self.accuracy))


    def compile_model(self, input_shape, output_shape):
        model = Sequential()

        model.add(Dense(self.layers[0][0], activation=self.layers[0][1], input_shape=input_shape))
        for i in range(self.nb_layers-1):
            model.add(Dense(self.layers[i][0], activation=self.layers[i][1]))

        model.add(Dense(output_shape, activation="linear"))
        model.compile(loss="MSE", optimizer=self.optimizer, metrics=['accuracy'])

        return model


    def train_and_score(self, environment, memory, epochs=500):
        env = gym.make(environment)
        output_shape = env.action_space.n
        input_shape = env.observation_space.shape

        model = self.compile_model(input_shape, output_shape)
        memory = copy.deepcopy(memory)
        score = train(environment, model, memory, epochs)

        return score
