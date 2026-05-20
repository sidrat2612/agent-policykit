"""Shared enumerations and type aliases for agent-policykit."""

from enum import Enum


class RuleCategory(str, Enum):
    """Categories of rules in the policy system."""

    GOVERNANCE = "governance"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    ARCHITECTURE = "architecture"
    REVIEW = "review"
    TESTING = "testing"
    OPERATIONS = "operations"
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    PROJECT_TYPE = "project_type"
    OUTPUT_CONTRACT = "output_contract"


class Severity(str, Enum):
    """Severity levels for rules."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MergeStrategy(str, Enum):
    """How an adapter merges with existing files."""

    OVERWRITE = "overwrite"
    SECTION_MERGE = "section_merge"
    APPEND = "append"
    SKIP_IF_EXISTS = "skip_if_exists"


class AgentTarget(str, Enum):
    """Supported agent output targets."""

    COPILOT_REPO = "copilot"
    COPILOT_PATH = "copilot-path"
    AGENTS_MD = "agents-md"
    GENERIC_MARKDOWN = "generic-markdown"
    ROOCODE = "roocode"
    WINDSURF = "windsurf"
    ZED = "zed"
    WARP = "warp"
    JUNIE = "junie"
    DEVIN = "devin"
    AMP = "amp"
    AUGMENT_CODE = "augment-code"
    FACTORY = "factory"
    JULES = "jules"
    GOOSE = "goose"
    OPENCODE = "opencode"
    PHOENIX = "phoenix"
    SEMGREP = "semgrep"
    ONA = "ona"
    CURSOR = "cursor"
    CLAUDE_CODE = "claude-code"
    AIDER = "aider"
    CODEX = "codex"
    GEMINI_CLI = "gemini-cli"


class ProjectType(str, Enum):
    """Supported project types."""

    API_SERVICE = "api_service"
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    WORKER = "worker"
    CLI_TOOL = "cli_tool"
    SDK = "sdk"
    LIBRARY = "library"
    MONOLITH = "monolith"
    MONOREPO = "monorepo"
    MICROSERVICE = "microservice"
    DATA_PIPELINE = "data_pipeline"
