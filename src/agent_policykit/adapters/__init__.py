"""Adapter base protocol and registry."""

from __future__ import annotations

from typing import Protocol

from agent_policykit.core.models import AdapterOutput, PolicyBundle, ProjectContext
from agent_policykit.types import AgentTarget


class Adapter(Protocol):
    """Protocol that all output adapters must implement."""

    target: AgentTarget
    max_bytes: int | None
    max_lines: int | None

    def output_paths(self, context: ProjectContext) -> list[str]:
        """Return all output paths the adapter would generate for this context."""
        ...

    def render(self, bundle: PolicyBundle, context: ProjectContext) -> list[AdapterOutput]:
        """Render the policy bundle into one or more output files."""
        ...

    def supports_target(self, target: AgentTarget) -> bool:
        """Check if this adapter handles the given target."""
        ...


# Global adapter registry
_ADAPTER_REGISTRY: dict[AgentTarget, type] = {}


def register_adapter(target: AgentTarget):
    """Decorator to register an adapter class for a target."""
    def decorator(cls):
        _ADAPTER_REGISTRY[target] = cls
        return cls
    return decorator


def get_adapter(target: AgentTarget) -> Adapter:
    """Get an adapter instance for the given target."""
    adapter_cls = _ADAPTER_REGISTRY.get(target)
    if adapter_cls is None:
        raise ValueError(f"No adapter registered for target: {target.value}")
    instance: Adapter = adapter_cls()
    return instance


def list_adapters() -> list[AgentTarget]:
    """List all registered adapter targets."""
    return list(_ADAPTER_REGISTRY.keys())
