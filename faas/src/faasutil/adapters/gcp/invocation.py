"""GCP Cloud Functions invocation adapter."""

from typing import Dict

from google.api_core.exceptions import GoogleAPICallError
from google.cloud import functions_v1

from ..core.ports import InvocationPort


class GCPInvocationAdapter(InvocationPort):
    """Implements InvocationPort for Google Cloud Functions."""

    def __init__(self, project_id: str, location: str = "us-central1"):
        self.client = functions_v1.CloudFunctionsServiceClient()
        self.parent = f"projects/{project_id}/locations/{location}"

    def invoke_function(self, function_name: str, payload: Dict) -> Dict:
        """Invoke a Google Cloud Function."""
        try:
            response = self.client.call_function(
                name=f"{self.parent}/functions/{function_name}", data=payload
            )
            return {"status": "success", "response": response.result}
        except GoogleAPICallError as e:
            return {"status": "error", "message": str(e)}
