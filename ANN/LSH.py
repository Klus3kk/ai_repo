# Locality-Sensitive Hashing (LSH) - one of the most popular methods for ANN
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.random_projection import GaussianRandomProjection

# Generate sample data (1000 points in 50 dimentions)
data = np.random.rand(1000, 50)

# Reduce the dimensions using Gaussian Random Projection
transformer = GaussianRandomProjection(n_components=10)
reduced_data = transformer.fit_transform(data)

# Perform Nearest Neighbors search
nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(reduced_data)
distances, indices = nbrs.kneighbors(reduced_data)

# Check nearest neighbors of the first data point
print(indices[0], distances[0])