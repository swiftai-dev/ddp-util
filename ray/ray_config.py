import os
from pathlib import Path

from dotenv import load_dotenv


def load_ray_config():
    """Load Ray configuration from .env file"""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)

    head_ip = os.getenv("RAY_HEAD_IP")
    client_port = os.getenv("RAY_CLIENT_PORT")

    if not head_ip or not client_port:
        raise ValueError("RAY_HEAD_IP and RAY_CLIENT_PORT must be set in .env file")

    return f"ray://{head_ip}:{client_port}"
