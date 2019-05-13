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
from equal_groups import EqualGroupsKMeans

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
        classes_.append('./data/CASIA1_classes_3/{}' .format(i+1))

    medians_ = [0,3,5,7,9,11,13,15,17,19]

    iterations_ = []
    for i in range(21):
        iterations_.append(i)

    threshold_ = []
    for i in range(40):
        threshold_.append(i)

    for i, item in enumerate(classes_):
        fakes_list = os.listdir(item)
        fakes = load_fakes(fakes_list, item, './data/CASIA1_originals')

        best = 0
        best_median_filter_size = 0
        best_number_of_iterations = 0
        best_thresh = 0
        for x, median_filter_size in enumerate(medians_):
            for y, number_of_iterations in enumerate(iterations_):
                for t, thresh in enumerate(threshold_):
                    whole_score = 0
                    for e, elem in enumerate(fakes):
                        image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', elem.path.split('\\')[-1]))

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


def get_combination(class_):
    medians_ = [0,3,5,7,9,11,13,15,17,19]

    iterations_ = []
    for i in range(21):
        iterations_.append(i)

    threshold_ = []
    for i in range(40):
        threshold_.append(i)

    fakes_list = os.listdir(class_)
    fakes = load_fakes(fakes_list, class_, './data/CASIA1_originals')

    best = 0
    best_median_filter_size = 0
    best_number_of_iterations = 0
    best_thresh = 0
    for x, median_filter_size in enumerate(medians_):
        for y, number_of_iterations in enumerate(iterations_):
            for t, thresh in enumerate(threshold_):
                whole_score = 0
                for e, elem in enumerate(fakes):
                    image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', elem.path.split('\\')[-1]))

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


def create_ela_noise_files():
    fakes_list = os.listdir('./data/CASIA1_fakes')

    fakes = load_fakes(fakes_list, './data/CASIA1_fakes', './data/CASIA1_originals')

    create_folder_if_nexist('./data/CASIA1_ela_noise')
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', item.path.split('\\')[-1]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        image = cv2.inRange(image, np.array([0,0,0]), np.array([180,255,60]))
        image = cv2.bitwise_not(image)

        cv2.imwrite("{}" .format(os.path.join('./data/CASIA1_ela_noise', item.path.split('\\')[-1])), image)


def train_kmeans():
    ela_noise = os.listdir('./data/CASIA1_ela_noise')
    x = np.zeros((len(ela_noise), 294912))

    for i, item in enumerate(ela_noise):
        image = cv2.imread(os.path.join('./data/CASIA1_ela_noise', item))
        if np.shape(image)[0] > np.shape(image)[1]:
            image = cv2.resize(image, (384, 256))
        else:
            image = cv2.resize(image, (256, 384))
        x[i] = image.flatten()

    kmeans = KMeans(n_clusters=20, random_state=0).fit(x)
    #print(kmeans.labels_)
    with open("clustering_model.pkl", "wb") as output:
        pickle.dump(kmeans, output, pickle.HIGHEST_PROTOCOL)


def train_kmeans_2():
    ela_noise = os.listdir('./data/CASIA1_ela_noise')
    x = np.zeros((len(ela_noise), 294912))

    for i, item in enumerate(ela_noise):
        image = cv2.imread(os.path.join('./data/CASIA1_ela_noise', item))
        if np.shape(image)[0] > np.shape(image)[1]:
            image = cv2.resize(image, (384, 256))
        else:
            image = cv2.resize(image, (256, 384))
        x[i] = image.flatten()

    kmeans = EqualGroupsKMeans(n_clusters=20, random_state=0, verbose=1).fit(x)
    #print(kmeans.labels_)
    with open("clustering_model.pkl", "wb") as output:
        pickle.dump(kmeans, output, pickle.HIGHEST_PROTOCOL)


def create_classes_kmeans():
    kmeans = None
    
    with open("./models/kmeans_model.pkl", "rb") as input:
        kmeans = pickle.load(input)

    create_folder_if_nexist('./data/CASIA1_classes_2')
    for i in range(20):
        create_folder_if_nexist('./data/CASIA1_classes_2/{}' .format(i))

    fakes_list = os.listdir('./data/CASIA1_fakes')

    fakes = load_fakes(fakes_list, './data/CASIA1_fakes', './data/CASIA1_originals')

    noises = []
    for i, item in enumerate(fakes):
        image = cv2.imread(os.path.join('./data/CASIA1_fakes_ela', item.path.split('\\')[-1]))
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

        cv2.imwrite("{}" .format(os.path.join('./data/CASIA1_classes_2/{}' .format(class_), item.path.split('\\')[-1])), item.image)

def get_coeff(an, k):
    e_an = 0.5 * np.sqrt((-np.pi/np.log(0.5))) * np.median(an.flatten())

    o_g = e_an / np.sqrt(np.pi / 2.0)

    u_r = o_g * np.sqrt(np.pi / 2.0)

    T = u_r + k * o_g

    print("E(a_n): {}; O_g: {}; U_r: {}; T: {}; Median: {}" .format(e_an, o_g, u_r, T, np.median(an.flatten())))

    return T

if __name__ == '__main__':

    #image = cv2.imread("./src/Sp_D_NNN_A_ani0055_pla0025_0287.jpg")
    #cv2.imshow("imread", image)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #image_ = pywt.threshold(image, 2, 'soft')
    #cv2.imshow("pywt", image_)

    #coeffs2 = pywt.dwtn(image, 'haar', axes)
    #LL, (LH, HL, HH) = coeffs2

    #LL = pywt.threshold(LL, 2, 'soft')
    #LH = pywt.threshold(LH, 2, 'soft')
    #HL = pywt.threshold(HL, 2, 'soft')
    #HH = pywt.threshold(HH, 2, 'soft')

    #coeffs2 = (LL, (LH, HL, HH))
    #image = pywt.idwt2(coeffs2, 'haar')

    #cv2.imshow("threshold", image)
    #cv2.waitKey(0)
    ##array([ 0. ,  0. ,  0. ,  0.5,  1. ,  1.5,  2. ])
    #pywt.threshold(data, 2, 'hard')
    ##array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    #pywt.threshold(data, 2, 'garrote')
    ##array([ 0.        ,  0.        ,  0.        ,  0.9       ,  1.66666667,       2.35714286,  3.        ])
    #pywt.threshold(data, 2, 'greater')
    ##array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    #pywt.threshold(data, 2, 'less')
    ##array([ 1. ,  1.5,  2. ,  0. ,  0. ,  0. ,  0. ])

    #import numpy as np
    #import pywt
    #import numpy
    #import PIL
    #from PIL import Image
    #img = PIL.Image.open("./src/Sp_D_NNN_A_ani0055_pla0025_0287.jpg").convert("L")
    #imgarr = numpy.array(img) 
    #print(np.shape(imgarr))
    #coeffs = pywt.dwt2(imgarr, 'haar')
    #pywt.idwt2(coeffs, 'haar')  
    #image = cv2.imread('./src/Sp_D_CNN_A_cha0025_pla0067_0269.jpg')
    #b,g,r=cv2.split(image)
    ## RGB - Blue
    #cv2.imshow('B-RGB', b)
    ##print(np.shape(b))
    #
    ## RGB - Green
    #cv2.imshow('G-RGB', g)
    #
    ## RGB - Red
    #cv2.imshow('R-RGB', r)
    ##img = cv2.merge((b,g,r))
    ##cv2.imshow('G-RsaGB', img)

    ##image_ = pywt.threshold(image, 18, 'soft')
    ##normalizedImg = np.zeros((256, 384, 3))
    ##normalizedImg = image_.copy()
    ##normalizedImg = cv2.normalize(image_,  normalizedImg, 0, 1, cv2.NORM_MINMAX)
    ##cv2.imshow("pywt", normalizedImg)

    #coeffs2 = pywt.dwt2(b, 'haar')
    #LL, (LH, HL, HH) = coeffs2
    ##print(LL)
    ##print(np.shape(LL))
    ##print(np.median(LL.flatten()))



    #thresh = get_coeff(LL, 10)
    #LL = pywt.threshold(LL, 10, 'soft')
    #thresh = get_coeff(LH, 10)
    #LH = pywt.threshold(LH, 10, 'soft')
    #thresh = get_coeff(HL, 10)
    #HL = pywt.threshold(HL, 10, 'soft')
    #thresh = get_coeff(HH, 10)
    #HH = pywt.threshold(HH, 10, 'soft')

    #coeffs2 = (LL, (LH, HL, HH))
    #image_ = pywt.idwt2(coeffs2, 'haar')

    #normalizedImg = b.copy()
    #normalizedImg = cv2.normalize(image_,  normalizedImg, 0, 1, cv2.NORM_MINMAX)
    #cv2.imshow("pywt", normalizedImg)
    #
    ##print(image.dtype)
    ##normalizedImg = np.zeros((256, 384))
    ##normalizedImg = cv2.normalize(image,  normalizedImg, 0, 1, cv2.NORM_MINMAX)
    ##cv2.imshow('dst_rt', normalizedImg)
    ###cv2.imshow('R-RGB_sa', )
    ###print(normalizedImg)
    #cv2.waitKey(0)

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--folder', type=int)

    args = parser.parse_args()

    get_combination("./data/CASIA1_classes_by_simple_kmeans/{}" .format(args.folder))
