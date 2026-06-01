# langchain-content-normalizer

[![CI](https://github.com/BenjaminJornet/langchain-content-normalizer/actions/workflows/ci.yml/badge.svg)](https://github.com/BenjaminJornet/langchain-content-normalizer/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/langchain-content-normalizer.svg)](https://pypi.org/project/langchain-content-normalizer/)
[![Downloads](https://static.pepy.tech/badge/langchain-content-normalizer/month)](https://pepy.tech/project/langchain-content-normalizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)

Normalize the messy content shapes produced by LangChain, MCP tools, Anthropic content blocks, and multimodal chat APIs.

The package has no runtime dependencies. It works by duck typing instead of importing LangChain or MCP classes.

## What it solves

LLM agent stacks often receive content as one of many incompatible shapes:

| Source | Example shape | Output |
| --- | --- | --- |
| Classic chat | `"plain text"` | `"plain text"` |
| Anthropic blocks | `[{"type": "text", "text": "hi"}]` | `"hi"` |
| Tool calls | `[{"type": "tool_use", ...}]` | skipped by default |
| MCP tool results | `[{"type": "tool_result", "content": [...]}]` | flattened text |
| MCP objects | objects exposing `.text` | extracted text |
| Message wrappers | objects exposing `.content` | recursively normalized |

## Install

```bash
uv add langchain-content-normalizer
```

## Text normalization

```python
from lc_content_normalizer import extract_text_content, normalize_tool_output

content = [
    {"type": "text", "text": "Reading logs..."},
    {"type": "tool_use", "name": "tail_logs", "input": {"service": "api"}},
]

assert extract_text_content(content) == "Reading logs..."
assert "tail_logs" in extract_text_content(content, skip_tool_use=False)

safe_output = normalize_tool_output(huge_tool_payload, max_chars=50_000)
```

## Vision format routing

```python
from lc_content_normalizer import build_human_message_content, detect_vision_format

vision_format = detect_vision_format("anthropic", "claude-3-5-sonnet")
content = build_human_message_content(
    "Explain this alert screenshot",
    images=[{"data_url": "data:image/png;base64,...", "mime_type": "image/png"}],
    vision_format=vision_format,
)
```

`detect_vision_format()` returns:

| Provider/model | Format |
| --- | --- |
| `anthropic` | native Anthropic `image` block with `source.base64` |
| `ollama` + `llava`/`vision` model name | OpenAI-compatible `image_url` block |
| `ollama` text-only model | `none`, images are dropped |
| OpenAI-compatible providers | OpenAI-compatible `image_url` block |

## Examples

- `examples/normalize_mcp_output.py` shows how MCP-style tool results are flattened.
- `examples/build_vision_content.py` shows provider-aware image block generation.

## Roadmap

- Add strict mode for unknown content blocks.
- Add more MCP fixture coverage.
- Add provider-specific adapters as content formats evolve.
- Keep runtime dependencies at zero.

## Development

```bash
uv sync --dev
uv run ruff check .
uv run pytest
uv run python scripts/smoke.py
```

## License

MIT
