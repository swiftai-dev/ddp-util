import os

import pandas as pd
import pyarrow as pa
import pyarrow.csv as pv
import ray

from ray_config import load_ray_config

print("Step 1: Initializing Ray...")
try:
    ray_address = load_ray_config()
    print(f"Connecting to: {ray_address}")
    ray.init(address=ray_address, runtime_env={"pip": ["pyarrow", "pandas"]})
    print("✓ Successfully connected to Ray cluster")
except Exception as e:
    print(f"✗ Failed to connect to Ray cluster: {str(e)}")
    raise

print("\nStep 2: Checking cluster resources...")
print(ray.cluster_resources())

print("\nStep 3: Creating a small test dataset...")
# First create a small DataFrame locally
test_df = pd.DataFrame({"source": [1, 2, 3, 4, 5], "target": [10, 20, 30, 40, 50]})

print("\nStep 4: Converting local DataFrame to Ray Dataset...")
try:
    ds = ray.data.from_pandas(test_df)
    print("✓ Successfully created Ray Dataset from Pandas")
    print("Dataset schema:", ds.schema())
except Exception as e:
    print("✗ Failed to create Ray Dataset:", str(e))
    raise

print("\nStep 5: Testing basic Ray Data operations...")
try:
    # Count operation
    print("Testing count()...")
    count = ds.count()
    print(f"✓ Count successful: {count} rows")

    # Take operation
    print("\nTesting take()...")
    first_rows = ds.take(2)
    print(f"✓ Take successful, first 2 rows: {first_rows}")

    # Map operation
    print("\nTesting map()...")
    ds_mapped = ds.map(
        lambda row: {"source": row["source"], "target": row["target"] * 2}
    )
    print("✓ Map operation successful")
    print("First few rows after map:")
    ds_mapped.show(2)

    # GroupBy operation
    print("\nTesting groupby()...")
    ds_grouped = ds.groupby("source").count()
    print("✓ GroupBy operation successful")
    print("Grouped results:")
    ds_grouped.show(2)

except Exception as e:
    print(f"✗ Operation failed: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    raise

print("\nStep 6: Testing CSV read operation...")
try:
    # First verify the file exists and check its content
    if not os.path.exists("edges.tsv"):
        raise FileNotFoundError("edges.tsv not found")

    print(f"File size: {os.path.getsize('edges.tsv')} bytes")

    # Try to read the first few lines to verify content
    with open("edges.tsv", "r") as f:
        print("First 3 lines of file:")
        for _ in range(3):
            print(f.readline().strip())

    # Set up CSV read options
    read_options = pv.ReadOptions(column_names=["source", "target"])
    parse_options = pv.ParseOptions(delimiter="\t")
    convert_options = pv.ConvertOptions(
        column_types={"source": pa.int64(), "target": pa.int64()}
    )

    # Try to read the CSV in smaller chunks
    print("\nAttempting to read the CSV file...")
    ds_csv = ray.data.read_csv(
        "edges.tsv",
        read_options=read_options,
        parse_options=parse_options,
        convert_options=convert_options,
    )

    print("\n✓ Successfully created dataset from CSV")
    print("Dataset schema:", ds_csv.schema())
    print("\nFirst few rows:")
    ds_csv.show(3)

    # Try a simple operation on the CSV dataset
    print("\nTesting count on CSV dataset...")
    csv_count = ds_csv.count()
    print(f"✓ CSV dataset has {csv_count} rows")

except Exception as e:
    print(f"\n✗ CSV read operation failed: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    raise

finally:
    print("\nCleaning up...")
    try:
        ray.shutdown()
        print("Ray shutdown successfully")
    except Exception as e:
        print(f"Error during Ray shutdown: {e}")
