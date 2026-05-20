from fastapi import APIRouter
from backend.api import companies
from backend.api import contacts
from backend.api import enrichment
from backend.api import scoring
from backend.api import crm
from backend.api import workflows
from backend.api import monitoring
from backend.api import billing
from backend.api import auth_routes
from backend.api import leads
from backend.api import analytics

router = APIRouter()

# Include leads and analytics under /api namespace
router.include_router(leads.router, prefix="/api/leads", tags=["Leads"])
router.include_router(analytics.router, prefix="/api", tags=["Analytics"])

router.include_router(companies.router, prefix="/companies", tags=["Companies"])
router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
router.include_router(enrichment.router, prefix="/enrichment", tags=["Enrichment"])
router.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
router.include_router(crm.router, prefix="/crm", tags=["CRM"])
router.include_router(workflows.router, prefix="/workflows", tags=["Workflows"])
router.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
router.include_router(billing.router, prefix="/billing", tags=["Billing"])
router.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])

