from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.models.contact import Contact

router = APIRouter()

@router.get("/")
def get_contacts(
    db: Session = Depends(get_db)
):

    return db.query(Contact).all()

@router.post("/")
def create_contact(
    data: dict,
    db: Session = Depends(get_db)
):

    contact = Contact(
        company_id=data.get("company_id"),
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        job_title=data.get("job_title"),
        department=data.get("department"),
        confidence_score=data.get("confidence_score", 0)
    )

    db.add(contact)

    db.commit()

    db.refresh(contact)

    return contact
