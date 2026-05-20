"""Configuration loading from pyproject.toml [tool.agent-policykit]."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from agent_policykit.types import AgentTarget, ProjectType


@dataclass
class Config:
    """Parsed configuration from [tool.agent-policykit] in pyproject.toml."""

    targets: list[AgentTarget] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    project_type: ProjectType | None = None
    review_mode: bool = False
    output_dir: Path = Path(".")

    @classmethod
    def from_pyproject(cls, project_root: Path) -> Config:
        """Load config from pyproject.toml [tool.agent-policykit] section."""
        pyproject_path = project_root / "pyproject.toml"
        if not pyproject_path.exists():
            return cls()

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        tool_config = data.get("tool", {}).get("agent-policykit", {})
        if not tool_config:
            return cls()

        targets = []
        for t in tool_config.get("targets", []):
            try:
                targets.append(AgentTarget(t))
            except ValueError:
                pass

        project_type = None
        pt_value = tool_config.get("project_type")
        if pt_value:
            try:
                project_type = ProjectType(pt_value)
            except ValueError:
                pass

        return cls(
            targets=targets,
            languages=tool_config.get("languages", []),
            frameworks=tool_config.get("frameworks", []),
            project_type=project_type,
            review_mode=tool_config.get("review_mode", False),
            output_dir=Path(tool_config.get("output_dir", ".")),
        )
