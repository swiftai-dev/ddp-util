# FAAS Utility

A Cloud Functions utility package following hexagonal architecture principles.

## Features

- Multi-provider support (currently GCP)
- Clean separation of core domain and provider implementations
- Type-safe interfaces for deployment and invocation

## Installation

```bash
pip install faasutil
```

## Usage

### Initializing a Provider

```python
from faasutil.core.domain import ProviderConfig
from faasutil.providers.gcp import GCPProvider

config = ProviderConfig(
    name="gcp",
    credentials={"project_id": "your-project-id"},
    region="us-central1"
)
provider = GCPProvider(config)
```

### Deploying a Function

```python
from faasutil.core.domain import ServerlessFunction

deployment = provider.get_deployment_adapter()
function = ServerlessFunction(
    name="my-function",
    runtime="python311",
    handler="main.handler",
    environment={"ENV_VAR": "value"}
)

deployment_id = deployment.deploy_function(function)
```

### Invoking a Function

```python
invocation = provider.get_invocation_adapter()
response = invocation.invoke_function("my-function", {"key": "value"})
```

## Architecture

The package follows hexagonal architecture principles:

1. **Core Domain**: Contains the business logic and interfaces
2. **Ports**: Define the interfaces for external interactions
3. **Adapters**: Implement the ports for specific providers

## Contributing

To add support for a new cloud provider:

1. Implement the DeploymentPort and InvocationPort interfaces
2. Create a provider factory class
3. Add tests for your implementation
