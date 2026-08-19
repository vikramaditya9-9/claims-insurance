from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ClaimStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    DOCUMENT_VERIFICATION = "DOCUMENT_VERIFICATION"
    POLICY_VERIFICATION = "POLICY_VERIFICATION"
    CLAIM_ASSESSMENT = "CLAIM_ASSESSMENT"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    FRAUD_REVIEW = "FRAUD_REVIEW"
    REJECTED = "REJECTED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Document(BaseModel):
    document_id: str
    file_name: str
    document_type: str
    size_bytes: int
    uploaded_at: datetime


class Policy(BaseModel):
    policy_id: str
    policy_number: str
    customer_id: str
    customer_name: str
    insurance_type: str
    start_date: date
    expiry_date: date
    coverage_amount: float
    deductible_amount: float
    status: str
    coverage_conditions: list[str]
    exclusions: list[str]


class Claim(BaseModel):
    claim_id: str
    claim_number: str
    policy_id: str
    policy_number: str
    customer_id: str
    customer_name: str
    claim_type: str
    incident_date: date
    incident_location: str
    incident_description: str
    claimed_amount: float
    approved_amount: Optional[float] = None
    deductible: float
    final_settlement_amount: Optional[float] = None
    status: ClaimStatus
    investigation_status: str
    risk_level: RiskLevel
    risk_score: int
    risk_reasons: list[str]
    documents: list[Document]
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ClaimCreate(BaseModel):
    policy_number: str = Field(min_length=3)
    claim_type: str = Field(min_length=2)
    incident_date: date
    incident_location: str = Field(min_length=2)
    incident_description: str = Field(min_length=10)
    claimed_amount: float = Field(gt=0)


class DocumentCreate(BaseModel):
    file_name: str = Field(min_length=1)
    document_type: str = Field(min_length=2)
    size_bytes: int = Field(gt=0, le=10_485_760)


class ValidationResult(BaseModel):
    claim_id: str
    valid: bool
    checks: list[dict[str, str | bool]]
    risk_level: RiskLevel
    risk_score: int
    risk_reasons: list[str]
