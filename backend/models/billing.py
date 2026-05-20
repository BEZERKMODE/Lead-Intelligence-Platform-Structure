from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String

from backend.database import Base

class Billing(Base):

    __tablename__ = "billing"

    id = Column(
        Integer,
        primary_key=True
    )

    tenant_id = Column(Integer)

    amount = Column(Float)

    status = Column(String(100))
