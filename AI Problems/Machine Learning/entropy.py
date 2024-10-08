import numpy as np 
def calculate_entropy(labels: list) -> float:
    _, counts = np.unique(labels, return_counts=True)
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return np.round(entropy, 4)