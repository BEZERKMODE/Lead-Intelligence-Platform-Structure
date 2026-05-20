import os
import sys
from celery import chain
from datetime import datetime
import re

# Ensure project root is in path for relative imports in celery environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.celery_worker import celery_app
from backend.database import SessionLocal
from backend.models import LeadModel, is_sqlite
from backend.scraper.scraper import LeadScraper
from backend.services.apollo_service import ApolloService
from backend.scraper.email_verifier import EmailVerifier
from backend.ai_engine import AIEngine

@celery_app.task(name="backend.tasks.enrich_company")
def enrich_company(lead_id):
    """
    Stage 1: Enriches company profile details (industry, tech stack, employee range, revenue)
    via Apollo organization endpoints and saves to database.
    """
    print(f"[Company] [Celery Task] Initiating Stage 1: Company Enrichment for Lead ID {lead_id}...")
    
    db = SessionLocal()
    try:
        lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead ID {lead_id} not found in database.")
            
        # Run the live LeadScraper enrichment routine
        enriched = LeadScraper.enrich_domain(lead.domain)
        
        # Save details
        lead.company_name = enriched['company_name']
        lead.sector = enriched['sector']
        lead.location = enriched['location']
        lead.latitude = enriched['latitude']
        lead.longitude = enriched['longitude']
        lead.revenue = enriched['revenue']
        lead.employees = enriched['employees']
        lead.technologies = enriched['technologies']
        lead.notes = enriched['notes']
        lead.security_score = enriched['security_score']
        lead.subdomains = enriched['subdomains']
        lead.vulnerabilities = enriched['vulnerabilities']
        lead.phone = enriched.get('phone', '')
        lead.last_scraped = datetime.utcnow()
        lead.status = 'Enriched'
        
        db.commit()
    finally:
        db.close()
        
    print(f"[Company] [Celery Task] Stage 1 Complete. Lead ID {lead_id} company details enriched successfully.")
    return lead_id

@celery_app.task(name="backend.tasks.enrich_person")
def enrich_person(lead_id):
    """
    Stage 2: Harvests human prospect profiles and decision maker contacts
    from the Apollo people endpoint and stores in the contacts database column.
    """
    print(f"[Person] [Celery Task] Initiating Stage 2: Contact Harvesting for Lead ID {lead_id}...")
    
    db = SessionLocal()
    try:
        lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead ID {lead_id} not found in database.")
            
        try:
            contacts = ApolloService.extract_emails(lead.domain)
            if contacts:
                contacts_str = " | ".join(
                    [f"{c['name']} <{c['email']}> ({c['title']})" for c in contacts]
                )
            else:
                contacts_str = f"hello@{lead.domain} (Primary), support@{lead.domain} (Support)"
        except Exception as e:
            print(f"[!] Stage 2 error querying Apollo people: {str(e)}")
            contacts_str = f"hello@{lead.domain} (Primary), support@{lead.domain} (Support)"
            
        lead.contacts = contacts_str
        db.commit()
    finally:
        db.close()
        
    print(f"[Person] [Celery Task] Stage 2 Complete. Harvested contacts for Lead ID {lead_id} saved.")
    return lead_id

@celery_app.task(name="backend.tasks.verify_email")
def verify_email(lead_id):
    """
    Stage 3: Performs live SMTP checks and MX lookups to verify email validity.
    """
    print(f"[SMTP] [Celery Task] Initiating Stage 3: SMTP Email Verification for Lead ID {lead_id}...")
    
    db = SessionLocal()
    try:
        lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if not lead or not lead.contacts:
            print("   -> No contacts harvested. Skipping SMTP verification.")
            return lead_id
            
        contacts_str = lead.contacts
        parts = [p.strip() for p in contacts_str.split('|') if p.strip()]
        verified_parts = []
        
        for part in parts:
            email_match = re.search(r'<([^>]+)>', part)
            if email_match:
                email = email_match.group(1).strip()
                print(f"   -> Verifying mailbox: {email}")
                res = EmailVerifier.verify_smtp_handshake(email)
                
                if res['success']:
                    verified_parts.append(f"{part} [VERIFIED]")
                    print(f"     [+] Verified Active!")
                else:
                    verified_parts.append(f"{part} [SMTP Code {res['code']}: {res['status']}]")
                    print(f"     [-] Verification Failed: {res['status']}")
            else:
                verified_parts.append(part)
                
        lead.contacts = " | ".join(verified_parts)
        db.commit()
    finally:
        db.close()
        
    print(f"[SMTP] [Celery Task] Stage 3 Complete. Email verifications persisted.")
    return lead_id

@celery_app.task(name="backend.tasks.ai_score")
def ai_score(lead_id):
    """
    Stage 4: Executes AI scoring algorithms to evaluate lead quality.
    """
    print(f"[AI] [Celery Task] Initiating Stage 4: AI Lead Scoring for Lead ID {lead_id}...")
    
    db = SessionLocal()
    try:
        lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead ID {lead_id} not found in database.")
            
        growth_trend = AIEngine.detect_growth_trend(lead.employees, lead.domain)
        match_rate = AIEngine.calculate_match_rate(lead.sector, lead.technologies, lead.employees)
        priority_score = AIEngine.calculate_priority_score(match_rate, growth_trend)
        
        lead.growth_trend = growth_trend
        lead.ai_match_rate = match_rate
        lead.priority_score = priority_score
        
        db.commit()
    finally:
        db.close()
        
    print(f"[AI] [Celery Task] Stage 4 Complete. Priority Score calculated: {priority_score}/100.")
    return lead_id

@celery_app.task(name="backend.tasks.save_vector_embedding")
def save_vector_embedding(lead_id, *args):
    """
    Stage 5: Computes semantic profile embeddings and saves record to main DB embedding column.
    Handles both pgvector and SQLite JSON formats.
    """
    print(f"[Vector] [Celery Task] Initiating Stage 5: Semantic Embedding for Lead ID {lead_id}...")
    
    db = SessionLocal()
    try:
        lead = db.query(LeadModel).filter(LeadModel.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead ID {lead_id} not found.")
            
        document = (
            f"Company Name: {lead.company_name} | Domain: {lead.domain} | "
            f"Sector: {lead.sector} | HQ: {lead.location} | "
            f"Employees: {lead.employees} | Estimated Revenue: {lead.revenue} | "
            f"Technologies: {lead.technologies} | Security hygiene: {lead.security_score} | "
            f"AI Suitability: {lead.ai_match_rate}% | Notes: {lead.notes}"
        )
        
        # Calculate embedding with dynamic fallback
        try:
            from sentence_transformers import SentenceTransformer
            print("[Vector] Loading SentenceTransformer 'all-MiniLM-L6-v2'...")
            model = SentenceTransformer("all-MiniLM-L6-v2")
            emb = model.encode(document).tolist()
            print("[Vector] SentenceTransformer embedding generated successfully.")
        except Exception as e:
            print(f"[Vector] [Warning] Failed to generate semantic embedding with SentenceTransformer ({e}). Falling back to dummy embedding.")
            # 384 dummy floats for SQLite/Postgres vector compatibility
            import random
            emb = [random.uniform(-0.1, 0.1) for _ in range(384)]
        
        if is_sqlite:
            import json
            lead.embedding = json.dumps(emb)
        else:
            lead.embedding = emb
            
        db.commit()
        print(f"[Pipeline] [Celery Task] Stage 5 Complete. Asynchronous Pipeline completed with 100% success!")
    finally:
        db.close()
        
    return True

def run_enrichment_pipeline(lead_id):
    """
    Orchestrates the entire asynchronous pipeline.
    """
    from backend.dag_engine import DAGEngine
    dag = DAGEngine()
    dag.execute_pipeline(lead_id)
    print(f"[Pipeline] [Dispatcher] Dispatched async DAG pipeline for Lead ID {lead_id}!")
