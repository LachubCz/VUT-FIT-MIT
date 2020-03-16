"""
Utility used by the Network class to actually train.

Based on:
    https://github.com/fchollet/keras/blob/master/examples/mnist_mlp.py

"""
import numpy as np
import logging
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping
from keras import losses
from sklearn import metrics

# Helper: Early stopping.
early_stopper = EarlyStopping(patience=5)


def train_and_score(network, dataset, typeisch):
    """Train the model, return test loss.

    Args:
        network (dict): the parameters of the network
        dataset (str): Dataset to use for training/evaluating

    """
    nb_classes = 1
    epochs = 2500
    batch_size = 1024
    input_shape = (50,)

    model = compile_model(network, nb_classes, input_shape)
    X, Y = dataset.get_val_batch(typeisch)

    lowest = 1000000
    logging.info("#####################################")
    logging.info(network)
    for eps in range(epochs):
        X_trn, Y_trn = dataset.get_trn_minibatch(batch_size, typeisch)
        X_val, Y_val = dataset.get_val_batch(typeisch)

        history = model.fit(X_trn, Y_trn, epochs=1, verbose=0)

        predictions = model.predict(X)
        test = metrics.log_loss(Y, np.squeeze(predictions, axis=1))

        if test < lowest:
            logging.info("############ LogLoss: {}".format(test))
            model.save_weights("./{}-neural_network-{}.h5".format(typeisch, test))
            lowest = test
        if eps == 100:
            if lowest == 1000000:
                logging.info("This model doesn't learn.")
                break

    logging.info("############ LogLoss Final: {}".format(lowest))
    return lowest
