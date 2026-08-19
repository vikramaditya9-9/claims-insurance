# Claims Intake Service

Microservice 3 for the insurance claims platform: claim submission, document collection, policy/amount validation, duplicate detection, and explainable risk flags. It ships with a lightweight dashboard and deterministic mock data so the workflow is runnable locally without a database.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the dashboard. API documentation is available at http://127.0.0.1:8000/docs.

## API surface

- `GET /api/claims` and `GET /api/claims/{claim_id}` - browse claims
- `POST /api/claims` - submit a claim after policy lookup
- `POST /api/claims/{claim_id}/documents` - associate document metadata with a claim
- `POST /api/claims/{claim_id}/validate` - run eligibility, coverage, duplicate, and document checks
- `GET /api/policies` - mock policies used by intake validation
- `GET /health` - service health check

The mock repository in `app/data.py` can be replaced by a database adapter later. High-impact decisions remain outside this service and are surfaced as review flags rather than automatic fraud conclusions.
