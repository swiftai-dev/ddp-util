# Ray Cluster Usage Notes

## Client Mode Limitations

When using Ray in client mode (`ray://`):

- Basic operations like `count()` work reliably
- Many Ray Data operations (show, take, groupby) may fail with "Global node is not initialized"
- Performance may be suboptimal for data-intensive workloads

## Recommended Approaches

1. **For development/testing**:

   - Use basic operations that work in client mode
   - Keep datasets small
   - Use `count()` and simple transformations

2. **For production/full functionality**:
   - Connect directly using Redis address (`<head_ip>:6379`)
   - Run code directly on cluster nodes
   - Consider increasing object store memory

## Job Submission Methods

### 1. Using Ray Jobs API (Recommended)

```python
from ray.job_submission import JobSubmissionClient

client = JobSubmissionClient("http://<head_ip>:8265")
job_id = client.submit_job(
    entrypoint="python your_script.py",
    runtime_env={
        "working_dir": ".",
        "excludes": ["venv/*", "*.pyc", "__pycache__"],
        "pip": ["ray[default]", "pandas"]
    }
)
```

### 2. Using ray submit CLI

```bash
ray submit cluster_config.yaml --python=python3 your_script.py
```

### 3. Direct SSH Execution

```bash
ssh ubuntu@<head_ip> "python3 /path/to/your_script.py"
```

## Troubleshooting Tips

- Ensure cluster is running: `./run_ray_gcp.sh status`
- Check job status at: http://<head_ip>:8265
- For "Global node not initialized" errors, use Job API instead of client mode
