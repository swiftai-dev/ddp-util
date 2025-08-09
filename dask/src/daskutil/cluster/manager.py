"""Base cluster manager interface for Dask utilities."""

from abc import ABC, abstractmethod
from typing import Any

from dask.distributed import Client


class BaseClusterManager(ABC):
    """Abstract base class for cluster managers."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        """Initialize with optional configuration.

        Args:
            config: Dictionary of configuration parameters

        """
        self.config = config or {}

    @abstractmethod
    def create_cluster(self) -> Any:
        """Create and return a cluster instance."""

    @abstractmethod
    def get_client(self) -> Client:
        """Get a Dask client connected to the cluster."""

    @abstractmethod
    def scale(self, n_workers: int) -> None:
        """Scale the cluster to the specified number of workers."""

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the cluster and clean up resources."""
