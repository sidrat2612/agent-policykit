"""Language detection from file extensions and config files."""

from __future__ import annotations

from pathlib import Path

# Map of file extensions to language identifiers
EXTENSION_MAP: dict[str, str] = {
    ".py": "python",
    ".pyi": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".java": "java",
    ".kt": "kotlin",
    ".go": "go",
    ".cs": "csharp",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c",
    ".hpp": "cpp",
    ".scala": "scala",
    ".zig": "zig",
    ".m": "objective_c",
    ".mm": "objective_c",
    ".dart": "dart",
    ".groovy": "groovy",
    ".ex": "elixir",
    ".exs": "elixir",
    ".erl": "erlang",
    ".hrl": "erlang",
    ".jl": "julia",
    ".sh": "bash",
    ".bash": "bash",
    ".ps1": "powershell",
    ".psm1": "powershell",
    ".hs": "haskell",
    ".lhs": "haskell",
    ".fs": "fsharp",
    ".fsi": "fsharp",
    ".fsx": "fsharp",
    ".clj": "clojure",
    ".cljs": "clojure",
    ".cljc": "clojure",
    ".lua": "lua",
    ".r": "r",
}

# Config files that confirm a language presence
LANGUAGE_MARKERS: dict[str, list[str]] = {
    "python": ["pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "requirements.txt"],
    "typescript": ["tsconfig.json", "tsconfig.base.json"],
    "javascript": ["package.json"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "go": ["go.mod", "go.sum"],
    "csharp": ["*.csproj", "*.sln"],
    "rust": ["Cargo.toml"],
    "ruby": ["Gemfile", "*.gemspec"],
    "kotlin": ["build.gradle.kts"],
    "php": ["composer.json"],
    "scala": ["build.sbt"],
    "zig": ["build.zig"],
    "swift": ["Package.swift"],
    "dart": ["pubspec.yaml"],
    "groovy": ["build.gradle"],
    "elixir": ["mix.exs"],
    "erlang": ["rebar.config"],
    "r": ["DESCRIPTION", "renv.lock"],
    "julia": ["Project.toml", "Manifest.toml"],
    "powershell": ["*.ps1", "*.psm1"],
    "haskell": ["stack.yaml", "cabal.project", "*.cabal"],
    "fsharp": ["*.fsproj"],
    "clojure": ["deps.edn", "project.clj", "bb.edn"],
    "lua": ["*.rockspec"],
}


def detect_languages(root: Path, max_depth: int = 3) -> list[str]:
    """Detect programming languages present in the project.

    Scans file extensions and looks for language-specific config files.
    Returns languages sorted by file count (most prevalent first).
    """
    language_counts: dict[str, int] = {}

    # Check for marker files at root level
    for language, markers in LANGUAGE_MARKERS.items():
        for marker in markers:
            if "*" in marker:
                if list(root.glob(marker)):
                    language_counts[language] = language_counts.get(language, 0) + 10
            elif (root / marker).exists():
                language_counts[language] = language_counts.get(language, 0) + 10

    # Scan source files up to max_depth
    for path in _iter_source_files(root, max_depth):
        ext = path.suffix.lower()
        lang = EXTENSION_MAP.get(ext)
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1

    # Sort by count descending
    sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
    return [lang for lang, _ in sorted_langs]


def _iter_source_files(root: Path, max_depth: int) -> list[Path]:
    """Iterate source files, skipping hidden dirs and common non-source directories."""
    skip_dirs = {
        ".git", ".venv", "venv", "node_modules", "__pycache__",
        ".tox", ".mypy_cache", "dist", "build", ".next", "target",
        "bin", "obj", ".idea", ".vscode",
    }
    results: list[Path] = []

    def _scan(path: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            for entry in path.iterdir():
                if entry.name.startswith(".") and entry.is_dir():
                    continue
                if entry.is_dir():
                    if entry.name not in skip_dirs:
                        _scan(entry, depth + 1)
                elif entry.is_file():
                    results.append(entry)
        except PermissionError:
            pass

    _scan(root, 0)
    return results
