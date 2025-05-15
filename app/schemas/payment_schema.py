from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    user_id: int
    booking_id: int
    amount: float
    method: str
    status: str

class PaymentOut(PaymentCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
