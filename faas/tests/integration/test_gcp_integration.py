"""Integration tests for GCP functionality."""

import os
import time

import pytest

from faasutil.core.domain import ProviderConfig, ServerlessFunction
from faasutil.core.ports import DeploymentPort, InvocationPort
from faasutil.providers.gcp import GCPProvider


@pytest.mark.integration
@pytest.fixture(scope="module")
def gcp_provider() -> GCPProvider:
    """Create GCP provider with credentials from environment."""
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        pytest.skip("GCP_PROJECT_ID environment variable not set")

    return GCPProvider(
        ProviderConfig(
            name="gcp",
            credentials={"project_id": project_id},
            region=os.getenv("GCP_REGION", "us-central1"),
        )
    )


@pytest.mark.integration
@pytest.fixture
def test_function() -> ServerlessFunction:
    """Test function configuration."""
    return ServerlessFunction(
        name=f"test-function-{int(time.time())}",
        runtime="python311",
        handler="main.handler",
        environment={"TEST_ENV": "value"},
        timeout=60,
        memory=256,
    )


@pytest.mark.integration
def test_full_workflow(gcp_provider: GCPProvider, test_function: ServerlessFunction) -> None:
    """Test deploy -> invoke -> delete workflow."""
    deployment = gcp_provider.get_deployment_adapter()
    invocation = gcp_provider.get_invocation_adapter()

    # Deploy function
    operation_id = deployment.deploy_function(test_function)
    assert operation_id is not None

    # Wait for deployment to complete
    time.sleep(30)  # Give time for deployment to complete

    # Invoke function
    response = invocation.invoke_function(test_function.name, {"test": "data"})
    assert response["status"] == "success"
    assert "Hello World" in response["response"]  # Basic function response

    # Clean up - delete function
    assert deployment.delete_function(test_function.name)


@pytest.mark.integration
def test_nonexistent_function(gcp_provider: GCPProvider) -> None:
    """Test behavior with non-existent function."""
    invocation = gcp_provider.get_invocation_adapter()
    response = invocation.invoke_function("nonexistent-function", {})
    assert response["status"] == "error"
    assert "NOT_FOUND" in response["message"]
