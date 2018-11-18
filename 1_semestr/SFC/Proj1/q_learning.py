import random
from collections import deque

import keras
import numpy as np
from mockup import neural_network
from keras.models import Model
from keras.layers import Input, Conv2D, Flatten, Dense, Concatenate, Lambda, Subtract, Add
from keras import optimizers, losses

from environment import FrozenLake

def train(model, memory, minibatch_size, gamma):
    if minibatch_size > len(memory):
        return
    minibatch = random.sample(list(memory), minibatch_size)

    state = np.array([i[0] for i in minibatch])
    action = [i[1] for i in minibatch]
    reward = [i[2] for i in minibatch]
    next_state = np.array([i[3] for i in minibatch])
    done = [i[4] for i in minibatch]

    q_value = model.predict(np.array(state))
    ns_model_pred = model.predict(np.array(next_state))

    for i in range(0, minibatch_size):
        if done[i] == 1:
            q_value[i][action[i]] = reward[i]
        else:
            q_value[i][action[i]] = reward[i] + gamma * np.max(ns_model_pred[i])

    model.fit(state, q_value)


def get_q_values(model):
    all_states = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

    return model.predict(np.array(all_states))


def fill_memory(env, memory):
    for eps in range(10000):
        state = env.reset()
        last_position = env.position

        already = np.empty((0,16))
        already = np.append(already, np.array([state]), axis=0)

        done = False
        for _ in range(100):
            action = np.random.randint(0, 4, size=1)[0]
            next_state, reward, done = env.step(action)

            for i, item in enumerate(already):
                flag = True
                for e, elem in enumerate(next_state):
                    if item[e] != elem:
                        flag = False
                        break
                if flag:
                    reward -= 0.1
                break

            already = np.append(already, np.array([next_state]), axis=0)

            if last_position == env.position:
                reward = -0.1

            memory.append((state, action, reward, next_state, done))

            state = next_state
            last_position = env.position

            if done:
                if len(memory) == 1000:
                    return memory
                break
    return memory


def test(env, eps, epsilon, model):
    state = env.reset()
    done = False
    for step in range(100):
        action = np.argmax(model.predict(np.array([state])))
        next_state, reward, done = env.step(action)
        state = next_state
        if done:
            if reward == 1:
                print(eps, epsilon, "WIN", step+1)
            else:
                print(eps, epsilon, "LOSS", step+1)
            return


def main():
    env = FrozenLake()
    model = neural_network(16, 16, 4, 0.01)
    memory = deque(maxlen=1000)
    memory = fill_memory(env, memory)
    epsilon = 1

    for eps in range(10000):
        state = env.reset()
        last_position = env.position

        already = np.empty((0,16))
        already = np.append(already, np.array([state]), axis=0)

        done = False
        for _ in range(100):
            #env.render_wQ(get_q_values(model))
            if np.random.rand() > epsilon:
                action = np.argmax(model.predict(np.array([state])))
            else:
                action = np.random.randint(0, 4, size=1)[0]

            next_state, reward, done = env.step(action)
            
            for i, item in enumerate(already):
                flag = True
                for e, elem in enumerate(next_state):
                    if item[e] != elem:
                        flag = False
                        break
                if flag:
                    reward -= 0.1
                break

            already = np.append(already, np.array([next_state]), axis=0)

            if epsilon > 0.1:
                epsilon -= 0.00005

            if last_position == env.position:
                reward -= 0.1

            memory.append((state, action, reward, next_state, done))
            train(model, memory, 64, 0.9)

            state = next_state
            last_position = env.position

            if done:
                test(env, eps, epsilon, model)
                break


if __name__ == "__main__":
    main()
