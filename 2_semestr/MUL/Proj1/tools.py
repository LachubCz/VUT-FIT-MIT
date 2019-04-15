import os
import sys
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import cv2
import imutils
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


def sound_notification():
    """
    method notificates user via sound
    """
    sys.stdout.write('\a')
    sys.stdout.flush()


def email_notification(data, timestamp):
    """
    method prepares emails to send
    """
    for _, item in enumerate(data['recievers']):
        send_email(from_addr    = data['sender_email'],
                   to_addr      = item,
                   cc_addr_list = [''],
                   subject      = "New motion - " + timestamp,
                   message      = '',
                   login        = data['sender_email'],
                   password     = data['sender_password'],
                   timestamp    = timestamp)
    print("Email notifications were sent.")


def send_email(from_addr, to_addr, cc_addr_list, subject, message, login, 
               password, timestamp, smtpserver='smtp.gmail.com:587'):
    """
    method sends email notification
    """
    image = open('{}.jpg' .format(timestamp), 'rb').read()
    msg = MIMEMultipart()
    print(from_addr, to_addr)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr

    image = MIMEImage(image, name=os.path.basename('{}.jpg' .format(timestamp)))
    msg.attach(image)

    server = smtplib.SMTP(smtpserver)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

def find_bbox(frame, thresh):
    thresh = np.asarray(thresh, dtype=np.uint8)

    kernel = np.ones((3, 3), np.uint8) 
    closing = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, 
                                kernel, iterations = 2) 
      
    # Background area using Dialation 
    bg = cv2.dilate(closing, kernel, iterations = 4) 
      
    # Finding foreground area 
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0) 
    ret, fg = cv2.threshold(dist_transform, 0.02
                            * dist_transform.max(), 255, 0) 

    fg = cv2.convertScaleAbs(fg)
    cnts = cv2.findContours(fg.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
 
    whites = round(np.count_nonzero(fg == 255)/ (fg.shape[0]*fg.shape[1]), 2)
    
    if whites <= 0.15:
        bulgarian_constant = 5000
    elif whites <= 0.25:
        bulgarian_constant = 10000
    elif whites <= 0.35:
        bulgarian_constant = 15000
    elif whites <= 0.45:
        bulgarian_constant = 35000
    else:
        bulgarian_constant = 75000
    print(whites, bulgarian_constant)
    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < bulgarian_constant:
            continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"

    return frame, fg