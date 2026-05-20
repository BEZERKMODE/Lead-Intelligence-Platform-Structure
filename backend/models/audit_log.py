from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from backend.database import Base

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(Integer)

    action = Column(Text)
