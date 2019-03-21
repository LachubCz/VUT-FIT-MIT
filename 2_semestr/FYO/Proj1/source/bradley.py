import cv2
import cvui
import tools

def bradley(frame):
    curr_expr = 0
    experiments = [[False] for i in range(6)]

    animation = 0
    animate = False
    galileo_coord_bottom = 385
    galileo_coord_top = 985
    distance = [0.2]

    while (True):
        galileo_default = cv2.imread("images/galileo_default.png", 1)
        galileo_yellow_dot = cv2.imread("images/galileo_yellow_dot.png", 1)
        galileo_fire = cv2.imread("images/galileo_fire.png", 1)

        cvui.image(frame, 0, 0, galileo_default)

        if animate:
            galileo_coord_bottom = 368
            galileo_coord_top = 968
            cvui.image(frame, 314, 393, galileo_fire)
            if animation < 21:
                for _ in range(animation+1):
                    cvui.image(frame, galileo_coord_bottom, 400, galileo_yellow_dot)
                    galileo_coord_bottom = galileo_coord_bottom + 30
            else:
                for _ in range(21):
                    cvui.image(frame, galileo_coord_bottom, 400, galileo_yellow_dot)
                    galileo_coord_bottom = galileo_coord_bottom + 30

            if animation >= 21 and animation < 42 :
                cvui.image(frame, 1036, 390, galileo_fire)
                for _ in range(animation+1-21):
                    cvui.image(frame, galileo_coord_top, 375, galileo_yellow_dot)
                    galileo_coord_top = galileo_coord_top - 30
            elif animation == 42:
                cvui.image(frame, 1036, 390, galileo_fire)
                for _ in range(21):
                    cvui.image(frame, galileo_coord_top, 375, galileo_yellow_dot)
                    galileo_coord_top = galileo_coord_top - 30

            if animation < 42:
                animation += 1

            cvui.text(frame, 1079, 278, "250 ms", 0.4);
            cvui.text(frame, 248, 285, "250 ms", 0.4);
            cvui.text(frame, 660, 343, "250 ms", 0.5);

        cvui.window(frame, 1000, 2, 277.5, 212, 'Experiment settings')

        cvui.trackbar(frame,  1010, 50, 260, distance, 0.1, 10.0);
        cvui.rect(frame, 1010, 85, 260, 25, 0x313431, 0x313431);
        if cvui.button(frame, 1010, 90, "Execute"):
            animate = True
        cvui.text(frame, 1010, 30, "Distance")

    cvui.window(frame, 2, 2, 155, 165, 'Experiments')

    cvui.checkbox(frame, 10,  30, "1638 - Galileo",   experiments[0])
    cvui.checkbox(frame, 10,  53, "1676 - Roemer",    experiments[1])
    cvui.checkbox(frame, 10,  76, "1729 - Bradley",   experiments[2])
    cvui.checkbox(frame, 10,  99, "1849 - Fizeau",    experiments[3])
    cvui.checkbox(frame, 10, 122, "1862 - Foucalt",   experiments[4])
    cvui.checkbox(frame, 10, 145, "1879 - Michelson", experiments[5])

    curr_expr = exp_type(curr_expr, experiments)
    experiments = [[False] for i in range(6)]
    experiments[curr_expr] = [True]

    cvui.update()

    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(20) == 27:
        return -1

    if curr_expr != 0:
        return curr_expr