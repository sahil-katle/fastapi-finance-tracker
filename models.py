from sqlalchemy import Column, Integer, Date, String, Numeric, Text, DateTime, func, Boolean
from db import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200), nullable=False, index=True)
    amount = Column(Numeric(12,2), nullable=False) # 12 digits total and 2 decimal places
    kind = Column(String(10), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    occured_on = Column(Date, nullable=False, index=True)
    note = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(),
                        nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="1")

