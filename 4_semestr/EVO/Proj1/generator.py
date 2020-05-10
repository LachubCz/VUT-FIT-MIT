import os
import random
import logging
logging.basicConfig(filename=os.path.join(os.getcwd(), 'records.log'), level=logging.DEBUG)

import numpy as np
from functools import reduce
from operator import add

from network import Network

class Generator():
    def __init__(self, nn_param, retain=0.4, random_select=0.1, mutate_chance=0.2):
        self.mutate_chance = mutate_chance
        self.random_select = random_select
        self.retain = retain
        self.nn_param = nn_param


    def create_random_population(self, count):
        networks = []

        for _ in range(0, count):
            layers = []
            nb_layers = random.choice(self.nn_param["nb_layers"])

            for l in range(nb_layers):
                nb_neurons = random.choice(self.nn_param["nb_neurons"])
                activation = random.choice(self.nn_param["activation"])
                layers.append([nb_neurons, activation])

            optimizer = random.choice(self.nn_param["optimizer"])

            network = Network(layers, optimizer)
            networks.append(network)

        return networks


    @staticmethod
    def fitness(network):
        return network.accuracy


    def grade(self, pop):
        summed = reduce(add, (self.fitness(network) for network in pop))
        return summed / float((len(pop)))


    def breed(self, mother, father):
        children = []
        for _ in range(2):
            child = {}

            min_layers = min([mother.nb_layers, father.nb_layers])
            max_layers = max([mother.nb_layers, father.nb_layers])

            nb_layers = np.random.randint(min_layers, max_layers+1, size=(1))[0]

            layers = []
            for i in range(nb_layers):
                if i < mother.nb_layers and i < father.nb_layers:
                    layers.append(random.choice([mother.layers[i], father.layers[i]]))
                elif i < mother.nb_layers:
                    layers.append(random.choice([mother.layers[i], mother.layers[i]]))
                elif i < father.nb_layers:
                    layers.append(random.choice([father.layers[i], father.layers[i]]))

            optimizer = random.choice([mother.optimizer, father.optimizer])

            network = Network(layers, optimizer)
            network.create_set(child)

            if self.mutate_chance > random.random():
                network = self.mutate(network)

            children.append(network)

        return children


    def mutate(self, network, change_nb_layers=0.3, change_layers=0.7, change=0.5):
        if change_nb_layers > random.random():
            new_nb_layers = random.choice(self.nn_param["nb_layers"])
            if new_nb_layers > network.nb_layers and (network.nb_layers+1) <= max(self.nn_param["nb_layers"]):
                position = np.random.randint(0, max(self.nn_param["nb_layers"])+1, size=(1))[0]
                network.layers.insert(position, [random.choice(self.nn_param["nb_neurons"]), random.choice(self.nn_param["activation"])])
                network.nb_layers = len(network.layers)
            elif new_nb_layers < network.nb_layers and (network.nb_layers-1) >= min(self.nn_param["nb_layers"]):
                position = np.random.randint(0, network.nb_layers, size=(1))[0]
                del network.layers[position]
                network.nb_layers = len(network.layers)

        layers_for_change = []
        if change_layers > random.random():
            nb_layers = np.random.randint(0, network.nb_layers, size=(network.nb_layers))
            layers_for_change = set(nb_layers)

        for nb_layer in layers_for_change:
            if change > random.random():
                network.layers[nb_layer][0] = random.choice(self.nn_param["nb_neurons"])
            if change > random.random():
                network.layers[nb_layer][1] = random.choice(self.nn_param["activation"])

        return network


    def evolve(self, pop):
        graded = [(self.fitness(network), network) for network in pop]
        graded = [x[1] for x in sorted(graded, key=lambda x: x[0])]
        retain_length = int(len(graded)*self.retain)

        parents = graded[:retain_length]

        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents.append(individual)

        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []

        while len(children) < desired_length:
            male = random.randint(0, parents_length-1)
            female = random.randint(0, parents_length-1)

            if male != female:
                male = parents[male]
                female = parents[female]
                babies = self.breed(male, female)

                for baby in babies:
                    if len(children) < desired_length:
                        children.append(baby)

        parents.extend(children)

        return parents
