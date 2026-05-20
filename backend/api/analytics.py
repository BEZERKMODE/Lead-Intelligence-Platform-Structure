from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import LeadModel

router = APIRouter()

@router.get("/analytics")
@router.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # 1. Total leads count
    total_leads = db.query(LeadModel).count()
    
    # 2. Highly Qualified (Priority score >= 80)
    highly_qualified = db.query(LeadModel).filter(LeadModel.priority_score >= 80).count()
    
    # 3. Average Match Rate / Priority Score
    avg_score_raw = db.query(func.avg(LeadModel.priority_score)).scalar() or 0
    avg_priority_score = int(avg_score_raw)
    
    # 4. CRM Synced leads (leads with status SQL or Contacted)
    synced_crm_count = db.query(LeadModel).filter(LeadModel.status.in_(["SQL", "Contacted"])).count()
    
    return {
        "metrics": {
            "total_leads": total_leads,
            "highly_qualified": highly_qualified,
            "avg_priority_score": avg_priority_score,
            "synced_crm_count": synced_crm_count
        }
    }
