from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from backend.database import Base

class Tenant(Base):

    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True
    )

    company_name = Column(String(255))

    subscription_plan = Column(String(255))
