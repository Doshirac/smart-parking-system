from sqlalchemy import Column, Integer, ForeignKey, Enum, TIMESTAMP
from ..sqlalchemy_conn import Base
import enum

class ReservationStatus(str, enum.Enum):
    reserved = "reserved"
    cancelled = "cancelled"
    completed = "completed"

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    spot_id = Column(Integer, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
