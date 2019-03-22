from collections import deque

import cv2
import cvui
from timeit import default_timer as timer

from tools import exp_type, overlay_image_alpha


def get_60(fizeau_default, fizeau_sprocket):
    array = deque([])
    (h, w) = fizeau_sprocket.shape[:2]
    center = (w / 2, h / 2)

    for e in range(4):
        for i in range(15):
            M = cv2.getRotationMatrix2D(center, 2*i, 1.0)
            temp = cv2.warpAffine(fizeau_sprocket, M, (h, w))
            blank = fizeau_default.copy()
            overlay_image_alpha(blank, temp[:, :, 0:3], (795, 495), temp[:, :, 3] / 255.0)
            array.append(blank)

    return array


def put_line(sprites, fizeau_dot):
    x = 153
    x_lenght = 1007 + 639 + 249 #63.1
    y = 495
    x_right = 1160
    shift = 521

    y_high = 249
    for i, item in enumerate(sprites):
        if i < 30:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x+i*32.67), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i == 30:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (x_right, y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i > 32 and i < 50:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x_right-(i-30)*32.67), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i > 48 and i < 58:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (shift, int(y-(i-50)*32.67)), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i == 58:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (shift, y_high), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
    return sprites


def fizeau(frame, expr):
    curr_expr = expr
    experiments = [[False] for i in range(4)]

    fizeau_default = cv2.imread("images/fizeau_default.png", 1)
    fizeau_line = cv2.imread("images/fizeau_line.png", 1)
    fizeau_dot = cv2.imread("images/fizeau_dot.png", cv2.IMREAD_UNCHANGED)
    fizeau_sprocket = cv2.imread("images/fizeau_sprocket.png", cv2.IMREAD_UNCHANGED)
    wheel_sprites = get_60(fizeau_default, fizeau_sprocket)
    wheel_sprites = put_line(wheel_sprites, fizeau_dot)
    wheel_sprites.rotate(15)
    wheel_sprites = put_line(wheel_sprites, fizeau_dot)
    wheel_sprites.rotate(15)
    wheel_sprites = put_line(wheel_sprites, fizeau_dot)
    wheel_sprites.rotate(15)
    wheel_sprites = put_line(wheel_sprites, fizeau_dot)
    
    animation = 0
    frequency_tr = [1.1]

    while (True):
        frame[:] = (49,52,49)
        #Animation window
        cvui.image(frame, 0, 0, wheel_sprites[animation])
        cvui.image(frame, 872, 499, fizeau_line)
        animation += 1
        if animation == 60:
            animation = 0

        #cvui.image(frame, 400, 400, fizeau_sprocket)
        cvui.window(frame, 2, 2, 155, 121, 'Experiments')

        cvui.checkbox(frame, 10, 30, "1638 - Galileo",   experiments[0])
        cvui.checkbox(frame, 10, 53, "1676 - Roemer",    experiments[1])
        cvui.checkbox(frame, 10, 76, "1849 - Fizeau",    experiments[2])
        cvui.checkbox(frame, 10, 99, "1879 - Michelson", experiments[3])

        #Experiment settings window
        cvui.window(frame, 1033.5, 2, 243.5, 133, 'Experiment settings')
        
        cvui.trackbar(frame,  1030, 39, 249, frequency_tr, 1.1, 10.0)
        cvui.rect(frame, 1035, 39, 240, 12, 0x313131, 0x313131)
        cvui.rect(frame, 1035, 74, 240, 25, 0x313131, 0x313131)
        cvui.text(frame, 1041, 32, "Frequency")
        cvui.text(frame, 1042, 82, "{:,} Hz".format(round((frequency_tr[0])**8, 0)))


        curr_expr = exp_type(curr_expr, experiments)
        experiments = [[False] for i in range(4)]
        experiments[curr_expr] = [True]

        cvui.update()

        cv2.imshow('Speed of Light Measurement', frame)

        if cv2.waitKey(20) == 27:
            return -1

        if curr_expr != expr:
            return curr_expr
