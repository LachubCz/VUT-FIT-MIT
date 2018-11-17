import numpy as np  
import matplotlib.pyplot as plt
"""
np.random.seed(42)

cat_images = np.random.randn(700, 2) + np.array([0, -3])  
mouse_images = np.random.randn(700, 2) + np.array([3, 3])  
dog_images = np.random.randn(700, 2) + np.array([-3, 3])

feature_set = np.vstack([cat_images, mouse_images, dog_images])

labels = np.array([0]*700 + [1]*700 + [2]*700)

one_hot_labels = np.zeros((2100, 3))

for i in range(2100):  
    one_hot_labels[i, labels[i]] = 1

plt.figure(figsize=(10,7))  
plt.scatter(feature_set[:,0], feature_set[:,1], c=labels, cmap='plasma', s=100, alpha=0.5)  
plt.show()

"""
def linear(x):
  return x

def sigmoid(x):  
    return 1/(1+np.exp(-x))

def sigmoid_der(x):  
    return sigmoid(x) *(1-sigmoid (x))

def softmax(A):  
    expA = np.exp(A)
    return expA / expA.sum(axis=1, keepdims=True)

def relu(X):
    return np.maximum(X, 0)

def relu_derivative(X):
    return 1. * (X > 0)

class neural_network():
    def __init__(self, input_shape, hidden_neurons, output_shape, learning_rate):
        self.wh = np.random.rand(input_shape,hidden_neurons)  
        self.bh = np.random.randn(hidden_neurons)

        self.wo = np.random.rand(hidden_neurons,output_shape)  
        self.bo = np.random.randn(output_shape)  
        self.lr = learning_rate

    def fit(self, feature_set, one_hot_labels):
        error_cost = []

        for epoch in range(1):  
        ############# feedforward

            # Phase 1
            zh = np.dot(feature_set, self.wh) + self.bh
            ah = relu(zh)

            # Phase 2
            zo = np.dot(ah, self.wo) + self.bo
            ao = linear(zo)

        ########## Back Propagation

        ########## Phase 1

            dcost_dzo = ao - one_hot_labels
            dzo_dwo = ah

            dcost_wo = np.dot(dzo_dwo.T, dcost_dzo)

            dcost_bo = dcost_dzo

        ########## Phases 2

            dzo_dah = self.wo
            dcost_dah = np.dot(dcost_dzo , dzo_dah.T)
            dah_dzh = relu_derivative(zh)
            dzh_dwh = feature_set
            dcost_wh = np.dot(dzh_dwh.T, dah_dzh * dcost_dah)

            dcost_bh = dcost_dah * dah_dzh

            # Update Weights ================
            #print(self.wh, self.bh, self.wo, self.bo)
            self.wh -= self.lr * dcost_wh
            self.bh -= self.lr * dcost_bh.sum(axis=0)

            self.wo -= self.lr * dcost_wo
            self.bo -= self.lr * dcost_bo.sum(axis=0)

            if epoch % 200 == 0:
                loss = np.mean ( np.subtract(one_hot_labels, ao) **2)
                #print('Loss function value: ', loss)
                error_cost.append(loss)

    def predict(self, feature_set):
        zh = np.dot(feature_set, self.wh) + self.bh
        ah = relu(zh)

        # Phase 2
        zo = np.dot(ah, self.wo) + self.bo
        ao = linear(zo)

        return ao
"""
nn = neural_network(feature_set.shape[1], 4, 3, 10e-4)
nn.fit(feature_set, one_hot_labels)
print(nn.predict(feature_set))
"""