import time
import random
import numpy as np


from model import neural_network
from environment import FrozenLake
from helper import get_q_values, err_print

















def test_main(model_name):
    """
    main for testing mode
    """
    env = FrozenLake()
    model = neural_network(16, 16, 4, 0.01)
    model.load_model(model_name)

    env.render_wQ(get_q_values(model))
    state = env.reset()
    env.render()
    done = False
    for step in range(100):
        time.sleep(0.5)
        action = np.argmax(model.predict(np.array([state])))
        next_state, reward, done = env.step(action)
        state = next_state
        env.render()
        if done:
            break


