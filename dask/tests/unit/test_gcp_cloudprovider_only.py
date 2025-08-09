"""Unit tests for GCP cloudprovider cluster manager (without Coiled dependencies)."""

from unittest.mock import Mock, patch

from dask_cloudprovider.gcp import GCPCluster
import pytest

from daskutil.auth.gcp import GCPAuth
from daskutil.cluster.gcp_cloudprovider import GCPCloudProviderCluster


class TestGCPCloudProviderCluster:
    """Test suite for GCPCloudProviderCluster."""

    @pytest.fixture
    def mock_auth(self):
        """Mock GCPAuth instance."""
        with patch("daskutil.cluster.gcp_cloudprovider.GCPAuth") as mock:
            mock.return_value.get_credentials.return_value = ("creds", "project")
            yield mock

    def test_init(self, mock_auth):
        """Test cluster initialization."""
        config = {"project_id": "test-project"}
        cluster = GCPCloudProviderCluster(config)

        assert cluster.config == config
        mock_auth.assert_called_once_with("test-project")

    @patch("daskutil.cluster.gcp_cloudprovider.GCPCluster")
    def test_create_cluster(self, mock_gcp_cluster, mock_auth):
        """Test cluster creation."""
        config = {
            "zone": "us-east1-b",
            "machine_type": "n2-standard-4",
            "n_workers": 2,
            "env_vars": {"TEST": "value"},
            "cluster_kwargs": {"extra_arg": "value"},
        }

        cluster = GCPCloudProviderCluster(config)
        result = cluster.create_cluster()

        mock_gcp_cluster.assert_called_once_with(
            projectid="project",
            zone="us-east1-b",
            machine_type="n2-standard-4",
            n_workers=2,
            env_vars={"TEST": "value"},
            extra_arg="value",
        )
        assert result == mock_gcp_cluster.return_value

    def test_get_client(self, mock_auth):
        """Test getting client from cluster."""
        with patch.object(GCPCloudProviderCluster, "create_cluster") as mock_create:
            cluster = GCPCloudProviderCluster({})
            client = cluster.get_client()

            mock_create.assert_called_once()
            assert client == mock_create.return_value.get_client.return_value

    def test_scale(self, mock_auth):
        """Test scaling cluster."""
        with patch.object(GCPCloudProviderCluster, "create_cluster") as mock_create:
            cluster = GCPCloudProviderCluster({})
            cluster.cluster = Mock()
            cluster.scale(5)

            cluster.cluster.scale.assert_called_once_with(5)

    def test_shutdown(self, mock_auth):
        """Test cluster shutdown."""
        with patch.object(GCPCloudProviderCluster, "create_cluster") as mock_create:
            cluster = GCPCloudProviderCluster({})
            cluster.cluster = Mock()
            cluster.shutdown()

            cluster.cluster.close.assert_called_once()
            assert cluster.cluster is None
