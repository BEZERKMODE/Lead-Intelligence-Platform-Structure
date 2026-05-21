from fastapi import APIRouter, HTTPException

from backend.intelligence.india_geo_engine import IndiaGeoEngine
from backend.intelligence.cybersecurity_opportunity_engine import CybersecurityOpportunityEngine
from backend.intelligence.sector_classifier import SectorClassifier
from backend.intelligence.india_company_engine import IndiaCompanyEngine
from backend.intelligence.email_accuracy_engine import EmailAccuracyEngine
from backend.intelligence.phone_discovery_engine import PhoneDiscoveryEngine
from backend.intelligence.dlp_target_engine import DLPTargetEngine

router = APIRouter()

@router.post("/india-geo")
def analyze_india_geo(data: dict):
    city = data.get("city")
    if not city:
        raise HTTPException(status_code=400, detail="'city' field required")
    return IndiaGeoEngine.analyze_city(city)

@router.post("/cybersecurity/opportunity")
def analyze_cybersecurity_opportunity(data: dict):
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Request body must be an object")
    return CybersecurityOpportunityEngine.calculate(data)

@router.post("/sector/classify")
def classify_sector(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="'text' field required")
    return {"sector": SectorClassifier.classify(text)}

@router.post("/india-company/discover")
def discover_india_companies(data: dict):
    city = data.get("city")
    sector = data.get("sector")
    if not city or not sector:
        raise HTTPException(status_code=400, detail="'city' and 'sector' fields required")
    engine = IndiaCompanyEngine()
    return engine.discover(city=city, sector=sector)

@router.post("/email/verify")
def verify_email_accuracy(data: dict):
    domain = data.get("domain")
    if not domain:
        raise HTTPException(status_code=400, detail="'domain' field required")
    engine = EmailAccuracyEngine()
    return engine.verify(domain)

@router.post("/phone/discover")
def discover_phone_numbers(data: dict):
    text = data.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="'text' field required")
    engine = PhoneDiscoveryEngine()
    return {"phones": engine.discover(text)}

@router.post("/dlp/analyze")
def analyze_dlp_target(data: dict):
    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="Request body must be an object")
    return DLPTargetEngine.analyze(data)
