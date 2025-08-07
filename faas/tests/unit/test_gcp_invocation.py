"""Tests for GCP invocation adapter."""

from unittest.mock import MagicMock, patch

import pytest
from google.cloud.functions_v1 import CloudFunctionsServiceClient

from src.faasutil.adapters.gcp.invocation import GCPInvocationAdapter


@pytest.fixture
def mock_gcp_client():
    with patch("google.cloud.functions_v1.CloudFunctionsServiceClient") as mock:
        yield mock


@pytest.fixture
def invocation_adapter(mock_gcp_client):
    return GCPInvocationAdapter(project_id="test-project")


def test_successful_invocation(invocation_adapter, mock_gcp_client):
    mock_client = mock_gcp_client.return_value
    mock_response = MagicMock()
    mock_response.result = "test result"
    mock_client.call_function.return_value = mock_response

    result = invocation_adapter.invoke_function("test-function", {"key": "value"})
    assert result["status"] == "success"
    assert result["response"] == "test result"
    mock_client.call_function.assert_called_once()


def test_failed_invocation(invocation_adapter, mock_gcp_client):
    mock_client = mock_gcp_client.return_value
    mock_client.call_function.side_effect = Exception("test error")

    result = invocation_adapter.invoke_function("test-function", {"key": "value"})
    assert result["status"] == "error"
    assert "test error" in result["message"]
