import datetime

import cv2
import numpy as np

def four_quadrants(image):
    """
    method splits image into four quadrants
    -------+-------
    second | first
    -------+-------
    third  | fourth
    -------+-------
    """
    width = np.size(image, 0)
    height = np.size(image, 1)

    half_width = int(width / 2)
    half_height = int(height / 2)

    first = image[0:half_width, half_height:height]
    second = image[0:half_width, 0:half_height]
    third = image[half_width:width, 0:half_height]
    fourth = image[half_width:width, half_height:height]

    return [first, second, third, fourth]


def mse(imageA, imageB):
    """
    method computes mse for two images
    """
    diff = (imageA.astype("float") - imageB.astype("float")) ** 2
    err = np.sum(diff)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err


def resize(image, size):
    """
    method resizes image into square
    """
    return cv2.resize(image, (size, size))


def gray(image):
    """
    method changes color image to gray
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def blur(image):
    """
    method blurs image
    """
    return cv2.GaussianBlur(image, (21, 21), 0)


def create_timestamp():
    """
    method creates timestamps
    """
    timestamp = str(datetime.datetime.now())
    timestamp = timestamp.replace(' ', '-')
    timestamp = timestamp.replace(':', '-')
    timestamp = timestamp[:-4]
    timestamp = timestamp.replace('.', '-')

    return timestamp


def divisible_numbers(a_list, a_list_of_terms, div):
    """
    method returns list of elements with certain div from the first list,
    which is common for all divisors in the second list
    """
    return [i for i in a_list if all(i%j==div for j in a_list_of_terms)]


def get_neighbors(index):
    """
    method return neighbors for element with certain index
    """
    neighbors = set()
    div = index-(8*(index//8))
    if index > 7 and index < 56 and div != 0 and div != 7:
        neighbors.add(index-9)
        neighbors.add(index-8)
        neighbors.add(index-7)
        neighbors.add(index-1)
        neighbors.add(index+1)
        neighbors.add(index+7)
        neighbors.add(index+8)
        neighbors.add(index+9)
    elif index > 7 and index < 56 and div == 0:
        neighbors.add(index-8)
        neighbors.add(index-7)
        neighbors.add(index+1)
        neighbors.add(index+8)
        neighbors.add(index+9)
    elif index > 7 and index < 56 and div == 7:
        neighbors.add(index-9)
        neighbors.add(index-8)
        neighbors.add(index-1)
        neighbors.add(index+7)
        neighbors.add(index+8)
    elif index > 0 and index < 7:
        neighbors.add(index-1)
        neighbors.add(index+1)
        neighbors.add(index+7)
        neighbors.add(index+8)
        neighbors.add(index+9)
    elif index > 55 and index < 63:
        neighbors.add(index-9)
        neighbors.add(index-8)
        neighbors.add(index-7)
        neighbors.add(index-1)
        neighbors.add(index+1)
    elif index == 0:
        neighbors.add(1)
        neighbors.add(8)
        neighbors.add(9)
    elif index == 7:
        neighbors.add(6)
        neighbors.add(14)
        neighbors.add(15)
    elif index == 56:
        neighbors.add(48)
        neighbors.add(49)
        neighbors.add(57)
    elif index == 63:
        neighbors.add(54)
        neighbors.add(55)
        neighbors.add(62)

    return neighbors
