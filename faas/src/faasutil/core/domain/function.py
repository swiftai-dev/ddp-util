"""Core domain model for serverless functions."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class FunctionProtocol(Protocol):
    """Interface for serverless function operations."""

    def deploy(self, config: dict) -> str:
        """Deploy function with given configuration.
        Returns deployment ID.
        """
        ...

    def invoke(self, payload: dict) -> dict:
        """Invoke function with given payload.
        Returns function response.
        """
        ...


@dataclass
class ServerlessFunction:
    """Core domain model representing a serverless function."""

    name: str
    runtime: str
    handler: str
    environment: dict
    timeout: int = 30
    memory: int = 128
