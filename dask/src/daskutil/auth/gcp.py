"""GCP authentication module for Dask utilities."""

from typing import Any

from google.auth import default
from google.auth.exceptions import DefaultCredentialsError


class GCPAuth:
    """Handles GCP authentication with sensible defaults."""

    def __init__(self, project_id: str | None = None) -> None:
        """Initialize with optional project ID.

        Args:
            project_id: GCP project ID. If None, will attempt to detect from environment.

        """
        self.project_id = project_id

    def get_credentials(self) -> tuple[Any, str | None]:
        """Get GCP credentials and resolved project ID.

        Returns:
            Tuple of (credentials, project_id)

        Raises:
            DefaultCredentialsError: If no credentials could be found

        """
        try:
            credentials, project = default()
            return credentials, self.project_id or project
        except DefaultCredentialsError as e:
            raise DefaultCredentialsError(
                "Could not automatically determine credentials. "
                "Please set GOOGLE_APPLICATION_CREDENTIALS or "
                "configure Application Default Credentials."
            ) from e
