from backend.celery_worker import celery

from backend.services.ai_scoring_engine import AIScoringEngine

scoring = AIScoringEngine()

@celery.task
def score_company(data):

    return scoring.calculate_score(data)
