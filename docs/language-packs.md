# Language Packs

## Implemented packs

The repository currently ships V1 language packs for:

- Python
- TypeScript
- Java
- Go
- C#

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

## Next expansion

The remaining planned packs include JavaScript, PHP, Ruby, Kotlin, Scala, Rust, C, C++, Zig, Swift, Objective-C, Dart, Groovy, Elixir, Erlang, R, Julia, Bash, PowerShell, Haskell, F#, Clojure, and Lua.
