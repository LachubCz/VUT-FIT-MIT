import os
import sys
import argparse

import cv2
import imutils
import numpy as np

from image import Image as Dato
from tools import load_fakes, load_originals, create_folder_if_nexist, ela
from bbox_evaluation import evaluate_augmentation_fit
from extracting_inception import create_graph, extract_features
from train_svm import get_model

def parseargs():
    print( ' '.join(sys.argv))
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--path-to-originals', type=str, default="./data/CASIA1_originals",
                        help="")
    parser.add_argument('--path-to-fakes', type=str, default="./data/CASIA1_fakes",
                        help="")
    parser.add_argument('--path-to-originals-ela', type=str, default="./data/CASIA1_originals_ela",
                        help="")
    parser.add_argument('--path-to-fakes-ela', type=str, default="./data/CASIA1_fakes_ela",
                        help="")
    parser.add_argument('--path-to-nn', type=str, default="./models/tensorflow_inception_graph.pb", 
                        help="")
    parser.add_argument('--path-to-svm', type=str, default="./models/classifier_model.pkl", 
                        help="")
    parser.add_argument('--use-classifier', action="store_true", default=False,
                        help="")
    parser.add_argument('--just-fakes', action="store_true", default=False,
                        help="")
    parser.add_argument('--show', action="store_true", default=False,
                        help="")

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    max_value = 255
    max_value_H = 360//2
    low_H = 0
    low_S = 0
    low_V = 0
    high_H = max_value_H
    high_S = max_value
    high_V = max_value
    window_capture_name = 'Video Capture'
    window_detection_name = 'Object Detection'
    low_H_name = 'Low H'
    low_S_name = 'Low S'
    low_V_name = 'Low V'
    high_H_name = 'High H'
    high_S_name = 'High S'
    high_V_name = 'High V'
    def on_low_H_thresh_trackbar(val):
        global low_H
        global high_H
        low_H = val
        low_H = min(high_H-1, low_H)
        cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
    def on_high_H_thresh_trackbar(val):
        global low_H
        global high_H
        high_H = val
        high_H = max(high_H, low_H+1)
        cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
    def on_low_S_thresh_trackbar(val):
        global low_S
        global high_S
        low_S = val
        low_S = min(high_S-1, low_S)
        cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
    def on_high_S_thresh_trackbar(val):
        global low_S
        global high_S
        high_S = val
        high_S = max(high_S, low_S+1)
        cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
    def on_low_V_thresh_trackbar(val):
        global low_V
        global high_V
        low_V = val
        low_V = min(high_V-1, low_V)
        cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
    def on_high_V_thresh_trackbar(val):
        global low_V
        global high_V
        high_V = val
        high_V = max(high_V, low_V+1)
        cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

    cv2.namedWindow(window_detection_name)
    cv2.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
    cv2.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
    cv2.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
    cv2.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
    cv2.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
    cv2.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)


    args = parseargs()

    if args.just_fakes:
        fakes_list = os.listdir(args.path_to_fakes)
    else: 
        originals_list = os.listdir(args.path_to_originals)
        fakes_list = os.listdir(args.path_to_fakes)

    if not args.just_fakes:
        originals = load_originals(originals_list, args.path_to_originals)
    fakes = load_fakes(fakes_list, args.path_to_fakes, args.path_to_originals)

    if args.use_classifier:
        #inception network model
        create_graph(args.path_to_nn)
        #svm model
        model = get_model(args.path_to_svm)

        #originals
        if not args.just_fakes:
            originals_path = []
            for i, item in enumerate(originals):
                originals_path.append(item.path)

            for i, item in enumerate(os.listdir(args.path_to_originals_ela)):
                originals_path.append(os.path.join(args.path_to_originals_ela, item))

            #feature extraction
            features = extract_features(originals_path, verbose=True)

            #SVM training
            predictions = model.predict(features)
            true_positive = np.count_nonzero(predictions == 1)
            false_positive = np.count_nonzero(predictions == 0)

        #fakes
        fakes_path = []
        for i, item in enumerate(fakes):
            fakes_path.append(item.path)

        for i, item in enumerate(os.listdir(args.path_to_fakes_ela)):
            fakes_path.append(os.path.join(args.path_to_fakes_ela, item))
        
        #feature extraction
        features = extract_features(fakes_path, verbose=True)

        #SVM training
        predictions = model.predict(features)
        true_negative = np.count_nonzero(predictions == 1)
        false_negative = np.count_nonzero(predictions == 0)

        if not args.just_fakes:
            print("###############")
            print("Classification")
            print("--------------")
            print("True positive:  {}" .format(true_positive))
            print("False positive: {}" .format(false_positive))
            print("True negative:  {}" .format(true_negative))
            print("False negative: {}" .format(false_negative))
            print("Score: {} %" .format((true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)))
            print("###############")
        else:
            print("###############")
            print("Classification")
            print("--------------")
            print("True positive:  {}" .format(true_positive))
            print("False positive: {}" .format(false_positive))
            print("True negative:  {}" .format(true_negative))
            print("False negative: {}" .format(false_negative))
            print("Score: {} %" .format((true_positive+true_negative)/(true_positive+true_negative+false_positive+false_negative)))
            print("###############")

    whole_score = 0
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(args.path_to_fakes_ela, item.path.split('\\')[-1]))


        frame_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)





        image = cv2.medianBlur(image, 3)
        cv2.imshow("medianBlur", image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("cvtColor", image)
        ret, image = cv2.threshold(image,50,255,cv2.THRESH_BINARY)
        cv2.imshow("threshold", image)
        kernel = np.ones((3, 3), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 4)
        cv2.imshow("morphologyEx", image)
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        max_idx = 0
        max_pnts = 0
        for e, elem in enumerate(cnts):
            if cv2.contourArea(elem) < max_pnts:
                continue
            else:
                max_idx = e
                max_pnts = cv2.contourArea(elem)

        if len(cnts) > 0:
            (x, y, w, h) = cv2.boundingRect(cnts[max_idx])
            pred =  {
              "x": x,
              "y": y,
              "w": w,
              "h": h
            }
            cv2.rectangle(item.image, (pred['x'], pred['y']), (pred['x'] + pred['w'], pred['y'] + pred['h']), (0, 255, 0), 2)
            cv2.rectangle(item.image, (item.bbox['x'], item.bbox['y']), (item.bbox['x'] + item.bbox['w'], item.bbox['y'] + item.bbox['h']), (255, 0, 0),2)
        else:
            pred = None

        score = evaluate_augmentation_fit(pred, item)

        whole_score += score


        while True:
            frame_threshold = cv2.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
            cv2.imshow(window_detection_name, frame_threshold)
            key = cv2.waitKey(30)
            if key == ord('w'):
                break


        if args.show:
            cv2.imshow("frame", item.image)
            cv2.waitKey(0)
            print(score)

    print((whole_score/(len(data)))*100)
