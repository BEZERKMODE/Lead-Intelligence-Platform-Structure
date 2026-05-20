from fastapi import APIRouter

router = APIRouter()

@router.post("/score")
def score_lead(data: dict):
    return {"status": "scored"}
