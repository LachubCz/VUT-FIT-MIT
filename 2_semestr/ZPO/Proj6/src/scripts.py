import os

import cv2
import pywt
import pickle
import imutils
import argparse
import numpy as np
from sklearn.cluster import KMeans

from tools import load_fakes, ela, estimate_noise, create_folder_if_nexist
from bbox_evaluation import evaluate_augmentation_fit

def create_ela_files(originals='./data/CASIA1_originals', originals_ela='./data/CASIA1_originals_ela',
                fakes='./data/CASIA1_fakes', fakes_ela='./data/CASIA1_fakes_ela'):
    """
    method creates folders with ela of original and fake images
    """
    for i, item in enumerate(os.listdir(originals)):
        image = ela(os.path.join(originals, item))
        cv2.imwrite(os.path.join(originals_ela, item), image)
    
    for i, item in enumerate(os.listdir(fakes)):
        image = ela(os.path.join(fakes, item))
        cv2.imwrite(os.path.join(fakes_ela, item), image)


def create_ela_noise_files(originals='./data/CASIA1_originals', fakes='./data/CASIA1_fakes',
                           fakes_ela='./data/CASIA1_fakes_ela', fakes_ela_noise='./data/CASIA1_ela_noise'):
    """
    method creates folder with ela noise from fake images
    """
    fakes_list = os.listdir(fakes)

    fakes = load_fakes(fakes_list, fakes, originals)

    create_folder_if_nexist(fakes_ela_noise)
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(fakes_ela, item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)

        cv2.imwrite("{}" .format(os.path.join(fakes_ela_noise, item.path.split('\\')[-1])), image)


def create_classes_noise(fakes='./data/CASIA1_fakes', originals='./data/CASIA1_originals', 
                         fakes_ela='./data/CASIA1_fakes_ela', classes='./data/CASIA1_classes/'):
    """
    method creates image classes based on noise
    """
    fakes_list = os.listdir(fakes)

    fakes = load_fakes(fakes_list, fakes, originals)

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(fakes_ela, item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)
        noises.append(estimate_noise(image))

    fakes = np.array(fakes)
    noises = np.array(noises)
    idxs = noises.argsort()
    sorted_by_noise = fakes[idxs]

    create_folder_if_nexist(classes)
    for i in range(20):
        create_folder_if_nexist('{}{}' .format(classes, i+1))

    count = int(len(sorted_by_noise)/20)
    if count > (len(sorted_by_noise)/20):
        pass
    else:
        count -= 1

    class_ = 1
    for i, item in enumerate(sorted_by_noise):
        if (class_*count) < (i+1):
            class_ += 1

        cv2.imwrite("{}" .format(os.path.join('{}{}' .format(classes, class_),
                                 item.path.split('\\')[-1])), item.image)


def create_classes_kmeans(fakes='./data/CASIA1_fakes', originals='./data/CASIA1_originals', 
                          fakes_ela='./data/CASIA1_fakes_ela', classes='./data/CASIA1_classes_2/',
                          model='./models/kmeans_model.pkl'):
    """
    method creates image classes based kmeans classifier
    """
    kmeans = None
    
    with open(model, "rb") as input:
        kmeans = pickle.load(input)

    create_folder_if_nexist(classes)
    for i in range(20):
        create_folder_if_nexist('{}{}' .format(classes, i))

    fakes_list = os.listdir(fakes)

    fakes = load_fakes(fakes_list, fakes, originals)

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(fakes_ela, item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)

        if np.shape(image)[0] > np.shape(image)[1]:
            image = cv2.resize(image, (384, 256))
        else:
            image = cv2.resize(image, (256, 384))

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        image = np.array([image.flatten()])
        class_ = kmeans.predict(image)[0]

        cv2.imwrite("{}" .format(os.path.join('{}' .format(classes, class_), item.path.split('\\')[-1])), item.image)


def get_combinations(classes_folder='./data/CASIA1_classes_by_unbalanced_kmeans/', 
                     originals='./data/CASIA1_originals', fakes_ela='./data/CASIA1_fakes_ela'):
    """
    method finds ideal combination of dwt thresholding, median blur,
    opening parameteres for all classes determined by kmeans
    """
    classes_ = []
    for i in range(20):
        classes_.append('{}{}' .format(classes_folder, i+1))

    medians_ = [0,3,5,7,9,11,13,15,17,19]

    iterations_ = []
    for i in range(21):
        iterations_.append(i)

    threshold_ = []
    for i in range(40):
        threshold_.append(i)

    for i, item in enumerate(classes_):
        fakes_list = os.listdir(item)
        fakes = load_fakes(fakes_list, item, originals)

        best = 0
        best_median_filter_size = 0
        best_number_of_iterations = 0
        best_thresh = 0
        for x, median_filter_size in enumerate(medians_):
            for y, number_of_iterations in enumerate(iterations_):
                for t, thresh in enumerate(threshold_):
                    whole_score = 0
                    for e, elem in enumerate(fakes):
                        image = cv2.imread(os.path.join(fakes_ela, elem.path.split('\\')[-1]))

                        if thresh > 0:
                            image_ = pywt.threshold(image, thresh, 'soft')
                            image = cv2.normalize(image_, image, 0, 1, cv2.NORM_MINMAX)
                            image = 255 * image
                            image = image.astype(np.uint8)

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
                        best_median_filter_size = median_filter_size
                        best_number_of_iterations = number_of_iterations
                        best_thresh = thresh
                    print("Class: {}; MedianFilterSize: {}; Iterations: {}; Thresh: {}; Score: {}" .format(item, median_filter_size, number_of_iterations, thresh, round(whole_score, 2)))
        print("###########")
        print("Best: {} -> {} % ({}, {}, {})" .format(round(best, 2), round((best/len(fakes)), 2), best_median_filter_size, best_number_of_iterations, best_thresh))
        print("###########")


def get_combination(class_, originals='./data/CASIA1_originals', fakes_ela='./data/CASIA1_fakes_ela'):
    """
    method finds ideal combination of dwt thresholding, median blur,
    opening parameteres for certain class determined by kmeans
    """
    medians_ = [0,3,5,7,9,11,13,15,17,19]

    iterations_ = []
    for i in range(21):
        iterations_.append(i)

    threshold_ = []
    for i in range(40):
        threshold_.append(i)

    fakes_list = os.listdir(class_)
    fakes = load_fakes(fakes_list, class_, originals)

    best = 0
    best_median_filter_size = 0
    best_number_of_iterations = 0
    best_thresh = 0
    for x, median_filter_size in enumerate(medians_):
        for y, number_of_iterations in enumerate(iterations_):
            for t, thresh in enumerate(threshold_):
                whole_score = 0
                for e, elem in enumerate(fakes):
                    image = cv2.imread(os.path.join(fakes_ela, elem.path.split('\\')[-1]))

                    if thresh > 0:
                        image_ = pywt.threshold(image, thresh, 'soft')
                        image = cv2.normalize(image_, image, 0, 1, cv2.NORM_MINMAX)
                        image = 255 * image
                        image = image.astype(np.uint8)

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
                    best_median_filter_size = median_filter_size
                    best_number_of_iterations = number_of_iterations
                    best_thresh = thresh
                print("Class: {}; MedianFilterSize: {}; Iterations: {}; Thresh: {}; Score: {}" .format(class_, median_filter_size, number_of_iterations, thresh, round(whole_score, 2)))
    print("###########")
    print("Best: {} -> {} % ({}, {}, {})" .format(round(best, 2), round((best/len(fakes)), 2), best_median_filter_size, best_number_of_iterations, best_thresh))
    print("###########")


def get_noise_thresholds(size_of_class=45, fakes='./data/CASIA1_fakes', originals='./data/CASIA1_originals', 
                         fakes_ela='./data/CASIA1_fakes_ela'):
    """
    method finds boundaries of classes estimated by noise
    """
    fakes_list = os.listdir(fakes)

    fakes = load_fakes(fakes_list, fakes, originals)

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join(fakes_ela, item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)
        noises.append(estimate_noise(image))

    fakes = np.array(fakes)
    noises = np.array(noises)
    idxs = noises.argsort()
    sorted_by_noise = fakes[idxs]

    for i, item in enumerate(sorted(noises)):
        if (i+1) % size_of_class == 0:
            print("####", i+1, item)
        else:
            print(i+1, item)


def train_balanced_kmeans(ela_noise='./data/CASIA1_ela_noise', model='clustering_model.pkl'):
    """
    method trains unbalanced kmeans
    """
    ela_noise = os.listdir(ela_noise)
    x = np.zeros((len(ela_noise), 294912))

    for i, item in enumerate(ela_noise):
        image = cv2.imread(os.path.join(ela_noise, item))
        if np.shape(image)[0] > np.shape(image)[1]:
            image = cv2.resize(image, (384, 256))
        else:
            image = cv2.resize(image, (256, 384))
        x[i] = image.flatten()

    kmeans = KMeans(n_clusters=20, random_state=0).fit(x)

    with open(model, "wb") as output:
        pickle.dump(kmeans, output, pickle.HIGHEST_PROTOCOL)


def train_balanced_kmeans(ela_noise='./data/CASIA1_ela_noise', model='clustering_model.pkl'):
    """
    method trains balanced kmeans
    """
    ela_noise = os.listdir(ela_noise)
    x = np.zeros((len(ela_noise), 294912))

    for i, item in enumerate(ela_noise):
        image = cv2.imread(os.path.join(ela_noise, item))
        if np.shape(image)[0] > np.shape(image)[1]:
            image = cv2.resize(image, (384, 256))
        else:
            image = cv2.resize(image, (256, 384))
        x[i] = image.flatten()

    kmeans = EqualGroupsKMeans(n_clusters=20, random_state=0, verbose=1).fit(x)

    with open(model, "wb") as output:
        pickle.dump(kmeans, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    pass
