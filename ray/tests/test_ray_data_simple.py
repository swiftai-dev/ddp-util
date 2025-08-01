import os

import pandas as pd
import ray

from ray_config import load_ray_config

# Get Ray address
ray_address = load_ray_config()
print(f"Connecting to: {ray_address}")

# Initialize Ray
ray.init(
    address=ray_address,
    runtime_env={"pip": ["pyarrow", "pandas"]},
    namespace="simple_test",
)

# Create a simple dataset
df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})

# Convert to Ray Dataset
ds = ray.data.from_pandas(df)

# Simple operations
print("\nDataset Stats:")
print(f"Count: {ds.count()}")
print(f"Schema: {ds.schema()}")

# Try to read first row
print("\nFirst row:")
print(ds.take(1))

ray.shutdown()
