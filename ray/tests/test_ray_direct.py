import pandas as pd
import ray

from ray_config import load_ray_config

if __name__ == "__main__":
    # Get the Ray address but extract just the IP
    ray_address = load_ray_config()  # This returns ray://IP:PORT
    head_ip = ray_address.split("//")[1].split(":")[0]

    print(f"Connecting to Ray head node at: {head_ip}")

    # Connect directly to the head node
    ray.init(
        address=f"ray://{head_ip}:10001",
        runtime_env={"pip": ["pyarrow", "pandas"]},
        _node_ip_address=head_ip,  # Explicitly set the node IP
        namespace="direct_test",
    )

    try:
        # Create a simple test dataset
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})

        # Convert to Ray Dataset
        print("\nCreating dataset...")
        ds = ray.data.from_pandas(df)

        print("\nDataset info:")
        print(f"Count: {ds.count()}")
        print(f"Schema: {ds.schema()}")

        print("\nTrying to read data...")
        batch = ds.take_batch()
        print("First batch:", batch)

    finally:
        ray.shutdown()
