"""Tests for GCP deployment adapter."""

from unittest.mock import MagicMock, patch

import pytest
from google.api_core.operation import Operation
from google.cloud.functions_v2 import FunctionServiceClient

from src.faasutil.adapters.gcp.deployment import GCPDeploymentAdapter
from src.faasutil.core.domain.function import ServerlessFunction


@pytest.fixture
def mock_gcp_client():
    with patch("google.cloud.functions_v2.FunctionServiceClient") as mock:
        yield mock


@pytest.fixture
def deployment_adapter(mock_gcp_client):
    return GCPDeploymentAdapter(project_id="test-project")


@pytest.fixture
def sample_function():
    return ServerlessFunction(
        name="test-function",
        runtime="python311",
        handler="main.handler",
        environment={"KEY": "value"},
    )


def test_deploy_function(deployment_adapter, mock_gcp_client, sample_function):
    mock_client = mock_gcp_client.return_value
    mock_operation = MagicMock(spec=Operation)
    mock_operation.operation.name = "test-operation"
    mock_client.create_function.return_value = mock_operation

    result = deployment_adapter.deploy_function(sample_function)
    assert result == "test-operation"
    mock_client.create_function.assert_called_once()


def test_update_function(deployment_adapter, mock_gcp_client, sample_function):
    mock_client = mock_gcp_client.return_value
    mock_operation = MagicMock(spec=Operation)
    mock_operation.operation.name = "test-operation"
    mock_client.update_function.return_value = mock_operation

    result = deployment_adapter.update_function(sample_function)
    assert result == "test-operation"
    mock_client.update_function.assert_called_once()


def test_delete_function(deployment_adapter, mock_gcp_client):
    mock_client = mock_gcp_client.return_value
    result = deployment_adapter.delete_function("test-function")
    assert result is True
    mock_client.delete_function.assert_called_once()
