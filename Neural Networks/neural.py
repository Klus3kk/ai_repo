import numpy as np

class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes 
        self.biases = [np.random.randn(y,1) for y in sizes[1:]] # Gaussian Distributions
        self.weights = [np.random.randn(y, x)
                        for x,y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        # Returns the output if "a" is input
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a 

def sigmoid(z):
    return 1.0/(1.0 + np.exp(-z))


net = Network([2, 3, 1]) # 2 neurons in the I layer, 3 neurons in the II layer, 1 neuron in the III layer


