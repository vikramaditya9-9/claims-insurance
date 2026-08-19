from datetime import date, datetime, timezone

from .models import Claim, ClaimStatus, Document, Policy, RiskLevel


def now() -> datetime:
    return datetime.now(timezone.utc)


policies = [
    Policy(
        policy_id="pol_001", policy_number="PROP-2026-1042", customer_id="cus_001",
        customer_name="Ananya Rao", insurance_type="Property", start_date=date(2026, 1, 1),
        expiry_date=date(2026, 12, 31), coverage_amount=500000, deductible_amount=20000,
        status="ACTIVE", coverage_conditions=["Fire", "Water damage", "Theft"],
        exclusions=["Intentional damage", "War and nuclear risk"],
    ),
    Policy(
        policy_id="pol_002", policy_number="PROP-2026-1088", customer_id="cus_002",
        customer_name="Rohan Mehta", insurance_type="Property", start_date=date(2026, 3, 15),
        expiry_date=date(2027, 3, 14), coverage_amount=750000, deductible_amount=25000,
        status="ACTIVE", coverage_conditions=["Fire", "Natural disaster", "Theft"],
        exclusions=["Vacant property over 60 days"],
    ),
    Policy(
        policy_id="pol_003", policy_number="PROP-2025-0911", customer_id="cus_003",
        customer_name="Meera Shah", insurance_type="Property", start_date=date(2025, 1, 1),
        expiry_date=date(2025, 12, 31), coverage_amount=300000, deductible_amount=15000,
        status="EXPIRED", coverage_conditions=["Fire", "Water damage"], exclusions=["Theft"],
    ),
]


claims = [
    Claim(
        claim_id="clm_001", claim_number="CLM-2026-00041", policy_id="pol_001",
        policy_number="PROP-2026-1042", customer_id="cus_001", customer_name="Ananya Rao",
        claim_type="Water damage", incident_date=date(2026, 7, 22), incident_location="Pune",
        incident_description="Burst pipe damaged the kitchen flooring and lower cabinets.",
        claimed_amount=185000, approved_amount=None, deductible=20000,
        status=ClaimStatus.DOCUMENT_VERIFICATION, investigation_status="NOT_REQUIRED",
        risk_level=RiskLevel.LOW, risk_score=18, risk_reasons=["All core fields present"],
        documents=[Document(document_id="doc_001", file_name="repair-estimate.pdf", document_type="Repair estimate", size_bytes=284000, uploaded_at=now())],
        created_at=now(), updated_at=now(),
    ),
    Claim(
        claim_id="clm_002", claim_number="CLM-2026-00038", policy_id="pol_002",
        policy_number="PROP-2026-1088", customer_id="cus_002", customer_name="Rohan Mehta",
        claim_type="Fire", incident_date=date(2026, 7, 18), incident_location="Mumbai",
        incident_description="Electrical fire affected the garage and storage area.",
        claimed_amount=620000, approved_amount=None, deductible=25000,
        status=ClaimStatus.MANUAL_REVIEW, investigation_status="REQUIRED",
        risk_level=RiskLevel.HIGH, risk_score=72, risk_reasons=["High-value claim above review threshold", "Investigation required"],
        documents=[Document(document_id="doc_002", file_name="fire-report.pdf", document_type="Police report", size_bytes=512000, uploaded_at=now()), Document(document_id="doc_003", file_name="damage-photos.zip", document_type="Photographs", size_bytes=1900000, uploaded_at=now())],
        created_at=now(), updated_at=now(),
    ),
]
