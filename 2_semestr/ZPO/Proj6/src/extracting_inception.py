#################################################################################
# Description:  File contains methods for training of SVM
#               
# Authors:      May Yeung
#
# Date:     2016/10/21
# 
# Note:     This source code originally comes from https://bit.ly/2GcFtDG and
#           was used as part of project created on UnIT extended 2019.
#################################################################################

import os

import numpy as np

import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile

def create_graph(model_path):
    """
    create_graph loads the inception model to memory, should be called before
    calling extract_features.
    model_path: path to inception model in protobuf form.
    """
    with gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def extract_features(image_paths, verbose=False):
    """
    extract_features computed the inception bottleneck feature for a list of images
    image_paths: array of image path
    return: 2-d array in the shape of (len(image_paths), 2048)
    """
    feature_dimension = 4096
    lenght = int(len(image_paths)/2)
    features = np.empty((lenght, feature_dimension))

    with tf.Session() as sess:
        flattened_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        for i in range(lenght):
            #original
            if verbose:
                print('Processing %s...' % (image_paths[i]))

            if not gfile.Exists(image_paths[i]):
                tf.logging.fatal('File does not exist %s', image)

            image_data = gfile.FastGFile(image_paths[i], 'rb').read()
            feature = sess.run(flattened_tensor, {'DecodeJpeg/contents:0': image_data})
            features[i, 2048:] = np.squeeze(feature)
            #ela
            if verbose:
                print('Processing %s...' % (image_paths[i+lenght]))

            if not gfile.Exists(image_paths[i+lenght]):
                tf.logging.fatal('File does not exist %s', image)

            image_data = gfile.FastGFile(image_paths[i+lenght], 'rb').read()
            feature = sess.run(flattened_tensor, {'DecodeJpeg/contents:0': image_data})
            features[i, :2048] = np.squeeze(feature)

    return features


def extract_feature(image_path, verbose=False):
    """
    extract_feature computed the inception bottleneck feature for a list of images
    image_path: array of image path
    return: 2-d array in the shape of (len(image_path), 2048)
    """
    feature_dimension = 2048
    features = np.empty((len(image_path), feature_dimension))

    with tf.Session() as sess:
        flattened_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        if verbose:
            print('Processing %s...' % (image_path[0]))

        if not gfile.Exists(image_path[0]):
            tf.logging.fatal('File does not exist %s', image)

        image_data = gfile.FastGFile(image_path[0], 'rb').read()
        feature = sess.run(flattened_tensor, {
            'DecodeJpeg/contents:0': image_data
        })
        features[0, :] = np.squeeze(feature)

    return features
