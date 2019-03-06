import argparse

import cv2
from timeit import default_timer as timer

from grid import Grid

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', action="store", choices=["real-time", "time-capsule"],
                        default="real-time", help="training dataset file")
    parser.add_argument('--threshold', action="store", type=int,
                        default=20, help="training dataset file")
    parser.add_argument('--time_jump', action="store", type=int,
                        default=20, help="time jump in seconds for time-capsule mode")
    parser.add_argument('--email', action="store", 
                        default=None, help="email addres for email notifications")
    parser.add_argument('-s', '--sound_notification', action="store_true", 
                        default=False, help="flag for sound notification")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    last = Grid(frame)

    while(True):
        ret, frame = cap.read()

        frame = Grid(frame)

        start_time = timer()
        frame.put_text(last)
        end_time = timer() - start_time
        print("Computations: " + str(end_time))

        cv2.imshow('frame',frame.original)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        last = frame

    cap.release()
    cv2.destroyAllWindows()
