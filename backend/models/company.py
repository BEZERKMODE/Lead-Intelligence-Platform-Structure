from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from backend.database import Base

class Company(Base):

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)

    company_name = Column(String(255))

    domain = Column(String(255))

    industry = Column(String(255))

    employee_count = Column(Integer)

    revenue = Column(String(255))

    location = Column(Text)

    linkedin_url = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
