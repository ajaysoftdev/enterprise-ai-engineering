"""Allow-listed tool selection and policy gate; request text never grants tool authority."""
TOOL_RULES = {
    "gather_supplier_info": {
        "tool": "supplier_directory.search",
        "risk": "LOW",
        "status": "READY",
        "reason": "Read-only supplier lookup is within the synthetic allow-list.",
        "steps": ["Validate procurement request scope", "Search synthetic supplier directory", "Return source references for human review"],
    },
    "draft_purchase_order": {
        "tool": "procurement.order.draft",
        "risk": "MEDIUM",
        "status": "AWAITING_APPROVAL",
        "reason": "Creating a draft is a bounded write and requires a human checkpoint in this demonstrator.",
        "steps": ["Validate supplier and requested items", "Prepare a non-committing purchase-order draft", "Pause for authorised human review"],
    },
    "submit_purchase_order": {
        "tool": "procurement.order.submit",
        "risk": "HIGH",
        "status": "AWAITING_APPROVAL",
        "reason": "Submitting a purchase order is consequential and cannot proceed without explicit human approval.",
        "steps": ["Validate purchase-order draft and limits", "Present amount, supplier and terms to approver", "Pause before any external submission"],
    },
    "delete_supplier": {
        "tool": "supplier.delete",
        "risk": "PROHIBITED",
        "status": "BLOCKED",
        "reason": "Destructive supplier deletion is outside the prototype's permitted tool capabilities.",
        "steps": ["Reject the requested destructive operation", "Record the policy outcome for review"],
    },
}


def plan_for(action: str) -> dict:
    # Only a fixed action key selects a tool. Untrusted request_text is never parsed as instructions.
    return TOOL_RULES[action].copy()
