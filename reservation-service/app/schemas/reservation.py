from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ReservationStatus(str, Enum):
    reserved = "reserved"
    cancelled = "cancelled"
    completed = "completed"

class ReservationCreate(BaseModel):
    user_id: int
    spot_id: int
    start_time: datetime
    end_time: datetime

class ReservationOut(BaseModel):
    reservation_id: int
    user_id: int
    spot_id: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus
    created_at: datetime

    class Config:
        orm_mode = True
