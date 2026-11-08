"""Deterministic capability gap and dependency analysis."""
def analyse(capabilities: list[dict], dependencies: list[dict]) -> dict:
    names = {item["name"] for item in capabilities}
    gaps = []
    roadmap = []
    for item in capabilities:
        gap = item["target_maturity"] - item["current_maturity"]
        if gap > 0:
            gaps.append({
                "capability": item["name"], "current_maturity": item["current_maturity"],
                "target_maturity": item["target_maturity"], "gap": gap,
                "evidence_references": item["evidence_references"],
            })
            roadmap.append({
                "initiative": f"Improve {item['name']}",
                "capability": item["name"], "priority": "HIGH" if gap >= 2 else "MEDIUM",
                "maturity_gap": gap, "phase": "FOUNDATION" if gap >= 2 else "ENHANCEMENT",
            })
    findings = []
    for item in dependencies:
        if item["source_capability"] not in names or item["target_capability"] not in names:
            findings.append({**item, "finding": "UNRESOLVED_CAPABILITY_REFERENCE"})
        elif item["relationship"] == "DUPLICATES":
            findings.append({**item, "finding": "POTENTIAL_CAPABILITY_DUPLICATION"})
        else:
            findings.append({**item, "finding": "RECORDED_DEPENDENCY"})
    current = round(sum(item["current_maturity"] for item in capabilities) / len(capabilities), 2)
    target = round(sum(item["target_maturity"] for item in capabilities) / len(capabilities), 2)
    roadmap.sort(key=lambda item: (-item["maturity_gap"], item["capability"]))
    return {
        "overall_current_maturity": current,
        "overall_target_maturity": target,
        "capability_gaps": gaps,
        "dependency_findings": findings,
        "roadmap": roadmap,
    }
