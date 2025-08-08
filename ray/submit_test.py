import os

import ray


def main():
    try:
        # Initialize Ray (will use cluster config automatically)
        ray.init()

        print("\nCluster resources:")
        print(ray.cluster_resources())

        # Test basic operation
        @ray.remote
        def test_func():
            return "Success"

        result = ray.get(test_func.remote())
        print(f"\nRemote function test: {result}")

        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    finally:
        ray.shutdown()


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
