from datetime import date

from .models import Claim, ClaimCreate, ClaimStatus, Document, DocumentCreate, Policy, RiskLevel


ALLOWED_DOCUMENT_TYPES = {"Identity proof", "Policy document", "Bill", "Receipt", "Medical report", "Repair estimate", "Photographs", "Police report", "Other"}
REQUIRED_DOCUMENT_TYPES = {"Repair estimate", "Bill", "Police report", "Photographs"}


def find_policy(policies: list[Policy], policy_number: str) -> Policy | None:
    return next((policy for policy in policies if policy.policy_number == policy_number), None)


def assess_claim(claim: Claim, policy: Policy, all_claims: list[Claim]) -> tuple[RiskLevel, int, list[str], list[dict[str, str | bool]]]:
    checks: list[dict[str, str | bool]] = []
    reasons: list[str] = []
    score = 10
    active = policy.status == "ACTIVE"
    in_period = policy.start_date <= claim.incident_date <= policy.expiry_date
    within_limit = claim.claimed_amount <= policy.coverage_amount
    duplicate = any(existing.policy_id == claim.policy_id and existing.incident_date == claim.incident_date and existing.claim_type == claim.claim_type and existing.claim_id != claim.claim_id for existing in all_claims)
    checks.extend([
        {"name": "Policy is active", "passed": active, "detail": "Policy status is ACTIVE" if active else "Policy is expired or inactive"},
        {"name": "Incident within coverage period", "passed": in_period, "detail": "Incident date is covered" if in_period else "Incident date falls outside policy dates"},
        {"name": "Claim within coverage limit", "passed": within_limit, "detail": f"Limit is Rs {policy.coverage_amount:,.0f}"},
        {"name": "No potential duplicate", "passed": not duplicate, "detail": "No matching claim found" if not duplicate else "Matching policy, date, and claim type found"},
    ])
    if not active or not in_period:
        score += 45
        reasons.append("Policy eligibility needs manual review")
    if not within_limit:
        score += 25
        reasons.append("Claimed amount exceeds policy coverage")
    if duplicate:
        score += 35
        reasons.append("Potential duplicate claim detected")
    if claim.claimed_amount > 500000:
        score += 20
        reasons.append("High-value claim above review threshold")
    score = min(score, 100)
    level = RiskLevel.CRITICAL if score >= 85 else RiskLevel.HIGH if score >= 60 else RiskLevel.MEDIUM if score >= 35 else RiskLevel.LOW
    return level, score, reasons or ["No elevated risk indicators detected"], checks


def validate_documents(claim: Claim) -> list[dict[str, str | bool]]:
    has_documents = bool(claim.documents)
    supported = all(document.document_type in ALLOWED_DOCUMENT_TYPES for document in claim.documents)
    return [
        {"name": "Supporting documents supplied", "passed": has_documents, "detail": "At least one document attached" if has_documents else "Add supporting evidence before submission"},
        {"name": "Document types supported", "passed": supported, "detail": "All document types are accepted" if supported else "One or more document types are unsupported"},
    ]
