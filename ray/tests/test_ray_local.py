import numpy as np
import pandas as pd
import ray

# Initialize Ray without specifying an address (will try to use the cluster)
if not ray.is_initialized():
    ray.init()

print("Ray Cluster Resources:", ray.cluster_resources())

# Create a simple dataset
df = pd.DataFrame({"value": np.random.rand(1000)})

# Convert to Ray Dataset
ds = ray.data.from_pandas(df)

# Perform a simple computation
result = ds.map(lambda x: {"value": x["value"] * 2})

print("\nFirst few results:")
result.show(5)

ray.shutdown()
