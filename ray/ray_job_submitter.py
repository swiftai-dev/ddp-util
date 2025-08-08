import ray
from ray.job_submission import JobSubmissionClient


def submit_ray_job(head_ip: str, script_path: str):
    """Submit a Python script as a Ray job to the cluster."""
    try:
        # Connect to the Ray cluster's job server
        client = JobSubmissionClient(f"http://{head_ip}:8265")

        # Submit the job
        job_id = client.submit_job(
            entrypoint=f"python {script_path}",
            runtime_env={
                "working_dir": ".",
                "excludes": ["venv/*", "*.pyc", "__pycache__"],
                "pip": ["ray[default]", "pandas"],
            },
        )

        print(f"Successfully submitted job with ID: {job_id}")
        print(f"Job status can be checked at: http://{head_ip}:8265")
        return job_id
    except Exception as e:
        print(f"Failed to submit job: {str(e)}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--head-ip", required=True, help="Cluster head node IP")
    parser.add_argument("--script", required=True, help="Path to Python script to run")
    args = parser.parse_args()

    submit_ray_job(args.head_ip, args.script)
