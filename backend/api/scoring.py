from fastapi import APIRouter

from backend.services.ai_scoring_engine import AIScoringEngine

router = APIRouter()

scoring_engine = AIScoringEngine()

@router.post("/")
def calculate_score(data: dict):

    score = scoring_engine.calculate_score(data)

    return {
        "score": score
    }
