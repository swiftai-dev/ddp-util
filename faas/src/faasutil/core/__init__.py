"""Core package for FaaS utilities."""

from .domain.function import ServerlessFunction
from .ports import DeploymentPort, InvocationPort, MonitoringPort, ProviderConfig

__all__ = [
    "ServerlessFunction",
    "DeploymentPort",
    "InvocationPort",
    "MonitoringPort",
    "ProviderConfig",
]
