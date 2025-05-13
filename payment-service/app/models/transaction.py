from sqlalchemy import Column, Integer, ForeignKey, Enum, DECIMAL, TIMESTAMP
from ..sqlalchemy_conn import Base
from enum import Enum as PyEnum
from datetime import datetime

class PaymentMethod(str, PyEnum):
    ApplePay = "ApplePay"
    GooglePay = "GooglePay"
    Visa = "Visa"
    MasterCard = "MasterCard"

class TransactionStatus(str, PyEnum):
    pending = "pending"
    completed = "completed"
    failed = "failed"

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(TransactionStatus), nullable=False)
    paid_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
