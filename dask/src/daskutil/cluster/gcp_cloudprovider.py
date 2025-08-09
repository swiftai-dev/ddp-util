"""GCP cluster manager using dask-cloudprovider."""

from typing import Any

from dask.distributed import Client
from dask_cloudprovider.gcp import GCPCluster

from daskutil.auth.gcp import GCPAuth

from .manager import BaseClusterManager


class GCPCloudProviderCluster(BaseClusterManager):
    """GCP cluster manager using dask-cloudprovider."""

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize with GCP configuration.

        Args:
            config: Dictionary of GCP-specific configuration

        """
        super().__init__(config)
        self.auth = GCPAuth(config.get("project_id") if config else None)
        self.cluster = None

    def create_cluster(self) -> GCPCluster:
        """Create and return a GCPCluster instance."""
        credentials, project_id = self.auth.get_credentials()

        self.cluster = GCPCluster(
            projectid=project_id,
            zone=self.config.get("zone", "us-central1-a"),
            machine_type=self.config.get("machine_type", "n1-standard-1"),
            n_workers=self.config.get("n_workers", 1),
            env_vars=self.config.get("env_vars", {}),
            **self.config.get("cluster_kwargs", {}),
        )
        return self.cluster

    def get_client(self) -> Client:
        """Get a Dask client connected to the GCP cluster.

        Returns:
            A connected Dask Client instance

        Raises:
            RuntimeError: If cluster creation fails

        """
        if not self.cluster:
            self.create_cluster()
        if not self.cluster:
            raise RuntimeError("Failed to create GCP cluster")
        return self.cluster.get_client()

    def scale(self, n_workers: int) -> None:
        """Scale the GCP cluster."""
        if self.cluster:
            self.cluster.scale(n_workers)

    def shutdown(self) -> None:
        """Shutdown the GCP cluster."""
        if self.cluster:
            self.cluster.close()
            self.cluster = None
