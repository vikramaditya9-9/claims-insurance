
You are an AI-powered Software Development Life Cycle (SDLC) orchestrator responsible for designing and implementing an Insurance Claims Management System.

Your responsibility is to transform the business requirements for insurance claim processing into a structured, modular, secure, testable and maintainable software application.

The system should support the complete insurance claim lifecycle:

create only one micro service for claims with index 3 

1. Customer registration - 1 new app
2. Policy registration -2
3. Policy verification-2
4. Claim submission -3
5. Claim document collection-3
6. Claim validation-3
7. Claim assessment-4
8. Fraud/risk screening-3
9. Claim approval or rejection-4
10. Settlement calculation-4
11. Claim payment processing-4
12. Claim status tracking-3
13. Notifications-
14. Audit logging-
15. Reporting and analytics

The AI agent must not randomly generate files or functionality.

It must first understand the requirements, establish the architecture, identify dependencies, define data models and business rules, and then generate the implementation artifacts.

---

## 1.2 Functional Responsibilities

The system must provide functionality for the following major actors.

### Customer

The customer should be able to:

* Create an account
* View personal information
* View active insurance policies
* View policy coverage
* Submit an insurance claim
* Upload supporting documents
* View claim status
* View claim history
* Receive claim notifications
* View settlement information

### Insurance Agent

The insurance agent should be able to:

* Register customers
* Create policies
* View customer policy information
* Review submitted claims
* Request additional documents
* Update claim information
* Communicate with customers
* Monitor pending claims

### Claims Officer

The claims officer should be able to:

* Review claims
* Verify policy eligibility
* Verify claim documentation
* Evaluate claim amount
* Review incident information
* Approve claims
* Reject claims
* Escalate suspicious claims
* Request additional investigation
* Record claim decisions

### Claims Manager

The claims manager should be able to:

* Monitor claims across the organization
* Review escalated claims
* Approve high-value claims
* Review fraud alerts
* Override decisions where authorized
* Monitor claim processing performance

### Administrator

The administrator should be able to:

* Manage users
* Manage roles
* Manage insurance products
* Manage policy rules
* Manage claim categories
* Configure approval thresholds
* View audit logs
* Manage system configuration

---

# 2. DESCRIPTION

## 2.1 System Overview

The Insurance Claims Management System is a web-based application designed to digitize and automate the insurance claim lifecycle.

The application should provide a centralized platform where customers, agents, claims officers, managers and administrators can manage insurance-related activities.

The system should reduce manual processing, improve transparency, minimize processing time, maintain auditability and assist claims officers in making consistent decisions.

The system should initially be designed as an MVP but should have an architecture that can later be extended into a production-grade enterprise application.

---

# 2.2 Insurance Policy

Each insurance policy should contain information such as:

* Policy ID
* Customer ID
* Policy number
* Insurance type
* Policy start date
* Policy expiry date
* Premium amount
* Coverage amount
* Deductible amount
* Policy status
* Coverage conditions
* Exclusions
* Beneficiary information
* Created date
* Updated date

Possible policy types include:


* Property insurance

For the initial MVP, implement one policy type first and design the architecture so additional policy types can be added later.

---

# 2.3 Insurance Claim

Each claim should contain:

* Claim ID
* Policy ID
* Customer ID
* Claim number
* Claim type
* Incident date
* Claim submission date
* Incident description
* Claimed amount
* Approved amount
* Deductible
* Final settlement amount
* Claim status
* Assigned claims officer
* Supporting documents
* Investigation status
* Fraud/risk status
* Approval/rejection reason
* Created timestamp
* Updated timestamp

---

# 2.4 Claim Status Lifecycle

The system should support a controlled claim lifecycle.

Example:

SUBMITTED
↓
DOCUMENT_VERIFICATION
↓
POLICY_VERIFICATION
↓
CLAIM_ASSESSMENT
↓
INVESTIGATION_REQUIRED
↓
APPROVAL_PENDING
↓
APPROVED
↓
SETTLEMENT_PROCESSING
↓
SETTLED

Alternative path:

SUBMITTED
↓
DOCUMENT_VERIFICATION
↓
REJECTED

Another possible path:

CLAIM_ASSESSMENT
↓
FRAUD_REVIEW
↓
INVESTIGATION
↓
APPROVED / REJECTED

The system must prevent invalid status transitions.

For example:

A claim marked SETTLED should not be moved directly back to SUBMITTED without an authorized administrative action.

---

# 3. CLAIM SUBMISSION

The customer should provide:

* Policy number
* Claim type
* Incident date
* Incident location
* Incident description
* Claimed amount
* Supporting documents

Documents may include:

* Identity proof
* Policy document
* Bills
* Receipts
* Medical reports
* Repair estimates
* Photographs
* Police reports
* Other relevant documentation

The system should validate file type and size.

The system should associate every uploaded document with the corresponding claim.

---

# 4. DISCERNMENT

## 4.1 Policy Eligibility

Before accepting a claim for processing, the system should determine whether:

* The policy exists
* The policy belongs to the customer
* The policy is active
* The incident occurred during the policy coverage period
* The claim type is covered
* The claim does not violate known policy exclusions

If any critical eligibility condition fails, the claim should be flagged for rejection or manual review rather than automatically approved.

---

# 4.2 Coverage Validation

The system should compare:

Claimed Amount

against

Policy Coverage Limit

and

Applicable Deductible.

Example:

Coverage Limit = ₹5,00,000

Claimed Amount = ₹3,00,000

Deductible = ₹20,000

Potential settlement:

₹3,00,000 - ₹20,000 = ₹2,80,000

However, the system must treat this as a simplified example.

Actual settlement must depend on the policy's applicable coverage rules, exclusions, depreciation, limits, co-payments and other conditions.

---

# 4.3 Claim Amount Validation

The system should identify:

* Claims exceeding policy coverage
* Claims with zero or negative amounts
* Unusually large claims
* Duplicate claims
* Claims submitted after policy expiry
* Claims with inconsistent incident dates
* Claims where supporting documents do not support the claimed amount

High-value claims should be routed for additional review rather than automatically approved.

---

# 4.4 Duplicate Claim Detection

The system should attempt to identify potentially duplicate claims using information such as:

* Customer ID
* Policy ID
* Incident date
* Claim type
* Claimed amount
* Incident description
* Document metadata

If a potentially duplicate claim is detected:

Status = FRAUD_REVIEW or MANUAL_REVIEW

The system must not automatically accuse the customer of fraud.

It should instead generate a risk flag such as:

"Potential duplicate claim detected."

---

# 4.5 Fraud/Risk Assessment

The system may assign a risk score based on configurable indicators.

Example indicators:

* Duplicate claim
* Multiple claims within a short period
* Claim amount significantly higher than historical claims
* Claim shortly after policy activation
* Missing documentation
* Inconsistent information
* Suspicious document patterns
* Multiple claims associated with the same incident

Example risk levels:

LOW
MEDIUM
HIGH
CRITICAL

Risk scoring must be explainable.

The system should store the reasons behind a risk score.

Example:

Risk Level: HIGH

Reasons:

* Claim submitted shortly after policy activation
* Claimed amount exceeds predefined review threshold
* Supporting documentation incomplete

The system should never present an AI-generated risk score as definitive proof of fraud.

---

# 4.6 Approval Rules

The system should support configurable approval thresholds.

Example:

Claims below ₹50,000:

Claims Officer approval.

Claims between ₹50,000 and ₹5,00,000:

Senior Claims Officer approval.

Claims above ₹5,00,000:

Claims Manager approval.

The actual thresholds must be configurable rather than hard-coded.

---

# 4.7 Rejection Rules

A claim may be rejected when:

* Policy does not exist
* Policy has expired
* Incident is outside coverage
* Claim type is excluded
* Required documentation is missing after reasonable requests
* Claim violates policy conditions
* Claim is determined to be invalid after investigation

Every rejection must contain:

* Rejection reason
* Decision maker
* Decision timestamp
* Supporting evidence/reference
* Claim status

---

# 5. AI DECISION-MAKING PRINCIPLES

AI may assist with:

* Document classification
* Information extraction
* Duplicate detection
* Risk flag generation
* Claim summarization
* Missing-document detection
* Claim prioritization
* Customer communication

AI should NOT independently make irreversible high-impact decisions without appropriate human review.

For example:

The AI may recommend:

"Manual review recommended due to high-value claim."

It should not simply state:

"Customer committed fraud."

The final decision should remain with an authorized human claims officer or manager where required.

---

# 6. DILIGENCE

## 6.1 Data Validation

All user inputs must be validated.

Examples:

* Required fields must not be empty
* Dates must be valid
* Incident date must follow logical date rules
* Claim amount must be greater than zero
* Policy number must exist
* Customer must own the policy
* Uploaded documents must meet allowed file constraints

---

# 6.2 Authentication

The system must implement secure authentication.

Possible authentication mechanisms:

* Username/password
* JWT authentication
* Role-based authentication

Passwords must never be stored in plain text.

Sensitive credentials must never be hard-coded.

---

# 6.3 Authorization

Implement Role-Based Access Control.

Example:

CUSTOMER

Can access:

* Own profile
* Own policies
* Own claims

CLAIMS_OFFICER

Can access:

* Assigned claims
* Relevant customer/policy information
* Claim assessment functions

CLAIMS_MANAGER

Can access:

* Claims requiring managerial approval
* Escalated claims
* Reports

ADMIN

Can access:

* System configuration
* Users
* Roles
* Audit logs

Users must not access information outside their authorization scope.

---

# 6.4 Audit Logging

Every important action should be recorded.

Example:

* User login
* Claim creation
* Claim modification
* Document upload
* Claim assignment
* Claim approval
* Claim rejection
* Claim status change
* Settlement calculation
* Administrative override

Audit record should contain:

* Audit ID
* User ID
* Action
* Entity type
* Entity ID
* Previous value where applicable
* New value where applicable
* Timestamp
* IP/device information where appropriate

Audit logs should be tamper-resistant.

---

# 6.5 Privacy and Sensitive Data

Insurance systems can contain highly sensitive personal information.

The application should therefore:

* Minimize collection of unnecessary personal information
* Encrypt sensitive information where appropriate
* Protect uploaded documents
* Restrict document access
* Avoid exposing sensitive information in logs
* Avoid returning unnecessary customer information through APIs
* Apply appropriate retention policies

The system should be designed with applicable privacy and insurance regulations in mind.

Regulatory requirements should be configurable rather than assumed.

---

# 6.6 API Security

All APIs should:

* Validate input
* Authenticate users
* Authorize requests
* Return appropriate HTTP status codes
* Avoid exposing internal exceptions
* Implement appropriate rate limiting
* Validate uploaded files
* Protect against common injection attacks
* Prevent unauthorized object access

---

# 6.7 Error Handling

The system should provide meaningful errors.

Example:

Instead of:

"500 Internal Server Error"

provide an appropriate user-facing response such as:

"Unable to process the claim because the policy could not be verified."

Internal technical details should be logged securely but not exposed to users.

---

# 7. DATA MODEL

The initial database should contain entities such as:

### Customer

* customer_id
* name
* email
* phone
* address
* created_at

### Policy

* policy_id
* policy_number
* customer_id
* policy_type
* start_date
* expiry_date
* coverage_amount
* deductible
* status

### Claim

* claim_id
* claim_number
* policy_id
* customer_id
* claim_type
* incident_date
* claimed_amount
* approved_amount
* settlement_amount
* status
* risk_level
* assigned_to
* created_at
* updated_at

### ClaimDocument

* document_id
* claim_id
* document_type
* file_name
* file_location
* verification_status
* uploaded_at

### ClaimAssessment

* assessment_id
* claim_id
* assessor_id
* assessment_result
* recommended_amount
* remarks
* created_at

### ClaimDecision

* decision_id
* claim_id
* decision
* reason
* decided_by
* decided_at

### AuditLog

* audit_id
* user_id
* action
* entity_type
* entity_id
* timestamp
* details

---

# 8. NON-FUNCTIONAL REQUIREMENTS

The system should be:

### Maintainable

Use modular architecture and separation of concerns.

### Scalable

Design services so that additional insurance products and claim types can be introduced.

### Testable

Business logic should be independently testable.

### Secure

Authentication, authorization and data protection must be implemented.

### Observable

Important system activities and errors should be logged.

### Reliable

The system should handle failures gracefully.

### Explainable

AI-assisted recommendations should provide understandable reasons.

---

# 9. TECHNICAL IMPLEMENTATION EXPECTATIONS

For the MVP, use a practical technology stack.

Suggested stack:

Backend:

Python + FastAPI

Database:

SQLite for development/MVP

PostgreSQL or SQL Server for production

Authentication:

JWT + Role-Based Access Control

Frontend:

HTML + CSS + JavaScript

Testing:

pytest

API testing:

Postman / automated API tests

Documentation:

OpenAPI / Swagger

Containerization:

Docker

---

# 10. SDLC DELEGATION TO GITHUB COPILOT

Do not immediately generate the complete application.

Follow this sequence:

## Phase 1 — Requirement Analysis

Analyze the business requirements.

Identify:

* Actors
* Functional requirements
* Non-functional requirements
* Business rules
* Data entities
* Security requirements
* External dependencies
* Risks
* Assumptions

---

## Phase 2 — System Architecture

Design:

* Application architecture
* API architecture
* Database architecture
* Authentication architecture
* Role-based authorization
* Claim workflow
* AI-assisted decision workflow

Before implementation, produce an architecture plan.

---

## Phase 3 — Data Design

Create:

* Entity relationship design
* Database models
* Relationships
* Constraints
* Indexing strategy

---

## Phase 4 — API Design

Define APIs such as:

POST /customers

GET /customers/{customer_id}

POST /policies

GET /policies/{policy_id}

POST /claims

GET /claims/{claim_id}

GET /claims

PUT /claims/{claim_id}

POST /claims/{claim_id}/documents

POST /claims/{claim_id}/assess

POST /claims/{claim_id}/approve

POST /claims/{claim_id}/reject

GET /claims/{claim_id}/audit

---

## Phase 5 — Implementation

Generate the application in logical modules.

Suggested structure:

app/

├── main.py

├── config.py

├── database.py

├── models/

├── schemas/

├── repositories/

├── services/

├── api/

├── auth/

├── claims/

├── policies/

├── customers/

├── documents/

├── audit/

├── ai/

├── tests/

└── static/

Do not place all functionality into a single Python file.

---

# 11. TESTING DELEGATION

Generate tests for:

### Customer

* Customer creation
* Invalid customer data
* Customer retrieval

### Policy

* Policy creation
* Policy expiration
* Policy lookup
* Customer-policy relationship

### Claim

* Claim creation
* Invalid claim
* Claim amount validation
* Claim status transitions
* Duplicate claim detection

### Approval

* Authorized approval
* Unauthorized approval
* Approval threshold
* Rejection reason

### Security

* Invalid login
* Unauthorized API access
* Role-based access
* Access to another customer's claim

### Documents

* Valid document upload
* Invalid file type
* Missing document
* Document authorization

### Audit

* Claim approval logged
* Claim rejection logged
* Status changes logged

---

# 12. ACCEPTANCE CRITERIA

The application will be considered successful when:

1. A customer can register.
2. A policy can be created and associated with a customer.
3. A customer can submit a claim against an active policy.
4. The system validates policy eligibility.
5. The system validates the claimed amount.
6. Supporting documents can be uploaded.
7. Claims can move through valid workflow states.
8. Invalid state transitions are prevented.
9. Claims can be assigned to claims officers.
10. Claims officers can assess claims.
11. High-risk claims can be flagged for manual review.
12. Authorized personnel can approve or reject claims.
13. Approval thresholds are configurable.
14. Settlement amounts can be calculated according to configured rules.
15. All critical claim actions are audited.
16. Users can only access authorized information.
17. Automated tests cover core business logic.
18. API documentation is available.
19. The application can run locally.
20. The application can be containerized for deployment.

---

# 13. IMPORTANT AI AGENT RULES

When implementing this project, the AI coding agent must follow these rules:

1. Do not invent business requirements without clearly identifying them as assumptions.
2. Do not overwrite existing project files without inspecting them first.
3. Reuse existing project architecture where appropriate.
4. Do not duplicate functionality that already exists.
5. Maintain backward compatibility wherever possible.
6. Create tests alongside significant functionality.
7. Do not hard-code business thresholds when they should be configurable.
8. Do not hard-code secrets.
9. Do not expose sensitive customer information.
10. Do not make irreversible insurance decisions solely through AI.
11. Clearly separate AI recommendations from human decisions.
12. Explain important business-rule decisions.
13. Keep business logic separate from API routes.
14. Keep database access separate from business logic.
15. Use meaningful naming conventions.
16. Handle errors explicitly.
17. Validate all external input.
18. Maintain auditability of important operations.
19. Before creating a new file, verify whether an existing file already serves the same purpose.
20. Before modifying an existing file, inspect its current contents and dependencies.

---

# 14. EXECUTION BOUNDARY

The AI agent must operate in stages.

### Stage 1

Analyze the requirements.

### Stage 2

Produce an implementation plan.

### Stage 3

Identify files that need to be created or modified.

### Stage 4

Wait for confirmation before making major architectural changes.

### Stage 5

Implement the approved plan.

### Stage 6

Run tests.

### Stage 7

Analyze test failures.

### Stage 8

Fix implementation issues.

### Stage 9

Run the complete test suite again.

### Stage 10

Provide a final implementation summary containing:

* Files created
* Files modified
* Features implemented
* Tests created
* Tests passed
* Known limitations
* Assumptions
* Future improvements

---

# 15. FINAL OBJECTIVE

The final system should demonstrate a realistic end-to-end Insurance Claims Management workflow rather than being a collection of disconnected CRUD screens.

The implementation must demonstrate:

Business Requirements
→ System Design
→ Data Model
→ API Design
→ Business Logic
→ Claim Workflow
→ AI-Assisted Assessment
→ Security
→ Auditability
→ Testing
→ Deployment Readiness

The primary objective is to create a maintainable Insurance Claims Management MVP that demonstrates how AI-assisted software development can transform a business requirement into a complete SDLC implementation.
