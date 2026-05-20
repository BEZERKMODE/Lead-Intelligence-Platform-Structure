from fastapi import APIRouter, HTTPException
from backend.services.enrichment_engine import EnrichmentEngine

router = APIRouter()

@router.post("/")
async def enrich_company(data: dict):
    """Enrich a company by domain using Apollo API.
    Expected payload: {"domain": "example.com"}
    """
    domain = data.get("domain")
    if not domain:
        raise HTTPException(status_code=400, detail="'domain' field required")
    engine = EnrichmentEngine()
    result = engine.enrich_company(domain)
    return result
