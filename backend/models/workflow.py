from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from backend.database import Base

class Workflow(Base):

    __tablename__ = "workflows"

    id = Column(
        Integer,
        primary_key=True
    )

    workflow_name = Column(String(255))

    status = Column(String(100))
