import numpy as np
import nmslib
from sklearn.decomposition import PCA
import time
import csv

# 1. Load Your Data (replace this with actual loading code)
# Simulating the dataset (1,000,000 base points, 200 dimensions)
base_data = np.random.rand(1000000, 200)  # Replace with actual data loading
query_data = np.random.rand(5000, 200)  # Replace with actual query data

# Simulate ground truth nearest neighbors (for illustration purposes)
# In reality, you would have true nearest neighbors, possibly computed using an exact method
ground_truth_neighbors = np.random.randint(0, 1000000, size=(5000, 10))  # Simulated ground truth for each query

# 2. Dimensionality Reduction with PCA (reduce to 50 or 100 dimensions)
pca = PCA(n_components=100)  # You can try different numbers like 50 or 100
reduced_base_data = pca.fit_transform(base_data)
reduced_query_data = pca.transform(query_data)

print(f"Base Data Shape After PCA: {reduced_base_data.shape}")
print(f"Query Data Shape After PCA: {reduced_query_data.shape}")

# 3. Create HNSW Index (for ANN)
index = nmslib.init(method='hnsw', space='l2')  # 'l2' is for Euclidean distance
index.addDataPointBatch(reduced_base_data)  # Adding the base data to the index

# Tune parameters for HNSW index construction
index.createIndex({'M': 32, 'efConstruction': 400}, print_progress=True)

# 4. Set Query Time Parameters to optimize recall (increase efSearch for higher recall)
index.setQueryTimeParams({'efSearch': 200})

# 5. Measure Performance (Run the queries and calculate QPS)

# Start timing
start_time = time.time()

# Query 5,000 points in batches (batch size can be tuned for better performance)
batch_size = 500
all_neighbors = []

for i in range(0, len(reduced_query_data), batch_size):
    batch = reduced_query_data[i:i + batch_size]
    neighbors = index.knnQueryBatch(batch, k=10)  # Find 10 nearest neighbors for each query
    all_neighbors.extend(neighbors)

# End timing
end_time = time.time()

# Calculate total time and Queries Per Second (QPS)
total_time = end_time - start_time
qps = len(reduced_query_data) / total_time

print(f"Total time: {total_time:.2f} seconds")
print(f"QPS (Queries Per Second): {qps:.2f}")

# 6. Calculate Recall (using simulated ground truth)
correct_neighbors = 0
total_neighbors = 0

for i in range(len(all_neighbors)):
    predicted_neighbors = set(all_neighbors[i][0])  # The indices of the predicted neighbors
    actual_neighbors = set(ground_truth_neighbors[i])  # Simulated ground truth neighbors

    # Count how many predicted neighbors are in the ground truth
    correct_neighbors += len(predicted_neighbors.intersection(actual_neighbors))
    total_neighbors += 10  # We're looking for the top 10 neighbors for each query

# Calculate Recall 10@10
recall = correct_neighbors / total_neighbors
print(f"Recall 10@10: {recall:.2f}")

# 7. Log Parameters, Results, and Recall to a CSV file
parameters = ['batch_size', 'efSearch', 'M', 'PCA_components', 'total_time', 'QPS', 'Recall_10@10']
results = [batch_size, 200, 32, 100, total_time, qps, recall]

with open('experiment_results.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    
    # Uncomment this if writing the header for the first time
    # writer.writerow(parameters)
    
    writer.writerow(results)

# Optional: Check neighbors for the first query point
print(f"Indices of nearest neighbors for first query point: {all_neighbors[0][0]}")
print(f"Distances to nearest neighbors for first query point: {all_neighbors[0][1]}")
