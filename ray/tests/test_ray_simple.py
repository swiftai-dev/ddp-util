import pandas as pd
import ray

from ray_config import load_ray_config

# Initialize Ray
ray_address = load_ray_config()
print(f"Connecting to: {ray_address}")
ray.init(address=ray_address)

# Create a simple dataset
df = pd.DataFrame({"A": range(10), "B": range(10, 20)})

# Convert to Ray Dataset
ds = ray.data.from_pandas(df)

# Perform some operations
print("Dataset count:", ds.count())
print("\nFirst few rows:")
ds.show(3)

# Try a groupby operation
result = ds.groupby("A").count()
print("\nGroupby result:")
result.show(3)

# Clean up
ray.shutdown()
