# Security

- YAML is parsed with `safe_load`; executable YAML tags are not supported.
- Treat specifications as untrusted input in CI.
- The compiler performs no network calls and executes no repository code.
- Repository-path validation checks existence only.
