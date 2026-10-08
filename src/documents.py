from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class EnterpriseDocument:
    path: Path
    title: str
    doc_type: str
    system: str
    environment: str
    document_id: str
    content: str


META = re.compile(r"^---\n(.*?)\n---\n", re.S)


def extract_field(text: str, field_name: str, default: str = "UNKNOWN") -> str:
    """
    Extract a simple metadata field from document content.

    Example:
        Platform: Boomi
        Environment: PROD
        Document ID: RB-BOOMI-001
    """
    pattern = rf"(?im)^{re.escape(field_name)}:\s*(.+)$"
    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    return default


def infer_doc_type(path: Path) -> str:
    """
    Infer document type from its parent directory.

    Example:
        knowledge/runbooks/file.md -> runbook
        knowledge/incidents/file.md -> incident
    """
    mapping = {
        "runbooks": "runbook",
        "incidents": "incident",
        "architecture": "architecture",
        "procedures": "procedure",
        "policies": "policy",
    }

    return mapping.get(path.parent.name.lower(), path.parent.name.lower())


def extract_title(text: str, path: Path) -> str:
    """
    Use the first Markdown H1 heading as the title.
    Fall back to the filename when no H1 exists.
    """
    match = re.search(r"(?m)^#\s+(.+)$", text)

    if match:
        return match.group(1).strip()

    return path.stem.replace("_", " ").title()


def load_document(path: Path) -> EnterpriseDocument:
    text = path.read_text(encoding="utf-8")

    # ---------------------------------------------------------
    # Format 1:
    # Existing documents containing YAML-style front matter.
    # ---------------------------------------------------------
    match = META.match(text)

    if match:
        metadata = {}

        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

        content = text[match.end():].strip()

        return EnterpriseDocument(
            path=path,
            title=metadata.get("title", extract_title(content, path)),
            doc_type=metadata.get("doc_type", infer_doc_type(path)),
            system=metadata.get("system", "UNKNOWN"),
            environment=metadata.get("environment", "UNKNOWN"),
            document_id=metadata.get("document_id", path.stem),
            content=content,
        )

    # ---------------------------------------------------------
    # Format 2:
    # Enterprise documents without YAML front matter.
    # Metadata is extracted/inferred from content and path.
    # ---------------------------------------------------------
    title = extract_title(text, path)
    doc_type = infer_doc_type(path)

    system = extract_field(text, "Platform")

    if system == "UNKNOWN":
        system = extract_field(text, "Service")

    environment = extract_field(text, "Environment")

    document_id = extract_field(text, "Document ID")

    if document_id == "UNKNOWN":
        document_id = extract_field(text, "Incident")

    if document_id == "UNKNOWN":
        document_id = path.stem

    return EnterpriseDocument(
        path=path,
        title=title,
        doc_type=doc_type,
        system=system,
        environment=environment,
        document_id=document_id,
        content=text.strip(),
    )


def load_corpus(root: Path) -> list[EnterpriseDocument]:
    return [
        load_document(path)
        for path in sorted(root.rglob("*.md"))
    ]