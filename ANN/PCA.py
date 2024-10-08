# Principal Component Analysis (PCA)
from sklearn.decomposition import PCA
import tensorflow as tf
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import time

# Load MNIST datasets
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize the images to a range between 0 and 1
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255

# Flatten the 28x28 images into 1D arrays (28*28 = 784)
train_images_flat = train_images.reshape(-1, 28*28)
test_images_flat = test_images.reshape(-1, 28*28)

# Reduce dimensions from 784 to 50 using PCA
pca = PCA(n_components=50)
train_images_reduced = pca.fit_transform(train_images_flat)
test_images_reduced = pca.transform(test_images_flat)

# Check the shape of the reduced data
print(f"Reduced Train Images Shape: {train_images_reduced.shape}")
print(f"Reduced Test Images Shape: {test_images_reduced.shape}")

# Implementing ANN to find similar images
# Fit the NearestNeighbors model on the reduced training data
nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(train_images_reduced)

# Use a test image as a query to find similar images
query_image = test_images_reduced[0].reshape(1, -1)  # The first test image

# Find the 10 nearest neighbors to the query image
distances, indices = nbrs.kneighbors(query_image)

# Display the indices of the similar images
print("Indices of similar images:", indices[0])
print("Distances to similar images:", distances[0])

# Display the query image (from the test set)
plt.figure(figsize=(8, 8))
plt.subplot(1, 11, 1)
plt.imshow(test_images[0], cmap='gray')
plt.title("Query")
plt.axis('off')

# Display the 10 nearest neighbors (from the train set)
for i in range(10):
    plt.subplot(1, 11, i + 2)
    plt.imshow(train_images[indices[0][i]].reshape(28, 28), cmap='gray')
    plt.title(f"NN {i+1}")
    plt.axis('off')

plt.show()


# Measure the time taken to find neighbors for 1000 test images
start_time = time.time()

for i in range(1000):
    query_image = test_images_reduced[i].reshape(1, -1)
    nbrs.kneighbors(query_image)

end_time = time.time()

print(f"Time taken for 1000 queries: {end_time - start_time} seconds")
print(f"Average QPS (Queries Per Second): {1000 / (end_time - start_time)}")