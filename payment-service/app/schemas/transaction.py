from pydantic import BaseModel
from enum import Enum
from decimal import Decimal
from typing import Optional
from datetime import datetime

class PaymentMethod(str, Enum):
    ApplePay = "ApplePay"
    GooglePay = "GooglePay"
    Visa = "Visa"
    MasterCard = "MasterCard"

class TransactionStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class TransactionCreate(BaseModel):
    reservation_id: int
    user_id: int
    amount: Decimal
    payment_method: PaymentMethod

class TransactionOut(BaseModel):
    transaction_id: int
    reservation_id: int
    user_id: int
    amount: Decimal
    payment_method: PaymentMethod
    status: TransactionStatus
    paid_at: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True
