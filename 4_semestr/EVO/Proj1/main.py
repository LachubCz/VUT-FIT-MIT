import os
import json
import logging
logging.basicConfig(filename=os.path.join(os.getcwd(), 'records.log'), level=logging.DEBUG)
import argparse

from generator import Generator
from dqn import fill_memory

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--nn-parameters", action="store", dest="nn_parameters", default="./nn_parameters.json",
                        help="parameters of neural network")
    parser.add_argument("--generations", action="store", dest="generations", default=10,
                        help="number of generations")
    parser.add_argument("--population", action="store", dest="population", default=20,
                        help="population size")
    parser.add_argument("--environment", action="store", dest="environment", default='CartPole-v0',
                        help="name of environment")

    args = parser.parse_args()

    return args


def print_networks(networks):
    for network in networks:
        network.print_network()


def evolve(nn_parameters, generations, population, environment):
    generator = Generator(nn_parameters)
    networks = generator.create_random_population(population)

    memory = fill_memory(environment)

    for i in range(generations):
        logging.info("***Doing generation {} of {}" .format(i + 1, generations))

        total_accuracy = 0
        for network in networks:
            network.train(environment, memory)
            total_accuracy += network.accuracy

        logging.info("Generation average: {}" .format((total_accuracy / len(networks)) * 100))

        if i != generations - 1:
            networks = generator.evolve(networks)

    networks = sorted(networks, key=lambda x: x.accuracy)

    print_networks(networks[:5])


def main():
    args = get_args()
    nn_parameters = args.nn_parameters
    generations = args.generations
    population = args.population
    environment = args.environment

    with open(nn_parameters) as json_file:
        nn_params = json.load(json_file)

    logging.info("***Evolving {} generations with population {}" .format(generations, population))

    evolve(nn_params, generations, population, environment)


if __name__ == '__main__':
    main()
