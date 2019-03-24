import time

import cv2
import cvui
import numpy as np
from timeit import default_timer as timer

from galileo import galileo
from fizeau import fizeau

def main():
    frame = np.zeros((720, 1280, 3), np.uint8)
    cvui.init('Speed of Light Measurement')

    curr_experiment = 0
    while (True):
        if curr_experiment == 0:
            curr_experiment = galileo(frame, curr_experiment)
        elif curr_experiment == 1:
            curr_experiment = fizeau(frame, curr_experiment)

if __name__ == '__main__':
    main()
