# Dask Utils

A package of reusable Dask components that abstracts away the details of managing and deploying distributed computing workloads using Dask and its ecosystem of tools.

## Features

- Authentication to cloud providers (GCP currently supported)
- Cluster setup and management
- Deployment automation
- Monitoring integration

## Current Implementation

### GCP Support

- CloudProvider-based cluster management
- Coiled-based cluster management (experimental)
- Automated credential handling

### Testing

- Unit tests for core functionality
- Integration tests (require GCP credentials)
- Mocked cloud provider interactions

## Development Status

- Basic cluster operations implemented
- Initial test coverage in place
- Documentation in progress
