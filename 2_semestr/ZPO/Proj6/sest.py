from keras.models import Sequential
from keras.layers import Conv2D

import numpy as np

# Keras version of this example:
# https://stackoverflow.com/questions/34619177/what-does-tf-nn-conv2d-do-in-tensorflow
# Requires a custom kernel initialise to set to value from example
# kernel = [[1,0,1],[2,1,0],[0,0,1]]
# image = [[4,3,1,0],[2,1,0,1],[1,2,4,1],[3,1,0,2]]
# output = [[14, 6],[6,12]] 

#Set Image
image = [[4,3,1,0],[2,1,0,1],[1,2,4,1],[3,1,0,2]]

# Pad to "channels_last" format 
# which is [batch, width, height, channels]=[1,4,4,1]
image = np.expand_dims(np.expand_dims(np.array(image),2),0)

#Initialise to set kernel to required value
def kernel_init(shape):
    kernel = np.zeros(shape)
    kernel[:,:,0,0] = np.array([[1,0,1],[2,1,0],[0,0,1]])
    print(kernel)
    return kernel

#Build Keras model
model = Sequential()
model.add(Conv2D(1, [3,3], kernel_initializer=kernel_init, 
                 input_shape=(4,4,1), padding="valid"))
model.build()

# To apply existing filter, we use predict with no training
out = model.predict(image)
print(out)
print(out[0,:,:,0])