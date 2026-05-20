from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def monitoring():

    return {
        "api": "healthy",
        "database": "healthy",
        "redis": "healthy",
        "workers": "running"
    }
