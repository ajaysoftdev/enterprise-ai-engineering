"""Basic metadata quality rules for synthetic research records."""
REQUIRED_BY_TYPE = {
    "EXPERIMENT": ["protocol_id"],
    "SAMPLE": ["material_id"],
    "METHOD": ["method_version"],
    "ASSAY_RESULT": ["sample_id", "method_id", "result_value", "unit"],
}


def validate(record: dict) -> list[str]:
    issues = []
    for field in REQUIRED_BY_TYPE[record["record_type"]]:
        if field not in record["payload"] or record["payload"][field] in (None, ""):
            issues.append(f"Missing required payload field: {field}")
    return issues
