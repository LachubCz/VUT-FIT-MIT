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

import sklearn
from sklearn import cross_validation, grid_search
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
from sklearn.externals import joblib

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
