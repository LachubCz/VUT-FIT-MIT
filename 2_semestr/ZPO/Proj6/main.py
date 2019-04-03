from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
import cv2, numpy as np


def VGG_16(weights_path=None):
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
    
    model.layers.pop()
    model.layers.pop()
    model.layers.pop()
    model.layers.pop()
    model.layers.pop()
    model.layers.pop()

    return model

if __name__ == "__main__":
    from keras.applications.vgg16 import decode_predictions
    im = cv2.resize(cv2.imread('2019-03-20-17-40-24-80.jpg'), (224, 224)).astype(np.float32)
    im[:,:,0] -= 103.939
    im[:,:,1] -= 116.779
    im[:,:,2] -= 123.68
    im = im.transpose((1,0,2))
    im = np.expand_dims(im, axis=0)

    # Test pretrained model
    model = VGG_16('vgg16_weights_tf_dim_ordering_tf_kernels.h5')
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy')
    model.summary()
    out = model.predict(im)
    predictions = decode_predictions(out)
    #print(out)
    #print(predictions)