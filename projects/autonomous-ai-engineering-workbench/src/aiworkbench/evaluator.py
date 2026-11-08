"""Deterministic patch checks. Submitted code is inspected as text and never executed."""
import re
from .tasks import TASKS

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(password|api_key|secret)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]
UNSAFE_PATTERNS = [
    re.compile(r"\beval\s*\("),
    re.compile(r"\bexec\s*\("),
    re.compile(r"\bos\.system\s*\("),
    re.compile(r"\bsubprocess\.(?:Popen|run|call)\s*\("),
]


def evaluate(task_id: str, patch_files: dict[str, str]) -> dict:
    task = TASKS[task_id]
    acceptance_findings = []
    required_files = task["required_files"]
    for path in required_files:
        if path not in patch_files:
            acceptance_findings.append(f"Missing required file: {path}")
    for path, snippets in task["required_snippets"].items():
        content = patch_files.get(path, "")
        for snippet in snippets:
            if snippet not in content:
                acceptance_findings.append(f"Missing acceptance marker in {path}: {snippet}")
    acceptance_score = 60 if not acceptance_findings else max(0, 60 - 15 * len(acceptance_findings))

    security_findings = []
    for path, content in patch_files.items():
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                security_findings.append(f"Potential secret pattern detected in {path}")
        for pattern in UNSAFE_PATTERNS:
            if pattern.search(content):
                security_findings.append(f"Potentially unsafe execution pattern detected in {path}")
    security_score = 25 if not security_findings else 0
    evidence_score = 15 if patch_files else 0
    score = acceptance_score + security_score + evidence_score
    return {
        "score": score, "acceptance_score": acceptance_score,
        "security_score": security_score, "evidence_score": evidence_score,
        "acceptance_findings": acceptance_findings,
        "security_findings": security_findings,
        "test_execution": "NOT_RUN — static evaluation only",
        "merge_eligible": score == 100 and not security_findings,
    }
