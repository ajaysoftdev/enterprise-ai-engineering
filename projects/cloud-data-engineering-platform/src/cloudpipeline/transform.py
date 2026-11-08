"""Deterministic synthetic sales batch transformations and quality rules."""
from datetime import date


def process_rows(rows: list[dict]) -> dict:
    seen = set()
    curated = []
    quarantine = []
    duplicates = 0
    required = {"order_id", "product_id", "quantity", "unit_price", "event_date"}
    for index, raw in enumerate(rows):
        issues = []
        missing = sorted(required - set(raw))
        if missing:
            issues.append("Missing fields: " + ", ".join(missing))
        if not missing:
            try:
                quantity = float(raw["quantity"])
                unit_price = float(raw["unit_price"])
                if quantity <= 0:
                    issues.append("quantity must be greater than zero")
                if unit_price < 0:
                    issues.append("unit_price must not be negative")
                date.fromisoformat(str(raw["event_date"]))
            except (TypeError, ValueError):
                issues.append("quantity, unit_price or event_date has invalid format")
        order_id = str(raw.get("order_id", "")).strip()
        if order_id and order_id in seen:
            duplicates += 1
            issues.append("Duplicate order_id in this batch")
        if order_id:
            seen.add(order_id)
        if issues:
            quarantine.append({"row_number": index + 1, "source_row": raw, "issues": issues})
            continue
        curated.append({
            "order_id": order_id, "product_id": str(raw["product_id"]).strip(),
            "quantity": quantity, "unit_price": unit_price,
            "line_total": round(quantity * unit_price, 2),
            "event_date": date.fromisoformat(str(raw["event_date"])).isoformat(),
        })
    totals = {}
    for row in curated:
        item = totals.setdefault(row["product_id"], {"product_id": row["product_id"], "quantity": 0.0, "revenue": 0.0})
        item["quantity"] += row["quantity"]
        item["revenue"] += row["line_total"]
    gold = [{"product_id": key, "quantity": round(value["quantity"], 2), "revenue": round(value["revenue"], 2)}
            for key, value in sorted(totals.items())]
    return {
        "curated_rows": curated, "quarantine": quarantine,
        "duplicate_count": duplicates, "gold_summary": gold,
    }
