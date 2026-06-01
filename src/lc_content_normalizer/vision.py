from __future__ import annotations

from typing import Any

VISION_FORMAT_OPENAI = "openai"
VISION_FORMAT_ANTHROPIC_NATIVE = "anthropic_native"
VISION_FORMAT_NONE = "none"


def detect_vision_format(provider: str, model: str) -> str:
    """Pick the multimodal block format expected by a provider/model pair."""
    provider_name = (provider or "").lower()
    model_name = (model or "").lower()

    if provider_name == "anthropic":
        return VISION_FORMAT_ANTHROPIC_NATIVE
    if provider_name == "ollama":
        if "llava" in model_name or "vision" in model_name:
            return VISION_FORMAT_OPENAI
        return VISION_FORMAT_NONE
    return VISION_FORMAT_OPENAI


def image_block_for_format(image: dict[str, str], vision_format: str) -> dict[str, Any]:
    """Render one image into the multimodal block expected by the target API."""
    if vision_format == VISION_FORMAT_ANTHROPIC_NATIVE:
        data_url = image.get("data_url", "")
        header, _, b64_data = data_url.partition(",")
        media_type = image.get("mime_type") or header.removeprefix("data:").split(";", 1)[0]
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": b64_data},
        }
    return {"type": "image_url", "image_url": {"url": image["data_url"]}}


def build_human_message_content(
    text: str,
    images: list[dict[str, str]] | None = None,
    vision_format: str = VISION_FORMAT_OPENAI,
) -> str | list[dict[str, Any]]:
    """Build text-only or multimodal human message content for LangChain."""
    if not images or vision_format == VISION_FORMAT_NONE:
        return text

    content: list[dict[str, Any]] = []
    if text:
        content.append({"type": "text", "text": text})
    for image in images:
        content.append(image_block_for_format(image, vision_format))
    return content
