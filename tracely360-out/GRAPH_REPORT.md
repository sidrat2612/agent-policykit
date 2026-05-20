# Graph Report - .  (2026-05-20)

## Corpus Check
- Corpus is ~12,361 words - fits in a single context window. You may not need a graph.

## Summary
- 460 nodes · 1542 edges · 7 clusters detected
- Extraction: 32% EXTRACTED · 68% INFERRED · 0% AMBIGUOUS · INFERRED: 1041 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Cluster Hubs (Navigation)
- [[_CLUSTER_Cluster 0|Cluster 0]]
- [[_CLUSTER_Cluster 1|Cluster 1]]
- [[_CLUSTER_Cluster 2|Cluster 2]]
- [[_CLUSTER_Cluster 3|Cluster 3]]
- [[_CLUSTER_Cluster 4|Cluster 4]]
- [[_CLUSTER_Cluster 5|Cluster 5]]
- [[_CLUSTER_Cluster 6|Cluster 6]]

## God Nodes (most connected - your core abstractions)
1. `PolicyBundle` - 102 edges
2. `AgentTarget` - 94 edges
3. `AdapterOutput` - 83 edges
4. `ProjectContext` - 81 edges
5. `RuleCategory` - 80 edges
6. `MergeStrategy` - 75 edges
7. `Rule` - 73 edges
8. `Severity` - 68 edges
9. `RulePack` - 65 edges
10. `ProjectType` - 61 edges

## Surprising Connections (you probably didn't know these)
- `test_load_language_pack()` --calls--> `load_language_pack()`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/core/loader.py
- `test_load_framework_pack()` --calls--> `load_framework_pack()`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/core/loader.py
- `test_load_project_type_pack()` --calls--> `load_project_type_pack()`  [INFERRED]
  tests/test_loader.py → src/agent_policykit/core/loader.py
- `TestLanguageDetector` --uses--> `ProjectType`  [INFERRED]
  tests/test_analysis.py → src/agent_policykit/types.py
- `TestLanguageDetector` --uses--> `AgentTarget`  [INFERRED]
  tests/test_analysis.py → src/agent_policykit/types.py

## Hyperedges (group relationships)
- **Supported Languages** — lang_python, lang_javascript, lang_typescript, lang_java, lang_go, lang_csharp, lang_php, lang_ruby, lang_rust [INFERRED]
- **Supported Frameworks** — framework_fastapi, framework_django, framework_flask, framework_express, framework_nestjs, framework_nextjs, framework_spring_boot, framework_aspnet, framework_laravel, framework_rails [INFERRED]
- **Supported Project Types** — ptype_api_service, ptype_web_app, ptype_mobile_app, ptype_worker, ptype_cli_tool, ptype_sdk, ptype_microservice, ptype_monolith, ptype_data_pipeline [INFERRED]
- **Rule Categories** — rule_governance, rule_security, rule_compliance, rule_architecture, rule_review, rule_testing, rule_operations, rule_language, rule_framework, rule_project_type [INFERRED]
- **Core Engine Modules** — module_core_loader, module_core_merger, module_core_validator, module_core_renderer, module_core_diff_engine, module_core_update_engine, module_core_policy_engine [INFERRED]
- **Analysis and Detection Modules** — analyzer_repo_detector, analyzer_language_detector, analyzer_framework_detector, analyzer_project_type_detector, analyzer_path_selector [INFERRED]
- **Tier 1 Agent Adapters** — adapter_copilot_repo, adapter_copilot_path, adapter_agents_md, adapter_cursor, adapter_claude_code, adapter_aider, adapter_codex, adapter_gemini_cli [INFERRED]

## Clusters

### Cluster 0 - "Cluster 0"
Cohesion: 0.0
Nodes (73): load_framework_pack(), load_governance_packs(), load_language_pack(), load_pack_file(), load_packs_from_directory(), load_project_type_pack(), _parse_category(), _parse_rules() (+65 more)

### Cluster 1 - "Cluster 1"
Cohesion: 0.0
Nodes (57): AgentsMdAdapter, AGENTS.md adapter — generates AGENTS.md for multi-agent support., Generates AGENTS.md for multi-agent systems (Copilot, Codex)., AiderAdapter, Aider adapter — generates .aider.conf.yml., Generates .aider.conf.yml for Aider., ClaudeCodeAdapter, Claude Code adapter — generates CLAUDE.md. (+49 more)

### Cluster 2 - "Cluster 2"
Cohesion: 0.0
Nodes (35): compute_diff(), DiffResult, _extract_managed_section(), FileDiff, Diff engine — compares current files with generated output., Generate a unified diff string., Extract content between managed markers, or None if not found., Represents the diff between existing and proposed content. (+27 more)

### Cluster 3 - "Cluster 3"
Cohesion: 0.0
Nodes (66): AGENTS.md, Aider, Claude Code, OpenAI Codex, GitHub Copilot (path-specific), GitHub Copilot (repo-wide), Cursor, Gemini CLI (+58 more)

### Cluster 4 - "Cluster 4"
Cohesion: 0.0
Nodes (39): detect(), diff(), init(), main(), CLI entry point for agent-policykit., Update existing instruction files safely., Universal instruction compiler for coding agents., Show diff between current and regenerated instruction files. (+31 more)

### Cluster 5 - "Cluster 5"
Cohesion: 0.0
Nodes (25): generate(), Generate instruction files for configured agent targets., Adapter, Protocol that all output adapters must implement., Render the policy bundle into one or more output files., Check if this adapter handles the given target., _add_rule_to_bundle(), filter_bundle_by_severity() (+17 more)

### Cluster 6 - "Cluster 6"
Cohesion: 0.0
Nodes (13): detect_languages(), _iter_source_files(), Language detection from file extensions and config files., Detect programming languages present in the project.      Scans file extensions, Iterate source files, skipping hidden dirs and common non-source directories., detect_project_type(), Project type detection based on structure and configuration., Detect the project type based on file structure and frameworks.      Returns the (+5 more)

## Knowledge Gaps
- **55 isolated node(s):** `Shared enumerations and type aliases for agent-policykit.`, `Categories of rules in the policy system.`, `Severity levels for rules.`, `How an adapter merges with existing files.`, `Supported agent output targets.` (+50 more)
  These have ≤1 connection - possible missing edges or undocumented components.