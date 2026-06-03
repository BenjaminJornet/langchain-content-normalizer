from __future__ import annotations

from typing import Any


class UnknownContentBlockError(ValueError):
    """Raised when strict mode cannot normalize an unknown content block."""


def extract_text_content(
    content: Any,
    *,
    skip_tool_use: bool = True,
    strict: bool = False,
    separator: str = "",
) -> str:
    """Normalize LangChain, Anthropic, and MCP content shapes to plain text.

    Supported inputs include strings, Anthropic-style content block lists,
    MCP TextContent-like objects exposing ``.text``, and message-like objects
    exposing ``.content``. Unknown non-empty block lists fall back to ``str`` so
    tool outputs are not silently lost. Set ``strict=True`` to raise
    ``UnknownContentBlockError`` instead of falling back.
    """
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        saw_known_block = False
        for block in content:
            if isinstance(block, str):
                parts.append(block)
                saw_known_block = True
                continue
            if isinstance(block, dict):
                block_type = block.get("type")
                if block_type in {"input_text", "output_text", "text"} and isinstance(
                    block.get("text"), str
                ):
                    parts.append(block["text"])
                    saw_known_block = True
                elif block_type == "tool_result":
                    parts.append(
                        extract_text_content(
                            block.get("content", ""),
                            skip_tool_use=skip_tool_use,
                            strict=strict,
                            separator=separator,
                        )
                    )
                    saw_known_block = True
                elif block_type == "tool_use":
                    saw_known_block = True
                    if not skip_tool_use:
                        parts.append(str(block.get("input", "")))
                elif block_type in {"image", "image_url"}:
                    saw_known_block = True
                elif strict:
                    raise UnknownContentBlockError(f"Unknown content block type: {block_type!r}")
                continue

            text_attr = getattr(block, "text", None)
            if isinstance(text_attr, str):
                parts.append(text_attr)
                saw_known_block = True
                continue

            parts.append(str(block))

        result = separator.join(parts)
        if not result and content and not saw_known_block:
            if strict:
                raise UnknownContentBlockError("Unknown content block list")
            return str(content)
        return result

    inner = getattr(content, "content", None)
    if inner is not None and inner is not content:
        return extract_text_content(
            inner,
            skip_tool_use=skip_tool_use,
            strict=strict,
            separator=separator,
        )

    text_attr = getattr(content, "text", None)
    if isinstance(text_attr, str):
        return text_attr

    if strict and isinstance(content, dict):
        raise UnknownContentBlockError("Unknown dict content")
    return str(content)


def normalize_tool_output(
    raw: Any,
    *,
    max_chars: int = 50_000,
    strict: bool = False,
    separator: str = "",
) -> str:
    """Extract a readable tool output string and truncate oversized payloads."""
    text = extract_text_content(raw, strict=strict, separator=separator)
    if len(text) <= max_chars:
        return text
    omitted = len(text) - max_chars
    return text[:max_chars] + f"\n\n[...truncated {omitted} chars]"
