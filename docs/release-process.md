# Release Process

This project uses semantic versioning while the API is pre-1.0.

## Checklist

1. Merge feature PRs to `main` after CI, build, and smoke checks pass.
2. Run `python scripts/prepare-release.py X.Y.Z`.
3. Review `git diff` and commit the release prep.
4. Push `main` and wait for CI, build, and smoke checks to pass.
5. Run `bash scripts/create-release.sh X.Y.Z`.
6. Confirm the `Publish to PyPI` workflow succeeds.
7. Run `bash scripts/run-pypi-install-check.sh`.

## Smoke checks

```bash
bash scripts/validate-release.sh
```

## Release notes format

```md
## vX.Y.Z

### Added

### Fixed

### Changed
```
