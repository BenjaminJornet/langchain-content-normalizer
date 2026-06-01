# Maintainers

## Primary maintainer

- Benjamin Jornet (`@BenjaminJornet`)

## Maintainer responsibilities

- Review pull requests that add new content shapes or provider adapters.
- Triage issues with reproducible input/output examples.
- Keep CI, packaging, and release workflows working.
- Preserve the zero-runtime-dependency contract unless a change is explicitly justified.
- Publish releases and update `CHANGELOG.md`.

## Review priorities

1. Unknown non-empty content must not be silently dropped.
2. Runtime dependencies should remain at zero.
3. Tests must cover each new block shape.
4. Public APIs should stay small and documented.
