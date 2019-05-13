import os
import argparse
from os import listdir
from os.path import isfile, join

import cv2
import numpy as np

import tensorflow as tf
import tensorflow.python.platform
from tensorflow.python.platform import gfile

import sklearn
from sklearn import cross_validation, grid_search
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
from sklearn.externals import joblib


def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--data-size', type="int", action="store", default=1000,
                        help='Number of images for training.')
    parser.add_argument('--model-name', action="store", 
                        help='Filename of SVM model.')

    args = parser.parse_args()

    return args


def train_svm_classifer(features, labels, model_output_path, cross_validation_gen=25):
    """
    train_svm_classifer will train a SVM, saved the trained and SVM model and
    report the classification performance
    features: array of input features
    labels: array of labels associated with the input features
    model_output_path: path for storing the trained svm model
    """
    # save 20% of data for performance evaluation
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features, labels, test_size=0.2)

    param = [
        {
            "kernel": ["linear"],
            "C": [1, 10, 100, 1000]
        },
        {
            "kernel": ["rbf"],
            "C": [1, 10, 100, 1000],
            "gamma": [1e-2, 1e-3, 1e-4, 1e-5]
        }
    ]

    # request probability estimation
    svm = SVC(probability=True)

    # 10-fold cross validation, use 4 thread as each fold and each parameter set can be train in parallel
    clf = grid_search.GridSearchCV(svm, param,
            cv=cross_validation_gen, n_jobs=4, verbose=3)

    clf.fit(X_train, y_train)

    joblib.dump(clf.best_estimator_, model_output_path)

    print("\nBest parameters set:")
    print(clf.best_params_)

    y_predict=clf.predict(X_test)

    labels=sorted(list(set(labels)))
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_predict, labels=labels))

    print("\nClassification report:")
    print(classification_report(y_test, y_predict))


def get_model(model):
    """
    returns loaded SVM model
    """
    clf = joblib.load(model)

    return clf


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


if __name__ == '__main__':
    args = get_args()
    batch = args.data_size

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
