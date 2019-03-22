import cv2
import cvui

from tools import exp_type

def roemer(frame, expr):
    curr_expr = expr
    experiments = [[False] for i in range(4)]

    while (True):
        frame[:] = (49,52,49)

        cvui.window(frame, 2, 2, 155, 121, 'Experiments')

        cvui.checkbox(frame, 10, 30, "1638 - Galileo",   experiments[0])
        cvui.checkbox(frame, 10, 53, "1676 - Roemer",    experiments[1])
        cvui.checkbox(frame, 10, 76, "1849 - Fizeau",    experiments[2])
        cvui.checkbox(frame, 10, 99, "1879 - Michelson", experiments[3])

        curr_expr = exp_type(curr_expr, experiments)
        experiments = [[False] for i in range(4)]
        experiments[curr_expr] = [True]

        cvui.update()

        cv2.imshow('Speed of Light Measurement', frame)

        if cv2.waitKey(20) == 27:
            return -1

        if curr_expr != expr:
            return curr_expr
