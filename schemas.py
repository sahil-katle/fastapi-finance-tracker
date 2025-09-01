from pydantic import BaseModel, Field
from typing import Optional, Literal 
from datetime import date 

# Common fields for transactions
class TransactionBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=200)
    amount : float = Field(..., gt=0)
    kind: Literal["income", "expense"]
    category: Optional[str] = Field(None, max_length=100)
    occured_on: date

class TransactionUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[float] = Field(None, gt=0)
    kind: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(None, max_length=100)
    occurred_on: Optional[date] = None
    note: Optional[str] = Field(None, max_length=1000)

# For creating transactions
class TransactionCreate(TransactionBase):

    pass

# For returning  transactions
class TransactionOut(TransactionBase):
    id : int

    class Config:
        from_attributes = True



