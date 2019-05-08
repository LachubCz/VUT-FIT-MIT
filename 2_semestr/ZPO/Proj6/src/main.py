import os
import sys
import argparse

import cv2
import imutils
import numpy as np

from image import Image as Dato
from tools import load_fakes, load_originals, create_folder_if_nexist, ela, estimate_noise
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
    parser.add_argument('--print-bbox-debug', action="store_true", default=False,
                        help="")
    parser.add_argument('--show', action="store_true", default=False,
                        help="")

    args = parser.parse_args()

    return args


if __name__ == '__main__':
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
    if args.print_bbox_debug:
        print("#######################")
        print("Debugging bounding box")
        print("----------------------")
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(args.path_to_fakes_ela, item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)
        noise = estimate_noise(image)
        if args.show:
            cv2.imshow("inRange", image)

        if noise < 5:
            pass
        elif noise < 10:
            pass
        elif noise < 15:
            image = cv2.medianBlur(image, 3)
        elif noise < 20:
            image = cv2.medianBlur(image, 5)
        elif noise < 25:
            image = cv2.medianBlur(image, 5)
        elif noise < 30:
            image = cv2.medianBlur(image, 7)
        elif noise < 35:
            image = cv2.medianBlur(image, 7)
        elif noise < 40:
            image = cv2.medianBlur(image, 7)
        elif noise < 45:
            image = cv2.medianBlur(image, 7)
        elif noise < 50:
            image = cv2.medianBlur(image, 13)
        elif noise < 55:
            image = cv2.medianBlur(image, 13)
        elif noise < 60:
            image = cv2.medianBlur(image, 13)
        elif noise < 65:
            image = cv2.medianBlur(image, 13)
        elif noise < 70:
            image = cv2.medianBlur(image, 13)
        elif noise < 75:
            image = cv2.medianBlur(image, 13)
        elif noise < 80:
            image = cv2.medianBlur(image, 13)
        elif noise < 85:
            image = cv2.medianBlur(image, 13)
        elif noise < 90:
            image = cv2.medianBlur(image, 13)
        elif noise < 95:
            image = cv2.medianBlur(image, 13)
        elif noise < 100:
            image = cv2.medianBlur(image, 19)
        else:
            image = cv2.medianBlur(image, 19)

        if args.show:
            cv2.imshow("medianBlur", image)

        kernel = np.ones((3, 3), np.uint8)

        if noise < 5:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
        elif noise < 10:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
        elif noise < 15:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
        elif noise < 20:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 7)
        elif noise < 25:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 7)
        elif noise < 30:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)
        elif noise < 35:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
        elif noise < 40:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
        elif noise < 45:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
        elif noise < 50:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
        elif noise < 55:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
        elif noise < 60:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 11)
        elif noise < 65:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 70:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 75:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 80:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 85:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 90:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 95:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
        elif noise < 100:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 13)
        else:
            image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)

        if args.show:
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
        if args.print_bbox_debug:
            print("{}: {}, {}" .format(item.path, round(noise, 2), round(score, 2)))

        if args.show:
            cv2.imshow("frame", item.image)
            cv2.waitKey(0)
    if args.print_bbox_debug:
        print("#######################")
    print("#############")
    print("Bounding box")
    print("------------")
    print("{} %" .format(round((whole_score/(len(fakes)))*100, 2)))
    print("#############")
