import numpy as np
import cv2
import cvui
import time
from timeit import default_timer as timer

WINDOW_NAME = 'Speed of Light Measurement'

class ReactionTimeDistribuion():
    def __init__(self):
        x = np.array([100, 120, 130, 140, 150, 160, 180, 200, 220, 240, 260, 280,
                      300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500])
        y = np.array([0, 8, 60, 100, 200, 600, 10000, 25000, 40000, 55000, 60000, 50000, 40000,
                      33000, 26000, 20000, 15000, 11000, 9000, 7500, 6200, 4800, 0])
        arr = np.arange(np.amin(x), np.amax(x), 0.01)
        self.distribution = interpolate.CubicSpline(x, y)

    def get_prob(self):
        while True:
            x = 100+(500-100)*np.random.rand(1,1)[0][0]
            y = 60344*np.random.rand(1,1)[0][0]
            if self.distribution(x) > y:
                return x

class State():
    def __init__(self):
        self.curr_expr = 0
        self.experiments = [[False] for i in range(6)]
        self.animation = 0
        self.animate = False
        self.sleep = 0.2
        self.galileo_coord_bottom = 385
        self.galileo_coord_top = 985
        self.distance = [0.2]

def exp_type(curr_expr, experiments):
    for i, item in enumerate(experiments):
        if item[0] and curr_expr!=i:
            return i

    return curr_expr


def main():
    # load sprites
    galileo_default = cv2.imread("galileo_default.png", 1)
    galileo_default_dot = cv2.imread("galileo_default_dot.png", 1)
    galileo_yellow_dot = cv2.imread("galileo_yellow_dot.png", 1)
    galileo_fire = cv2.imread("galileo_fire.png", 1)

    state = State()

    frame = np.zeros((720, 1280, 3), np.uint8)
    cvui.init(WINDOW_NAME)

    while (True):
        start_time = timer()
        frame[:] = (49, 52, 49)

        if state.experiments[0][0]:
            cvui.image(frame, 0, 0, galileo_default)

            if state.animate:
                state.galileo_coord_bottom = 368
                state.galileo_coord_top = 968
                cvui.image(frame, 314, 393, galileo_fire)
                if state.animation < 21:
                    for _ in range(state.animation+1):
                        cvui.image(frame, state.galileo_coord_bottom, 400, galileo_yellow_dot)
                        state.galileo_coord_bottom = state.galileo_coord_bottom + 30
                else:
                    for _ in range(21):
                        cvui.image(frame, state.galileo_coord_bottom, 400, galileo_yellow_dot)
                        state.galileo_coord_bottom = state.galileo_coord_bottom + 30

                if state.animation >= 21 and state.animation < 42 :
                    cvui.image(frame, 1036, 390, galileo_fire)
                    for _ in range(state.animation+1-21):
                        cvui.image(frame, state.galileo_coord_top, 375, galileo_yellow_dot)
                        state.galileo_coord_top = state.galileo_coord_top - 30
                elif state.animation == 42:
                    cvui.image(frame, 1036, 390, galileo_fire)
                    for _ in range(21):
                        cvui.image(frame, state.galileo_coord_top, 375, galileo_yellow_dot)
                        state.galileo_coord_top = state.galileo_coord_top - 30

                if state.animation < 42:
                    state.animation += 1

                cvui.text(frame, 1079, 278, "250 ms", 0.4);
                cvui.text(frame, 248, 285, "250 ms", 0.4);
                cvui.text(frame, 660, 343, "250 ms", 0.5);

            cvui.window(frame, 1000, 2, 277.5, 212, 'Experiment settings')

            cvui.trackbar(frame,  1010, 50, 260, state.distance, 0.1, 10.0);
            cvui.rect(frame, 1010, 85, 260, 25, 0x313431, 0x313431);
            if cvui.button(frame, 1010, 90, "Execute"):
                state.animate = True
            cvui.text(frame, 1010, 30, "Distance")

        cvui.window(frame, 2, 2, 155, 212, 'Experiments')

        cvui.checkbox(frame, 10,  30, "1638 - Galileo",   state.experiments[0])
        cvui.checkbox(frame, 10,  53, "1676 - Roemer",    state.experiments[1])
        cvui.checkbox(frame, 10,  76, "1729 - Bradley",   state.experiments[2])
        cvui.checkbox(frame, 10,  99, "1849 - Fizeau",    state.experiments[3])
        cvui.checkbox(frame, 10, 122, "1862 - Foucalt",   state.experiments[4])
        cvui.checkbox(frame, 10, 145, "1879 - Michelson", state.experiments[4])

        state.curr_expr = exp_type(state.curr_expr, state.experiments)
        state.experiments = [[False] for i in range(6)]
        state.experiments[state.curr_expr] = [True]

        cvui.update()

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(20) == 27:
            break
        
if __name__ == '__main__':
    main()
