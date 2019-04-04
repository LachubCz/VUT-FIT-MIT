import argparse

import cv2
import numpy as np
import tensorflow as tf

from keras.models import Sequential, Model
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers import Input, Layer
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.applications.vgg16 import decode_predictions
from keras import backend as K

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--vgg_16', action="store", default="vgg16_weights_tf_dim_ordering_tf_kernels.h5", 
                        help="file with weigths for vgg_16 network")
    parser.add_argument('--img_width', action="store", type=int, default=150, 
                        help="width of images that goes into network")
    parser.add_argument('--img_height', action="store", type=int, default=150, 
                        help="height of images that goes into network")

    args = parser.parse_args()

    return args


def conv_layers_VGG_16(weights_path=None, pop_useless=True):
    model = Sequential()

    model.add(ZeroPadding2D((1,1), input_shape=(224, 224, 3), data_format='channels_last'))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(64, kernel_size=(3, 3), strides=1, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2), data_format='channels_last'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2), data_format='channels_last'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2), data_format='channels_last'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2), data_format='channels_last'))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2), data_format='channels_last'))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1000, activation='softmax'))

    if weights_path:
        model.load_weights(weights_path)
    
    if pop_useless:
        model.layers.pop()
        model.layers.pop()
        model.layers.pop()
        model.layers.pop()
        model.layers.pop()
        model.layers.pop()

    return model


class RoiPoolingConv(Layer):
    '''ROI pooling layer for 2D inputs.
    See Spatial Pyramid Pooling in Deep Convolutional Networks for Visual Recognition,
    K. He, X. Zhang, S. Ren, J. Sun
    # Arguments
        pool_size: int
            Size of pooling region to use. pool_size = 7 will result in a 7x7 region.
        num_rois: number of regions of interest to be used
    # Input shape
        list of two 4D tensors [X_img,X_roi] with shape:
        X_img:
        4D tensor with shape:
        `(1, rows, cols, channels)`.
        X_roi:
        `(1, num_rois, 4)` list of rois, with ordering (x, y, w, h)
    # Output shape
        A tensor with shape:
        `(1, num_rois, pool_size, pool_size, channels)`
    '''
    def __init__(self, pool_size, num_rois, **kwargs):
        self.pool_size = pool_size
        self.num_rois = num_rois
        super(RoiPoolingConv, self).__init__(**kwargs)

    
    def build(self, input_shape):
        self.nb_channels = input_shape[0][3]

    
    def compute_output_shape(self, input_shape):
        return None, self.num_rois, self.pool_size, self.pool_size, self.nb_channels

    def call(self, x, mask=None):
        assert(len(x) == 2)
        img = x[0]
        rois = x[1]
        input_shape = K.shape(img)
        outputs = []

        for roi_idx in range(self.num_rois):

            x = rois[0, roi_idx, 0]
            y = rois[0, roi_idx, 1]
            w = rois[0, roi_idx, 2]
            h = rois[0, roi_idx, 3]

            x = K.cast(x, 'int32')
            y = K.cast(y, 'int32')
            w = K.cast(w, 'int32')
            h = K.cast(h, 'int32')
            rs = tf.image.resize_images(
                img[:, y:y+h, x:x+w, :], 
                (self.pool_size, self.pool_size)
            )
            outputs.append(rs)

        final_output = K.concatenate(outputs, axis=0)
        final_output = K.reshape(final_output, (1, self.num_rois, self.pool_size, self.pool_size, self.nb_channels))

        final_output = K.permute_dimensions(final_output, (0, 1, 2, 3, 4))

        return final_output
    
    
    def get_config(self):
        config = {
            'pool_size': self.pool_size,
            'num_rois': self.num_rois
        }
        base_config = super(RoiPoolingConv, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


def SRM(imgs):
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
    filters = [[filter1, filter1, filter1], [filter2, filter2, filter2], [filter3, filter3, filter3]]
    filters = np.einsum('klij->ijlk', filters)
    print("Eeej: ", filters)
    filters = tf.Variable(filters, dtype=tf.float32)
    imgs = np.array(imgs, dtype=float)
    input = tf.Variable(imgs, dtype=tf.float32)
    op = tf.nn.conv2d(input, filters, strides=[1, 1, 1, 1], padding='SAME')

    q = [4.0, 12.0, 2.0]
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
    filter1 = np.asarray(filter1, dtype=float) / q[0]
    filter2 = np.asarray(filter2, dtype=float) / q[1]
    filter3 = np.asarray(filter3, dtype=float) / q[2]
    filters = [[filter1, filter1, filter1], [filter2, filter2, filter2], [filter3, filter3, filter3]]
    filters = np.einsum('klij->ijlk', filters)
    filters = filters.flatten()
    initializer_srm = tf.constant_initializer(filters)

    op2 = slim.conv2d(input, 3, [5, 5], trainable=False, weights_initializer=initializer_srm,
                      activation_fn=None, padding='SAME', stride=1, scope='srm')

    neg = ((op2 + 2) + abs(op2 + 2)) / 2 - 2
    op2 = -(-neg+2 + abs(- neg+2)) / 2 + 2

    filter_coocurr = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 1],
                      [0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0]]
    filter_coocurr_zero = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]
    filters_coocurr = [[filter_coocurr, filter_coocurr_zero, filter_coocurr_zero],
                       [filter_coocurr_zero, filter_coocurr, filter_coocurr_zero],
                       [filter_coocurr_zero, filter_coocurr_zero, filter_coocurr]]
    filters_coocurr = np.einsum('klij->ijlk', filters_coocurr)
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        re = (sess.run(op))
        res = np.round(re[0])
        res[res > 2] = 2
        res[res < -2] = -2

        res2 = sess.run(op2)
        # print(sum(sum(sum(sum(res2>2)))))
    ress2 = np.array(res2, dtype=float)
    ress = np.array([res], dtype=float)
    # input = tf.Variable(ress, dtype=tf.float32)
    # op = tf.nn.conv2d(input, filters_coocurr, strides=[1, 1, 1, 1], padding='SAME')
    # with tf.Session() as sess:
    #     sess.run(tf.initialize_all_variables())
    #     res = (sess.run(op))
    return ress#, ress2


def network():
    #im = cv2.resize(cv2.imread('2019-03-20-17-40-24-80.jpg'), (224, 224)).astype(np.float32)
    #im[:,:,0] -= 103.939
    #im[:,:,1] -= 116.779
    #im[:,:,2] -= 123.68
    #im = im.transpose((1,0,2))
    #im = np.expand_dims(im, axis=0)
    args = get_args()    

    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    #########
    #VGG_16 - rgb_conv_layers - sequentiel model
    rgb_conv_layers = conv_layers_VGG_16(args.vgg_16)
    rgb_conv_layers.compile(optimizer=sgd, loss='categorical_crossentropy')
    rgb_conv_layers.summary()
    #out = rgb_conv_layers.predict(im)
    #predictions = decode_predictions(out)
    #########

    #########
    #VGG_16 - noise_conv_layers - sequentiel model
    #noise_conv_layers = conv_layers_VGG_16(args.vgg_16)
    #rgb_conv_layers.compile(optimizer=sgd, loss='categorical_crossentropy')
    #rgb_conv_layers.summary()
    #########

    #########
    #API model
    input_ = Input(batch_shape=rgb_conv_layers.output_shape)
    x = Dense(256, activation='relu')(input_)
    x = Dropout(0.5)(x)
    predict = Dense(1, activation='sigmoid')(x)
    api_model = Model(input_, predict)
    api_model.summary()
    #########

    #########
    #Connected models
    rbg_stream_input = Input(shape=(args.img_width, args.img_height, 3))
    x = rgb_conv_layers(rbg_stream_input)
    predict = api_model(x)
    model = Model(rbg_stream_input, predict)
    model.summary()
    #########

if __name__ == "__main__":
    main()
    """
    input_ = SRM(x)

    input_ = Input(shape=(150,150,3))

    x = Dense(256, activation='relu')(input_)
    x = Dropout(0.5)(x)
    predict = Dense(1, activation='sigmoid')(x)

    top_model = Model(input_, predict)
    top_model.summary()
    """