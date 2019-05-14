import os
import math

import cv2
import pywt
import imutils
import numpy as np
from scipy.signal import convolve2d

from fake import Fake
from image import Image

def ela(image, scale=10, quality=80, loaded=False):
    """
    method computes error level analysis of image
    """
    if not loaded:
        original = cv2.imread(image)
    else:
        original = image
    cv2.imwrite('./temp.jpg', original, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    temporary = cv2.imread('./temp.jpg')

    diff = cv2.absdiff(original, temporary)*scale

    return diff


def get_ground_truth(im1, im2):
    """
    method finds bounding box of largest manipulation based on cv2.absdiff
    """
    diff = cv2.absdiff(im1, im2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, diff = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)

    cnts = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    max_idx = 0
    max_pnts = 0
    for i, item in enumerate(cnts):
        if cv2.contourArea(item) < max_pnts:
            continue
        else:
            max_idx = i
            max_pnts = cv2.contourArea(item)

    (x, y, w, h) = cv2.boundingRect(cnts[max_idx])
    
    return x, y, w, h


def load_fakes(fakes_list, fakes_path, originals_path):
    """
    method loads images into Image structure
    """
    data = []
    to_remove = []
    for i, item in enumerate(fakes_list):
        #get originals names
        parametres = item.split('_')

        #load fake
        fake = cv2.imread(os.path.join(fakes_path, item), -1)

        #load original
        original = cv2.imread(os.path.join(originals_path, "Au_"+parametres[4][:3]+"_"+parametres[4][3:]+".jpg"), -1)

        #try - check if images have same dimension
        try:
            x, y, w, h = get_ground_truth(fake, original)
        except:
            to_remove.append(item)
            continue

        #load into required structure
        dato = Fake(fake, os.path.join(fakes_path, item), True, x, y, w, h)
        data.append(dato)

    #weird fakes, which does not correspond to naming protocol
    for i, item in enumerate(to_remove):
        print("Bad input: {}" .format(item))

    return data


def load_originals(originals_list, originals_path):
    """
    method loads images into Image structure
    """
    data = []
    for i, item in enumerate(originals_list):
        #load original
        original = cv2.imread(os.path.join(originals_path, item), -1)

        #load into required structure
        dato = Image(original, os.path.join(originals_path, item), False)
        data.append(dato)

    return data


def create_folder_if_nexist(name):
    """
    method creates folder if folder doesn't exist
    """
    if not os.path.exists(name):
        os.makedirs(name)


def estimate_noise(image):
    """
    method estimates noise in image
    """
    filter_ = np.array([[1, -2, 1],
                        [-2, 4, -2],
                        [1, -2, 1]])

    sigma = np.sum(np.sum(np.absolute(cv2.filter2D(image, cv2.CV_64F, filter_))))
    sigma = sigma * np.sqrt(0.5 * np.pi) / (6 * (image.shape[1]-2) * (image.shape[0]-2))

    return sigma


def median_blur_noise(image, noise):
    """
    method applies median blur with parametres based on noise in image
    """
    if noise < 3.50:
        pass
    elif noise < 5.25:
        pass
    elif noise < 7.50:
        image = cv2.medianBlur(image, 3)
    elif noise < 10.05:
        pass
    elif noise < 12.25:
        image = cv2.medianBlur(image, 3)
    elif noise < 14.40:
        image = cv2.medianBlur(image, 3)
    elif noise < 16.85:
        pass
    elif noise < 20.35:
        image = cv2.medianBlur(image, 5)
    elif noise < 22.80:
        image = cv2.medianBlur(image, 3)
    elif noise < 25.80:
        pass
    elif noise < 29.40:
        image = cv2.medianBlur(image, 5)
    elif noise < 34.65:
        pass
    elif noise < 39.00:
        image = cv2.medianBlur(image, 7)
    elif noise < 45.00:
        image = cv2.medianBlur(image, 5)
    elif noise < 53.55:
        image = cv2.medianBlur(image, 5)
    elif noise < 62.40:
        image = cv2.medianBlur(image, 5)
    elif noise < 69.75:
        image = cv2.medianBlur(image, 5)
    elif noise < 79.50:
        image = cv2.medianBlur(image, 5)
    elif noise < 94.50:
        image = cv2.medianBlur(image, 3)
    else:
        image = cv2.medianBlur(image, 5)

    return image


def median_blur_kmeans(image, class_):
    """
    method applies median blur with parametres based unbalanced
    kmeans classification applied on ela noise image
    """
    if class_ == 0:
        image = cv2.medianBlur(image, 5)
    elif class_ == 1:
        image = cv2.medianBlur(image, 5)
    elif class_ == 2:
        image = cv2.medianBlur(image, 17)
    elif class_ == 3:
        image = cv2.medianBlur(image, 3)
    elif class_ == 4:
        image = cv2.medianBlur(image, 3)
    elif class_ == 5:
        image = cv2.medianBlur(image, 7)
    elif class_ == 6:
        pass
    elif class_ == 7:
        image = cv2.medianBlur(image, 5)
    elif class_ == 8:
        image = cv2.medianBlur(image, 17)
    elif class_ == 9:
        image = cv2.medianBlur(image, 7)
    elif class_ == 10:
        image = cv2.medianBlur(image, 3)
    elif class_ == 11:
        image = cv2.medianBlur(image, 7)
    elif class_ == 12:
        image = cv2.medianBlur(image, 19)
    elif class_ == 13:
        image = cv2.medianBlur(image, 15)
    elif class_ == 14:
        image = cv2.medianBlur(image, 17)
    elif class_ == 15:
        image = cv2.medianBlur(image, 9)
    elif class_ == 16:
        image = cv2.medianBlur(image, 5)
    elif class_ == 17:
        image = cv2.medianBlur(image, 11)
    elif class_ == 18:
        image = cv2.medianBlur(image, 11)
    elif class_ == 19:
        image = cv2.medianBlur(image, 3)

    return image


def median_blur_kmeans_2(image, class_):
    """
    method applies median blur with parametres based balanced
    kmeans classification applied on ela noise image
    """
    if class_ == 0:
        image = cv2.medianBlur(image, 5)
    elif class_ == 1:
        pass
    elif class_ == 2:
        image = cv2.medianBlur(image, 11)
    elif class_ == 3:
        pass
    elif class_ == 4:
        image = cv2.medianBlur(image, 3)
    elif class_ == 5:
        image = cv2.medianBlur(image, 3)
    elif class_ == 6:
        image = cv2.medianBlur(image, 3)
    elif class_ == 7:
        image = cv2.medianBlur(image, 3)
    elif class_ == 8:
        image = cv2.medianBlur(image, 3)
    elif class_ == 9:
        image = cv2.medianBlur(image, 7)
    elif class_ == 10:
        image = cv2.medianBlur(image, 3)
    elif class_ == 11:
        pass
    elif class_ == 12:
        image = cv2.medianBlur(image, 7)
    elif class_ == 13:
        image = cv2.medianBlur(image, 5)
    elif class_ == 14:
        image = cv2.medianBlur(image, 5)
    elif class_ == 15:
        image = cv2.medianBlur(image, 3)
    elif class_ == 16:
        image = cv2.medianBlur(image, 3)
    elif class_ == 17:
        pass
    elif class_ == 18:
        pass
    elif class_ == 19:
        image = cv2.medianBlur(image, 5)

    return image


def median_blur_dwt(image, class_):
    """
    method applies median blur with parametres based balanced
    kmeans classification applied on ela image
    """
    if class_ == 0:
        image = cv2.medianBlur(image, 5)
    elif class_ == 1:
        image = cv2.medianBlur(image, 3)
    elif class_ == 2:
        image = cv2.medianBlur(image, 3)
    elif class_ == 3:
        image = cv2.medianBlur(image, 7)
    elif class_ == 4:
        image = cv2.medianBlur(image, 3)
    elif class_ == 5:
        image = cv2.medianBlur(image, 7)
    elif class_ == 6:
        image = cv2.medianBlur(image, 11)
    elif class_ == 7:
        image = cv2.medianBlur(image, 3)
    elif class_ == 8:
        image = cv2.medianBlur(image, 3)
    elif class_ == 9:
        image = cv2.medianBlur(image, 5)
    elif class_ == 10:
        pass
    elif class_ == 11:
        image = cv2.medianBlur(image, 3)
    elif class_ == 12:
        pass
    elif class_ == 13:
        image = cv2.medianBlur(image, 11)
    elif class_ == 14:
        image = cv2.medianBlur(image, 5)
    elif class_ == 15:
        image = cv2.medianBlur(image, 3)
    elif class_ == 16:
        image = cv2.medianBlur(image, 7)
    elif class_ == 17:
        pass
    elif class_ == 18:
        image = cv2.medianBlur(image, 5)
    elif class_ == 19:
        image = cv2.medianBlur(image, 3)

    return image


def morphology_ex_noise(image, noise):
    """
    method applies opening with parametres based on noise in image
    """
    kernel = np.ones((3, 3), np.uint8)

    if noise < 3.50:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif noise < 5.25:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 3)
    elif noise < 7.50:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 11)
    elif noise < 10.05:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif noise < 12.25:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif noise < 14.40:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 7)
    elif noise < 16.85:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif noise < 20.35:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
    elif noise < 22.80:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 7)
    elif noise < 25.80:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif noise < 29.40:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
    elif noise < 34.65:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif noise < 39.00:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 13)
    elif noise < 45.00:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
    elif noise < 53.55:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 16)
    elif noise < 62.40:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 18)
    elif noise < 69.75:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif noise < 79.50:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 11)
    elif noise < 94.50:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 4)
    else:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)

    return image


def morphology_ex_kmeans(image, class_):
    """
    method applies opening with parametres based unbalanced
    kmeans classification applied on ela noise image
    """
    kernel = np.ones((3, 3), np.uint8)
    
    if class_ == 0:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)
    elif class_ == 1:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 2:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 3:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 4:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 3)
    elif class_ == 5:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 6:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 7:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)
    elif class_ == 8:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 9:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)
    elif class_ == 10:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 11:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
    elif class_ == 12:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 13:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 14:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 15:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 16:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 17:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 18:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 19:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 4)

    return image


def morphology_ex_kmeans_2(image, class_):
    """
    method applies opening with parametres based balanced
    kmeans classification applied on ela noise image
    """
    kernel = np.ones((3, 3), np.uint8)
    
    if class_ == 0:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 1:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 2:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 3:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 4:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 5:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 6:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 3)
    elif class_ == 7:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 8:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 9:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 10:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 13)
    elif class_ == 11:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 12:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
    elif class_ == 13:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 14:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif class_ == 15:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif class_ == 16:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 3)
    elif class_ == 17:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 18:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 1)
    elif class_ == 19:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)

    return image


def morphology_ex_dwt(image, class_):
    """
    method applies opening with parametres based balanced
    kmeans classification applied on ela image
    """
    kernel = np.ones((3, 3), np.uint8)
    
    if class_ == 0:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 1:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 2:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 11)
    elif class_ == 3:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
    elif class_ == 4:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 10)
    elif class_ == 5:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 17)
    elif class_ == 6:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif class_ == 7:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 8)
    elif class_ == 8:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 5)
    elif class_ == 9:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 10:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 11:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 14)
    elif class_ == 12:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 3)
    elif class_ == 13:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 6)
    elif class_ == 14:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif class_ == 15:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 9)
    elif class_ == 16:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 12)
    elif class_ == 17:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 2)
    elif class_ == 18:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 7)
    elif class_ == 19:
        image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel, iterations = 4)

    return image


def dwt_dwt(image, class_):
    """
    method applies wavelet soft-thresholding with parametres
    based balanced kmeans classification applied on ela image
    """
    passed = False
    if class_ == 0:
        passed = True
    elif class_ == 1:
        image_ = pywt.threshold(image, 10, 'soft')
    elif class_ == 2:
        image_ = pywt.threshold(image, 26, 'soft')
    elif class_ == 3:
        image_ = pywt.threshold(image, 1, 'soft')
    elif class_ == 4:
        image_ = pywt.threshold(image, 33, 'soft')
    elif class_ == 5:
        image_ = pywt.threshold(image, 8, 'soft')
    elif class_ == 6:
        image_ = pywt.threshold(image, 9, 'soft')
    elif class_ == 7:
        passed = True
    elif class_ == 8:
        image_ = pywt.threshold(image, 15, 'soft')
    elif class_ == 9:
        image_ = pywt.threshold(image, 8, 'soft')
    elif class_ == 10:
        image_ = pywt.threshold(image, 37, 'soft')
    elif class_ == 11:
        image_ = pywt.threshold(image, 38, 'soft')
    elif class_ == 12:
        image_ = pywt.threshold(image, 23, 'soft')
    elif class_ == 13:
        passed = True
    elif class_ == 14:
        image_ = pywt.threshold(image, 10, 'soft')
    elif class_ == 15:
        image_ = pywt.threshold(image, 20, 'soft')
    elif class_ == 16:
        image_ = pywt.threshold(image, 4, 'soft')
    elif class_ == 17:
        image_ = pywt.threshold(image, 28, 'soft')
    elif class_ == 18:
        image_ = pywt.threshold(image, 9, 'soft')
    elif class_ == 19:
        image_ = pywt.threshold(image, 4, 'soft')
    
    if not passed:
        image = cv2.normalize(image_, image, 0, 1, cv2.NORM_MINMAX)
        image = 255 * image
        image = image.astype(np.uint8)

    return image
