import tensorflow as tf
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# Load MNIST datasets
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# # Check the shapes of the dataset
# print(f"Train Images Shape: {train_images.shape}")
# print(f"Test Images Shape: {test_images.shape}")
# print(f"Train Labels Shape: {train_labels.shape}")

for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(train_images[i], cmap='gray')  # Display as grayscale image
    plt.title(f"Label: {train_labels[i]}")
    plt.axis('off')

plt.show()

# Normalize the images to a range between 0 and 1
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255

# Flatten the 28x28 images into 1D arrays (28*28 = 784)
train_images_flat = train_images.reshape(-1, 28*28)
test_images_flat = test_images.reshape(-1, 28*28)

# Check the new shapes
print(f"Flattened Train Images Shape: {train_images_flat.shape}")
print(f"Flattened Test Images Shape: {test_images_flat.shape}")


