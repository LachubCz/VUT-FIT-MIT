from collections import deque

import cv2
import cvui

from tools import exp_type, overlay_image_alpha, resource_path


def get_120(fizeau_default, fizeau_sprocket):
    array = deque([])
    (h, w) = fizeau_sprocket.shape[:2]
    center = (w / 2, h / 2)

    for e in range(8):
        for i in range(15):
            M = cv2.getRotationMatrix2D(center, 2*i, 1.0)
            temp = cv2.warpAffine(fizeau_sprocket, M, (h, w))
            blank = fizeau_default.copy()
            overlay_image_alpha(blank, temp[:, :, 0:3], (795, 495), temp[:, :, 3] / 255.0)
            array.append(blank)

    return array


def put_dots_pos(sprites, fizeau_dot, fizeau_dot_grey):
    x = 153
    x_lenght = 1007 + 639 + 249
    y = 495
    x_right = 1160
    shift = 521

    for i, item in enumerate(sprites):
        if i < 62:
            if i in [18,19,20,21,22]:
                overlay_image_alpha(item, fizeau_dot_grey[:, :, 0:3], (int(x+i*16.335), y), fizeau_dot_grey[:, :, 3] / 255.0)
            else:
                overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x+i*16.335), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i == 62:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (x_right, y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i > 62 and i < 102:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x_right-(i-62)*16.335), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i > 101 and i < 118:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (shift, int(y-(i-102)*16.335)), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item

    return sprites


def put_dots_neg(sprites, fizeau_dot, fizeau_dot_grey):
    x = 153
    x_lenght = 1007 + 639 + 249
    y = 495
    x_right = 1160
    shift = 521

    for i, item in enumerate(sprites):
        if i < 62:
            if i in [18,19,20,21,22]:
                overlay_image_alpha(item, fizeau_dot_grey[:, :, 0:3], (int(x+i*16.335), y), fizeau_dot_grey[:, :, 3] / 255.0)
            else:
                overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x+i*16.335), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i == 62:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (x_right, y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item
        elif i > 62 and i < 80:
            overlay_image_alpha(item, fizeau_dot[:, :, 0:3], (int(x_right-(i-62)*16.335), y), fizeau_dot[:, :, 3] / 255.0)
            sprites[i] = item

    return sprites


def get_graph(fizeau_metre, fizeau_blank, fizeau_darkstripes, fizeau_lightstripes, coord=0, crop_light=False):
    temp = fizeau_blank.copy()
    overlay_image_alpha(temp, fizeau_lightstripes[:, :, 0:3], (coord, 0), fizeau_lightstripes[:, :, 3] / 255.0)
    if crop_light:
        overlay_image_alpha(temp, fizeau_darkstripes[:, :, 0:3], (0, 0), fizeau_darkstripes[:, :, 3] / 255.0)
    overlay_image_alpha(temp, fizeau_metre[:, :, 0:3], (0, 0), fizeau_metre[:, :, 3] / 255.0)
    temp = temp[0:63, 0:190]

    return temp


def get_coord(frequency):
    N = 720.0
    f = frequency
    max_f = 12.0577
    D = 8633.0
    tau = 1 / (2 * N * f)
    tau_max = 1 / (2 * N * max_f)
    diff = tau_max / tau

    return int(23 * diff)


def fizeau(frame, expr):
    curr_expr = expr
    experiments = [[False] for i in range(2)]

    fizeau_default = cv2.imread(resource_path("images/fizeau_default.png"), 3)
    fizeau_not_default = cv2.imread(resource_path("images/fizeau_not_default.png"), 3)
    fizeau_line = cv2.imread(resource_path("images/fizeau_line.png"), 3)
    fizeau_distance = cv2.imread(resource_path("images/fizeau_distance.png"), 3)
    fizeau_dot = cv2.imread(resource_path("images/fizeau_dot.png"), cv2.IMREAD_UNCHANGED)
    fizeau_dot_grey = cv2.imread(resource_path("images/fizeau_dot_grey.png"), cv2.IMREAD_UNCHANGED)
    fizeau_sprocket = cv2.imread(resource_path("images/fizeau_sprocket.png"), cv2.IMREAD_UNCHANGED)
    fizeau_metre = cv2.imread(resource_path("images/fizeau_metre.png"), cv2.IMREAD_UNCHANGED)
    fizeau_blank = cv2.imread(resource_path("images/fizeau_blank.png"), cv2.IMREAD_UNCHANGED)
    fizeau_darkstripes = cv2.imread(resource_path("images/fizeau_darkstripes.png"), cv2.IMREAD_UNCHANGED)
    fizeau_lightstripes = cv2.imread(resource_path("images/fizeau_lightstripes.png"), cv2.IMREAD_UNCHANGED)

    wheel_sprites_pos = get_120(fizeau_default, fizeau_sprocket)
    wheel_sprites_pos = put_dots_pos(wheel_sprites_pos, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_pos.rotate(30)
    wheel_sprites_pos = put_dots_pos(wheel_sprites_pos, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_pos.rotate(30)
    wheel_sprites_pos = put_dots_pos(wheel_sprites_pos, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_pos.rotate(30)
    wheel_sprites_pos = put_dots_pos(wheel_sprites_pos, fizeau_dot, fizeau_dot_grey)

    wheel_sprites_neg = get_120(fizeau_not_default, fizeau_sprocket)
    wheel_sprites_neg = put_dots_neg(wheel_sprites_neg, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_neg.rotate(30)
    wheel_sprites_neg = put_dots_neg(wheel_sprites_neg, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_neg.rotate(30)
    wheel_sprites_neg = put_dots_neg(wheel_sprites_neg, fizeau_dot, fizeau_dot_grey)
    wheel_sprites_neg.rotate(30)
    wheel_sprites_neg = put_dots_neg(wheel_sprites_neg, fizeau_dot, fizeau_dot_grey)

    animation = 0
    frequency_tr = [6.0]

    while (True):
        frame[:] = (49,52,49)

        #Animation window
        coord = get_coord(frequency_tr[0])
        if coord == 23:
            cvui.image(frame, 0, 0, wheel_sprites_neg[animation])
            cvui.text(frame, 33, 200, "Calculation of the speed of light", 0.5)
            cvui.text(frame, 34, 220, "distance ... s = {:,} m" .format(8633), 0.5)
            cvui.text(frame, 34, 240, "number of teeth in sprocket ... N = 720", 0.5)
            cvui.text(frame, 34, 260, "c=4*s*N*f=4*{:,}*{:,}*{:,}={:,} km/s"
                .format(8633, 7200, round(frequency_tr[0], 2), round((4 * 8633 * 7200 * frequency_tr[0])/1000, 2)), 0.5)
        else:
            cvui.image(frame, 0, 0, wheel_sprites_pos[animation])
            cvui.text(frame, 33, 200, "Calculation of the speed of light", 0.5)
            cvui.text(frame, 34, 220, "distance ... s = {:,} m" .format(8633), 0.5)
            cvui.text(frame, 34, 240, "number of teeth in sprocket ... N = 720", 0.5)
            cvui.text(frame, 34, 260, "c=4*s*N*f ... proper frequency wasn't found", 0.5)
        cvui.image(frame, 872, 499, fizeau_line)

        cvui.image(frame, 874, 687, fizeau_distance)
        animation += 1
        if animation == 120:
            animation = 0

        cvui.text(frame,   58, 660, "Light source")
        cvui.text(frame,  473, 660, "Semipermeable mirror")
        cvui.text(frame,  840, 660, "Sprocket")
        cvui.text(frame,  994, 673, "Distance")
        cvui.text(frame, 1145, 660, "Mirror")

        cvui.text(frame, 892, 277, "-> Light behind sprocket")
        img = get_graph(fizeau_metre, fizeau_blank, fizeau_darkstripes, fizeau_lightstripes, coord=0, crop_light=False)
        cvui.image(frame, 896, 298, img)
        cvui.text(frame, 892, 377, "<- Reflected light before sprocket")
        img = get_graph(fizeau_metre, fizeau_blank, fizeau_darkstripes, fizeau_lightstripes, coord=coord, crop_light=False)
        cvui.image(frame, 896, 397, img)
        cvui.text(frame, 434, 100, "Reflected light behind sprocket")
        img = get_graph(fizeau_metre, fizeau_blank, fizeau_darkstripes, fizeau_lightstripes, coord=coord, crop_light=True)
        cvui.image(frame, 434, 120, img)

        #Experiment settings window
        cvui.window(frame, 1033.5, 2, 243.5, 104, 'Experiment settings')
        
        cvui.trackbar(frame,  1030, 39, 249, frequency_tr, 0.01, 12.0577)
        cvui.rect(frame, 1035, 39, 240, 12, 0x313131, 0x313131)
        cvui.rect(frame, 1035, 74, 240, 25, 0x313131, 0x313131)
        cvui.text(frame, 1041, 32, "Frequency")
        cvui.text(frame, 1042, 82, "{:,} Hz".format(round(frequency_tr[0], 2)))

        #Experiments window
        cvui.window(frame, 2, 2, 155, 75, 'Experiments')

        cvui.checkbox(frame, 10, 30, "1638 - Galileo",   experiments[0])
        cvui.checkbox(frame, 10, 53, "1849 - Fizeau",    experiments[1])

        curr_expr = exp_type(curr_expr, experiments)
        experiments = [[False] for i in range(2)]
        experiments[curr_expr] = [True]

        cvui.update()

        cv2.imshow('Speed of Light Measurement', frame)

        if cv2.waitKey(20) == 27:
            return -1

        if curr_expr != expr:
            return curr_expr
