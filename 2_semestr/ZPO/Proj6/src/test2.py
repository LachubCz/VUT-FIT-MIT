import os
from PIL import Image, ImageChops
import cv2
import numpy


def ELA(image, scale=10, quality=80):
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
    open_cv_image = numpy.array(pil_image) 
    # Convert RGB to BGR 
    return open_cv_image[:, :, ::-1].copy() 


im = ELA('./Sp_D_CNN_A_art0024_ani0032_0268.jpg')
im = pil_to_opencv(im)
cv2.imshow("frame", im)
cv2.waitKey(0)
