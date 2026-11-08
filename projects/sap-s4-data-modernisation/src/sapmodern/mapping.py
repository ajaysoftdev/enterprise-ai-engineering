"""Deterministic SAP-like source-to-canonical mapping and validation."""
REQUIRED = {
    "BUSINESS_PARTNER": ["name", "country", "tax_id"],
    "MATERIAL_MASTER": ["material_code", "description", "base_uom", "plant"],
}


def map_record(record: dict) -> tuple[dict | None, list[str]]:
    record_type = record["record_type"]
    payload = record["payload"]
    issues = [f"Missing required field: {field}" for field in REQUIRED[record_type]
              if field not in payload or payload[field] in (None, "")]
    if issues:
        return None, issues
    if record_type == "BUSINESS_PARTNER":
        target = {
            "domain_type": "BusinessPartner",
            "business_partner_id": str(record["source_key"]),
            "legal_name": str(payload["name"]).strip(),
            "country_code": str(payload["country"]).upper(),
            "tax_identifier": str(payload["tax_id"]).strip(),
        }
    else:
        target = {
            "domain_type": "Material",
            "material_id": str(record["source_key"]),
            "material_description": str(payload["description"]).strip(),
            "base_unit": str(payload["base_uom"]).upper(),
            "plant_code": str(payload["plant"]).upper(),
        }
    return target, []
