import os
import argparse
import tensorflow as tf
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import tensorflow.contrib.slim as slim
from timeit import default_timer as timer

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-path', action="store", required=True,
                        help='folder with input images')
    parser.add_argument('--output-path', action="store", required=True,
                        help='output folder for noisy images')

    args = parser.parse_args()

    return args


def srm_generator(list_of_images, input_path, output_path):
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
    filters = tf.Variable(filters, dtype=tf.float32)

    
    for i, item in enumerate(list_of_images):
        img = np.array(cv2.imread(os.path.join(input_path, item)), dtype=float)
        img = np.array([img], dtype=float)

        with tf.Session() as sess:
            input_ = tf.Variable(img, dtype=tf.float32)
            op = tf.nn.conv2d(input_, filters, strides=[1, 1, 1, 1], padding='SAME')
            sess.run(tf.initialize_all_variables())
            output = sess.run(op)

        output = np.round(output[0])
        output[output > 2] = 2
        output[output < -2] = -2

        output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(output_path, item), (output * 255).astype(np.uint8))




if __name__ == '__main__':
    args = get_args()

    image_list = os.listdir(args.input_path)

    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    srm_generator(image_list, args.input_path, args.output_path)
