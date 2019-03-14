import numpy as np
import cv2
import cvui
import time

WINDOW_NAME = 'Speed of Light Measurement'

class State():
    def __init__(self):
        self.curr_expr = 0
        self.experiments = [[False] for i in range(8)]
        self.animation = 0
        self.animate = False
        self.sleep = 0.2
        self.galileo_coord = 387

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
        frame[:] = (49, 52, 49)

        if state.experiments[0][0]:
            cvui.image(frame, 0, 0, galileo_default)
            

            if state.animate:
                state.galileo_coord = 387
                for _ in range(state.animation+1):
                    cvui.image(frame, 314, 393, galileo_fire)
                    cvui.image(frame, state.galileo_coord, 370, galileo_yellow_dot)
                    state.galileo_coord = state.galileo_coord + 30
                if state.animation < 20:
                    state.animation += 1

            #if state.animation == 21:
            #    state.animate = False

            if cvui.button(frame, 150, 600, "Animate"):
                state.animate = True


        cvui.window(frame, 2, 2, 155, 212, 'Experiments')

        cvui.checkbox(frame, 10,  30, "1600 - Galileo",   state.experiments[0])
        cvui.checkbox(frame, 10,  53, "1676 - Roemer",    state.experiments[1])
        cvui.checkbox(frame, 10,  76, "1729 - Bradley",   state.experiments[2])
        cvui.checkbox(frame, 10,  99, "1849 - Fizeau",    state.experiments[3])
        cvui.checkbox(frame, 10, 122, "1879 - Michelson", state.experiments[4])
        cvui.checkbox(frame, 10, 145, "1950 - Essen",     state.experiments[5])
        cvui.checkbox(frame, 10, 168, "1958 - Froome",    state.experiments[6])
        cvui.checkbox(frame, 10, 191, "1972 - Evenson",   state.experiments[7])

        state.curr_expr = exp_type(state.curr_expr, state.experiments)
        state.experiments = [[False] for i in range(8)]
        state.experiments[state.curr_expr] = [True]

        cvui.update()

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(20) == 27:
            break

if __name__ == '__main__':
    main()
