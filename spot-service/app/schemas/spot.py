from pydantic import BaseModel
from enum import Enum
from decimal import Decimal

class SpotType(str, Enum):
    compact = "compact"
    large = "large"
    handicapped = "handicapped"
    electric = "electric"

class SpotCreate(BaseModel):
    spot_number: int
    spot_type: SpotType
    hourly_rate: Decimal

class SpotOut(SpotCreate):
    spot_id: int
    is_available: bool

    class Config:
        orm_mode = True
