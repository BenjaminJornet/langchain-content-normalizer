from __future__ import annotations

from lc_content_normalizer import extract_text_content, normalize_tool_output


class FakeTextContent:
    def __init__(self, text: str) -> None:
        self.type = "text"
        self.text = text


raw_tool_output = [
    {
        "type": "tool_result",
        "content": [FakeTextContent("service=api status=healthy\n")],
    }
]

print(extract_text_content(raw_tool_output))
print(normalize_tool_output(raw_tool_output, max_chars=80))
