from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from backend.database import Base

class Contact(Base):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id")
    )

    first_name = Column(String(255))

    last_name = Column(String(255))

    email = Column(String(255))

    phone = Column(String(255))

    job_title = Column(String(255))

    department = Column(String(255))

    confidence_score = Column(Integer)

    validated = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
