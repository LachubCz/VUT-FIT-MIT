import os
import math

import cv2
import imutils
import numpy as np
from scipy.signal import convolve2d

from fake import Fake
from image import Image

def ela(image, scale=10, quality=80, loaded=False):
    if not loaded:
        original = cv2.imread(image)
    else:
        original = image
    cv2.imwrite('./temp.jpg', original, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    temporary = cv2.imread('./temp.jpg')

    #os.remove("./temp.jpg")

    diff = cv2.absdiff(original, temporary)*scale

    return diff


def get_ground_truth(im1, im2):
    diff = cv2.absdiff(im1, im2)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret,diff = cv2.threshold(diff,10,255,cv2.THRESH_BINARY)

    cnts = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    max_idx = 0
    max_pnts = 0
    for i, item in enumerate(cnts):
        if cv2.contourArea(item) < max_pnts:
            continue
        else:
            max_idx = i
            max_pnts = cv2.contourArea(item)
    #print("MAX:", max_pnts)

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

    #remove weird fakes, which does not correspond to naming protocol
    for i, item in enumerate(to_remove):
        os.remove(os.path.join(data_path, item))

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
    if not os.path.exists(name):
        os.makedirs(name)

def estimate_noise(image):
    height, width = image.shape

    filter_ = [[1, -2, 1],
               [-2, 4, -2],
               [1, -2, 1]]

    sigma = np.sum(np.sum(np.absolute(convolve2d(image, filter_))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (width-2) * (height-2))

    return sigma