from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models.company import Company

router = APIRouter()

@router.get("/")
def get_companies(
    db: Session = Depends(get_db)
):

    return db.query(Company).all()

@router.post("/")
def create_company(
    data: dict,
    db: Session = Depends(get_db)
):

    company = Company(
        company_name=data.get("company_name"),
        domain=data.get("domain"),
        industry=data.get("industry"),
        employee_count=data.get("employee_count"),
        revenue=data.get("revenue"),
        location=data.get("location"),
        linkedin_url=data.get("linkedin_url")
    )

    db.add(company)

    db.commit()

    db.refresh(company)

    return company
