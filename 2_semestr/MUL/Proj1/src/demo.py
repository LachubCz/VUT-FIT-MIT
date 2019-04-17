from collections import deque

import cv2
import cvui
import imutils
import numpy as np

from tools import find_bbox

def demo(source=None, height=240):
    """
    method creates window, that shows, what is happening with image,
    when is analyzed by algorithm
    """
    if not source:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(source)
    
    fgbg = cv2.createBackgroundSubtractorMOG2()
    ret, image = cap.read()

    image = imutils.resize(image, height=height)

    if image.shape[0] > image.shape[1]:
        width = image.shape[0]
    else:
        width = image.shape[1]

    frame = np.zeros(((height+27)*2-2, (width + 7)*4-5, 3), np.uint8)
    cvui.init('Motion Detection')

    while (True):
        frame[:] = (49,52,49)

        ret, image = cap.read()

        if type(image).__module__ != np.__name__:
            break

        map_ = fgbg.apply(image)
        image, op_1, op_2, op_3, op_4, op_5, op_6, op_7, cnt = find_bbox(image, map_, verbose=False)

        #To BGR
        op_1 = cv2.cvtColor(op_1, cv2.COLOR_GRAY2BGR)
        op_2 = cv2.cvtColor(op_2, cv2.COLOR_GRAY2BGR)
        op_3 = cv2.cvtColor(op_3, cv2.COLOR_GRAY2BGR)
        op_4 = cv2.cvtColor(op_4, cv2.COLOR_GRAY2BGR)
        op_5 = cv2.cvtColor(op_5, cv2.COLOR_GRAY2BGR)
        op_6 = cv2.cvtColor(op_6, cv2.COLOR_GRAY2BGR)
        op_7 = cv2.cvtColor(op_7, cv2.COLOR_GRAY2BGR)

        #Resize
        image = imutils.resize(image, height=height)
        op_1 = imutils.resize(op_1, height=height)
        op_2 = imutils.resize(op_2, height=height)
        op_3 = imutils.resize(op_3, height=height)
        op_4 = imutils.resize(op_4, height=height)
        op_5 = imutils.resize(op_5, height=height)
        op_6 = imutils.resize(op_6, height=height)
        op_7 = imutils.resize(op_7, height=height)

        #Window
        cvui.window(frame, 2, 2, width + 3, 263, 'Motion Detection')
        cvui.image(frame, 4, 24, image)

        cvui.window(frame, (width + 3) + 4, 2, width + 3, 263, 'operation_1 - MOG2')
        cvui.image(frame, (width + 3) + 4+2, 24, op_1)

        cvui.window(frame, ((width + 3) + 2)*2+2, 2, width + 3, 263, 'operation_2 - medianBlur')
        cvui.image(frame, ((width + 3) + 4)*2, 24, op_2)

        cvui.window(frame, ((width + 3) + 2)*3+2, 2, width + 3, 263, 'operation_3 - threshold')
        cvui.image(frame, ((width + 3) + 4)*3-2, 24, op_3)

        cvui.window(frame, 2, 265+2, width + 3, 263, 'operation_4 - medianBlur')
        cvui.image(frame, 4, 265+24, op_4)

        cvui.window(frame, (width + 3) + 4, 265+2, width + 3, 263, 'operation_5 - distanceTransform, threshold')
        cvui.image(frame, (width + 3) + 4+2, 265+24, op_5)

        cvui.window(frame, ((width + 3) + 2)*2+2, 265+2, width + 3, 263, 'operation_6 - medianBlur')
        cvui.image(frame, ((width + 3) + 4)*2, 265+24, op_6)

        cvui.window(frame, ((width + 3) + 2)*3+2, 265+2, width + 3, 263, 'operation_7 - morphologyEx')
        cvui.image(frame, ((width + 3) + 4)*3-2, 265+24, op_7)

        cvui.update()
        cv2.imshow('Motion Detection', frame)

        if cv2.waitKey(20) == 27:
            return -1
