from fastapi import APIRouter

router = APIRouter()

@router.post("/sync")
def sync_crm(data: dict):
    return {"status": "synced"}
