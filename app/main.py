from datetime import date
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .data import claims, now, policies
from .models import Claim, ClaimCreate, ClaimStatus, Document, DocumentCreate, Policy, ValidationResult
from .services import assess_claim, find_policy, validate_documents

app = FastAPI(title="Claims Intake Service", version="0.1.0", description="Microservice 3: claim submission, document collection, and validation")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "claims-intake", "version": "0.1.0"}


@app.get("/api/policies", response_model=list[Policy])
def list_policies() -> list[Policy]:
    return policies


@app.get("/api/claims", response_model=list[Claim])
def list_claims(status: ClaimStatus | None = None) -> list[Claim]:
    return [claim for claim in claims if status is None or claim.status == status]


@app.get("/api/claims/{claim_id}", response_model=Claim)
def get_claim(claim_id: str) -> Claim:
    claim = next((item for item in claims if item.claim_id == claim_id), None)
    if claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


@app.post("/api/claims", response_model=Claim, status_code=201)
def create_claim(payload: ClaimCreate) -> Claim:
    policy = find_policy(policies, payload.policy_number)
    if policy is None:
        raise HTTPException(status_code=422, detail="Policy number does not exist")
    claim = Claim(
        claim_id=f"clm_{uuid4().hex[:8]}", claim_number=f"CLM-{date.today().year}-{len(claims) + 1:05d}",
        policy_id=policy.policy_id, policy_number=policy.policy_number, customer_id=policy.customer_id,
        customer_name=policy.customer_name, claim_type=payload.claim_type, incident_date=payload.incident_date,
        incident_location=payload.incident_location, incident_description=payload.incident_description,
        claimed_amount=payload.claimed_amount, deductible=policy.deductible_amount,
        status=ClaimStatus.SUBMITTED, investigation_status="PENDING", risk_level="LOW", risk_score=10,
        risk_reasons=[], documents=[], created_at=now(), updated_at=now(),
    )
    risk_level, risk_score, reasons, _ = assess_claim(claim, policy, claims)
    claim.risk_level, claim.risk_score, claim.risk_reasons = risk_level, risk_score, reasons
    if risk_level in ("HIGH", "CRITICAL") or policy.status != "ACTIVE" or not policy.start_date <= payload.incident_date <= policy.expiry_date:
        claim.status = ClaimStatus.MANUAL_REVIEW
    else:
        claim.status = ClaimStatus.DOCUMENT_VERIFICATION
    claims.insert(0, claim)
    return claim


@app.post("/api/claims/{claim_id}/documents", response_model=Claim)
def add_document(claim_id: str, payload: DocumentCreate) -> Claim:
    claim = get_claim(claim_id)
    if payload.document_type not in {"Identity proof", "Policy document", "Bill", "Receipt", "Medical report", "Repair estimate", "Photographs", "Police report", "Other"}:
        raise HTTPException(status_code=422, detail="Unsupported document type")
    claim.documents.append(Document(document_id=f"doc_{uuid4().hex[:8]}", file_name=payload.file_name, document_type=payload.document_type, size_bytes=payload.size_bytes, uploaded_at=now()))
    claim.updated_at = now()
    return claim


@app.post("/api/claims/{claim_id}/documents/upload", response_model=Claim)
async def upload_document(claim_id: str, document_type: str = Form(...), file: UploadFile = File(...)) -> Claim:
    claim = get_claim(claim_id)
    if document_type not in {"Identity proof", "Policy document", "Bill", "Receipt", "Medical report", "Repair estimate", "Photographs", "Police report", "Other"}:
        raise HTTPException(status_code=422, detail="Unsupported document type")
    content = await file.read(10_485_761)
    if len(content) > 10_485_760:
        raise HTTPException(status_code=413, detail="Document exceeds the 10 MB limit")
    claim.documents.append(Document(document_id=f"doc_{uuid4().hex[:8]}", file_name=file.filename or "unnamed-document", document_type=document_type, size_bytes=len(content), uploaded_at=now()))
    claim.updated_at = now()
    return claim


@app.post("/api/claims/{claim_id}/validate", response_model=ValidationResult)
def validate_claim(claim_id: str) -> ValidationResult:
    claim = get_claim(claim_id)
    policy = next(policy for policy in policies if policy.policy_id == claim.policy_id)
    risk_level, risk_score, reasons, eligibility_checks = assess_claim(claim, policy, claims)
    checks = eligibility_checks + validate_documents(claim)
    valid = all(bool(check["passed"]) for check in checks)
    claim.risk_level, claim.risk_score, claim.risk_reasons = risk_level, risk_score, reasons
    claim.updated_at = now()
    return ValidationResult(claim_id=claim.claim_id, valid=valid, checks=checks, risk_level=risk_level, risk_score=risk_score, risk_reasons=reasons)
