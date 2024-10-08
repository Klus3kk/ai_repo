import nmslib
import numpy as np

# Assuming `reduced_data` is your base dataset with shape (1000000, 50)
# Create the HNSW index
index = nmslib.init(method='hnsw', space='l2')
index.addDataPointBatch(reduced_data)
index.createIndex({'post': 2}, print_progress=True)

# Query the index with the reduced query dataset (5000 queries)
neighbors = index.knnQueryBatch(reduced_query_data, k=10)  # Find 10 nearest neighbors

# Check results for the first query
print("Indices of nearest neighbors:", neighbors[0][0])
print("Distances to nearest neighbors:", neighbors[0][1])
