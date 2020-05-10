import gym
import argparse

from dqn import train, fill_memory

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--environment", action="store", dest="environment", default='CartPole-v0',
                        help="name of environment")

    args = parser.parse_args()

    return args


def get_model(input_shape, output_shape):
    model = Sequential()

    model.add(Dense(16, activation='tanh', input_shape=input_shape))
    model.add(Dense(64, activation='elu'))
    model.add(Dense(16, activation='sigmoid'))

    model.add(Dense(output_shape, activation="linear"))
    model.compile(loss="MSE", optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model


if __name__ == '__main__':
    args = get_args()

    environment = args.environment
    env = gym.make(environment)

    output_shape = env.action_space.n
    input_shape = env.observation_space.shape

    epochs = 500
    memory = fill_memory(environment)
    model = get_model(input_shape, output_shape)

    score = train(environment, model, memory, epochs)
    print(score)
