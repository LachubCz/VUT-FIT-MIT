import os
import sys
import time
import json
import argparse
import subprocess
from collections import deque

import cv2
from timeit import default_timer as timer

from tools import sound_notification, create_timestamp, email_notification, find_bbox, err_print
from demo import demo

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--mode', action="store", choices=["demo", "time_capsule"],
                        default="demo", help="training dataset file")
    parser.add_argument('--source', action="store",
                        default=None, help="video file to test algorithm")
    parser.add_argument('--time_jump', action="store", type=int,
                        default=20, help="time jump in seconds for time-capsule mode")
    parser.add_argument('-e', '--email_notification', action="store_true",
                        default=False, help="flag for email notification")
    parser.add_argument('-c', '--copy_to_server', action="store_true",
                        default=False, help="flag for email notification")
    parser.add_argument('-s', '--sound_notification', action="store_true",
                        default=False, help="flag for sound notification")
    parser.add_argument('-r', '--save_records', action="store_true",
                        default=False, help="flag for saving images with detected motion")
    parser.add_argument('-n', '--no_display', action="store_true",
                        default=False, help="flag for saving images with detected motion")

    args = parser.parse_args()

    return args


def time_capsule(args):
    """
    main for time-capsule mode
    """
    if args.email_notification:
        with open('email_settings.json') as f:
            email_data = json.load(f)

    if args.copy_to_server:
        with open('scp_settings.json') as f:
            scp_data = json.load(f)

    if args.save_records:
        if not os.path.isdir("./history"):
            os.mkdir('history')

    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while(True):
        ret, frame = cap.read()

        tm = create_timestamp()
        
        map_ = fgbg.apply(frame)

        frame, _, _, _, _, _, _, _, number_of_elm = find_bbox(frame, map_)

        if number_of_elm > 0:
            print(tm + " - Motion detected.")
            if args.sound_notification:
                sound_notification()
            if args.email_notification:
                cv2.imwrite(tm + '.jpg', frame)
                email_notification(email_data, tm)
                os.remove(tm + '.jpg')
            if args.save_records:
                cv2.imwrite('./history/' + tm + '.jpg', frame)
                print("Frame with motion was saved.")
            if args.copy_to_server:
                cv2.imwrite(tm + '.jpg', frame)
                p = subprocess.check_call(['scp', './' + tm + '.jpg', 
                                      scp_data['user']+'@'+scp_data['server']+':'+scp_data['path']])
                os.remove(tm + '.jpg')

        if not args.no_display:
            cv2.imshow('Motion detection', frame)
        for _ in range(int(args.time_jump/0.1)):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None
            time.sleep(0.1)


if __name__ == "__main__":
    args = get_args()
    if args.mode == "demo":
        demo(args.source)
    elif args.mode == "time_capsule":
        time_capsule(args)
