import tensorflow as tf
import numpy as np
import tensorflow.keras.backend as K

from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Flatten, BatchNormalization, Activation, PReLU, add
from tensorflow.python.keras.layers.advanced_activations import LeakyReLU
from tensorflow.python.keras.layers.convolutional import Conv2D, Conv2DTranspose

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

filter1 = np.asarray(filter1, dtype=float) / 4
filter2 = np.asarray(filter2, dtype=float) / 12
filter3 = np.asarray(filter3, dtype=float) / 2
filters = [[filter1, filter1, filter1], [filter2, filter2, filter2], [filter3, filter3, filter3]]
filters = np.einsum('klij->ijlk', filters)
#filters = tf.Variable(filters, dtype=tf.float32)
#
##imgs = np.array([imgs], dtype=float)
#input_ = tf.Variable(imgs, dtype=tf.float32)
#op = 
#
#
inputs = Input(shape=(None, None, None), name='img')
outputs = tf.nn.conv2d(inputs, filters, strides=[1, 1, 1, 1], padding='SAME')

model = Model(inputs=inputs, outputs=outputs, name='mnist_model')



#model = Sequential()
#model.add(Input(shape = (None, None, None, None)))
#model.add()
#model.compile()
#