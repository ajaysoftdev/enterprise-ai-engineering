"""Synthetic enterprise trust graph and deterministic attack-path traversal."""
from collections import deque

# All nodes and relationships are invented fixtures. No real network is contacted.
EDGES = [
    ("contractor-temp", "build-runner", "ASSIGNED_TO"),
    ("build-runner", "artifact-registry", "PUBLISHES_TO"),
    ("artifact-registry", "billing-api", "DEPLOYS_TO"),
    ("billing-api", "customer-db", "CONNECTS_TO"),
    ("billing-api", "secrets-vault", "READS_SECRET"),
    ("svc-reporting", "reporting-api", "CALLS"),
    ("reporting-api", "analytics-db", "READS"),
]
SENSITIVE = {"customer-db", "secrets-vault", "prod-admin"}
PRINCIPALS = {"contractor-temp", "svc-reporting"}


def paths_from(principal: str) -> list[dict]:
    if principal not in PRINCIPALS:
        return []
    adjacency: dict[str, list[tuple[str, str]]] = {}
    for source, target, relationship in EDGES:
        adjacency.setdefault(source, []).append((target, relationship))
    results = []
    queue = deque([(principal, [principal], [])])
    while queue:
        node, path, relationships = queue.popleft()
        for target, relationship in adjacency.get(node, []):
            if target in path:
                continue
            next_path = path + [target]
            next_relationships = relationships + [relationship]
            if target in SENSITIVE:
                results.append({
                    "principal": principal, "nodes": next_path,
                    "relationships": next_relationships, "target": target,
                    "risk": "HIGH" if target in {"customer-db", "secrets-vault"} else "MEDIUM",
                })
            else:
                queue.append((target, next_path, next_relationships))
    return results


def policy_decision(principal: str, resource: str, action: str) -> dict:
    known_paths = paths_from(principal)
    reachable = any(path["target"] == resource for path in known_paths)
    # Default deny: the synthetic demo permits no direct administrative action.
    if reachable and action == "read" and resource not in {"secrets-vault"}:
        return {"decision": "ALLOW", "reason": "Synthetic graph contains a read relationship"}
    return {"decision": "DENY", "reason": "No matching least-privilege grant; default deny"}
