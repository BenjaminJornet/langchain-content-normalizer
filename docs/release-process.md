# Release Process

This project uses semantic versioning while the API is pre-1.0.

## Checklist

1. Run `uv run ruff check .`.
2. Run `uv run pytest`.
3. Run `uv build`.
4. Update `CHANGELOG.md`.
5. Create a Git tag, for example `v0.1.1`.
6. Push the tag.
7. Create a GitHub release.
8. Publish to PyPI through the manual `Publish to PyPI` workflow.

## Smoke checks

```bash
uv run python examples/normalize_mcp_output.py
uv run python examples/build_vision_content.py
```

## Release notes format

```md
## vX.Y.Z

### Added

### Fixed

### Changed
```
