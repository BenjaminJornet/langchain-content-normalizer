from __future__ import annotations

from lc_content_normalizer import build_human_message_content, detect_vision_format

image = {"data_url": "data:image/png;base64,abc123", "mime_type": "image/png"}

for provider, model in [("anthropic", "claude"), ("ollama", "llava"), ("ollama", "llama")]:
    vision_format = detect_vision_format(provider, model)
    content = build_human_message_content("Explain this screenshot", [image], vision_format)
    print(provider, model, vision_format, content)
