import os

import cv2
import imutils
import numpy as np

from tools import load_fakes, ela, estimate_noise, create_folder_if_nexist
from bbox_evaluation import evaluate_augmentation_fit


def create_elas():
    for i, item in enumerate(os.listdir('./data/CASIA1_originals')):
        image = ela(os.path.join('./data/CASIA1_originals', item))
        cv2.imwrite(os.path.join('./data/CASIA1_originals_ela', item), image)
    
    for i, item in enumerate(os.listdir('./data/CASIA1_fakes')):
        image = ela(os.path.join('./data/CASIA1_fakes', item))
        cv2.imwrite(os.path.join('./data/CASIA1_fakes_ela', item), image)


def create_classes():
    fakes_list = os.listdir('./data/CASIA1_fakes')

    fakes = load_fakes(fakes_list, './data/CASIA1_fakes', './data/CASIA1_originals')

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)
        noises.append(estimate_noise(image))

    fakes = np.array(fakes)
    noises = np.array(noises)
    idxs = noises.argsort()
    sorted_by_noise = fakes[idxs]

    create_folder_if_nexist('./data/CASIA1_classes')
    for i in range(20):
        create_folder_if_nexist('./data/CASIA1_classes/{}' .format(i+1))

    count = int(len(sorted_by_noise)/20)
    if count > (len(sorted_by_noise)/20):
        pass
    else:
        count -= 1

    class_ = 1
    for i, item in enumerate(sorted_by_noise):
        if (class_*count) < (i+1):
            class_ += 1

        cv2.imwrite("{}" .format(os.path.join('./data/CASIA1_classes/{}' .format(class_), item.path.split('\\')[-1])), item.image)


def get_combinations():
    classes_ = []
    for i in range(20):
        classes_.append('./data/CASIA1_classes/{}' .format(i+1))

    medians_ = [0,3,5,7,9,11,13,15,17,19]

    iterations_ = []
    for i in range(21):
        iterations_.append(i)

    for i, item in enumerate(classes_):
        fakes_list = os.listdir(item)
        fakes = load_fakes(fakes_list, item, './data/CASIA1_originals')

        best = 0
        for x, median_filter_size in enumerate(medians_):
            for y, number_of_iterations in enumerate(iterations_):
                whole_score = 0
                for e, elem in enumerate(fakes):
                    image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', elem.path.split('\\')[-1]))
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                    
                    image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
                    image = cv2.bitwise_not(image)

                    if median_filter_size > 0:
                        image = cv2.medianBlur(image, median_filter_size)

                    kernel = np.ones((3, 3), np.uint8)
                    image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations=number_of_iterations)

                    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    max_idx = 0
                    max_pnts = 0
                    for u, ulem in enumerate(cnts):
                        if cv2.contourArea(ulem) < max_pnts:
                            continue
                        else:
                            max_idx = u
                            max_pnts = cv2.contourArea(ulem)

                    if len(cnts) > 0:
                        (x, y, w, h) = cv2.boundingRect(cnts[max_idx])
                        pred =  {
                          "x": x,
                          "y": y,
                          "w": w,
                          "h": h
                        }
                    else:
                        pred = None

                    whole_score += evaluate_augmentation_fit(pred, elem)
                if best < whole_score:
                    best = whole_score
                print("Class: {}; MedianFilterSize: {}; Iterations: {}; Score: {}" .format(item, median_filter_size, number_of_iterations, round(whole_score, 2)))
        print("###########")
        print("Best: {} -> {} %" .format(round(best, 2), round((best/len(fakes)), 2)))
        print("###########")


def get_noise_thresholds():
    fakes_list = os.listdir('./data/CASIA1_fakes')

    fakes = load_fakes(fakes_list, './data/CASIA1_fakes', './data/CASIA1_originals')

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)
        noises.append(estimate_noise(image))

    fakes = np.array(fakes)
    noises = np.array(noises)
    idxs = noises.argsort()
    sorted_by_noise = fakes[idxs]

    for i, item in enumerate(sorted(noises)):
        if (i+1) % 45 == 0:
            print("####", i+1, item)
        else:
            print(i+1, item)


if __name__ == '__main__':

