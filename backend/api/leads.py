from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
import json
import queue
import threading
import csv
import io
import random

from backend.database import get_db
from backend.models import LeadModel, is_sqlite, use_pgvector
from backend.ai_engine import AIEngine
from backend.tasks import run_enrichment_pipeline

router = APIRouter()

def format_lead(lead: LeadModel):
    # Split technologies
    techs = []
    if lead.technologies:
        techs = [t.strip() for t in lead.technologies.split(",") if t.strip()]
    
    # Split subdomains
    subs = []
    if lead.subdomains:
        subs = [s.strip() for s in lead.subdomains.split(",") if s.strip()]
        
    # Split vulnerabilities
    vulns = []
    if lead.vulnerabilities:
        vulns = [v.strip() for v in lead.vulnerabilities.split(",") if v.strip()]
        
    return {
        "id": lead.id,
        "company_name": lead.company_name,
        "domain": lead.domain,
        "sector": lead.sector,
        "location": lead.location,
        "latitude": lead.latitude,
        "longitude": lead.longitude,
        "revenue": lead.revenue,
        "employees": lead.employees,
        "technologies": techs,
        "contacts": lead.contacts,
        "priority_score": lead.priority_score,
        "ai_match_rate": lead.ai_match_rate,
        "growth_trend": lead.growth_trend,
        "status": lead.status,
        "notes": lead.notes,
        "security_score": lead.security_score,
        "subdomains": subs,
        "vulnerabilities": vulns,
        "phone": lead.phone
    }

@router.get("/")
def get_leads(
    search: Optional[str] = None,
    sector: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(LeadModel)
    if search:
        query = query.filter(
            LeadModel.company_name.ilike(f"%{search}%") | 
            LeadModel.domain.ilike(f"%{search}%") |
            LeadModel.technologies.ilike(f"%{search}%")
        )
    if sector:
        query = query.filter(LeadModel.sector == sector)
    if status:
        query = query.filter(LeadModel.status == status)
    
    leads = query.all()
    return [format_lead(lead) for lead in leads]

@router.post("/")
def create_lead(data: dict, db: Session = Depends(get_db)):
    domain = data.get("domain", "").lower().replace("http://", "").replace("https://", "").replace("www.", "").strip()
    if not domain:
        raise HTTPException(status_code=400, detail="Domain website is required.")
        
    # Check if already exists
    existing = db.query(LeadModel).filter(LeadModel.domain == domain).first()
    if existing:
        return format_lead(existing)
        
    lead = LeadModel(
        domain=domain,
        company_name=data.get("company_name") or domain.split('.')[0].capitalize(),
        sector=data.get("sector") or "Technology & SaaS",
        location=data.get("location") or "San Francisco, CA",
        status="New"
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    # Trigger background enrichment DAG pipeline automatically
    try:
        run_enrichment_pipeline(lead.id)
    except Exception as e:
        print(f"[Warning] Failed to run enrichment pipeline on creation: {e}")
        
    return format_lead(lead)

@router.get("/scrape-stream")
def scrape_stream(domain: str, db: Session = Depends(get_db)):
    domain = domain.lower().replace("http://", "").replace("https://", "").replace("www.", "").strip()
    q = queue.Queue()
    
    # Run the live crawler and enricher in a separate thread so Uvicorn can stream logs as they occur
    def run_scraper():
        try:
            # Check or create DB record
            lead = db.query(LeadModel).filter(LeadModel.domain == domain).first()
            if not lead:
                lead = LeadModel(
                    domain=domain,
                    company_name=domain.split('.')[0].capitalize(),
                    status="New"
                )
                db.add(lead)
                db.commit()
                db.refresh(lead)
                
            lead_id = lead.id
            
            def log_callback(msg, category="info"):
                q.put({"log": msg, "category": category})
                
            from backend.scraper.scraper import LeadScraper
            enriched = LeadScraper.enrich_domain(domain, log_callback=log_callback)
            
            # Save enriched fields
            lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
            if lead:
                lead.company_name = enriched['company_name']
                lead.sector = enriched['sector']
                lead.location = enriched['location']
                lead.latitude = enriched['latitude']
                lead.longitude = enriched['longitude']
                lead.revenue = enriched['revenue']
                lead.employees = enriched['employees']
                lead.technologies = enriched['technologies']
                lead.contacts = enriched['contacts']
                lead.notes = enriched['notes']
                lead.security_score = enriched['security_score']
                lead.subdomains = enriched['subdomains']
                lead.vulnerabilities = enriched['vulnerabilities']
                lead.phone = enriched.get('phone', '')
                lead.last_scraped = datetime.utcnow()
                lead.status = 'Enriched'
                
                # Run AIEngine analytics scoring
                growth_trend = AIEngine.detect_growth_trend(lead.employees, lead.domain)
                match_rate = AIEngine.calculate_match_rate(lead.sector, lead.technologies, lead.employees)
                priority_score = AIEngine.calculate_priority_score(match_rate, growth_trend)
                
                lead.growth_trend = growth_trend
                lead.ai_match_rate = match_rate
                lead.priority_score = priority_score
                
                # Compute vector embedding
                document = (
                    f"Company Name: {lead.company_name} | Domain: {lead.domain} | "
                    f"Sector: {lead.sector} | HQ: {lead.location} | "
                    f"Employees: {lead.employees} | Estimated Revenue: {lead.revenue} | "
                    f"Technologies: {lead.technologies} | Security hygiene: {lead.security_score} | "
                    f"AI Suitability: {lead.ai_match_rate}% | Notes: {lead.notes}"
                )
                
                try:
                    from sentence_transformers import SentenceTransformer
                    model = SentenceTransformer("all-MiniLM-L6-v2")
                    emb = model.encode(document).tolist()
                except Exception:
                    # Random high-dimensional float fallback for local execution
                    emb = [random.uniform(-0.1, 0.1) for _ in range(384)]
                    
                if not use_pgvector:
                    lead.embedding = json.dumps(emb)
                else:
                    lead.embedding = emb
                    
                db.commit()
                
            q.put({"complete": True, "lead_id": lead_id})
        except Exception as e:
            q.put({"error": str(e)})
            
    threading.Thread(target=run_scraper, daemon=True).start()
    
    def event_generator():
        while True:
            try:
                msg = q.get(timeout=25)
                yield f"data: {json.dumps(msg)}\n\n"
                if "complete" in msg or "error" in msg:
                    break
            except queue.Empty:
                # Keep-alive heartbeat message to prevent browser timeout disconnects
                yield f"data: {json.dumps({'log': 'Heartbeat ping...', 'category': 'info'})}\n\n"
                
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{lead_id}")
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
    return format_lead(lead)

@router.put("/{lead_id}")
def update_lead(lead_id: int, data: dict, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
        
    if "notes" in data:
        lead.notes = data["notes"]
    if "status" in data:
        lead.status = data["status"]
        
    db.commit()
    db.refresh(lead)
    return format_lead(lead)

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
    db.delete(lead)
    db.commit()
    return {"success": True}

@router.post("/{lead_id}/enrich-async")
def enrich_lead_async(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
    run_enrichment_pipeline(lead_id)
    return {"success": True, "message": "Enrichment pipeline dispatched."}

@router.post("/{lead_id}/sync")
@router.post("/{lead_id}/sync-crm")
def sync_crm(lead_id: int, data: Optional[dict] = None, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
        
    crm_name = (data or {}).get("crm", "Salesforce")
    
    # Mark status as SQL (Sales Qualified Lead) to reflect sync in analytics
    lead.status = "SQL"
    db.commit()
    
    # Mock dynamic integrations record ID creation
    crm_prefix = "SF" if crm_name.lower() == "salesforce" else "HS"
    record_id = f"{crm_prefix}-{random.randint(100000, 999999)}"
    
    return {
        "success": True,
        "crm": crm_name,
        "crm_record_id": record_id
    }

@router.post("/{lead_id}/email")
def generate_outreach_email_route(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found.")
        
    # Generate outreach email using our high-fidelity, customized AIEngine
    email_content = AIEngine.generate_outreach_email(
        company_name=lead.company_name,
        domain=lead.domain,
        sector=lead.sector,
        employees=lead.employees,
        technologies=lead.technologies,
        location=lead.location,
        growth_trend=lead.growth_trend,
        notes=lead.notes or ""
    )
    
    return {"email": email_content}

@router.post("/import")
def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(content))
        imported_count = 0
        
        for row in reader:
            domain = row.get("domain", "").lower().replace("http://", "").replace("https://", "").replace("www.", "").strip()
            if not domain:
                continue
                
            # Deduplicate domain records
            existing = db.query(LeadModel).filter(LeadModel.domain == domain).first()
            if existing:
                continue
                
            lead = LeadModel(
                domain=domain,
                company_name=row.get("company_name") or domain.split('.')[0].capitalize(),
                sector=row.get("sector") or "Technology & SaaS",
                location=row.get("location") or "San Francisco, CA",
                status="New"
            )
            db.add(lead)
            db.commit()
            db.refresh(lead)
            
            # Start asynchronous background enrichment pipeline
            try:
                run_enrichment_pipeline(lead.id)
            except Exception as e:
                print(f"[Warning] Failed to run pipeline for imported domain {domain}: {e}")
                
            imported_count += 1
            
        return {"success": True, "imported_count": imported_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV import failed: {str(e)}")
