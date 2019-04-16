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


def find_bbox(frame, thresh, verbose=False):
    """
    method searches for moving objects
    """
    #Median blur for removing noise (salt and pepper type)
    op_1 = cv2.medianBlur(thresh, 3)
    #Threshold for removing of alone darker regions
    ret, op_2 = cv2.threshold(op_1, 127, 255, 0)
    #Median blur for removing noise (salt and pepper type)
    op_3 = cv2.medianBlur(op_2, 3)

    #Value of each pixel is replaced by its distance to the nearest background pixel
    op_4 = cv2.distanceTransform(op_3, cv2.DIST_L2, 0)
    ret, op_4 = cv2.threshold(op_4, 0.02 * op_4.max(), 255, 0) 

    #Median blur for removing noise (salt and pepper type)
    op_5 = cv2.medianBlur(op_4, 3)
    op_5 = cv2.medianBlur(op_5, 3)
    
    #Enlargement of white regions
    kernel = np.ones((3, 3), np.uint8) 
    op_6 = cv2.morphologyEx(op_5, cv2.MORPH_GRADIENT, kernel, iterations = 4) 

    #Scales, calculates absolute values, and converts the result to 8-bit
    op_6 = cv2.convertScaleAbs(op_6)

    #Finding of countours
    cnts = cv2.findContours(op_6.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
 
    #Percentage of white pixels from all pixels (contours)
    whites = round(np.count_nonzero(op_6 == 255)/ (op_6.shape[0]*op_6.shape[1]), 2)

    #Setup of bulgarian constant, which is threshold for size of displayed countours
    if whites <= 0.02:
        bulgarian_constant = 1000
    elif whites <= 0.03:
        bulgarian_constant = 1500
    elif whites <= 0.05:
        bulgarian_constant = 2500
    elif whites <= 0.07:
        bulgarian_constant = 3500
    elif whites <= 0.15:
        bulgarian_constant = 5000
    elif whites <= 0.25:
        bulgarian_constant = 10000
    elif whites <= 0.35:
        bulgarian_constant = 15000
    elif whites <= 0.45:
        bulgarian_constant = 35000
    else:
        bulgarian_constant = 75000

    #Selecting big enough contours
    cnt = 0
    for _, item in enumerate(cnts):

        if cv2.contourArea(item) < bulgarian_constant:
            continue
 
        #Bounding box
        (x, y, w, h) = cv2.boundingRect(item)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cnt += 1

    if verbose:
        print(whites, bulgarian_constant, cnt)

    return frame, thresh, op_1, op_2, op_3, op_4, op_5, op_6, cnt
