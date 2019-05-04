#################################################################################
# Description:  File containing method for training of SVM classificator
#               
# Authors:      Petr Buchal         <petr.buchal@lachub.cz>
#               Martin Ivanco       <ivancom.fr@gmail.com>
#               Vladimir Jerabek    <jerab.vl@gmail.com>
#
# Date:     2019/04/13
# 
# Note:     This source code is part of project created on UnIT extended 2019.
#################################################################################

import argparse
from os import listdir
from os.path import isfile, join

import cv2
import numpy as np

from extracting_inception import create_graph, extract_features
from train_svm import train_svm_classifer

from tools import parse_data

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--trn-data-size', type="int", action="store", default=1000,
                        help='Number of images for training.')
    parser.add_argument('--model-name', action="store", 
                        help='Filename of SVM model.')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = get_args()
    batch = args.trn_data_size

    filenames = ["./images_png/"+f for f in listdir("./images_png") if isfile(join("./images_png", f))]

    #inception network model
    create_graph("./models/tensorflow_inception_graph.pb")

    labels = []
    for i, item in enumerate(filenames[:batch]):
        if item[-5] == 'T':
            labels.append(1)
        else:
            labels.append(0)

    #feature extraction
    features = extract_features(filenames[:batch], verbose=True)
    #SVM training
    train_svm_classifer(features, labels, args.model_name)
