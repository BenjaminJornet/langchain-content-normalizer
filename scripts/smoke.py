from __future__ import annotations

from lc_content_normalizer import build_human_message_content, extract_text_content


def main() -> None:
    text = extract_text_content(
        [{"type": "tool_result", "content": [{"type": "text", "text": "ok"}]}]
    )
    assert text == "ok"

    image_content = build_human_message_content(
        "describe",
        [{"data_url": "data:image/png;base64,abc", "mime_type": "image/png"}],
        "openai",
    )
    assert isinstance(image_content, list)
    assert image_content[1]["type"] == "image_url"
    print("smoke ok")


if __name__ == "__main__":
    main()
