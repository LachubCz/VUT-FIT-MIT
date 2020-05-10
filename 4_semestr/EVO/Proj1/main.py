import os
import json
import logging
logging.basicConfig(filename=os.path.join(os.getcwd(), 'ga.log'), level=logging.DEBUG)
import argparse

from generator import Generator
from dqn import fill_memory

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--nn-parameters", action="store", dest="nn_parameters", default="./nn_parameters.json",
                        help="parameters of neural network")

    args = parser.parse_args()

    return args


def print_networks(networks):
    for network in networks:
        network.print_network()


def evolve(args, generations, population):
    """Generate a network with the genetic algorithm.

    Args:
        generations (int): Number of times to evole the population
        population (int): Number of networks in each generation
        nn_param_choices (dict): Parameter choices for networks
        dataset (str): Dataset to use for training/evaluating

    """
    with open(args.nn_parameters) as json_file:
        nn_param = json.load(json_file)

    generator = Generator(nn_param)
    networks = generator.create_random_population(population)

    memory = fill_memory()

    # Evolve the generation.
    for i in range(generations):
        logging.info("***Doing generation {} of {}" .format(i + 1, generations))

        # Train and get accuracy for networks. Get the average accuracy for this generation.
        total_accuracy = 0
        for network in networks:
            network.train(memory)
            total_accuracy += network.accuracy

        # Print out the average accuracy each generation.
        logging.info("Generation average: {}" .format((total_accuracy / len(networks)) * 100))

        # Evolve, except on the last iteration.
        if i != generations - 1:
            # Do the evolution.
            networks = generator.evolve(networks)

    # Sort our final population.
    networks = sorted(networks, key=lambda x: x.accuracy, reverse=True)

    # Print out the top 5 networks.
    print_networks(networks[:5])


def main():
    """Evolve a network."""
    generations = 10  # Number of times to evole the population.
    population = 20  # Number of networks in each generation.

    logging.info("***Evolving {} generations with population {}" .format(generations, population))

    args = get_args()

    evolve(args, generations, population)


if __name__ == '__main__':
    main()
