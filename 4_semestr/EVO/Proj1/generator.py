"""
Class that holds a genetic algorithm for evolving a network.
"""
import numpy as np
from functools import reduce
from operator import add
import random
from network import Network

class Generator():
    """Class that implements genetic algorithm for MLP optimization."""
    def __init__(self, nn_param, count=20, retain=0.4, random_select=0.1, mutate_chance=0.2):
        """Create an optimizer.

        Args:
            nn_param_choices (dict): Possible network paremters
            retain (float): Percentage of population to retain after
                each generation
            random_select (float): Probability of a rejected network
                remaining in the population
            mutate_chance (float): Probability a network will be
                randomly mutated

        """
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
        """Return the accuracy, which is our fitness function."""
        return network.accuracy


    def grade(self, pop):
        """Find average fitness for a population.

        Args:
            pop (list): The population of networks

        Returns:
            (float): The average accuracy of the population

        """
        summed = reduce(add, (self.fitness(network) for network in pop))
        return summed / float((len(pop)))


    def breed(self, mother, father):
        """Make two children as parts of their parents.

        Args:
            mother (dict): Network parameters
            father (dict): Network parameters

        Returns:
            (list): Two network objects
        """
        children = []
        for _ in range(2):
            child = {}

            networks = []

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

            # Now create a network object.
            network = Network(layers, optimizer)
            network.create_set(child)

            # Randomly mutate some of the children.
            #if self.mutate_chance > random.random():
            network = self.mutate(network)

            children.append(network)

        return children


    def mutate(self, network, change_nb_layers=0.3, change_layers=0.7, change=0.5):
        """Randomly mutate one part of the network.

        Args:
            network (dict): The network parameters to mutate

        Returns:
            (Network): A randomly mutated network object

        """
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
        """Evolve a population of networks.

        Args:
            pop (list): A list of network parameters

        Returns:
            (list): The evolved population of networks

        """
        # Get scores for each network.
        graded = [(self.fitness(network), network) for network in pop]

        # Sort on the scores.
        graded = [x[1] for x in sorted(graded, key=lambda x: x[0])]

        # Get the number we want to keep for the next gen.
        retain_length = int(len(graded)*self.retain)

        # The parents are every network we want to keep.
        parents = graded[:retain_length]

        # For those we aren't keeping, randomly keep some anyway.
        for individual in graded[retain_length:]:
            if self.random_select > random.random():
                parents.append(individual)

        # Now find out how many spots we have left to fill.
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []

        # Add children, which are bred from two remaining networks.
        while len(children) < desired_length:

            # Get a random mom and dad.
            male = random.randint(0, parents_length-1)
            female = random.randint(0, parents_length-1)

            # Assuming they aren't the same network...
            if male != female:
                male = parents[male]
                female = parents[female]

                # Breed them.
                babies = self.breed(male, female)

                # Add the children one at a time.
                for baby in babies:
                    # Don't grow larger than desired length.
                    if len(children) < desired_length:
                        children.append(baby)

        parents.extend(children)

        return parents
