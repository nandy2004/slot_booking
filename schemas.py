from pydantic import BaseModel
from typing import Optional
import datetime

class SlotOut(BaseModel):
    id: int
    slot_time: str
    is_booked: bool
    booked_by: Optional[str]
    booked_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    slot_id: int
    name: str