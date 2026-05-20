from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from backend.database import Base

class CRMSyncLog(Base):

    __tablename__ = "crm_sync_logs"

    id = Column(
        Integer,
        primary_key=True
    )

    crm_name = Column(String(255))

    status = Column(String(100))

    response = Column(Text)
