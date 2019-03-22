import cv2
import cvui
import time
import tools
import numpy as np
from timeit import default_timer as timer

from galileo import galileo
from roemer import roemer
from fizeau import fizeau
from michelson import michelson

def main():
    frame = np.zeros((720, 1280, 3), np.uint8)
    cvui.init('Speed of Light Measurement')

    curr_experiment = 2
    while (True):
        if curr_experiment == 0:
            curr_experiment = galileo(frame, curr_experiment)
        elif curr_experiment == 1:
            curr_experiment = roemer(frame, curr_experiment)
        elif curr_experiment == 2:
            curr_experiment = fizeau(frame, curr_experiment)
        elif curr_experiment == 3:
            curr_experiment = michelson(frame, curr_experiment)
        
if __name__ == '__main__':
    main()
