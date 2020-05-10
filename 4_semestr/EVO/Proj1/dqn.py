import gym
import random
import numpy as np

from collections import deque

def fill_memory(environment):
    env = gym.make(environment)
    memory = deque(maxlen=1000)
    while True:
        state = env.reset()

        for _ in range(100):
            action = np.random.randint(0, env.action_space.n, size=1)[0]
            next_state, reward, done, _ = env.step(action)
            memory.append((state, action, reward, next_state, done))
            state = next_state

            if done:
                if len(memory) == 1000:
                    return memory
                break


def dqn(model, memory, minibatch_size, gamma):
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

    model.fit(state, q_value, verbose=0)


def test(environment, model):
    env = gym.make(environment)

    score = 0
    for game in range(100):
        state = env.reset()
        while True:
            action = np.argmax(model.predict(np.array([state])))
            next_state, reward, done, _ = env.step(action)
            score += reward
            state = next_state
            if done:
                break

        if game == 9 and score/10 < 195 and environment == 'CartPole-v0':
            return False
        if game == 9 and score/10 < -110 and environment == 'MountainCar-v0':
            return False

    if environment == 'CartPole-v0':
        if (score/100) >= 195:
            return True
        else:
            return False
    elif environment == 'MountainCar-v0':
        if (score/100) >= -110:
            return True
        else:
            return False


def train(environment, model, memory, episodes):
    env = gym.make(environment)
    epsilon = 1

    for eps in range(episodes):
        state = env.reset()

        while True:
            if np.random.rand() > epsilon:
                action = np.argmax(model.predict(np.array([state])))
            else:
                action = np.random.randint(0, env.action_space.n, size=1)[0]

            next_state, reward, done, _ = env.step(action)

            if epsilon > 0.1:
                epsilon -= 0.001

            memory.append((state, action, reward, next_state, done))
            dqn(model, memory, 16, 0.9)

            state = next_state

            if done:
                if test(environment, model):
                    return eps
                break

    return episodes
