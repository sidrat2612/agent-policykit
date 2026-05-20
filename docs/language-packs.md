# Language Packs

This page is for teams checking stack coverage before adopting `agent-policykit`.

Language packs inject language-specific coding rules into the shared policy bundle so generated instructions stay relevant to Python, TypeScript, Java, Go, and the rest of the supported catalog.

## Implemented packs

The repository currently ships all 28 language packs listed in the project specification:

- Python
- JavaScript
- TypeScript
- Java
- Go
- C#
- PHP
- Ruby
- Kotlin
- Scala
- Rust
- C
- C++
- Zig
- Swift
- Objective-C
- Dart
- Groovy
- Elixir
- Erlang
- R
- Julia
- Bash
- PowerShell
- Haskell
- F#
- Clojure
- Lua

Each language pack is declarative YAML under `src/agent_policykit/packs/languages/` and is loaded by `core/loader.py`.

## Pack structure

Language packs can provide rule lists such as:

- `api_rules`
- `service_rules`
- `data_rules`
- `method_rules`
- `error_handling_rules`
- `logging_rules`
- `concurrency_rules`
- `testing_rules`
- `security_checklist`
- `anti_patterns`

## Detection coverage

Language detection now covers the full shipped pack inventory through file extensions and common project markers such as `build.sbt`, `build.zig`, `Package.swift`, `pubspec.yaml`, `mix.exs`, `rebar.config`, `deps.edn`, `*.fsproj`, and `*.rockspec`.
