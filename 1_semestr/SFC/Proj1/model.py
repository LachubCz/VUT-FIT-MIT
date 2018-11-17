import numpy as np
import time

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def d_sigmoid(x):
    return x * (1 - x)

def tanh_prime(x):
    return 1 - np.tanh(x)**2

def relu(x):
    return np.max(0, x)

class neural_network():
    def __init__(self, input_shape, hidden_neurons, output_shape, learning_rate, momentum=0.9):
        self.first_l = np.random.normal(scale=0.1, size=(hidden_neurons, hidden_neurons))
        self.second_l = np.random.normal(scale=0.1, size=(hidden_neurons, output_shape))

        self.first_b = np.zeros(hidden_neurons)
        self.second_b = np.zeros(output_shape)

        self.learning_rate = learning_rate
        self.momentum = momentum

    def get_loss_grad(self, x, y):
        # forward
        A = np.dot(x, self.first_l) + self.first_b
        Z = sigmoid(A)

        B = np.dot(Z, self.second_l) + self.second_b
        Y = sigmoid(B)
        # backward
        ########## Phase 1
        Ew = Y - y

        p1 = np.dot(Z.T, Ew)

        ########## Phases 2
        p2 = np.dot(Y, self.second_b.T)

        dah_dzh = d_sigmoid(A)
        dcost_wh = np.dot(x.T, dah_dzh * p2)

        dcost_bh = p2 * dah_dzh

        """
        s2 = d_sigmoid(Y)
        s1 = d_sigmoid(Z)

        dY = Ew * s2

        Ev = dY.dot(self.second_l.T)

        dZ = Ev * s1
        """

        #Ev = tanh_prime(A) * np.dot(self.second_l, Ew)

        #dW = np.outer(Z, Ew)
        #dV = np.outer(x, Ev)

        loss = np.mean ( np.subtract(y, Y) **2)
        #print(dY.shape, self.second_l.shape, Z.shape)
        """
        self.first_l -= self.learning_rate * np.outer(x.T, dZ)
        self.first_b -= self.learning_rate * np.sum(dZ, axis=0, keepdims=True)
        self.second_l -= self.learning_rate * np.outer(Z.T, dY)
        self.second_b -= self.learning_rate * np.sum(dY, axis=0, keepdims=True)
        """
        
        """
        print(t)
        print("####")
        print(Y)
        """
        return loss, (dcost_wh, p1, dcost_bh.sum(axis=0), Ew.sum(axis=0))

    def fit(self, X, T):
        for epoch in range(1):
            err = []
            upd = [0,0,0,0] #pocet parametru

            t0 = time.clock()
            for i in range(X.shape[0]):
                loss, grad = self.get_loss_grad(X[i], T[i])
                self.first_l -= self.learning_rate * grad[0]
                self.second_l -= self.learning_rate * grad[1]
                self.first_b -= self.learning_rate * grad[2]
                self.second_b -= self.learning_rate * grad[3]
                """
                self.first_l -= upd[0]
                self.second_l -= upd[1]
                self.first_b -= upd[2]
                self.second_b -= upd[3]
                
                upd[0] = self.learning_rate * grad[0] + self.momentum * upd[0]
                upd[1] = self.learning_rate * grad[1] + self.momentum * upd[1]
                upd[2] = self.learning_rate * grad[2] + self.momentum * upd[2]
                upd[3] = self.learning_rate * grad[3] + self.momentum * upd[3]
                """
                err.append(loss)

        return(np.mean( err ))
        #print(err)

    def predict(self, x):
        temp_A = np.dot(x, self.first_l) + self.first_b
        temp_B = np.dot(sigmoid(temp_A), self.second_l) + self.second_b

        return sigmoid(temp_B)

"""
neural = neural_network(16, 16, 4, 0.1)

neural.train(np.array([[1, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0]]), np.array([[0, 0, 1, 0]]))

neural.train(np.array([[0, 0, 0, 0,
              1, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0]]), np.array([[0, 0, 1, 0]]))

neural.train(np.array([[0, 0, 0, 0,
              0, 0, 0, 0,
              1, 0, 0, 0,
              0, 0, 0, 0]]), np.array([[0, 0, 1, 0]]))

neural.train(np.array([[0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              1, 0, 0, 0]]), np.array([[0, 1, 0, 0]]))

neural.train(np.array([[0, 0, 0, 0,
              0, 0, 0, 0,
              0, 0, 0, 0,
              0, 1, 0, 0]]), np.array([[0, 1, 0, 0]]))

print(neural.predict(np.array([[1, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0]])))
"""