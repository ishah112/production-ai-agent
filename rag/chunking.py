from pathlib import Path

def parse_markdown_sections(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", maxsplit=2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"{path} is missing the expected front matter")

    front = parts[1]
    body = parts[2]

    # Read simple "key: value" metadata lines from the front
    metadata = {}
    for line in front.splitlines():
        # before,seperator,after (in case seperator is missing)
        key,seperator,value = line.partition(":")
        if seperator:
            metadata[key.strip()] = value.strip()

    # Each section starts with a newline followed by "## ".
    section_texts = body.split("\n## ")
    sections = []

    # The first piece is the document title and intro, before section 1.
    for section_text in section_texts[1:]:
        heading, separator, section_body = section_text.partition("\n")

        if not separator or not section_body.strip():
            continue

        sections.append({
            **metadata,
            "section_heading": heading.strip(),
            "text": f"## {section_text.strip()}",
        })

    return sections


