
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


META = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def extract_field(
    text: str,
    field_name: str,
    default: str = "UNKNOWN",
) -> str:
    """Extract a metadata field from document text."""

    pattern = rf"(?im)^{re.escape(field_name)}:\s*(.+)$"
    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    return default


def infer_doc_type(path: Path) -> str:
    """Infer document type from its directory."""

    mapping = {
        "runbooks": "runbook",
        "incidents": "incident",
        "architecture": "architecture",
        "procedures": "procedure",
        "policies": "policy",
    }

    return mapping.get(
        path.parent.name.lower(),
        path.parent.name.lower(),
    )


def extract_title(text: str, path: Path) -> str:
    """Extract Markdown title or use filename."""

    match = re.search(r"(?m)^#\s+(.+)$", text)

    if match:
        return match.group(1).strip()

    return path.stem.replace("_", " ").title()


def determine_system(text: str) -> str:
    """Extract system using supported metadata fields."""

    for field in ("Platform", "Service", "System"):
        value = extract_field(text, field)

        if value != "UNKNOWN":
            return value

    # Vendor metadata is used when system metadata is missing.
    vendor = extract_field(text, "Vendor")

    if vendor != "UNKNOWN":
        vendor_mapping = {
            "boomi": "Boomi",
            "tibco": "TIBCO BusinessWorks",
            "axway": "Axway",
            "broadcom": "Broadcom Layer7 API Gateway",
            "layer7": "Layer7",
        }

        vendor_lower = vendor.lower()

        for keyword, system in vendor_mapping.items():
            if keyword in vendor_lower:
                return system

    return "UNKNOWN"


def load_document(path: Path) -> EnterpriseDocument:
    text = path.read_text(encoding="utf-8")

    # Format 1: YAML-style front matter.
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
            title=metadata.get(
                "title",
                extract_title(content, path),
            ),
            doc_type=metadata.get(
                "doc_type",
                infer_doc_type(path),
            ),
            system=metadata.get(
                "system",
                determine_system(content),
            ),
            environment=metadata.get(
                "environment",
                "UNKNOWN",
            ),
            document_id=metadata.get(
                "document_id",
                path.stem,
            ),
            content=content,
        )

    # Format 2: Markdown without YAML front matter.
    title = extract_title(text, path)
    doc_type = infer_doc_type(path)

    system = determine_system(text)
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
