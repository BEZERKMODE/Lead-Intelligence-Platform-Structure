from fastapi import APIRouter

router = APIRouter()

@router.get("/plans")
def plans():
    return {
        "plans": [
            {
                "name": "Starter",
                "price": 49
            },
            {
                "name": "Growth",
                "price": 199
            },
            {
                "name": "Enterprise",
                "price": 999
            }
        ]
    }
