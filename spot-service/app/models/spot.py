from sqlalchemy import Column, Integer, Boolean, Text, Enum, DECIMAL, TIMESTAMP
from ..sqlalchemy_conn import Base
from enum import Enum as PyEnum
from datetime import datetime

class SpotType(str, PyEnum):
    compact = "compact"
    large = "large"
    handicapped = "handicapped"
    electric = "electric"

class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    spot_id = Column(Integer, primary_key=True, index=True)
    spot_number = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    spot_type = Column(Enum(SpotType), nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
