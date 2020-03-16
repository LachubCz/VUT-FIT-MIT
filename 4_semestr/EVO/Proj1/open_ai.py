import gym
import argparse
import numpy as np
from collections import deque


from helper import err_print

def get_args():
    """
    method parses arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--mode", action="store", dest="mode",
                        choices=["train", "showcase"], default="train",
                        help="application mode")
    parser.add_argument("--render", action="store_true", dest="render",
                        help="flag for rendering")
    parser.add_argument("--model", action="store", dest="model",
                        help="name of file which contains already trained model")
    parser.add_argument("--environment", action="store", dest="environment",
                        choices=["CartPole-v0", "CartPole-v0"], default="train",
                        help="name of environment")
    args = parser.parse_args()

    #if args.mode == "test" and args.model == None:
    #    err_print("Model was not selected.")
    #    exit(-1)

    return args

def train(args):
    pass

def showcase(args):
    env = gym.make(args.environment)
    observation = env.reset()
    for _ in range(100000):
      env.render()
      action = env.action_space.sample() # your agent here (this takes random actions)
      observation, reward, done, info = env.step(action)

      if done:
        observation = env.reset()
    env.close()


def fill_memory(env, memory):
    """
    method fills memory before learning
    """
    for eps in range(10000):
        state = env.reset()
        last_position = env.position

        already = np.empty((0, 16))
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
                reward -= 0.1

            memory.append((state, action, reward, next_state, done))

            state = next_state
            last_position = env.position

            if done:
                if len(memory) == 1000:
                    return memory
                break
    return memory


def dqn(model, memory, minibatch_size, gamma):
    """
    method performs q-learning
    """
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


def test(env, eps, epsilon, model, r_mode):
    """
    method tests succes of neural network
    """
    state = env.reset()
    done = False
    for step in range(100):
        action = np.argmax(model.predict(np.array([state])))
        next_state, reward, done = env.step(action)
        state = next_state
        if done:
            if reward == 1:
                if r_mode == "stats":
                    print("Episode: {}; Epsilon: {:.2}; Test outcome: {} in {} moves".format(eps, epsilon, "WIN",
                                                                                             step + 1))
                return True
            else:
                if r_mode == "stats":
                    print("Episode: {}; Epsilon: {:.2}; Test outcome: {} in {} moves".format(eps, epsilon, "LOSS",
                                                                                             step + 1))
                return False
    if r_mode == "stats":
        print("Episode: {}; Epsilon: {:.2}; Test outcome: {}".format(eps, epsilon, "CYCLE"))
    return False


def train(args):
    """
    main for training mode
    """
    env = gym.make(args.environment)
    model = neural_network(16, 16, 4, 0.01)
    memory = deque(maxlen=1000)
    memory = fill_memory(env, memory)
    epsilon = 1

    for eps in range(10000):
        state = env.reset()
        last_position = env.position

        already = np.empty((0, 16))
        already = np.append(already, np.array([state]), axis=0)

        done = False

        for _ in range(100):
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
                epsilon -= 0.001

            if last_position == env.position:
                reward -= 0.1

            memory.append((state, action, reward, next_state, done))
            dqn(model, memory, 64, 0.9)

            state = next_state
            last_position = env.position

            if done:
                if test(env, eps, epsilon, model, r_mode):
                    model.save_model("model")
                    print("[SUCCESSFUL RUN]")
                    return
                break



if __name__ == "__main__":
    args = get_args()
    if args.mode == "train":
        train(args)
    elif args.mode == "showcase":
        showcase(args)
