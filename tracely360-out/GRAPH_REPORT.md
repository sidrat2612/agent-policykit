# Graph Report - .  (2026-05-20)

## Corpus Check
- 71 files · ~72,173 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 636 nodes · 2106 edges · 17 clusters detected
- Extraction: 33% EXTRACTED · 67% INFERRED · 0% AMBIGUOUS · INFERRED: 1414 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Cluster Hubs (Navigation)
- [[_CLUSTER_Cluster 0|Cluster 0]]
- [[_CLUSTER_Cluster 1|Cluster 1]]
- [[_CLUSTER_Cluster 2|Cluster 2]]
- [[_CLUSTER_Cluster 3|Cluster 3]]
- [[_CLUSTER_Cluster 4|Cluster 4]]
- [[_CLUSTER_Cluster 5|Cluster 5]]
- [[_CLUSTER_Cluster 6|Cluster 6]]
- [[_CLUSTER_Cluster 7|Cluster 7]]
- [[_CLUSTER_Cluster 8|Cluster 8]]
- [[_CLUSTER_Cluster 9|Cluster 9]]
- [[_CLUSTER_Cluster 10|Cluster 10]]
- [[_CLUSTER_Cluster 11|Cluster 11]]
- [[_CLUSTER_Cluster 12|Cluster 12]]
- [[_CLUSTER_Cluster 13|Cluster 13]]
- [[_CLUSTER_Cluster 14|Cluster 14]]
- [[_CLUSTER_Cluster 15|Cluster 15]]
- [[_CLUSTER_Cluster 16|Cluster 16]]

## God Nodes (most connected - your core abstractions)
1. `PolicyBundle` - 127 edges
2. `AgentTarget` - 112 edges
3. `ProjectContext` - 112 edges
4. `AdapterOutput` - 107 edges
5. `RuleCategory` - 92 edges
6. `MergeStrategy` - 92 edges
7. `Rule` - 79 edges
8. `ProjectType` - 77 edges
9. `Severity` - 73 edges
10. `RulePack` - 53 edges

## Surprising Connections (you probably didn't know these)
- `test_load_project_type_pack()` --calls--> `load_project_type_pack()`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/core/loader.py
- `Tests for the YAML pack loader.` --uses--> `RuleCategory`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/types.py
- `Tests for loading individual pack files.` --uses--> `RuleCategory`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/types.py
- `Tests for loading all packs from a directory.` --uses--> `RuleCategory`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/types.py
- `Tests for the convenience governance pack loader.` --uses--> `RuleCategory`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/types.py

## Clusters

### Cluster 0 - "Cluster 0"
Cohesion: 0.0
Nodes (74): AgentsMdAdapter, AGENTS.md adapter — generates AGENTS.md for multi-agent support., Generates AGENTS.md for multi-agent systems (Copilot, Codex)., AiderAdapter, Aider adapter — generates CONVENTIONS.md and .aider.conf.yml., Generates Aider convention files., ClaudeCodeAdapter, Claude Code adapter — generates CLAUDE.md. (+66 more)

### Cluster 1 - "Cluster 1"
Cohesion: 0.0
Nodes (75): load_project_type_pack(), _parse_category(), _parse_rules(), _parse_severity(), YAML pack loader with schema validation., Load all YAML packs from a directory., Load all governance packs from the built-in packs directory., Load a specific language pack by name. (+67 more)

### Cluster 2 - "Cluster 2"
Cohesion: 0.0
Nodes (52): load_all_adapters(), Import all built-in adapters so they register themselves., compute_diff(), DiffResult, _extract_managed_section(), FileDiff, Diff engine — compares current files with generated output., Generate a unified diff string. (+44 more)

### Cluster 3 - "Cluster 3"
Cohesion: 0.0
Nodes (49): detect(), diff(), generate(), init(), main(), CLI entry point for agent-policykit., Generate and safely update agent-specific instruction files from one policy sour, Initialize agent-policykit config in the current repository. (+41 more)

### Cluster 4 - "Cluster 4"
Cohesion: 0.0
Nodes (31): _detect_existing_targets(), detect_project_context(), Unified project context detector — combines all analysis modules., Run full project analysis and return a ProjectContext.      Detects:     - Progr, Detect which agent targets already have config files in the project., detect_source_paths(), detect_subproject_paths(), detect_test_paths() (+23 more)

### Cluster 5 - "Cluster 5"
Cohesion: 0.0
Nodes (41): agent-policykit, agent-policykit CLI, Portable AGENTS.md, Aider, API Service, Claude Code, OpenAI Codex, GitHub Copilot Path-Scoped (+33 more)

### Cluster 6 - "Cluster 6"
Cohesion: 0.0
Nodes (19): load_framework_pack(), load_governance_packs(), load_language_pack(), load_pack_file(), load_packs_from_directory(), Tests for the YAML pack loader., Tests for language pack loading., Tests for framework pack loading. (+11 more)

### Cluster 7 - "Cluster 7"
Cohesion: 0.0
Nodes (22): Keep core governance/security in CLAUDE.md and move broader guidance into a shar, _split_shared_guidance(), _append_limit_warning(), apply_output_limits(), _condense_markdown_output(), _content_within_limits(), _is_markdown_like(), _MarkdownSection (+14 more)

### Cluster 8 - "Cluster 8"
Cohesion: 0.0
Nodes (9): Update existing instruction files safely., update(), _collect_dependencies(), detect_frameworks(), Framework detection from config files and dependencies., Detect frameworks used in the project.      Checks:     1. Presence of framework, Collect all dependency names from various package manager files., Tests for framework detection. (+1 more)

### Cluster 9 - "Cluster 9"
Cohesion: 0.0
Nodes (7): detect_languages(), _iter_source_files(), Language detection from file extensions and config files., Iterate source files, skipping hidden dirs and common non-source directories., Detect programming languages present in the project.      Scans file extensions, Tests for language detection., TestLanguageDetector

### Cluster 10 - "Cluster 10"
Cohesion: 0.0
Nodes (4): list_available_packs(), Policy engine — orchestrates pack selection, loading, and merging based on proje, List all available pack names by category., TestListAvailablePacks

### Cluster 11 - "Cluster 11"
Cohesion: 0.0
Nodes (6): Code of Conduct, Contribution Guide, GitHub Issues, GitHub Security Advisories, Security Policy, Support Guide

### Cluster 12 - "Cluster 12"
Cohesion: 0.0
Nodes (2): GET /health, health()

### Cluster 13 - "Cluster 13"
Cohesion: 0.0
Nodes (1): ApplicationController

### Cluster 14 - "Cluster 14"
Cohesion: 0.0
Nodes (0): 

### Cluster 15 - "Cluster 15"
Cohesion: 0.0
Nodes (0): 

### Cluster 16 - "Cluster 16"
Cohesion: 0.0
Nodes (0): 

## Knowledge Gaps
- **54 isolated node(s):** `End-to-end CLI tests.`, `Golden-path CLI tests.`, `ApplicationController`, `GET /health`, `Shared enumerations and type aliases for agent-policykit.` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin cluster `Cluster 13`** (2 nodes): `ApplicationController`, `application_controller.rb`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin cluster `Cluster 14`** (2 nodes): `page.tsx`, `Page()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin cluster `Cluster 15`** (2 nodes): `test_health.py`, `test_placeholder()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin cluster `Cluster 16`** (1 nodes): `routes.rb`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## API Endpoints
- 1 endpoint(s) detected

| Method | Path | Framework | Source |
|--------|------|-----------|--------|
| GET | `/health` | flask/fastapi | examples/fastapi-service/app/main.py L7 |