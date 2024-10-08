import numpy as np

def cross_validation_split(data, k):
    np.random.shuffle(data)  # This line can be removed if shuffling is not desired in examples
    fold_size = len(data) // k
    folds = []

    for i in range(k):
        start, end = i * fold_size, (i + 1) * fold_size if i != k-1 else len(data)
        test = data[start:end]
        train = np.concatenate([data[:start], data[end:]])
        folds.append([train.tolist(), test.tolist()])

    return folds