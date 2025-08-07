"""GCP provider implementation."""

from ..adapters.gcp.deployment import GCPDeploymentAdapter
from ..adapters.gcp.invocation import GCPInvocationAdapter
from ..core.domain import ProviderConfig
from ..core.ports import DeploymentPort, InvocationPort


class GCPProvider:
    """Factory for GCP adapters."""

    def __init__(self, config: ProviderConfig):
        if config.name != "gcp":
            raise ValueError("Invalid provider config - expected 'gcp'")
        self.config = config

    def get_deployment_adapter(self) -> DeploymentPort:
        """Get configured GCP deployment adapter."""
        return GCPDeploymentAdapter(
            project_id=self.config.credentials["project_id"],
            location=self.config.region,
        )

    def get_invocation_adapter(self) -> InvocationPort:
        """Get configured GCP invocation adapter."""
        return GCPInvocationAdapter(
            project_id=self.config.credentials["project_id"],
            location=self.config.region,
        )
