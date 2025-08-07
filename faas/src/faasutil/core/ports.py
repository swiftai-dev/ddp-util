"""Ports (interfaces) for hexagonal architecture."""

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class DeploymentPort(Protocol):
    """Interface for function deployment operations."""

    def deploy_function(self, function: "ServerlessFunction") -> str:  # noqa: F821
        """Deploy a serverless function.

        Returns deployment ID.
        """
        ...

    def update_function(self, function: "ServerlessFunction") -> str:  # noqa: F821
        """Update an existing function.

        Returns update ID.
        """
        ...

    def delete_function(self, function_name: str) -> bool:
        """Delete a function.

        Returns success status.
        """
        ...


@runtime_checkable
class InvocationPort(Protocol):
    """Interface for function invocation operations."""

    def invoke_function(self, function_name: str, payload: dict) -> dict:
        """Invoke a function with given payload.

        Returns function response.
        """
        ...


@runtime_checkable
class MonitoringPort(Protocol):
    """Interface for monitoring operations."""

    def get_logs(self, function_name: str, **filters: dict[str, Any]) -> list[dict]:
        """Get function logs.

        Returns list of log entries.
        """
        ...

    def get_metrics(self, function_name: str, **filters: dict[str, Any]) -> dict:
        """Get function metrics.

        Returns metrics data.
        """
        ...


@dataclass
class ProviderConfig:
    """Configuration for cloud provider."""

    name: str
    credentials: dict
    region: str
    additional_config: dict[str, Any] | None = None
