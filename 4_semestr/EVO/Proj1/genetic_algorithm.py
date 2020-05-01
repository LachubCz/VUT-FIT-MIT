import json
import argparse
import tensorflow as tf

from keras.backend.tensorflow_backend import set_session
from keras import backend as K

from generator import Generator

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--nn-parameters", action="store", dest="nn_parameters", default="./nn_parameters.json",
                        help="parameters of neural network")

    args = parser.parse_args()

    return args


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

    # Evolve the generation.
    for i in range(generations):
        print("***Doing generation {} of {}" .format(i + 1, generations))

        # Train and get accuracy for networks. Get the average accuracy for this generation.
        total_accuracy = 0
        for network in networks:
            network.train()
            total_accuracy += network.accuracy

        # Print out the average accuracy each generation.
        print("Generation average: {}" .format((total_accuracy / len(networks)) * 100))

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

    print("***Evolving {} generations with population {}" .format(generations, population))

    config = tf.ConfigProto(
        intra_op_parallelism_threads=1,
        inter_op_parallelism_threads=1)
    set_session(tf.Session(config=config))

    args = get_args()

    evolve(args, generations, population)

    K.clear_session()


if __name__ == '__main__':
    main()
