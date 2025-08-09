"""Integration tests for GCP cloudprovider cluster manager."""

import os

from dask.distributed import Client
import pytest

from daskutil.cluster.gcp_cloudprovider import GCPCloudProviderCluster


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), reason="GCP credentials not available")
class TestGCPCloudProviderIntegration:
    """Integration test suite for GCPCloudProviderCluster."""

    @pytest.fixture
    def basic_config(self):
        """Basic test configuration."""
        return {
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "zone": "us-central1-a",
            "machine_type": "n1-standard-1",
            "n_workers": 1,
        }

    def test_cluster_lifecycle(self, basic_config):
        """Test full cluster lifecycle."""
        cluster = GCPCloudProviderCluster(basic_config)

        # Test cluster creation
        dask_cluster = cluster.create_cluster()
        assert dask_cluster is not None

        # Test client connection
        client = cluster.get_client()
        assert isinstance(client, Client)

        # Test scaling
        cluster.scale(2)

        # Test shutdown
        cluster.shutdown()
