from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.enterprise_lead_engine import EnterpriseLeadEngine


class EnterpriseAnalyzeRequest(BaseModel):
    company_name: str = Field(..., example="Example Ltd")
    domain: str = Field(..., example="example.com")
    city: str = Field(..., example="Bangalore")
    state: str = Field(..., example="Karnataka")


class EmailValidationResult(BaseModel):
    email: str
    smtp_valid: bool
    zerobounce: Dict[str, Any]
    confidence_score: int


class EnterpriseAnalyzeResponse(BaseModel):
    company_name: str
    domain: str
    geo: Dict[str, Any]
    emails: List[EmailValidationResult]
    phones: List[str]
    technologies: Dict[str, Any]
    apollo_company: Dict[str, Any]
    apollo_people: Dict[str, Any]
    ai_analysis: Dict[str, Any]


router = APIRouter()

engine = EnterpriseLeadEngine()


@router.post(
    "/",
    response_model=EnterpriseAnalyzeResponse,
    summary="Analyze an enterprise lead with AI and enrichment",
    response_description="Enterprise intelligence analysis result"
)
def analyze_company(data: EnterpriseAnalyzeRequest):
    return engine.analyze_company(
        company_name=data.company_name,
        domain=data.domain,
        city=data.city,
        state=data.state
    )
