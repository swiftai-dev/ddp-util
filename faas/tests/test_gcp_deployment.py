"""Tests for GCP deployment adapter."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

from google.api_core.operation import Operation
import pytest

from faasutil.adapters.gcp.deployment import GCPDeploymentAdapter
from faasutil.core.domain.function import ServerlessFunction


@pytest.fixture
def mock_gcp_client() -> Generator[MagicMock, None, None]:
    """Provide a mock GCP client for testing.

    Returns:
        Generator[MagicMock, None, None]: A mock FunctionServiceClient.

    """
    with patch("google.cloud.functions_v2.FunctionServiceClient") as mock:
        yield mock


@pytest.fixture
def deployment_adapter() -> GCPDeploymentAdapter:
    """Create a GCP deployment adapter for testing.

    Returns:
        GCPDeploymentAdapter: A configured deployment adapter.

    """
    return GCPDeploymentAdapter(project_id="test-project")


@pytest.fixture
def sample_function() -> ServerlessFunction:
    """Create a sample serverless function for testing.

    Returns:
        ServerlessFunction: A configured serverless function.

    """
    return ServerlessFunction(
        name="test-function",
        runtime="python311",
        handler="main.handler",
        environment={"KEY": "value"},
    )


def test_deploy_function(
    deployment_adapter: GCPDeploymentAdapter,
    mock_gcp_client: MagicMock,
    sample_function: ServerlessFunction,
) -> None:
    """Test successful function deployment.

    Args:
        deployment_adapter: The deployment adapter under test.
        mock_gcp_client: Mock for the GCP client.
        sample_function: Test function configuration.

    """
    mock_client = mock_gcp_client.return_value
    mock_operation = MagicMock(spec=Operation)
    mock_operation.operation.name = "test-operation"
    mock_client.create_function.return_value = mock_operation

    result = deployment_adapter.deploy_function(sample_function)
    assert result == "test-operation"
    mock_client.create_function.assert_called_once()


def test_update_function(
    deployment_adapter: GCPDeploymentAdapter,
    mock_gcp_client: MagicMock,
    sample_function: ServerlessFunction,
) -> None:
    """Test successful function update.

    Args:
        deployment_adapter: The deployment adapter under test.
        mock_gcp_client: Mock for the GCP client.
        sample_function: Test function configuration.

    """
    mock_client = mock_gcp_client.return_value
    mock_operation = MagicMock(spec=Operation)
    mock_operation.operation.name = "test-operation"
    mock_client.update_function.return_value = mock_operation

    result = deployment_adapter.update_function(sample_function)
    assert result == "test-operation"
    mock_client.update_function.assert_called_once()


def test_delete_function(
    deployment_adapter: GCPDeploymentAdapter,
    mock_gcp_client: MagicMock,
) -> None:
    """Test successful function deletion.

    Args:
        deployment_adapter: The deployment adapter under test.
        mock_gcp_client: Mock for the GCP client.

    """
    mock_client = mock_gcp_client.return_value
    result = deployment_adapter.delete_function("test-function")
    assert result is True
    mock_client.delete_function.assert_called_once()
