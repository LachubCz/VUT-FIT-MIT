#import random
#from cv2 import CV_64F
#import keras.backend as K
#import numpy as np
#from keras.layers import Conv2D
#from sklearn.model_selection import train_test_split
#from sklearn.utils import shuffle
#from keras.utils import np_utils
#from keras.layers.convolutional import MaxPooling2D
#from keras.layers.core import Dense, Dropout, Activation, Flatten
#from keras.models import Sequential
#import cv2
#from theano import shared
#
#def custom_gabor(shape, dtype=None):
#    total_ker = []
#    for i in xrange(shape[0]):
#        kernels = []
#        for j in xrange(shape[1]):
#        # gk = gabor_kernel(frequency=0.2, bandwidth=0.1)
#            tmp_filter = cv2.getGaborKernel(ksize=(shape[3], shape[2]), sigma=1, theta=1, lambd=0.5, gamma=0.3, psi=(3.14) * 0.5, ktype=CV_64F)
#            filter = []
#            for row in tmp_filter:
#                filter.append(np.delete(row, -1))
#            kernels.append(filter)
#                # gk.real
#        total_ker.append(kernels)
#    np_tot = shared(np.array(total_ker))
#    return K.variable(np_tot, dtype=dtype)
import tensorflow as tf
import keras.backend as K
import numpy as np

import keras.backend
from keras.models import Sequential, Model
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from keras.layers import Input, InputLayer
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD


def SRM_kernel():
    filter1 = [[0, 0, 0, 0, 0],
               [0, -1, 2, -1, 0],
               [0, 2, -4, 2, 0],
               [0, -1, 2, -1, 0],
               [0, 0, 0, 0, 0]]
    filter2 = [[-1, 2, -2, 2, -1],
               [2, -6, 8, -6, 2],
               [-2, 8, -12, 8, -2],
               [2, -6, 8, -6, 2],
               [-1, 2, -2, 2, -1]]
    filter3 = [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 1, -2, 1, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
    q = [4.0, 12.0, 2.0]
    filter1 = np.asarray(filter1, dtype=float) / 4
    filter2 = np.asarray(filter2, dtype=float) / 12
    filter3 = np.asarray(filter3, dtype=float) / 2
    #print(filter1)
    #print(filter2)
    #print(filter3)

    filters = [[filter1, filter1, filter1], [filter2, filter2, filter2], [filter3, filter3, filter3]]
    #print(filters)
    filters = np.einsum('klij->ijlk', filters)
    #print(keras.backend.floatx())
    filters = keras.backend.variable(filters, dtype=keras.backend.floatx())
    #filters = tf.Variable(filters, dtype=tf.float32)
    return filters


wewe = SRM_kernel()
wewe= Input(tensor=wewe)
#print(filters)
"""
filter1 = [[0, 0, 0, 0, 0],
           [0, -1, 2, -1, 0],
           [0, 2, -4, 2, 0],
           [0, -1, 2, -1, 0],
           [0, 0, 0, 0, 0]]
"""
#model = Sequential()
input_ = Input(shape=(640,480,3))
#x = ZeroPadding2D((1,1), input_shape=(224, 224, 3), data_format='channels_last')(input_)
#x = keras.backend.conv2d(input_, wewe, strides=(1, 1), padding='valid', data_format="channels_last")#Conv2D(64, kernel_size=(5, 5), kernel_initializer=SRM_kernel, strides=1,  padding="valid"))

#wewe = Lambda(SRM_kernel)
output = keras.backend.conv2d(input_, wewe, strides=(1, 1), padding='valid', data_format="channels_last")

"""
x = Flatten()(x)
pr = Dense(256, activation='relu')(x)
"""
#x = Input(shape=(636, 476, 3))(x)
top_model = Model(input_, output)

#model.add(InputLayer((640,480,3)))
#model.add(Conv2D(3, [5,5], kernel_initializer=SRM_kernel, padding="valid"))
#model.build()
print("ee")
"""

input_ = Input(shape=(640,480,3))

x = ZeroPadding2D((1,1), input_shape=(224, 224, 3), data_format='channels_last')(input_)
x = Conv2D(3, [5,5], kernel_initializer=SRM_kernel, padding="valid")(x)
#x = Dropout(0.5)(x)
#predict = Dense(1, activation='sigmoid')(x)

top_model = Model(input_, x)
top_model.summary()
"""

def lol():


    filters = tf.Variable(filters, dtype=tf.float32)

    #imgs = np.array(imgs, dtype=float)

    input = Input(shape=(150,150,3))
    #input = tf.Variable(imgs, dtype=tf.float32)



    op = tf.nn.conv2d(input, filters, strides=[1, 1, 1, 1], padding='SAME')
    #kernel = K.variable(filters, dtype=tf.float32)

    #print(kernel)


    #print(tf.shape(op))
    input_ = Input(op)


    #output = Conv2D(128, kernel_size=(3, 3), activation='relu')(input_)
    x = Dense(256, activation='relu')(input_)
    x = Dropout(0.5)(x)
    predict = Dense(1, activation='sigmoid')(x)

    top_model = Model(input, predict)
    top_model.summary()