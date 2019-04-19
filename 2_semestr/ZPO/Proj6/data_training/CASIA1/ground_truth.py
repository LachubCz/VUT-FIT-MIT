import os

import cv2
import imutils
import numpy as np
from PIL import Image, ImageChops

from image import Image as Dato

def ela_(image, scale=10, quality=80):
    original = Image.open(image)
    original.save("./temp.jpg", quality=quality)
    temporary = Image.open("./temp.jpg")
    os.remove("./temp.jpg")

    diff = ImageChops.difference(original, temporary)
    d = diff.load()
    width, height = diff.size
    for x in range(width):
        for y in range(height):
            d[x, y] = tuple(k * scale for k in d[x, y])

    return diff


def pil_to_opencv(pil_image):
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    return open_cv_image[:, :, ::-1].copy()


def ela(image, scale=10, quality=80):
    img = ela_(image, scale, quality)
    return pil_to_opencv(img)


def get_rect(im1, im2):
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


def parse_data(filename, data_path, ground_truths_path):
    """
    method parses csv file and loads images into structure Image
    """
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content]

    data = []
    for i, item in enumerate(content):
        if i == 0:
            continue
        parametres = item.split('_')

        image = cv2.imread(os.path.join(data_path, item), -1)

        #os.path.join(ground_truths_path, "Au_"+parametres[4][:3]+"_"+parametres[4][3:]+".jpg")

        gt1 = cv2.imread(os.path.join(ground_truths_path, "Au_"+parametres[4][:3]+"_"+parametres[4][3:]+".jpg"), -1)

        try:
            x, y, w, h = get_rect(image, gt1)
        except:
            continue

        dato = Dato(image, os.path.join(data_path, item), x, y, w, h)
        data.append(dato)

    return data

def find_augmentation(image):
    pass


if __name__ == '__main__':
    data = parse_data("./Sp_im.txt", "./Sp/", "./Au/")
    for i, item in enumerate(data):
        image = ela(item.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


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
        #print("MAX:", max_pnts)

        (x, y, w, h) = cv2.boundingRect(cnts[max_idx])
        cv2.rectangle(item.image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("frame", item.image)
        cv2.waitKey(0)