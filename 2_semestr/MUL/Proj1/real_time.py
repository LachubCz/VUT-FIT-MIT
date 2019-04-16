from collections import deque

import cv2
import cvui
import imutils
import numpy as np

from tools import exp_type, find_bbox

def real_time(height=240):
    #cap = cv2.VideoCapture('example.mp4')
    #cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    ret, image = cap.read()

    image = imutils.resize(image, height=height)

    if image.shape[0] > image.shape[1]:
        width = image.shape[0]
    else:
        width = image.shape[1]

    frame1 = np.zeros((height+27, width + 7, 3), np.uint8)
    cvui.init('Motion Detection - finished')

    frame2 = np.zeros((height+27, width + 7, 3), np.uint8)
    cvui.init('Motion Detection - MOG2')

    frame3 = np.zeros((height+27, width + 7, 3), np.uint8)
    cvui.init('Motion Detection - closing operation')

    frame4 = np.zeros((height+27, width + 7, 3), np.uint8)
    cvui.init('Motion Detection - foreground area')

    while (True):
        frame1[:] = (49,52,49)
        frame2[:] = (49,52,49)
        frame3[:] = (49,52,49)
        frame4[:] = (49,52,49)

        ret, image = cap.read()
        #im = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
        #new = cv2.equalizeHist(im)

        map_ = fgbg.apply(image)
        image, fg, dist_transform, closing = find_bbox(image, map_)
        
        #To BGR
        fg = cv2.cvtColor(fg, cv2.COLOR_GRAY2BGR)
        dist_transform = cv2.cvtColor(dist_transform, cv2.COLOR_GRAY2BGR)
        closing = cv2.cvtColor(closing, cv2.COLOR_GRAY2BGR)

        #Resize
        image = imutils.resize(image, height=height)
        fg = imutils.resize(fg, height=height)
        dist_transform = imutils.resize(dist_transform, height=height)
        closing = imutils.resize(closing, height=height)

        #Window
        cvui.window(frame1, 2, 2, width + 3, 599, 'Motion Detection - finished')
        cvui.image(frame1, 4, 24, image)

        cvui.window(frame2, 2, 2, width + 3, 599, 'Motion Detection - MOG2')
        cvui.image(frame2, 4, 24, fg)

        cvui.window(frame3, 2, 2, width + 3, 599, 'Motion Detection - closing operation')
        cvui.image(frame3, 4, 24, closing)

        cvui.window(frame4, 2, 2, width + 3, 599, 'Motion Detection - foreground area')
        cvui.image(frame4, 4, 24, dist_transform)

        cvui.update()
        cv2.imshow('Motion Detection - finished', frame1)
        cv2.imshow('Motion Detection - MOG2', frame2)
        cv2.imshow('Motion Detection - closing operation', frame3)
        cv2.imshow('Motion Detection - foreground area', frame4)

        if cv2.waitKey(20) == 27:
            return -1
