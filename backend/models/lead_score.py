from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from backend.database import Base

class LeadScore(Base):

    __tablename__ = "lead_scores"

    id = Column(
        Integer,
        primary_key=True
    )

    contact_id = Column(
        Integer,
        ForeignKey("contacts.id")
    )

    intent_score = Column(Integer)

    buying_stage = Column(String(100))

    ai_summary = Column(Text)
