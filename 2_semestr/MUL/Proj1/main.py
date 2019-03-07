import os
import sys
import time
import json
import argparse

import cv2
from timeit import default_timer as timer

from grid import Grid
from tools import sound_notification, create_timestamp, email_notification

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
    parser.add_argument('-r', '--save_records', action="store_true",
                        default=False, help="flag for saving images with detected motion")

    args = parser.parse_args()

    return args


def real_time(args):
    """
    main for real-time mode
    """
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    last = Grid(frame)

    while(True):
        ret, frame = cap.read()

        frame = Grid(frame)

        #start_time = timer()
        frame.draw(last)
        #end_time = timer() - start_time
        #print("Computation time: " + str(end_time))

        cv2.imshow('frame',frame.original)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        last = frame

    cap.release()
    cv2.destroyAllWindows()


def time_capsule(args):
    """
    main for time-capsule mode
    """
    if args.email_notification:
        with open('email_settings.json') as f:
            email_data = json.load(f)

    if args.save_records:
        if not os.path.isdir("./history"):
            os.mkdir('history')

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    last = Grid(frame)

    while(True):
        ret, frame = cap.read()

        tm = create_timestamp()
        
        frame = Grid(frame)

        number_of_elm = frame.draw(last)

        if number_of_elm > 0:
            if args.sound_notification:
                sound_notification()
            if args.email_notification:
                cv2.imwrite(tm + '.jpg', frame.original)
                email_notification(email_data, tm)
                os.remove(tm + '.jpg')
            if args.save_records:
                cv2.imwrite('./history/' + tm + '.jpg', frame.original)

        cv2.imshow('frame',frame.original)
        for _ in range(int(args.time_jump/0.1)):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None
            time.sleep(0.1)

        last = frame


if __name__ == "__main__":
    args = get_args()
    if args.mode == "real_time":
        real_time(args)
    elif args.mode == "time_capsule":
        time_capsule(args)
