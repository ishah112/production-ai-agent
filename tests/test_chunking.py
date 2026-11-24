from pathlib import Path

import pytest

from rag.chunking import parse_markdown_sections


def test_parse_markdown_sections_extracts_metadata_and_sections(tmp_path: Path) -> None:
    markdown_file = tmp_path / "policy.md"
    markdown_file.write_text(
        """---
document_id: test-policy
title: Test Policy
version: 1.0
---
# Test Policy

## Scope
This policy applies to test orders.

## Returns
Items may be returned within the stated window.
""",
        encoding="utf-8",
    )

    sections = parse_markdown_sections(markdown_file)

    assert len(sections) == 2
    assert sections[0]["document_id"] == "test-policy"
    assert sections[0]["title"] == "Test Policy"
    assert sections[0]["version"] == "1.0"
    assert sections[0]["section_heading"] == "Scope"
    assert sections[0]["text"] == "## Scope\nThis policy applies to test orders."
    assert sections[1]["section_heading"] == "Returns"
    assert "Items may be returned" in sections[1]["text"]


def test_parse_markdown_sections_skips_empty_sections(tmp_path: Path) -> None:
    markdown_file = tmp_path / "empty-section.md"
    markdown_file.write_text(
        """---
document_id: empty-section
---
# Example

## Empty section

## Has content
This section is not empty.
""",
        encoding="utf-8",
    )

    sections = parse_markdown_sections(markdown_file)

    assert len(sections) == 1
    assert sections[0]["section_heading"] == "Has content"


def test_parse_markdown_sections_rejects_missing_front_matter(tmp_path: Path) -> None:
    markdown_file = tmp_path / "no-front-matter.md"
    markdown_file.write_text("# Policy\n\n## Scope\nText.\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing the expected front matter"):
        parse_markdown_sections(markdown_file)
