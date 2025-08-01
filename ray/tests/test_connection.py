import sys

import ray

from ray_config import load_ray_config

# Print local versions first
print("Local environment:")
print(f"Python version: {sys.version}")
print(f"Ray version: {ray.__version__}")
try:
    import pyarrow

    print(f"PyArrow version: {pyarrow.__version__}")
except ImportError:
    print("PyArrow not installed locally")

try:
    import pandas

    print(f"Pandas version: {pandas.__version__}")
except ImportError:
    print("Pandas not installed locally")

# Connect to the cluster
print("\nConnecting to Ray cluster...")
ray_address = load_ray_config()
print(f"Connecting to: {ray_address}")
ray.init(address=ray_address)


# Check cluster versions
@ray.remote
def check_versions():
    import sys

    import ray

    versions = {
        "python": sys.version,
        "ray": ray.__version__,
    }
    try:
        import pyarrow

        versions["pyarrow"] = pyarrow.__version__
    except ImportError:
        versions["pyarrow"] = "not installed"

    try:
        import pandas

        versions["pandas"] = pandas.__version__
    except ImportError:
        versions["pandas"] = "not installed"

    return versions


print("\nCluster environment:")
cluster_versions = ray.get(check_versions.remote())
for k, v in cluster_versions.items():
    print(f"{k}: {v}")

ray.shutdown()
