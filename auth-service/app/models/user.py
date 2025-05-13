from sqlalchemy import Column, Integer, Text, TIMESTAMP
from ..sqlalchemy_conn import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone_number = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
