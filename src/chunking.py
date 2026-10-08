from dataclasses import dataclass
from pathlib import Path
import re

from src.documents import EnterpriseDocument


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_id: str
    title: str
    section: str
    doc_type: str
    system: str
    environment: str
    source: Path
    content: str


SECTION_PATTERN = re.compile(
    r"(?m)^##\s+(.+)$"
)


def split_markdown_sections(content: str) -> list[tuple[str, str]]:
    """
    Split Markdown content using H2 headings.

    Returns:
        [
            ("Introduction", "..."),
            ("Symptoms", "..."),
            ("Troubleshooting", "..."),
        ]
    """
    matches = list(SECTION_PATTERN.finditer(content))

    if not matches:
        return [("Document", content.strip())]

    sections = []

    # Content before first H2 heading.
    preamble = content[:matches[0].start()].strip()

    if preamble:
        sections.append(("Overview", preamble))

    for index, match in enumerate(matches):
        section_name = match.group(1).strip()

        content_start = match.end()

        if index + 1 < len(matches):
            content_end = matches[index + 1].start()
        else:
            content_end = len(content)

        section_content = content[content_start:content_end].strip()

        if section_content:
            sections.append(
                (section_name, section_content)
            )

    return sections


def slugify(value: str) -> str:
    """
    Convert text into a stable chunk identifier component.
    """
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)

    return value.strip("-")


def chunk_document(
    document: EnterpriseDocument,
) -> list[DocumentChunk]:
    """
    Convert one enterprise document into structure-aware chunks.
    """
    sections = split_markdown_sections(document.content)

    chunks = []

    for index, (section_name, section_content) in enumerate(
        sections,
        start=1,
    ):
        chunk_id = (
            f"{document.document_id}-"
            f"{index:03d}-"
            f"{slugify(section_name)}"
        )

        chunks.append(
            DocumentChunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                title=document.title,
                section=section_name,
                doc_type=document.doc_type,
                system=document.system,
                environment=document.environment,
                source=document.path,
                content=section_content,
            )
        )

    return chunks


def chunk_corpus(
    documents: list[EnterpriseDocument],
) -> list[DocumentChunk]:
    """
    Convert the entire enterprise corpus into chunks.
    """
    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks