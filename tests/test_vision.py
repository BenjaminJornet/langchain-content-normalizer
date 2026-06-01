from __future__ import annotations

from lc_content_normalizer import (
    VISION_FORMAT_ANTHROPIC_NATIVE,
    VISION_FORMAT_NONE,
    VISION_FORMAT_OPENAI,
    build_human_message_content,
    detect_vision_format,
    image_block_for_format,
)

PNG = {"data_url": "data:image/png;base64,abc123", "mime_type": "image/png"}


def test_detect_vision_format_anthropic_native():
    assert detect_vision_format("anthropic", "claude-3-5-sonnet") == VISION_FORMAT_ANTHROPIC_NATIVE


def test_detect_vision_format_ollama_vision_models_use_openai_blocks():
    assert detect_vision_format("ollama", "llava:13b") == VISION_FORMAT_OPENAI
    assert detect_vision_format("ollama", "model-with-vision") == VISION_FORMAT_OPENAI


def test_detect_vision_format_ollama_text_only():
    assert detect_vision_format("ollama", "llama3") == VISION_FORMAT_NONE


def test_detect_vision_format_openai_compatible_default():
    assert detect_vision_format("openrouter", "gpt-4o-mini") == VISION_FORMAT_OPENAI


def test_image_block_for_openai_format():
    assert image_block_for_format(PNG, VISION_FORMAT_OPENAI) == {
        "type": "image_url",
        "image_url": {"url": "data:image/png;base64,abc123"},
    }


def test_image_block_for_anthropic_native_format():
    block = image_block_for_format(PNG, VISION_FORMAT_ANTHROPIC_NATIVE)

    assert block["type"] == "image"
    assert block["source"] == {"type": "base64", "media_type": "image/png", "data": "abc123"}


def test_build_human_message_content_returns_text_without_images():
    assert build_human_message_content("hello", []) == "hello"


def test_build_human_message_content_drops_images_when_no_vision():
    assert build_human_message_content("hello", [PNG], VISION_FORMAT_NONE) == "hello"


def test_build_human_message_content_returns_multimodal_blocks():
    content = build_human_message_content("hello", [PNG], VISION_FORMAT_OPENAI)

    assert content == [
        {"type": "text", "text": "hello"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,abc123"}},
    ]
