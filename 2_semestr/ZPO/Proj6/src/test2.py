import os
import cv2
import numpy


def ELA2(image, scale=10, quality=80):
    original = cv2.imread(image)
    cv2.imwrite('./temp.jpg', original, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    temporary = cv2.imread('./temp.jpg')

    os.remove("./temp.jpg")

    diff = cv2.absdiff(original, temporary)*scale

    return diff

im = ELA2('./Sp_D_CNN_A_nat0071_ani0024_0270.jpg')
cv2.imshow("frame1", im)
cv2.waitKey(0)
