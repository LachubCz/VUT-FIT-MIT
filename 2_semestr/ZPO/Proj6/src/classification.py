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


def train_svm_classifer(features, labels, model_output_path, cross_validation_gen=20):
    """
    method trains a SVM classifier
    """
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

    svm = SVC(probability=True)

    clf = grid_search.GridSearchCV(svm, param, cv=cross_validation_gen, n_jobs=4, verbose=3)

    clf.fit(X_train, y_train)

    joblib.dump(clf.best_estimator_, model_output_path)

    y_predict=clf.predict(X_test)
    labels=sorted(list(set(labels)))

    print("\nBest parameters set:")
    print(clf.best_params_)

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_predict, labels=labels))

    print("\nClassification report:")
    print(classification_report(y_test, y_predict))


def get_model(model):
    """
    method returns loaded SVM model
    """
    clf = joblib.load(model)

    return clf


def create_graph(model_path):
    """
    method loads the inception model
    """
    with gfile.FastGFile(model_path, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def extract_features(image_paths, verbose=False):
    """
    method computes the inception bottleneck feature for a list of images
    """
    features = np.empty((len(image_paths), feature_dimension))

    with tf.Session() as sess:
        flattened_tensor = sess.graph.get_tensor_by_name('pool_3:0')

        for i in range(len(image_paths)):
            if not gfile.Exists(image_paths[i]):
                tf.logging.fatal('File does not exist %s', image)

            image_data = gfile.FastGFile(image_paths[i], 'rb').read()
            feature = sess.run(flattened_tensor, {'DecodeJpeg/contents:0': image_data})
            features[i, :] = np.squeeze(feature)

    return features


if __name__ == '__main__':
    args = get_args()
    batch = args.data_size

    originals_ela = ["./data/CASIA1_originals_ela/"+f for f in listdir("./data/CASIA1_originals_ela/") if isfile(join("./data/CASIA1_originals_ela/", f))]
    fakes_ela = ["./data/CASIA1_fakes_ela/"+f for f in listdir("./data/CASIA1_fakes_ela/") if isfile(join("./data/CASIA1_fakes_ela/", f))]

    #inception network model
    create_graph("./models/tensorflow_inception_graph.pb")

    labels = []
    for i, item in enumerate(fakes_ela):
        labels.append(1)
    for i, item in enumerate(originals_ela):
        labels.append(0)

    filenames = fakes_ela + originals_ela
    #feature extraction
    features = extract_features(filenames, verbose=True)
    #SVM training
    train_svm_classifer(features, labels, 'classifier_model.pkl')
