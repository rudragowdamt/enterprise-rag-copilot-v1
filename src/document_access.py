def filter_authorized_records(
    records: list[dict],
    allowed_systems: list[str],
) -> list[dict]:
    """Return only documents from authorized systems."""

    if not allowed_systems:
        return []

    allowed = {system.lower() for system in allowed_systems}

    return [
        record
        for record in records
        if record.get("system", "").lower() in allowed
    ]
