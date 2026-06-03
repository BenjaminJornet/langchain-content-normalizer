from __future__ import annotations

import pytest

from lc_content_normalizer import (
    UnknownContentBlockError,
    extract_text_content,
    normalize_tool_output,
)


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeTextContent:
    def __init__(self, text: str):
        self.type = "text"
        self.text = text


def test_string_passthrough():
    assert extract_text_content("hello") == "hello"


def test_none_returns_empty():
    assert extract_text_content(None) == ""


def test_anthropic_text_blocks_are_concatenated_and_tool_use_is_skipped():
    content = [
        {"type": "text", "text": "The file "},
        {"type": "tool_use", "name": "read_file", "input": {"path": "app.py"}},
        {"type": "text", "text": "is ready."},
    ]

    assert extract_text_content(content) == "The file is ready."


def test_text_blocks_can_use_separator():
    content = [{"type": "text", "text": "one"}, {"type": "text", "text": "two"}]

    assert extract_text_content(content, separator="\n") == "one\ntwo"


def test_tool_use_can_be_included_explicitly():
    content = [{"type": "tool_use", "input": {"path": "app.py"}}]

    assert "app.py" in extract_text_content(content, skip_tool_use=False)


def test_tool_result_nested_content_is_flattened():
    content = [{"type": "tool_result", "content": [{"type": "text", "text": "inner"}]}]

    assert extract_text_content(content) == "inner"


def test_realistic_mcp_tool_result_fixture_is_flattened_with_separator():
    content = [
        {
            "type": "tool_result",
            "tool_use_id": "call_123",
            "content": [
                {"type": "text", "text": "stdout: service healthy"},
                {"type": "text", "text": "stderr: "},
            ],
            "is_error": False,
        }
    ]

    assert extract_text_content(content, separator="\n") == "stdout: service healthy\nstderr: "


def test_anthropic_server_tool_result_fixture_preserves_text():
    content = [
        {"type": "text", "text": "I checked the host."},
        {
            "type": "tool_result",
            "tool_use_id": "toolu_01",
            "content": [{"type": "text", "text": "load average: 0.12"}],
        },
    ]

    assert extract_text_content(content, separator="\n") == (
        "I checked the host.\nload average: 0.12"
    )


def test_openai_responses_output_text_fixture_is_preserved():
    content = [
        {"type": "output_text", "text": "The deployment is healthy."},
        {"type": "output_text", "text": "No action required."},
    ]

    assert extract_text_content(content, separator="\n") == (
        "The deployment is healthy.\nNo action required."
    )


def test_openai_responses_input_text_fixture_is_preserved():
    content = [
        {"type": "input_text", "text": "Summarize this incident."},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,abc"}},
    ]

    assert extract_text_content(content) == "Summarize this incident."


def test_mcp_text_content_object_is_extracted():
    assert extract_text_content(FakeTextContent("from MCP")) == "from MCP"


def test_mcp_text_content_list_is_extracted():
    assert extract_text_content([FakeTextContent("from MCP")]) == "from MCP"


def test_message_like_content_is_unwrapped():
    assert extract_text_content(FakeMessage([{"type": "text", "text": "wrapped"}])) == "wrapped"


def test_unknown_dict_is_preserved_as_string():
    result = extract_text_content({"status": "ok", "count": 2})

    assert "status" in result
    assert "2" in result


def test_unknown_block_list_does_not_silently_disappear():
    result = extract_text_content([{"request_id": "abc", "message": "hello"}])

    assert "request_id" in result
    assert "hello" in result


def test_strict_mode_raises_for_unknown_block_list():
    with pytest.raises(UnknownContentBlockError):
        extract_text_content([{"request_id": "abc", "message": "hello"}], strict=True)


def test_strict_mode_raises_for_unknown_dict_block_type():
    with pytest.raises(UnknownContentBlockError):
        extract_text_content([{"type": "custom", "payload": "hello"}], strict=True)


def test_strict_mode_raises_for_raw_dict_content():
    with pytest.raises(UnknownContentBlockError):
        extract_text_content({"status": "ok"}, strict=True)


def test_image_blocks_are_dropped():
    content = [{"type": "text", "text": "screenshot:"}, {"type": "image", "source": {}}]

    assert extract_text_content(content) == "screenshot:"


def test_normalize_tool_output_truncates_large_payloads():
    result = normalize_tool_output("x" * 20, max_chars=10)

    assert result.startswith("x" * 10)
    assert "truncated 10 chars" in result


def test_normalize_tool_output_accepts_separator():
    result = normalize_tool_output(
        [{"type": "text", "text": "line 1"}, {"type": "text", "text": "line 2"}],
        separator="\n",
    )

    assert result == "line 1\nline 2"
