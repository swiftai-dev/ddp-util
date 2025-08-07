"""GCP Cloud Functions deployment adapter."""

from typing import Optional

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import functions_v2

from ..core.domain.function import ServerlessFunction
from ..core.ports import DeploymentPort


class GCPDeploymentAdapter(DeploymentPort):
    """Implements DeploymentPort for Google Cloud Functions."""

    def __init__(self, project_id: str, location: str = "us-central1"):
        self.client = functions_v2.FunctionServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"

    def deploy_function(self, function: ServerlessFunction) -> str:
        """Deploy a function to Google Cloud Functions."""
        try:
            operation = self.client.create_function(
                parent=self.parent, function=self._build_gcp_function(function)
            )
            return operation.operation.name
        except GoogleAPICallError as e:
            raise RuntimeError(f"Failed to deploy function: {e}")

    def update_function(self, function: ServerlessFunction) -> str:
        """Update an existing function in Google Cloud Functions."""
        try:
            operation = self.client.update_function(
                function=self._build_gcp_function(function)
            )
            return operation.operation.name
        except GoogleAPICallError as e:
            raise RuntimeError(f"Failed to update function: {e}")

    def delete_function(self, function_name: str) -> bool:
        """Delete a function from Google Cloud Functions."""
        try:
            self.client.delete_function(name=f"{self.parent}/functions/{function_name}")
            return True
        except GoogleAPICallError:
            return False

    def _build_gcp_function(
        self, function: ServerlessFunction
    ) -> functions_v2.Function:
        """Build GCP Function object from our domain model."""
        return functions_v2.Function(
            name=f"{self.parent}/functions/{function.name}",
            environment=function.environment,
            build_config=functions_v2.BuildConfig(
                runtime=function.runtime,
                entry_point=function.handler,
            ),
            service_config=functions_v2.ServiceConfig(
                available_memory=f"{function.memory}Mi",
                timeout_seconds=function.timeout,
            ),
        )
