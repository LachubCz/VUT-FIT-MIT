import os

import cv2

from tools import ela

if __name__ == '__main__':
    for i, item in enumerate(os.listdir('./data/CASIA1_originals')):
        image = ela(os.path.join('./data/CASIA1_originals', item))
        cv2.imwrite(os.path.join('./data/CASIA1_originals_ela', item), image)
    
    for i, item in enumerate(os.listdir('./data/CASIA1_fakes')):
        image = ela(os.path.join('./data/CASIA1_fakes', item))
        cv2.imwrite(os.path.join('./data/CASIA1_fakes_ela', item), image)
