# Contributing

Thanks for helping improve `langchain-content-normalizer`.

## Development setup

```bash
uv sync --dev
uv run ruff check .
uv run pytest
```

## Contribution guidelines

- Keep runtime dependencies at zero unless there is a strong reason.
- Prefer duck typing over importing LangChain, MCP, or provider SDK classes.
- Add tests for every new content shape or provider format.
- Do not silently drop unknown non-empty content. Preserve it with a safe fallback.
- Keep public APIs small and documented in `README.md`.

## Useful PRs

- New MCP or LangChain content fixtures.
- Better multimodal provider adapters.
- Strict-mode behavior for applications that prefer errors over fallback strings.
