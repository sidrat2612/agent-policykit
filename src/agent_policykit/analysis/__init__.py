"""Analysis module — project context detection."""

from agent_policykit.analysis.detector import detect_project_context
from agent_policykit.analysis.path_selector import (
	detect_source_paths,
	detect_test_paths,
	select_instruction_globs,
)
from agent_policykit.analysis.repo_detector import detect_repository

__all__ = [
	"detect_project_context",
	"detect_repository",
	"detect_source_paths",
	"detect_test_paths",
	"select_instruction_globs",
]
