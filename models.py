from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_time = Column(String(50), nullable=False)
    is_booked = Column(Boolean, default=False)
    booked_by = Column(String(100), nullable=True)
    booked_at = Column(DateTime, nullable=True)