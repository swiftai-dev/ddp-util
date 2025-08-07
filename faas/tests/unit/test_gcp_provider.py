"""Tests for GCP provider."""

from unittest.mock import MagicMock, patch

import pytest

from src.faasutil.core.domain import ProviderConfig
from src.faasutil.providers.gcp import GCPProvider


@pytest.fixture
def gcp_config():
    return ProviderConfig(
        name="gcp", credentials={"project_id": "test-project"}, region="us-central1"
    )


@patch("src.faasutil.adapters.gcp.deployment.GCPDeploymentAdapter")
@patch("src.faasutil.adapters.gcp.invocation.GCPInvocationAdapter")
def test_gcp_provider(mock_invocation, mock_deployment, gcp_config):
    provider = GCPProvider(gcp_config)

    # Test deployment adapter creation
    deployment_adapter = provider.get_deployment_adapter()
    mock_deployment.assert_called_once_with(
        project_id="test-project", location="us-central1"
    )
    assert deployment_adapter == mock_deployment.return_value

    # Test invocation adapter creation
    invocation_adapter = provider.get_invocation_adapter()
    mock_invocation.assert_called_once_with(
        project_id="test-project", location="us-central1"
    )
    assert invocation_adapter == mock_invocation.return_value


def test_invalid_provider_config():
    with pytest.raises(ValueError, match="expected 'gcp'"):
        GCPProvider(ProviderConfig(name="aws", credentials={}, region="us-east-1"))
