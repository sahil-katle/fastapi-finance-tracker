from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, List
from datetime import date , datetime

# Common fields for transactions
class TransactionBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    amount : float = Field(..., gt=0)
    kind: Literal["income", "expense"]
    category: Optional[str] = Field(None, max_length=100)
    occured_on: date
    note: Optional[str] = Field(None, max_length=1000)


class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    kind: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, max_length=100)
    occured_on: Optional[date] = None
    note: Optional[str] = Field(None, max_length=1000)

    @field_validator("occured_on")
    @classmethod
    def not_in_future(cls, v: date) -> date:
        from datetime import date as _date
        if v > _date.today():
            raise ValueError("occured_on cannot be in future.")
        return v
    
# For creating transactions
class TransactionCreate(TransactionBase):
    @field_validator("occured_on")
    @classmethod
    def not_in_future(cls, v: date) -> date:
        from datetime import date as _date
        if v > _date.today():
            raise ValueError("occured_on cannot be in future.")
        return v

# For returning  transactions
class TransactionOut(TransactionBase):
    id : int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Advanced list response
class TransactionListOut(BaseModel):
    items: List[TransactionOut]
    total: int
    limit: int
    offset: int
