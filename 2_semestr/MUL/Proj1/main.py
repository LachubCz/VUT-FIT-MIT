import sys
import time
import json
import argparse

import cv2
from timeit import default_timer as timer

from grid import Grid
from tools import sound_notification

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', action="store", choices=["real_time", "time_capsule"],
                        default="real-time", help="training dataset file")
    parser.add_argument('--threshold', action="store", type=int,
                        default=20, help="training dataset file")
    parser.add_argument('--time_jump', action="store", type=int,
                        default=20, help="time jump in seconds for time-capsule mode")
    parser.add_argument('-e', '--email_notification', action="store_true", 
                        default=False, help="flag for email notification")
    parser.add_argument('-s', '--sound_notification', action="store_true", 
                        default=False, help="flag for sound notification")

    args = parser.parse_args()

    return args


def real_time(args):
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


def time_capsule(args):
    if args.email_notification:
        with open('email_settings.json') as f:
            email_data = json.load(f)
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    last = Grid(frame)

    while(True):
        ret, frame = cap.read()

        frame = Grid(frame)

        number_of_elm = frame.put_text(last)

        if number_of_elm > 0:
            if args.sound_notification:
                sound_notification()
            if args.email_notification:
                tm = create_timestamp()
                cv2.imwrite(tm + '.jpg', frame.original)
                email_notification()
                os.remove(tm + '.jpg')

        cv2.imshow('frame',frame.original)
        for _ in range(args.time_jump*10):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None
            time.sleep(args.time_jump/10)

        last = frame


if __name__ == "__main__":
    args = get_args()
    if args.mode == "real_time":
        real_time(args)
    elif args.mode == "time_capsule":
        time_capsule(args)
