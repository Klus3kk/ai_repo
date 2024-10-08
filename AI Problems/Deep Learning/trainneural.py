import random

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = 0

    def parameters(self):
        return []

class Neuron(Module):
    def __init__(self, nin, nonlin=True):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(0)
        self.nonlin = nonlin

    def __call__(self, x):
        act = sum((wi*xi for wi,xi in zip(self.w, x)), self.b)
        return act.relu() if self.nonlin else act

    def parameters(self):
        return self.w + [self.b]

class Layer(Module):
    def __init__(self, nin, nout, **kwargs):
        self.neurons = [Neuron(nin, **kwargs) for _ in range(nout)]

    def __call__(self, x):
        return [n(x) for n in self.neurons]

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]

class MLP(Module):
    def __init__(self, nin, nouts):
        sizes = [nin] + nouts
        self.layers = [Layer(sizes[i], sizes[i+1], nonlin=i<len(nouts)-1) for i in range(len(sizes)-1)]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)[0]  # Assuming single output from final layer for simplicity
        return x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def update_parameters(self, lr):
        for p in self.parameters():
            p.data -= lr * p.grad

# Example usage
def train_network():
    mlp = MLP(2, [3, 1])
    inputs = [Value(0.5), Value(-0.1)]
    target = Value(0.4)

    for epoch in range(100):
        output = mlp(inputs)
        loss = (output - target) ** 2
        mlp.zero_grad()
        loss.backward()
        mlp.update_parameters(0.01)
        print(f'Epoch {epoch}, Loss: {loss.data}')

train_network()