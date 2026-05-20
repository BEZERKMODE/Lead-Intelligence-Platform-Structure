from backend.celery_worker import celery

from backend.services.enrichment_engine import EnrichmentEngine

engine = EnrichmentEngine()

@celery.task
def enrich_company(domain):

    return engine.enrich_company(domain)
