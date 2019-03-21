import numpy as np
import cv2
import cvui
import time
import tools
from timeit import default_timer as timer
from galileo import galileo
from roemer import roemer
from bradley import bradley
from fizeau import fizeau
from foucalt import foucalt
from michelson import michelson

WINDOW_NAME = 'Speed of Light Measurement'

def main():
    frame = np.zeros((720, 1280, 3), np.uint8)
    cvui.init(WINDOW_NAME)

    curr_experiment = 0
    while (True):
        if curr_experiment == 0:
            curr_experiment = galileo(frame)
        elif curr_experiment == 1:
            curr_experiment = roemer(frame)
        elif curr_experiment == 2:
            curr_experiment = bradley(frame)
        elif curr_experiment == 3:
            curr_experiment = fizeau(frame)
        elif curr_experiment == 4:
            curr_experiment = foucalt(frame)
        elif curr_experiment == 5:
            curr_experiment = michelson(frame)
        
if __name__ == '__main__':
    main()
