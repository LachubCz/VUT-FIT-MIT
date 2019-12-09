from __future__ import print_function

# To plot graphs.
import numpy as np

import sys

from tools import collage
from tools import readCIFAR
from matplotlib import pyplot as plt


# Example showing how to train and use a Convolutional Neural Network in Keras.
#
# You need Keras, OpenCV and tensorflow
# Install the needed libraries by:
# pip install keras tensorflow matplotlib
# If you have cuda-capable GPU, install tensorflow-gpu to make the training
# much faster.
#
# You can use prepared environmenet on merlin.fit.vutbr.cz
# source /mnt/matylda1/hradis/POV/du03_env/bin/activate
#
# The code is compatible only with tensorflow backend. On Merlin, run it by:
# KERAS_BACKEND=tensorflow python du03.py
#
# The KERAS_BACKEND=tensorflow would not bee needed on your own machine as this
# would be specified in Keras configuration.
#
# Get the dataset first by:
# cd ./data
# ./downloadCIFAR.sh
#
# Feel free to experiment with the network to reach better accuracy.
# It is possible to get ~92% accuracy using larger network of similar arch.
# To compare to others, look at:
# http://rodrigob.github.io/are_we_there_yet/build/classification_datasets_results.html#43494641522d3130


# Define network.
# Input: batch of images 32x32x3
# Use ReLU nonlinearities after each layer with optimized parameters.
# Layers:
#   Convolution with 8 3x3 filters
#   Max-pooling with step 2 and pooling area 2x2
#   Convolution with 16 3x3 filters
#   Max-pooling with step 2 and pooling area 2x2
#   Fully connected layer with 256 neurons
#   Dropout with probability 15%
#   Fully connected layer with 256 neurons
#   Dropout with probability 15%
#   Fully connected layer with 10 neurons and softmax activation
# The last layer will produce probabilities for the 10 classes in CIFAR-10 and
# it is the output of the model.
def build_simple_network():
    # Thease are the layers you need for the network.
    # Documentation is at https://keras.io/layers/core/
    #
    # You can build either sequential model which is simple but restricts the
    # network to single input and single output.
    # https://keras.io/getting-started/sequential-model-guide/
    #
    # Or you can use functional API to build the network which is more
    # flexible and explicitly specifies connections between layers.
    # https://keras.io/getting-started/functional-api-guide/
    from keras.layers import Input, Dense, Dropout, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    from keras.models import Model, Sequential

    # FILL
    model = Sequential()

    model.add(Conv2D(8, (3, 3), strides=2, input_shape = (32, 32, 3), activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Conv2D(16, (3, 3), strides=2, activation = 'relu'))
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Flatten())
    model.add(Dense(256, activation = 'relu'))
    model.add(Dropout(0.15))
    model.add(Dense(256, activation = 'relu'))
    model.add(Dropout(0.15))
    model.add(Dense(10, activation = 'softmax'))

    return model


# Get the dataset first by:
# cd ./data
# ./downloadCIFAR.sh
def prepareData(downsample=1):
    # This reads the dataset.
    trnData, tstData, trnLabels, tstLabels = readCIFAR(
        './data/cifar-10-batches-py')
    print('\nDataset tensors')
    print('Training shapes: ', trnData.shape, trnLabels.shape)
    print('Testing shapes: ', tstData.shape, tstLabels.shape)
    print()

    # Convert images from RGB to BGR
    trnData = trnData[::downsample, :, :, ::-1]
    tstData = tstData[::downsample, :, :, ::-1]
    trnLabels = trnLabels[::downsample]
    tstLabels = tstLabels[::downsample]

    # Normalize data
    # This maps all values in trn. and tst. data to range <-0.5,0.5>.
    # Some kind of value normalization is preferable to provide
    # consistent behavior accross different problems and datasets.
    trnData = trnData.astype(np.float32) / 255.0 - 0.5
    tstData = tstData.astype(np.float32) / 255.0 - 0.5
    return trnData, tstData, trnLabels, tstLabels


def main():

    model = build_simple_network()
    print('Model summary:')
    model.summary()

    from keras import optimizers
    from keras import losses
    from keras import metrics
    model.compile(
        loss=losses.sparse_categorical_crossentropy,
        optimizer=optimizers.Adam(lr=0.001),
        metrics=[metrics.sparse_categorical_accuracy])


    trnData, tstData, trnLabels, tstLabels = prepareData()
    # Show 64 images from each set.
    trnCollage = collage(trnData[:64] + 0.5)
    tstCollage = collage(tstData[:64] + 0.5)
    
    plt.imshow(trnCollage)
    plt.title('Training data')
    plt.show()
    plt.imshow(tstCollage)
    plt.title('Testing data')
    plt.show()

    # Train the network for 5 epochs.
    model.fit(
        x=trnData, y=trnLabels,
        batch_size=64, epochs=5, verbose=1,
        validation_data=[tstData, tstLabels], shuffle=True)


    # To save the network use:
    model.save('model.h5')

    # Compute network predictions for the test set and show results.
    print('Compute model predictions for test images and display the results.')

    dataToTest = tstData[::20]

    # Compute network (model) responses for dataToTest input.
    # This should produce a 2D tensor of the 10 class probabilites for each
    # image in dataToTest. The subsequent code displays the predicted classes.
    # FILL
    classProb = model.predict(dataToTest)

    print('Prediction shape:', classProb.shape)

    classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog',
               'horse', 'ship', 'truck']
    predictedClasses = np.argmax(classProb, axis=1)
    for i in range(classProb.shape[1]):
        classImages = dataToTest[predictedClasses == i]
        if classImages.shape[0]:
            classCollage = collage(classImages)
            title = 'Predicted class {} - {}'.format(i, classes[i])
            plt.imshow(classCollage + 0.5)
            plt.title(title)
            plt.show()


    print('Evaluate network error outside of training.')
    loss, acc = model.evaluate(x=tstData, y=tstLabels, batch_size=64)
    print()
    print('Test loss', loss)
    print('Test accuracy', acc)


if __name__ == "__main__":
    main()
